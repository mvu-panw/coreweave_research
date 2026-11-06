# Access Google Cloud Storage from CKS pods

Source: https://docs.coreweave.com/products/cks/auth-access/workload-identity/oidc-gcp

# Access Google Cloud Storage from CKS pods

> Configure secure access to Google Cloud Storage from CKS pods using OIDC Workload Identity Federation

This tutorial demonstrates how to configure a CoreWeave Kubernetes Service (CKS) cluster to authenticate to Google Cloud Storage (GCS) using OIDC Workload Identity Federation. By the end of this tutorial, a Kubernetes ServiceAccount in CKS can access GCS directly, without any stored credentials. This pattern is useful for teams running data, ML, or batch workloads on CKS that need secure, short-lived access to GCS buckets without managing static service account keys.

## Overview

CKS issues OIDC-compliant ServiceAccount tokens to pods. Workloads can use these tokens to authenticate to external services like Google Cloud Platform (GCP) by establishing OIDC trust. This eliminates the need for long-lived credentials and lets you scope access to cloud resources per ServiceAccount.

Benefits of this approach:

* No credentials are stored in secrets or container images.
* Tokens are short-lived and rotated automatically by Kubernetes.
* IAM permissions can be tightly scoped to individual ServiceAccounts.
* No TLS thumbprint management is required, as with AWS.

After completing this tutorial, you'll have the following setup:

1. **Pod requests access**: The `gcs-client` pod uses its mounted OIDC token.
2. **GCP validates identity**: Google Cloud verifies the token against your CKS cluster's OIDC endpoint.
3. **Impersonation granted**: GCP lets the pod impersonate the `gcs-reader` service account.
4. **Resource access**: The pod can read from your GCS bucket using temporary credentials.

## Prerequisites

Before you begin, ensure you have the following:

### CoreWeave requirements

* **CKS cluster**: A CoreWeave Kubernetes Service cluster with OIDC Workload Identity enabled.
* **Cluster access**: `kubectl` configured to access your CKS cluster.
* **Cluster details**: Your cluster's OIDC issuer URL (instructions to find this are included in this tutorial).

### Google Cloud Platform requirements

* **GCP project**: A Google Cloud Platform project where you'll configure Workload Identity.
* **GCP permissions**: Your GCP account must have the following IAM roles:
  * `Workload Identity Pool Admin` (to create pools and providers).
  * `Service Account Admin` (to create and manage service accounts).
  * `Project IAM Admin` (to bind service accounts to workload identities).
* **GCS bucket**: A Google Cloud Storage bucket for testing (or permission to create one).

### Command line tools

* **gcloud CLI**: [Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/install-sdk) installed and authenticated.
* **kubectl**: Kubernetes command line tool configured for your CKS cluster.

### GCP project information

You'll need these values during the tutorial. Gather them beforehand:

* **Project ID**: Your GCP project ID (for example, `my-project-123`).
* **Project Number**: Your GCP project number (numeric, for example, `123456789012`).

To find your project details:

```bash theme={"system"}
# Get both project ID and number
gcloud projects describe $(gcloud config get-value project)
```

### Verify your setup

Test that everything is configured correctly:

```bash theme={"system"}
# Verify gcloud authentication and project ID
gcloud auth list
gcloud config get-value project

# Verify kubectl access to your CKS cluster
kubectl get nodes

# Verify you have necessary GCP permissions
gcloud iam workload-identity-pools list --location=global
```

If any of these commands fail, resolve the authentication or permission issues before proceeding.

## Set up Kubernetes resources

Before configuring GCP, you need to create the Kubernetes namespace and ServiceAccount that you grant access to GCS. These resources represent the identity that GCP trusts through Workload Identity Federation.

The following sections describe how to create the namespace, ServiceAccount, and verify them.

### Create the namespace

Create a namespace called `foo` where your workloads will run:

```bash theme={"system"}
kubectl create namespace foo
```

### Create the ServiceAccount

Create a ServiceAccount called `bar` that your pods will use:

```bash theme={"system"}
kubectl create serviceaccount bar --namespace foo
```

### Verify the resources

Confirm both resources were created successfully:

```bash theme={"system"}
# Verify the namespace exists
kubectl get namespace foo

# Verify the ServiceAccount exists
kubectl get serviceaccount bar --namespace foo

# View the ServiceAccount details (including any tokens)
kubectl describe serviceaccount bar --namespace foo
```

Expected output should show:

* Namespace `foo` in `Active` status.
* ServiceAccount `bar` exists in the `foo` namespace.
* ServiceAccount has default token secrets (projected OIDC tokens replace these).

### Map Kubernetes resources to GCP identities

These Kubernetes resources will map to GCP identities as follows:

* **Namespace**: `foo` → GCP attribute `attribute.k8s_ns=foo`.
* **ServiceAccount**: `bar` → GCP attribute `attribute.k8s_sa=bar`.

When you configure the GCP Workload Identity binding, you reference this specific combination (`foo/bar`) to ensure only pods running with this ServiceAccount in this namespace can access your GCS resources.

> [!TIP]
>
> You can use different namespace and ServiceAccount names, but make sure to update all the GCP commands accordingly. The tutorial uses `foo/bar` as an example, but in production, use more descriptive names like `data-pipeline/gcs-reader`.

### Get the OIDC issuer URL from CKS

With the Kubernetes resources in place, the next step is to gather the cluster details that GCP needs to trust tokens issued by CKS.

To use identity federation, you must know the OIDC Issuer URL of your CKS cluster. This is the base URL that serves token metadata and keys. The URL is formatted as a valid HTTPS URL, such as:
`https://oidc.cks.coreweave.com/id/[CLUSTER-ID]`.

You can obtain it in a few ways:

> [tab] Cloud Console
>
> 1. In the Cloud Console, navigate to the [Clusters](https://console.coreweave.com/clusters) page.
> 2. Click the name of the cluster to expand the cluster details panel.
> 3. The OIDC Issuer URL is displayed in the **Overview** section.

> [tab] CKS API
>
> Use the CoreWeave Cloud API to query the cluster configuration and extract the `serviceAccountIssuer` value.
> Otherwise, you can call the [CKS API to get the CKS OIDC config](https://docs.coreweave.com/products/cks/reference/cks-api.md#get-/v1beta1/cks/clusters):
>
> ```bash title="Get the CKS OIDC config through the API" theme={"system"}
> curl -s -X GET https://api.coreweave.com/v1beta1/cks/clusters/{cluster-id} \
>      -H "Content-Type: application/json" \
>      -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
>      | jq -r '.cluster.oidc.issuerUrl'
> ```

> [tab] Terraform
>
> If you're using CoreWeave's Terraform provider, you can export the OIDC issuer as an output during cluster provisioning.
>
> The CKS OIDC config is an [attribute you can read from your Terraform provider](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs/data-sources/cks_cluster#nested-schema-for-oidc).
>
> Ensure the issuer endpoint exposes a `.well-known/openid-configuration` path and a valid JWKS endpoint.

### Create a workload identity pool in GCP

With the issuer URL in hand, you can now configure the GCP side of the trust relationship. A workload identity pool is the GCP construct that groups external identities (in this case, your CKS pods) so that IAM policies can reference them.

1. Create a pool to represent trusted external identities (your CKS pods):

   ```bash theme={"system"}
   gcloud iam workload-identity-pools create k8s-pool \
     --location="global" \
     --display-name="CKS Pool"
   ```

2. Confirm the pool was created successfully:

   ```bash theme={"system"}
   gcloud iam workload-identity-pools describe k8s-pool --location=global
   ```

   Expected output should show:

   * `state: ACTIVE`.
   * `name: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/k8s-pool`.

   If this fails, check that you have the `Workload Identity Pool Admin` role and are authenticated to the correct GCP project.

### Create an OIDC provider in the pool

The pool now exists, but it isn't yet configured to validate or interpret CKS tokens. Adding an OIDC provider specifies which issuer GCP trusts and how to map Kubernetes token claims to identity attributes based on namespace and ServiceAccount name.

1. Configure the provider to trust your CKS OIDC issuer and extract identity information from tokens. Replace `[REGION]` and `[CLUSTER-ID]` with your values.

   ```bash theme={"system"}
   gcloud iam workload-identity-pools providers create-oidc k8s-provider \
     --location="global" \
     --workload-identity-pool="k8s-pool" \
     --display-name="CKS OIDC Provider" \
     --issuer-uri="https://oidc.cks.coreweave.com/id/[CLUSTER-ID]" \
     --attribute-mapping="google.subject=assertion.sub,attribute.k8s_ns=assertion.kubernetes.io/serviceaccount/namespace,attribute.k8s_sa=assertion.kubernetes.io/serviceaccount/name"
   ```

2. Check that the provider was configured correctly:

   ```bash theme={"system"}
   gcloud iam workload-identity-pools providers describe k8s-provider \
     --location=global \
     --workload-identity-pool=k8s-pool
   ```

   Expected output should include:

   * `state: ACTIVE`.
   * Your CKS OIDC issuer URL in the `issuerUri` field.
   * The attribute mapping you configured.

### Create a Google Cloud service account and grant access

GCP now trusts your CKS cluster as an identity source, but federated identities still need a Google Cloud Service Account to impersonate to access GCP resources. In this section, you create that service account and grant it permission to read from GCS.

1. Create the service account that CKS workloads impersonate:

   ```bash theme={"system"}
   gcloud iam service-accounts create gcs-reader \
     --display-name="CKS GCS Reader"
   ```

2. Grant it permission to read from GCS. Replace `[PROJECT-ID]` with your project ID.

   ```bash theme={"system"}
   gcloud projects add-iam-policy-binding [PROJECT-ID] \
     --member="serviceAccount:gcs-reader@[PROJECT-ID].iam.gserviceaccount.com" \
     --role="roles/storage.objectViewer"
   ```

### Bind the CKS service account to the GSA

This binding connects the Kubernetes identity to the Google Cloud Service Account and controls which CKS pods can impersonate `gcs-reader`.

1. Authorize the Kubernetes ServiceAccount `bar` in namespace `foo` to impersonate the GSA through the identity pool. Replace `[PROJECT-NUMBER]` and `[PROJECT-ID]` with your values.

   ```bash theme={"system"}
   gcloud iam service-accounts add-iam-policy-binding gcs-reader@[PROJECT-ID].iam.gserviceaccount.com \
     --role="roles/iam.workloadIdentityUser" \
     --member="principalSet://iam.googleapis.com/projects/[PROJECT-NUMBER]/locations/global/workloadIdentityPools/k8s-pool/attribute.k8s_ns/foo/attribute.k8s_sa/bar"
   ```

2. Check that the binding was created correctly. Replace `[PROJECT-ID]` with your project ID.

   ```bash theme={"system"}
   gcloud iam service-accounts get-iam-policy gcs-reader@[PROJECT-ID].iam.gserviceaccount.com
   ```

   Expected output should include a binding with:

   * `role: roles/iam.workloadIdentityUser`.
   * `members` containing your `principalSet://iam.googleapis.com/projects/...` entry.

Only tokens issued to the `foo/bar` ServiceAccount can impersonate the `gcs-reader` account.

### Prepare a test GCS bucket

Before testing the authentication, create a GCS bucket or use an existing one:

> [tab] Create new test bucket
>
> ```bash theme={"system"}
> # Create a test bucket (bucket names must be globally unique)
> gsutil mb gs://my-cks-test-bucket-$(date +%s)
>
> # Add a test file
> echo "Hello from CKS!" | gsutil cp - gs://my-cks-test-bucket-$(date +%s)/test.txt
> ```

> [tab] Use existing bucket
>
> If you have an existing bucket, ensure the `gcs-reader` service account has appropriate permissions. Replace `[YOUR-BUCKET-NAME]` with your bucket name.
>
> ```bash theme={"system"}
> # Grant the service account access to your bucket
> gsutil iam ch serviceAccount:gcs-reader@[PROJECT-ID].iam.gserviceaccount.com:objectViewer gs://[YOUR-BUCKET-NAME]
> ```

If bucket creation fails, check the following:

* Bucket names must be globally unique. Try adding a timestamp or random suffix.
* Ensure you have `Storage Admin` permissions in your GCP project.

### Use a projected OIDC token in a pod to access GCS

With the trust relationship and IAM bindings in place, you're ready to test end-to-end access from a pod. In your workload, configure a projected service account token with the proper audience.

Create a pod YAML file called `gcs-client-pod.yaml` with the following content, filling in the placeholder values for `[PROJECT-NUMBER]`, `[PROJECT-ID]`, and `[YOUR-BUCKET-NAME]`.

```yaml title="gcs-client-pod.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: gcs-client
spec:
  serviceAccountName: bar
  containers:
  - name: gcs
    image: google/cloud-sdk:slim
    command:
    - bash
    - -c
    - |
      gcloud iam workload-identity-pools create-cred-config \
        projects/[PROJECT-NUMBER]/locations/global/workloadIdentityPools/k8s-pool/providers/k8s-provider \
        --service-account="gcs-reader@[PROJECT-ID].iam.gserviceaccount.com" \
        --credential-source-file=/var/run/secrets/tokens/oidc-token \
        --output-file=/tmp/creds.json && \
      gcloud auth login --cred-file=/tmp/creds.json && \
      gsutil ls gs://[YOUR-BUCKET-NAME]
    volumeMounts:
    - name: oidc-token
      mountPath: /var/run/secrets/tokens
    - name: creds
      mountPath: /tmp
  volumes:
  - name: oidc-token
    projected:
      sources:
      - serviceAccountToken:
          path: oidc-token
          audience: //iam.googleapis.com/projects/[PROJECT-NUMBER]/locations/global/workloadIdentityPools/k8s-pool/providers/k8s-provider
          expirationSeconds: 3600
  - name: creds
    emptyDir: {}
```

This pod uses the projected token to generate GCP-compatible credentials at runtime, then uses them to read from GCS.

#### Deploy and test the pod

1. Apply the pod configuration:

   ```bash theme={"system"}
   kubectl apply -f gcs-client-pod.yaml -n foo
   ```

2. Wait for the pod to start and check its status:

   ```bash theme={"system"}
   kubectl get pod gcs-client -n foo
   kubectl logs gcs-client -n foo
   ```

If the pod fails, check the following:

* `Error 403: Permission denied`: Check that the `gcs-reader` service account has access to your bucket.
* `Invalid token`: Verify your OIDC issuer URL matches your cluster's endpoint.
* Pod won't start: Ensure the `bar` ServiceAccount exists in the `foo` namespace.

Debug commands:

```bash theme={"system"}
# Check if token is being mounted
kubectl exec gcs-client -n foo -- ls -la /var/run/secrets/tokens/

# View detailed pod events
kubectl describe pod gcs-client -n foo
```

At this point you have a working OIDC Workload Identity Federation setup: CKS pods running with the `bar` ServiceAccount in the `foo` namespace can access your GCS bucket using short-lived, automatically rotated credentials.

## Clean up resources

If you're done testing, remove the resources to avoid charges and maintain security:

### Remove Kubernetes resources

```bash theme={"system"}
# Delete the test pod
kubectl delete pod gcs-client -n foo

# Delete the ServiceAccount (optional, if you're not using it elsewhere)
kubectl delete serviceaccount bar -n foo

# Delete the namespace (optional, will remove everything in it)
kubectl delete namespace foo
```

### Remove GCP resources

```bash theme={"system"}
# Remove the IAM binding
gcloud iam service-accounts remove-iam-policy-binding gcs-reader@[PROJECT-ID].iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/[PROJECT-NUMBER]/locations/global/workloadIdentityPools/k8s-pool/attribute.k8s_ns/foo/attribute.k8s_sa/bar"

# Delete the Google Cloud Service Account
gcloud iam service-accounts delete gcs-reader@[PROJECT-ID].iam.gserviceaccount.com

# Delete the OIDC provider
gcloud iam workload-identity-pools providers delete k8s-provider \
  --location=global \
  --workload-identity-pool=k8s-pool

# Delete the Workload Identity Pool
gcloud iam workload-identity-pools delete k8s-pool \
  --location=global
```

### Remove test bucket (if created)

```bash theme={"system"}
# Delete the test bucket and its contents
gsutil rm -r gs://[YOUR-BUCKET-NAME]
```

> [!WARNING]
>
> **Deleting shared resources**
>
> Deleting the Workload Identity Pool will break authentication for any other applications using it. Only delete shared resources if you're sure they're not needed elsewhere.
