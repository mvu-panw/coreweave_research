# Implement unmanaged authentication

Source: https://docs.coreweave.com/products/cks/auth-access/unmanaged-auth/implement-unmanaged-auth

# Implement unmanaged authentication

> Connect to the CKS unmanaged API endpoint using OIDC, Service Account tokens, or webhook authentication

## Overview

The CoreWeave Kubernetes Service (CKS) unmanaged authentication endpoint accepts Kubernetes-native auth methods
such as OpenID Connect (OIDC) tokens, Service Account tokens, and webhook-validated tokens. Use
this endpoint when you need authentication methods that the managed CKS endpoint
doesn't support, such as integrating with an external identity provider or
authenticating CI/CD pipelines with `ServiceAccount` tokens. Its URL format is:

```text theme={"system"}
https://api.[ORG-ID]-[CLUSTER-HASH].k8s.[ZONE].coreweave.com
```

`[ORG-ID]` is your organization ID, `[CLUSTER-HASH]` is the unique hash CoreWeave assigns to the cluster, and `[ZONE]` is the cluster's Availability Zone. To construct this URL, add the `api.` prefix to the `apiServerEndpoint` value
for your cluster. For example, if your `apiServerEndpoint` is:

```text theme={"system"}
abc123-abcd1234.k8s.us-east-04a.coreweave.com
```

The unmanaged authentication endpoint is:

```text theme={"system"}
api.abc123-abcd1234.k8s.us-east-04a.coreweave.com
```

You can find the `apiServerEndpoint` for your cluster in the Overview section
of the cluster's details in the Cloud Console, or in the `apiServerEndpoint`
field under the JSON tab of the cluster details.

> [!WARNING]
>
> **Deprecation notice**
>
> CKS clusters previously offered an unmanaged authentication endpoint at
> `https://api.[ORG-ID]-[CLUSTER-NAME].k8s.[ZONE].coreweave.com`. Endpoints
> that use the **Cluster Name** instead of the **Cluster Hash** are deprecated.

> [!NOTE]
>
> The unmanaged authentication endpoint doesn't support the API access tokens in the `kubeconfig` files downloaded from the Cloud Console. You must use one of
> the authentication methods described in [Authentication methods](#authentication-methods).

## Authentication methods

The unmanaged authentication endpoint supports three methods:

* **OIDC access tokens**: Authenticate using an external identity provider such
  as Google, Okta, or Microsoft Entra. Kubernetes validates the token against
  the configured issuer. [See OIDC authentication](#oidc-authentication).
* **Service Account tokens**: Authenticate using a Kubernetes `ServiceAccount`
  token. This is the recommended pattern for CI/CD pipelines and automation.
  [See Service account authentication](#service-account-authentication).
* **Webhook authentication**: Authenticate using a custom webhook that
  implements the [Kubernetes TokenReview API](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#webhook-token-authentication).

## OIDC authentication

This section walks through configuring a CKS cluster to trust an external OIDC
provider, then connecting `kubectl` to the unmanaged endpoint using the
[`kubelogin`](https://github.com/int128/kubelogin) plugin.

### Prerequisites

Before you begin, make sure you have:

* A CKS cluster and a CoreWeave API access token with permission to read and
  update that cluster.
* Administrative access to an OIDC identity provider (such as Google, Okta, or
  Microsoft Entra).
* The following CLI tools installed: `kubectl`, `kubelogin`, `curl`, and `jq`.

On macOS, you can install `kubelogin` with:

```bash theme={"system"}
brew install int128/kubelogin/kubelogin
```

You also need an existing admin `kubeconfig` for the cluster to create the initial
role-based access control (RBAC) binding for your OIDC identity.

### Step 1: Register an OIDC application with your identity provider

Create an OIDC application in your identity provider and collect the following
values:

* **Issuer URL**: The base URL of the OIDC discovery document (for example,
  `https://accounts.google.com` for Google or
  `https://login.microsoftonline.com/[TENANT-ID]/v2.0` for Microsoft Entra).
* **Client ID**: The identifier assigned to your application.
* **Client secret**: The secret used by `kubelogin` to request tokens.

When creating the application, add `http://localhost:8000` as an authorized
redirect URI. `kubelogin` uses this URI for the local browser
authentication flow.

### Step 2: Configure OIDC on the cluster

Export your CoreWeave API access token and the OIDC values you collected:

```bash theme={"system"}
export TOKEN="[COREWEAVE-API-ACCESS-TOKEN]"
export OIDC_ISSUER_URL="[OIDC-ISSUER-URL]"
export OIDC_CLIENT_ID="[OIDC-CLIENT-ID]"
```

Retrieve your cluster's `id` and `version` (both are required in the `PATCH`
body):

```bash theme={"system"}
curl -s https://api.coreweave.com/v1beta1/cks/clusters \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  | jq '.items[] | {id, name, version, apiServerEndpoint}'
```

Record the `id`, `version`, and `apiServerEndpoint` values for your cluster.

Configure OIDC trust by sending a `PATCH` request to the cluster:

```bash theme={"system"}
export CLUSTER_ID="[CLUSTER-ID]"
export CLUSTER_VERSION="[CLUSTER-VERSION]"

curl -s -X PATCH "https://api.coreweave.com/v1beta1/cks/clusters/$CLUSTER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"id\": \"$CLUSTER_ID\",
    \"version\": \"$CLUSTER_VERSION\",
    \"oidc\": {
      \"issuerUrl\": \"$OIDC_ISSUER_URL\",
      \"clientId\": \"$OIDC_CLIENT_ID\",
      \"usernameClaim\": \"email\"
    },
    \"updateMask\": \"oidc.issuerUrl,oidc.clientId,oidc.usernameClaim\"
  }"
```

Note the following details about the `PATCH` body:

* `id` and `version` are required in the `PATCH` body.
* `updateMask` must list the specific fields being updated.
* `usernameClaim` is the token claim that Kubernetes uses as the username in
  RBAC. Using `email` produces recognizable usernames like `alice@example.com`.

To authorize users through OIDC group claims instead of individual identities,
add the group fields to the `oidc` block and include them in `updateMask`.
Replace `[GROUPS-CLAIM]` with the name of the token claim that holds group
membership (for example, `groups`), and replace `[GROUPS-PREFIX]` with a
prefix Kubernetes adds to each group name to avoid collisions with built-in
groups:

```json theme={"system"}
{
  "oidc": {
    "issuerUrl": "[OIDC-ISSUER-URL]",
    "clientId": "[OIDC-CLIENT-ID]",
    "usernameClaim": "email",
    "groupsClaim": "[GROUPS-CLAIM]",
    "groupsPrefix": "[GROUPS-PREFIX]"
  }
}
```

The `groupsClaim` field is required for group authorization. If you omit it,
the cluster reads no groups from the token, and group bindings don't match. The
cluster stays healthy, so this failure is silent.

The optional `groupsPrefix` value is prepended to every group value. Kubernetes
adds no separator, so include the delimiter in the prefix. For example, a
`groupsPrefix` of `oidc:` turns the group `platform-admins` into
`oidc:platform-admins`. Use that complete prefixed value in the `--group`
argument when you create a `RoleBinding` or `ClusterRoleBinding`.

### Step 3: Verify the OIDC configuration

After the `PATCH` request, the cluster may briefly enter an updating state. Wait
until the cluster status returns to running and the `oidc` block is present:

```bash theme={"system"}
curl -s "https://api.coreweave.com/v1beta1/cks/clusters/$CLUSTER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  | jq '.cluster | {status, oidc}'
```

Expected output when the cluster is ready:

```text theme={"system"}
{
  "status": "STATUS_RUNNING",
  "oidc": {
    "issuerUrl": "https://accounts.google.com",
    "clientId": "my-id.apps.googleusercontent.com",
    "usernameClaim": "email"
  }
}
```

### Step 4: Create an RBAC binding for the OIDC user

Configuring OIDC grants authentication. It doesn't grant any Kubernetes
permissions. You must create an RBAC binding before the user can perform any actions.

Using an existing admin `kubeconfig`, create a binding for the OIDC identity.
Replace `[PATH-TO-EXISTING-ADMIN-KUBECONFIG]` with the path to that
kubeconfig file, and replace `[USER-EMAIL-ADDRESS]` with the email address of
the user you're granting access to:

```bash theme={"system"}
export KUBECONFIG="[PATH-TO-EXISTING-ADMIN-KUBECONFIG]"
export OIDC_USERNAME="[USER-EMAIL-ADDRESS]"

kubectl create clusterrolebinding oidc-user-admin \
  --clusterrole=cluster-admin \
  --user="$OIDC_USERNAME"
```

The `--user` value must exactly match the claim value that Kubernetes reads from
the OIDC token. Because `usernameClaim: email` was configured in Step 2, the
subject here is the user's email address.

For production environments, use a narrower role than `cluster-admin`. If your
provider exposes group claims, you can bind RBAC to a group instead. Replace
`[GROUP-NAME]` with the group name from your identity provider:

```bash theme={"system"}
kubectl create clusterrolebinding oidc-platform-admins \
  --clusterrole=cluster-admin \
  --group="[GROUPS-PREFIX][GROUP-NAME]"
```

Group-based bindings are easier to operate at scale because they don't require
a new binding for each user.

### Step 5: Configure a kubectl context with kubelogin

Create a `kubectl` context that points to the unmanaged CKS endpoint and uses
`kubelogin` to obtain OIDC tokens.

Set variables for the unmanaged API endpoint and OIDC credentials:

```bash theme={"system"}
export UNMANAGED_API_SERVER="https://api.[ORG-ID]-[CLUSTER-HASH].k8s.[ZONE].coreweave.com"
export OIDC_CONTEXT="cks-oidc"
export OIDC_CREDENTIAL="cks-oidc-user"
export OIDC_CLIENT_SECRET="[OIDC-CLIENT-SECRET]"
```

Configure the cluster entry:

```bash theme={"system"}
kubectl config set-cluster "$OIDC_CONTEXT" \
  --server="$UNMANAGED_API_SERVER"
```

Configure the credentials to invoke `kubelogin`:

```bash theme={"system"}
kubectl config set-credentials "$OIDC_CREDENTIAL" \
  --exec-api-version=client.authentication.k8s.io/v1beta1 \
  --exec-command=kubectl \
  --exec-arg=oidc-login \
  --exec-arg=get-token \
  --exec-arg=--oidc-issuer-url="$OIDC_ISSUER_URL" \
  --exec-arg=--oidc-client-id="$OIDC_CLIENT_ID" \
  --exec-arg=--oidc-client-secret="$OIDC_CLIENT_SECRET" \
  --exec-arg=--oidc-extra-scope=email
```

> [!NOTE]
>
> The `--oidc-extra-scope=email` argument is required for providers such as Google
> OAuth where the email claim is not included in the default token scope. For
> other providers, check which scopes are required to include the claim you
> configured as `usernameClaim`.

Create and activate the context:

```bash theme={"system"}
kubectl config set-context "$OIDC_CONTEXT" \
  --cluster="$OIDC_CONTEXT" \
  --user="$OIDC_CREDENTIAL"

kubectl config use-context "$OIDC_CONTEXT"
```

Verify that the context points to the unmanaged endpoint:

```bash theme={"system"}
kubectl config view --minify --context="$OIDC_CONTEXT" \
  -o jsonpath='{.clusters[0].cluster.server}{"\n"}'
```

Expected output:

```text theme={"system"}
https://api.[ORG-ID]-[CLUSTER-HASH].k8s.[ZONE].coreweave.com
```

The `api.` prefix is required. Without it, `kubectl` connects to the managed
CKS endpoint, which doesn't accept OIDC tokens.

### Step 6: Test authentication

Run a Kubernetes API request to confirm the setup works:

```bash theme={"system"}
kubectl get nodes
```

`kubelogin` opens a browser window and redirects you through your provider's
login flow. After you authenticate, `kubectl` receives the ID token and retries
the request. You should see your cluster's Nodes listed.

## Service account authentication

Kubernetes `ServiceAccount` tokens are the recommended authentication method for
CI/CD pipelines and automation that need to access the CKS API. The unmanaged
endpoint accepts these tokens directly, unlike the managed auth endpoint, which
only supports CoreWeave API access tokens.

Create a `ServiceAccount` in the namespace used by your automation. Replace
`[SERVICE-ACCOUNT-NAME]` with a name for the `ServiceAccount`, and replace
`[NAMESPACE]` with that namespace:

```bash theme={"system"}
kubectl create serviceaccount [SERVICE-ACCOUNT-NAME] -n [NAMESPACE]
```

Generate a token. The `--duration` flag controls how long the token is valid.
Without it, the token expires at the cluster's default (typically one hour),
which is too short for most CI use cases:

```bash theme={"system"}
kubectl create token [SERVICE-ACCOUNT-NAME] \
  --duration=8760h \
  -n [NAMESPACE]
```

Build a `kubeconfig` that uses the token and the unmanaged endpoint:

```bash theme={"system"}
kubectl config set-cluster cks-sa \
  --server="https://api.[ORG-ID]-[CLUSTER-HASH].k8s.[ZONE].coreweave.com"

kubectl config set-credentials [SERVICE-ACCOUNT-NAME] \
  --token="[SERVICE-ACCOUNT-TOKEN]"

kubectl config set-context cks-sa \
  --cluster=cks-sa \
  --user=[SERVICE-ACCOUNT-NAME] \
  --namespace=[NAMESPACE]
```

Grant the `ServiceAccount` the permissions it needs using standard Kubernetes
RBAC. Replace `[ROLE-NAME]` with the name of an existing `ClusterRole`, such
as the built-in `view` or `edit` roles, or a custom role you've defined:

```bash theme={"system"}
kubectl create rolebinding [SERVICE-ACCOUNT-NAME]-binding \
  --clusterrole=[ROLE-NAME] \
  --serviceaccount=[NAMESPACE]:[SERVICE-ACCOUNT-NAME] \
  -n [NAMESPACE]
```

Store the resulting `kubeconfig` securely (for example, in a GitHub Actions secret
or a secrets manager) and use it in your CI/CD workflows.
