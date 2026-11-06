# Pod Identity Webhook

Source: https://docs.coreweave.com/products/cks/clusters/coreweave-charts/pod-identity-webhook

# Pod Identity Webhook

> Configure pods to access CoreWeave AI Object Storage

| Chart reference | Description |
| - | - |
| `coreweave/pod-identity-webhook` | Configure pods to access CoreWeave AI Object Storage |

This page describes the Pod Identity Webhook chart, which configures Pods on a CKS cluster to authenticate to CoreWeave AI Object Storage without managing static credentials. It covers what the webhook does, an example manifest that shows the autoinjected configuration, and the chart values you need to set when you install it.

## About the Pod Identity Webhook

The *Pod Identity Webhook* is a deployment of the [EKS Pod Identity Webhook](https://github.com/aws/amazon-eks-pod-identity-webhook) configured to use CoreWeave's OIDC Workload Federation feature. Instead of using `AssumeRoleWithWebIdentity`, it uses a lesser-known API called the [Container Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html).

When installed, the webhook injects most of the variables needed to authenticate to AI Object Storage into any Pod that uses a [Service Account](https://kubernetes.io/docs/concepts/security/service-accounts/) with an annotation of `caios.coreweave.com/inject: "true"`.

## Example usage

The following example shows how the webhook injects authentication configuration into a Pod. If you apply the following manifest into a cluster with the webhook enabled, the resulting `Pod` has autoinjected configuration.

> [!NOTE]
>
> While the webhook handles all authentication, you still need to configure workloads to use Virtual Addressing Style. For examples, see [Attaching endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md).

```yaml title="test-pod.yaml" highlight={4-5} theme={"system"}
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    caios.coreweave.com/inject: "true"  # <-- This activates the webhook
  name: test
---
apiVersion: v1
kind: Pod
metadata:
  name: test-6cf468f7b7-2g4c7
spec:
  serviceAccountName: test
  initContainers:
  - name: aws-setup
    image: amazon/aws-cli:latest
    command:
    - sh
    args:
    - -c
    - |
        aws configure set default.s3.addressing_style virtual
        # Use https://cwobject.com if using from outside of a CKS Cluster
        aws configure set endpoint_url "http://cwlota.com"
    volumeMounts:
    - mountPath: /config
      name: aws-config
    env:
    - name: AWS_CONFIG_FILE
      value: /config/config
  containers:
  - name: awscli
    image: amazon/aws-cli:latest
    args:
    - s3
    - ls
    env:
    - name: AWS_CONFIG_FILE
      value: /aws/config
    volumeMounts:
    - mountPath: /aws
      name: aws-config
  volumes:
  - name: aws-config
    emptyDir: {}
```

The resulting `Pod` has autoinjected configuration, like the following example (some fields omitted for clarity). The webhook fills in `[ORG-ID]` in `AWS_CONTAINER_CREDENTIALS_FULL_URI` with your CoreWeave organization ID:

```yaml title="created-pod-config.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: rclone-test-hj7cc
spec:
  containers:
  - args:
    - lsd
    - 'caios:'
    - -vv
    env:
    - name: RCLONE_CONFIG
      value: /config/rclone.conf
    - name: AWS_DEFAULT_REGION
      value: US-EAST-04A
    - name: AWS_REGION
      value: US-EAST-04A
    - name: AWS_CONTAINER_CREDENTIALS_FULL_URI
      value: https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
    - name: AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE
      value: /var/run/secrets/cks.coreweave.com/serviceaccount/cks-pod-identity-token
    image: rclone/rclone
    name: rclone
    volumeMounts:
    - mountPath: /config
      name: rclone-conf
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-gzzsm
      readOnly: true
    - mountPath: /var/run/secrets/cks.coreweave.com/serviceaccount
      name: cks-pod-identity-token
      readOnly: true
  serviceAccountName: test
  volumes:
  - name: cks-pod-identity-token
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          audience: https://coreweave.com/iam
          expirationSeconds: 600
          path: cks-pod-identity-token
  - configMap:
      defaultMode: 420
      name: rclone-conf
    name: rclone-conf
  - name: kube-api-access-gzzsm
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
```

## Example chart configuration

The following section shows the values you set when you install the chart. To find the values for this configuration:

* Find your CoreWeave Organization ID in the [CoreWeave Console settings page](https://console.coreweave.com/account/settings).
* Use one of the following regions supported by AI Object Storage to configure the webhook:

  > [accordion] Availability Zones that support AI Object Storage
  >
  > > [tab] US-CENTRAL
  > >
  > > * `US-CENTRAL-05A`
  > > * `US-CENTRAL-06A`
  > > * `US-CENTRAL-07A`
  > > * `US-CENTRAL-08A`
  > > * `US-CENTRAL-08B`
  >
  > > [tab] US-EAST
  > >
  > > * `US-EAST-01A`
  > > * `US-EAST-02A`
  > > * `US-EAST-03A`
  > > * `US-EAST-04A`
  > > * `US-EAST-04B`
  > > * `US-EAST-06A`
  > > * `US-EAST-08A`
  > > * `US-EAST-13A`
  > > * `US-EAST-14A`
  > > * `US-EAST-15A`
  > > * `US-EAST-17A`
  >
  > > [tab] US-WEST
  > >
  > > * `RNO2A`
  > > * `US-WEST-01A`
  > > * `US-WEST-04A`
  > > * `US-WEST-09B`
  > > * `US-WEST-10A`
  >
  > > [tab] CA-EAST
  > >
  > > * `CA-EAST-01A`
  >
  > > [tab] EU-NORTH
  > >
  > > * `EU-NORTH-05A`
  >
  > > [tab] EU-SOUTH
  > >
  > > * `EU-SOUTH-03B`
  > > * `EU-SOUTH-04A`
  >
  > Learn more about [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).
* Find the `audience` value in your [OIDC Workload Federation](https://console.coreweave.com/organization/iam/workload-federation/oidc) configuration. The default value is `https://coreweave.com/iam`. It matches the OIDC configuration that CoreWeave creates automatically for each CKS cluster with OIDC Workload Identity enabled. Only set a different `audience` if you created an OIDC configuration with a custom audience.

```yaml title="pod-identity-webhook.yaml" theme={"system"}
config:
  # -- The CoreWeave Organization ID, six-character hexadecimal string found in the CoreWeave Console settings page
  orgID: "cweeee"

  # -- The CoreWeave <a href="https://docs.coreweave.com/glossary#availability-zone-az">Availability Zone (AZ)</a>, used as an AWS Region
  # Example: US-EAST-04A
  # See the <a href="https://docs.coreweave.com/platform/regions/about-regions-and-azs">CoreWeave Docs on Regions and AZs</a>
  region: "US-EAST-04A"

  # -- The Audience to be used for the projected token.
  # Must match the Audience requirement found in the Cloud Console
  # Workload Federation (OIDC) configuration.
  audience: https://coreweave.com/iam
```
