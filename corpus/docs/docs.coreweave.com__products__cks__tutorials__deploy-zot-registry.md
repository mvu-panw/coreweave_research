# Deploy a container registry on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-zot-registry

# Deploy a container registry on CKS

> Deploy an internal OCI container registry backed by CoreWeave AI Object Storage and LOTA on CKS

This tutorial shows you how to deploy [Zot](https://zotregistry.dev/), a container registry built for OCI, on CoreWeave Kubernetes Service (CKS). You'll store container images in CoreWeave AI Object Storage and use [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) as the S3 endpoint for faster reads within the cluster. When you finish, you'll have a private, TLS-secured registry that your CKS workloads can pull from and push to using a public hostname under `.coreweave.app`.

> [!NOTE]
>
> **OCI conformance**
>
> CoreWeave has tested that the Zot registry passes the [OCI Distribution Specification conformance suite](https://github.com/opencontainers/distribution-spec/tree/main/conformance), validating its compliance with the Open Container Initiative standards on the CoreWeave cloud. The conformance suite tests core registry operations including push and pull workflows, content discovery, and content management. This certification confirms that Zot works reliably with OCI-compatible tooling and clients across the container ecosystem.

## What you'll use

This tutorial uses:

* **[Zot](https://zotregistry.dev/)**: Container registry built for OCI.
* **[CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/about.md)**: S3-compatible object storage for image layers.
* **[LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md)**: Local Object Transport Accelerator for in-cluster performance.
* **[cert-manager](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md)**: Automatic TLS certificate management.
* **[Public LoadBalancer Service](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md)**: Direct external exposure with a public FQDN under `.coreweave.app`.

## What you'll do

In this tutorial, you:

1. **Install cert-manager** to issue a TLS certificate for the registry.
2. **Create registry credentials** for authenticating with the registry.
3. **Issue a TLS certificate** for the registry hostname.
4. **Deploy Zot** using Helm with S3-backed storage through LOTA, a public LoadBalancer Service, and the TLS certificate mounted into the Pod.
5. **Push and pull a container image** to verify the registry.

## Prerequisites

Before you start, you must have:

* A working [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md).
* Access Key and Secret Key with permissions to use a [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) bucket.

You'll need the following tools on your local machine:

* [kubectl](https://kubernetes.io/docs/reference/kubectl/) installed and [configured for your cluster](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
* [Helm](https://helm.sh/docs/intro/install/) version 3.8+.
* [Docker](https://docs.docker.com/get-started/get-docker/) or another OCI-compatible client.

## Verify cluster access

Before installing anything, confirm that `kubectl` is configured for the right cluster and that the cluster has the Node types this tutorial requires.

Verify that you can access your cluster with `kubectl`:

```bash theme={"system"}
kubectl cluster-info
```

You should see something similar to:

```text theme={"system"}
Kubernetes control plane is running at...
CoreDNS is running at...
node-local-dns is running at...
```

Verify your cluster has at least one CPU Node:

```bash theme={"system"}
kubectl get nodes -o=custom-columns="NAME:metadata.name,CLASS:metadata.labels['node\.coreweave\.cloud\/class']"
```

You should see at least one Node with `cpu` in the `CLASS` column:

```text theme={"system"}
NAME      CLASS
g5424e0   cpu
gd926d4   gpu
```

## Install cert-manager

This tutorial uses the [CoreWeave cert-manager Helm chart](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/cert-manager.md) to issue a TLS certificate for the registry.

Add the CoreWeave Helm repository:

```bash theme={"system"}
helm repo add coreweave https://charts.core-services.ingress.coreweave.com
helm repo update
```

Install `cert-manager`:

```bash theme={"system"}
helm upgrade --install cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --create-namespace
```

Enable the cert-issuers subchart to create Let's Encrypt `ClusterIssuers`:

```bash theme={"system"}
helm upgrade cert-manager coreweave/cert-manager \
  --namespace cert-manager \
  --set cert-issuers.enabled=true
```

Verify the `ClusterIssuers` are ready:

```bash theme={"system"}
kubectl get clusterissuer
```

You should see:

```text theme={"system"}
NAME                        READY   AGE
letsencrypt-prod            True    60s
letsencrypt-staging         True    60s
selfsigned-cluster-issuer   True    60s
```

## Determine the registry hostname

You need the registry's public hostname before you can issue a TLS certificate or push and pull images, so determine it now and reuse it in the steps that follow.

CoreWeave's External Hostname Controller allocates an FQDN under `.coreweave.app` for any public LoadBalancer Service annotated with `service.beta.kubernetes.io/external-hostname`. For more details, see [Create a public DNS name](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md).

Your registry hostname follows this pattern:

```text theme={"system"}
registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app
```

Replace:

* `[ORG-ID]` with your [organization ID](https://docs.coreweave.com/security/authn-authz/orgs-users.md#organization-ids).
* `[CLUSTER-NAME]` with the name of the target CKS cluster.

For example, if your Org ID is `abc123` and your cluster is named `prod`, your registry hostname is `registry.abc123-prod.coreweave.app`. Note this hostname for the following steps.

> [!TIP]
>
> If you already have any public LoadBalancer Service running in the cluster, you can inspect its `ExternalRecords` status condition to confirm the DNS suffix. Replace `[SERVICE-NAME]` and `[NAMESPACE]` with the name and namespace of that Service:
>
> ```bash theme={"system"}
> kubectl get svc [SERVICE-NAME] -n [NAMESPACE] \
>   -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
> ```

## Create a storage bucket

Zot uses an AI Object Storage bucket as its backing store for image layers and manifests. Create an AI Object Storage bucket in the [Cloud Console](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md). Note the bucket name for later use.

## Generate access credentials

Zot authenticates to the bucket with an S3-compatible Access Key. Create an [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) for the bucket in the Cloud Console. Save the **Access Key ID** and **Secret Key**. You'll need both when configuring Zot's storage driver.

## Create registry credentials

These credentials control who can push and pull images through the registry itself, separate from the bucket credentials in the previous step.

Generate a bcrypt-hashed password for the registry admin user. Replace `[USERNAME]` and `[PASSWORD]` with your chosen credentials:

```bash theme={"system"}
export REGISTRY_USER="[USERNAME]"
export REGISTRY_PASS="[PASSWORD]"
export HTPASSWD=$(htpasswd -nbB "$REGISTRY_USER" "$REGISTRY_PASS")
```

> [!NOTE]
>
> If `htpasswd` is not installed, install it with `apt-get install apache2-utils` on Debian/Ubuntu or `brew install httpd` on macOS.

> [!NOTE]
>
> This tutorial uses `htpasswd` for simplicity. Zot also supports [LDAP](https://zotregistry.dev/v2.1.14/articles/authn-authz/#ldap), [mutual TLS](https://zotregistry.dev/v2.1.14/articles/authn-authz/#mutual-tls-authentication), [bearer token (OAuth2)](https://zotregistry.dev/v2.1.14/articles/authn-authz/#http-bearer-authentication), and [OpenID Connect](https://zotregistry.dev/v2.1.14/articles/authn-authz/#social-login-using-openidoauth2) with providers like GitHub, Google, and GitLab.

Create a Kubernetes Secret containing the `htpasswd` file:

```bash theme={"system"}
kubectl create secret generic registry-htpasswd \
  --from-literal=htpasswd="$HTPASSWD"
```

## Issue a TLS certificate

Create a `Certificate` resource so `cert-manager` issues a TLS certificate for your registry hostname using the bundled `letsencrypt-prod` `ClusterIssuer`.

Save the following as `registry-cert.yaml`. Replace `registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app` with the hostname from the [previous step](#determine-the-registry-hostname):

```yaml title="registry-cert.yaml" theme={"system"}
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: registry-cert
spec:
  secretName: registry-cert
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app
```

Apply the manifest:

```bash theme={"system"}
kubectl apply -f registry-cert.yaml
```

Wait for the certificate to be ready. Issuance typically completes within one to two minutes:

```bash theme={"system"}
kubectl wait --for=condition=Ready certificate/registry-cert --timeout=5m
```

You should see:

```text theme={"system"}
certificate.cert-manager.io/registry-cert condition met
```

Confirm the certificate and its backing Secret exist:

```bash theme={"system"}
kubectl get certificate registry-cert
kubectl get secret registry-cert
```

The Secret contains `tls.crt` and `tls.key` keys, which you'll mount into the Zot Pod in the next step.

## Deploy Zot

With the certificate, bucket, and credentials in place, you can now install Zot itself. The following Helm values wire together the storage bucket through LOTA, the `htpasswd` Secret for authentication, the `cert-manager`-issued TLS Secret, and the public LoadBalancer Service annotations.

Add the Zot Helm repository:

```bash theme={"system"}
helm repo add zotregistry http://zotregistry.dev/helm-charts
helm repo update
```

Create a `zot-values.yaml` file. Replace the placeholder values with your own:

```yaml title="zot-values.yaml" theme={"system"}
replicaCount: 1

strategy:
  type: Recreate

serviceAccount:
  create: true

service:
  type: LoadBalancer
  port: 443
  annotations:
    service.beta.kubernetes.io/external-hostname: registry
    service.beta.kubernetes.io/coreweave-load-balancer-type: public

ingress:
  enabled: false

httpGet:
  scheme: HTTPS
  port: 5000

extraVolumes:
  - name: registry-tls
    secret:
      secretName: registry-cert

extraVolumeMounts:
  - name: registry-tls
    mountPath: /tls
    readOnly: true

persistence: false

mountConfig: true
configFiles:
  config.json: |
    {
      "storage": {
        "rootDirectory": "/tmp/zot",
        "dedupe": false,
        "storageDriver": {
          "name": "s3",
          "rootdirectory": "/zot",
          "region": "[REGION]",  # Replace with your bucket's region (for example, us-east-14a)
          "bucket": "[BUCKET-NAME]",  # Replace with your AI Object Storage bucket name
          "regionendpoint": "http://cwlota.com",
          "accesskey": "[ACCESS-KEY-ID]",  # Replace with your Access Key ID
          "secretkey": "[SECRET-KEY]",  # Replace with your Secret Key
          "forcepathstyle": false,
          "secure": false,
          "skipverify": false
        }
      },
      "http": {
        "address": "0.0.0.0",
        "port": "5000",
        "tls": {
          "cert": "/tls/tls.crt",
          "key": "/tls/tls.key"
        },
        "compat": ["docker2s2"],
        "auth": {
          "htpasswd": {
            "path": "/secret/htpasswd"
          }
        },
        "accessControl": {
          "adminPolicy": {
            # Replace [USERNAME] with the registry admin username from the credentials step
            "users": ["[USERNAME]"],
            "actions": ["read", "create", "update", "delete"]
          }
        }
      },
      "log": { "level": "info" }
    }

mountSecret: true
secretFiles:
  # Replace [HTPASSWD-STRING] with the $HTPASSWD value from the credentials step
  htpasswd: [HTPASSWD-STRING]
```

Replace the following placeholders:

| Placeholder | Value |
| - | - |
| `[REGION]` | The region of your AI Object Storage bucket (for example, `us-east-14a`) |
| `[BUCKET-NAME]` | Your AI Object Storage bucket name |
| `[ACCESS-KEY-ID]` | Your AI Object Storage Access Key ID |
| `[SECRET-KEY]` | Your AI Object Storage Secret Key |
| `[USERNAME]` | The registry admin username from the credentials step |
| `[HTPASSWD-STRING]` | The `$HTPASSWD` value generated in the credentials step |

**Configuration notes:**

* The `service` block creates a public `LoadBalancer` Service. The `external-hostname: registry` annotation instructs the External Hostname Controller to allocate `registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app` for the Service. The `coreweave-load-balancer-type: public` annotation provisions a public IP. The Service listens on port 443 and forwards to the container's `zot` named port, which is set by `httpGet.port` (described in the following item).
* The `ingress.enabled: false` field disables the chart's Ingress resource. External clients connect directly to the LoadBalancer Service, so no ingress controller is required.
* The `httpGet` block sets the probe scheme to `HTTPS` and the container port to `5000`. The chart uses these values for its startup probe and to name the container port that the Service targets. The scheme must be `HTTPS` because Zot terminates TLS on this port. Probing with `HTTP` fails.
* The `extraVolumes` and `extraVolumeMounts` fields mount the `registry-cert` Secret (created by `cert-manager` in the [previous step](#issue-a-tls-certificate)) at `/tls` inside the Zot container. The `http.tls` block in the Zot config points to `tls.crt` and `tls.key` in that directory, so Zot terminates TLS directly.
* The `region` must match where your AI Object Storage bucket was created. Find this in the [Cloud Console](https://console.coreweave.com/object-storage/buckets) on the bucket details page.
* The `regionendpoint` is set to `http://cwlota.com`, the [LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) endpoint. LOTA caches object storage reads on local Node disks for faster access. The `secure` field is `false` because LOTA uses HTTP within the cluster. To access the bucket from outside a CKS cluster, use `https://cwobject.com` as the endpoint and set `secure` to `true`.
* The `compat: ["docker2s2"]` field enables Docker v2 manifest support. Without this, `docker push` fails because Zot rejects Docker v2 manifests by default. Remove this field if your workflow exclusively uses OCI-format images.

Install the chart:

```bash theme={"system"}
helm upgrade --install zot zotregistry/zot \
  --version 0.1.98 \
  --atomic \
  --timeout 120s \
  -f zot-values.yaml
```

> [!NOTE]
>
> `cert-manager` renews the `registry-cert` Secret automatically before expiry. Because the Secret is mounted into the Zot Pod, the updated certificate is available on disk after rotation. Restart the Zot Pod to pick up the renewed certificate if Zot does not reload it automatically.

Verify the Pod is running:

```bash theme={"system"}
kubectl get pods -l app.kubernetes.io/name=zot
```

You should see:

```text theme={"system"}
NAME                   READY   STATUS    RESTARTS   AGE
zot-7b8f9d4c5f-k2vqp   1/1     Running   0          30s
```

Verify the LoadBalancer Service has an external IP and the expected public FQDN:

```bash theme={"system"}
kubectl get svc zot
kubectl get svc zot -o=jsonpath='{.status.conditions[?(@.type=="ExternalRecords")].message}'
```

The `EXTERNAL-IP` column shows a public IP address, and the second command prints `registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app`. DNS propagation typically completes within one to two minutes.

## Verify the registry

Confirm that the registry is reachable, that authentication works, and that the S3-backed storage driver is wired up correctly by pushing and pulling a small test image.

Log in to your registry using Docker. Replace `[ORG-ID]` and `[CLUSTER-NAME]` with the values for your cluster, and use the username and password you created in the [Create registry credentials](#create-registry-credentials) step:

```bash theme={"system"}
docker login registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app -u $REGISTRY_USER
```

When prompted, enter the password from `REGISTRY_PASS` in the [Create registry credentials](#create-registry-credentials) section (or use `-p $REGISTRY_PASS` to provide it directly).

Push a test image:

```bash theme={"system"}
docker pull hello-world
docker tag hello-world registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/hello-world:latest
docker push registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/hello-world:latest
```

You should see the image layers pushed:

```text theme={"system"}
The push refers to repository [registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/hello-world]
ac28800ec8bb: Pushed
latest: digest: sha256:... size: 524
```

Pull the image back to verify:

```bash theme={"system"}
docker pull registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/hello-world:latest
```

You should see:

```text theme={"system"}
latest: Pulling from hello-world
Digest: sha256:...
Status: Image is up to date for registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/hello-world:latest
```

## Enable the web UI (optional)

Zot ships with an optional web UI that lets you browse repositories, tags, and image manifests in a browser. The UI is deactivated by default. To turn it on, enable the `ui` and `search` [Zot extensions](https://zotregistry.dev/v2.1.14/articles/mirroring/#extensions) in the Zot config. Both are required because the UI depends on the `search` extension for catalog data.

Add the following `extensions` block to the `http` object in `zot-values.yaml`. Place it as a sibling of `log`:

```json title="zot-values.yaml: configFiles.config.json additions" theme={"system"}
"log": { "level": "info" },
"extensions": {
  "ui":     { "enable": true },
  "search": { "enable": true }
}
```

Apply the change with `helm upgrade`:

```bash theme={"system"}
helm upgrade zot zotregistry/zot \
  --version 0.1.98 \
  --atomic \
  --timeout 120s \
  -f zot-values.yaml
```

Wait for the Pod to roll out:

```bash theme={"system"}
kubectl rollout status deployment/zot --timeout=60s
```

Open the UI in a browser:

```text theme={"system"}
https://registry.[ORG-ID]-[CLUSTER-NAME].coreweave.app/
```

The UI prompts for credentials. Sign in with the admin username and password from the [Create registry credentials](#create-registry-credentials) step.

> [!NOTE]
>
> **Retrieving the login password**
>
> Zot stores only the bcrypt hash of the password in the `registry-htpasswd` Secret, so you can't read the plaintext password back from the cluster. If your shell still has the `$REGISTRY_PASS` environment variable from the [Create registry credentials](#create-registry-credentials) step, print it with:
>
> ```bash theme={"system"}
> echo "$REGISTRY_PASS"
> ```
>
> If `$REGISTRY_PASS` is no longer set, use the plaintext password you chose when you generated the `htpasswd` entry. If you've lost the password, rotate it by generating a new `htpasswd` entry and applying it through `helm upgrade`. Replace `[NEW-PASSWORD]` with the new password you want to set:
>
> ```bash theme={"system"}
> export REGISTRY_USER="[USERNAME]"
> export REGISTRY_PASS="[NEW-PASSWORD]"
> export HTPASSWD=$(htpasswd -nbB "$REGISTRY_USER" "$REGISTRY_PASS")
> ```
>
> Update the `secretFiles.htpasswd` field in `zot-values.yaml` with the new `$HTPASSWD` value, then:
>
> ```bash theme={"system"}
> helm upgrade zot zotregistry/zot \
>   --version 0.1.98 \
>   --atomic \
>   --timeout 120s \
>   -f zot-values.yaml
> ```
>
> Sign in with the new credentials.

## What you've deployed

You now have a Zot container registry running on CKS with `htpasswd` authentication, S3-backed storage through LOTA, a Let's Encrypt TLS certificate issued through a DNS01 challenge, and a public FQDN under the `.coreweave.app` domain.

External clients connect directly to the Zot LoadBalancer Service on port 443. Zot terminates TLS inside the Pod using the mounted `registry-cert` Secret, and no ingress controller sits in the request path. `cert-manager` renews the certificate automatically before expiry.

To pull images from this registry in your CKS workloads, create an `imagePullSecret` with the same credentials you used in the [Create registry credentials](#create-registry-credentials) step.

## Clean up

If you no longer need the registry, remove it and the supporting resources so they don't continue to consume cluster and storage resources.

To remove the registry and all resources installed in this tutorial:

```bash theme={"system"}
helm uninstall zot
kubectl delete secret registry-htpasswd
kubectl delete certificate registry-cert
kubectl delete secret registry-cert
helm uninstall cert-manager -n cert-manager
```

> [!NOTE]
>
> Uninstalling `cert-manager` leaves its [Custom Resource Definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) (CRDs) in the cluster. To remove them:
>
> ```bash theme={"system"}
> kubectl get crd -o name | grep cert-manager | xargs kubectl delete
> ```

## Additional resources

* [Zot documentation](https://zotregistry.dev/v2.1.14/admin-guide/admin-configuration/)
* [About LOTA](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md)
* [Performance best practices](https://docs.coreweave.com/products/storage/object-storage/improving-performance/best-practices.md)
* [About AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/about.md)
* [Manage AI Object Storage access keys](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md)
* [Workload Identity Federation for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md)
* [Expose a Service on CKS](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md)
* [Create a public DNS name](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md)
* [CoreWeave Helm charts](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction.md)
