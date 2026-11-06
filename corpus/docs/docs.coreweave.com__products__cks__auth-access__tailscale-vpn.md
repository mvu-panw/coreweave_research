# Access a CKS cluster through Tailscale VPN

Source: https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn

# Access a CKS cluster through Tailscale VPN

> Enable private access to the Kubernetes API server over a Tailscale VPN using a CoreWeave-managed proxy

CKS supports private API server access through a CoreWeave-managed Tailscale proxy. When you enable this feature, CKS creates a proxy that joins your [tailnet](https://tailscale.com/docs/concepts/tailnet) and forwards requests to your cluster's Kubernetes API server. This lets you access private clusters without exposing the API server to the public internet.

## Authentication modes

Before you begin, choose the authentication mode that matches how your team manages Kubernetes access. The proxy supports three authentication modes:

| Mode | Description |
| - | - |
| **Tailscale Managed Auth** | The proxy uses your Tailscale client identity to authenticate requests. User identity and groups come from Tailscale tags. You manage authorization using Kubernetes RBAC. |
| **CoreWeave Managed Auth** | The proxy routes requests through the CoreWeave API gateway. Authentication uses the Cloud Console API access token embedded in the kubeconfig. |
| **Direct Auth** | The proxy forwards raw packets directly to the API server. Use this mode with kubeconfigs that contain embedded client certificate credentials (`client-certificate-data` and `client-key-data`). |

## Prerequisites

Before you begin, make sure you have the following:

* A Tailscale account. Accounts are free at [login.tailscale.com](https://login.tailscale.com/).
* The Tailscale app installed on your workstation. You can use the [Tailscale desktop app](https://tailscale.com/download) (recommended) or the `tailscale` and `tailscaled` CLI binaries.
* A CKS cluster. See [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md).
* The CKS Admin role, assigned through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies.md). This role is required to update cluster configuration using the CKS API.
* A CoreWeave API access token. See [Manage API access tokens and kubeconfig files](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

## Configure Tailscale

The following steps configure your tailnet to allow the CoreWeave proxy to join. Enabling HTTPS certificates and setting up access controls are one-time tailnet tasks. Creating a trust credential is required once for each CKS cluster.

### Enable HTTPS certificates

The CoreWeave proxy uses a Tailscale HTTPS certificate to secure communication over your tailnet. You must enable HTTPS certificates on your tailnet before the proxy can obtain one.

1. Navigate to the [Tailscale DNS settings](https://login.tailscale.com/admin/dns).
2. Scroll to the **HTTPS Certificates** section and click **Enable HTTPS**.

### Configure access controls

The CoreWeave proxy needs permission to join your tailnet and register a Tailscale service without requiring manual approval each time.

1. Navigate to the [Tailscale access controls editor](https://login.tailscale.com/admin/acls/file).
2. Add the following entries to your tailnet policy JSON:

```json theme={"system"}
{
  "autoApprovers": {
    "services": {
      "tag:coreweave": [
        "tag:coreweave"
      ]
    }
  },
  "tagOwners": {
    "tag:coreweave": []
  }
}
```

The `tagOwners` entry with an empty array prevents individual users from manually assigning the `tag:coreweave` tag. Only machines provisioned through workload identity federation can claim this tag. The `autoApprovers` entry lets the proxy register a [Tailscale service](https://tailscale.com/docs/features/tailscale-services) automatically.

### Create a trust credential

The proxy authenticates to your tailnet using [workload identity federation](https://tailscale.com/docs/features/workload-identity-federation). Your CKS cluster acts as an OIDC (OpenID Connect) issuer, and the proxy exchanges a short-lived OIDC token for a Tailscale API token. CoreWeave doesn't store or distribute long-lived credentials.

You need one trust credential per CKS cluster. The issuer URL includes the cluster ID (`https://oidc.cks.coreweave.com/id/[CLUSTER-ID]`), which means the trust credential is unique to each cluster. This is intentional: the kube-apiserver is configured with `--service-account-issuer=https://oidc.cks.coreweave.com/id/[CLUSTER-ID]`, so tokens are not trusted across clusters even within the same organization. This design preserves the security boundary on both the CoreWeave and Tailscale sides.

The practical consequence is a one-time ordering constraint: you must create the trust credential in Tailscale before you can enable Tailscale VPN on the cluster, because the credential requires the cluster ID that only exists after you create the cluster. After the credential exists, you can enable Tailscale on the cluster.

The issuer URL for each cluster has the following format, where `[CLUSTER-ID]` is your cluster's ID:

```text theme={"system"}
https://oidc.cks.coreweave.com/id/[CLUSTER-ID]
```

To find your cluster ID, open the cluster detail dialog in the [Cloud Console](https://console.coreweave.com/clusters). The console also provides a button to copy the full **OIDC issuer url** directly.

To create a trust credential:

1. Navigate to [Tailscale trust credentials settings](https://login.tailscale.com/admin/settings/trust-credentials).

2. Click **+ Credential** and select **Open ID Connect**.

3. Complete the form with the following values:

   | Field | Value |
   | - | - |
   | Description | A name for this credential, for example, the cluster name |
   | Issuer | Custom Issuer |
   | Issuer URL | `https://oidc.cks.coreweave.com/id/[CLUSTER-ID]` |
   | Subject | `system:serviceaccount:cw-tailscale:tailscale` |
   | Audience | Unset; defaults to `api.tailscale.com/[CLIENT-ID]` |

   The Subject value is always `system:serviceaccount:cw-tailscale:tailscale` for all CKS clusters.

4. Click **Continue**.

5. On the scopes page, grant the following two scopes. For each scope, add `tag:coreweave` as the associated tag:
   * Write Access for **General > Services**
   * Write Access for **Keys > Auth Keys**

6. For both of these settings, from the **Add tags** menu, choose `tag:coreweave`.

7. Click **Generate credential**.

After saving, note the **Client ID** that Tailscale displays. Use this value when you enable Tailscale on your cluster.

#### Optional: Terraform alternative

You can provision the trust credential using the [Tailscale Terraform provider](https://registry.terraform.io/providers/tailscale/tailscale/latest) with the [tailscale\_federated\_identity](https://registry.terraform.io/providers/tailscale/tailscale/latest/docs/resources/federated_identity) resource. Replace `[CLUSTER-ID]` with your cluster's ID.

```hcl theme={"system"}
resource "tailscale_federated_identity" "cks_cluster" {
  description = "[DESCRIPTION]"
  issuer      = "https://oidc.cks.coreweave.com/id/[CLUSTER-ID]"
  subject     = "system:serviceaccount:cw-tailscale:tailscale"
  scopes = [
    "auth_keys",
    "services"
  ]
  tags = ["tag:coreweave"]
}
```

## Enable Tailscale VPN for a cluster

With your tailnet configured and a trust credential in place, enable the Tailscale proxy on your CKS cluster using the CKS API to set the Tailscale client ID.

### Get your cluster ID and API key

To find your CKS cluster ID, open the [CoreWeave Cloud Console](https://console.coreweave.com/clusters).

1. Go to **Compute > Clusters** in the Cloud Console.
2. Find your cluster, then open its details page.
3. Open the **JSON** view.
4. Copy the `id` value.

To create a new API key for your cluster, see [Create a new API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md#create-a-new-api-access-token).

### Enable Tailscale

Set the following environment variables, replacing the placeholders with your values:

```bash theme={"system"}
export CLUSTER_ID="[CLUSTER-ID]"
export API_ACCESS_TOKEN="[API-ACCESS-TOKEN]"
```

Send the PATCH request, replacing `[CLIENT-ID]` with the client ID from the trust credential you created in the preceding section.

```bash theme={"system"}
curl -X PATCH "https://api.coreweave.com/v1beta1/cks/clusters/$CLUSTER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_ACCESS_TOKEN" \
  -d '{
    "updateMask": "tailscale.clientId",
    "tailscale": {
      "clientId": "[CLIENT-ID]"
    }
  }'
```

You should see output similar to the following:

```text theme={"system"}
{
  "cluster": {
    "id": "00000000-0000-0000-0000-000000000000",
    "name": "example-cluster",

    . . .

    "status": "STATUS_UPDATING",
    "apiServerEndpoint": "abc123-def45678.k8s.us-east-04a.coreweave.com",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:05:00Z",
    "isUpgradeable": true
  }
}
```

After CKS receives the client ID, CKS creates a Tailscale proxy for your cluster. The proxy joins your tailnet and appears in the Tailscale admin console under **Services**.

To verify the client ID is set, retrieve your cluster:

```bash theme={"system"}
curl -H "Authorization: Bearer $API_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     "https://api.coreweave.com/v1beta1/cks/clusters/$CLUSTER_ID"
```

A cluster with Tailscale VPN enabled includes a `tailscale` field in the response. After provisioning completes, the response also includes a `tailnetDomain` field, where `[TAILNET-DOMAIN]` is your tailnet's name:

```json theme={"system"}
{
  "cluster": {
    "tailscale": {
      "clientId": "[CLIENT-ID]",
      "tailnetDomain": "[TAILNET-DOMAIN].ts.net"
    }
  }
}
```

> [!NOTE]
>
> Because of how the system propagates values, `tailnetDomain` can take up to 10 minutes to appear in the API response after provisioning completes.

You can also confirm provisioning status using the Tailscale admin console:

* **Trust credential status**: Go to `https://login.tailscale.com/admin/settings/trust-credentials?q=[CLIENT-ID]`. The credential detail page shows an authentication error if the proxy cannot authenticate to your tailnet, for example, because of a mistyped issuer URL or missing scopes.
* **Service status**: Go to `https://login.tailscale.com/admin/services/svc:[SERVICE-NAME]`. The service detail page shows the service definition and its proxy hosts after they're provisioned.

Together with `tailscale status` on your local machine, these pages give you a complete view of provisioning progress.

### Disable Tailscale

To disable the Tailscale proxy on a cluster, set the client ID to `null`:

```bash theme={"system"}
curl -X PATCH "https://api.coreweave.com/v1beta1/cks/clusters/$CLUSTER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_ACCESS_TOKEN" \
  -d '{
    "updateMask": "tailscale.clientId",
    "tailscale": {
      "clientId": null
    }
  }'
```

CKS tears down the proxy for the cluster and removes the service from your tailnet.

## Connect with the Tailscale client

With the proxy running on your cluster, connect your local machine to the tailnet so it can reach the proxy.

**If you use the Tailscale desktop app**, open the app and log in through the GUI. The app handles authentication and route acceptance automatically. Skip to the verification step that follows.

**If you use the `tailscaled` CLI**, start the daemon:

```bash theme={"system"}
sudo tailscaled
```

If you haven't previously connected to your tailnet, authenticate:

```bash theme={"system"}
tailscale login
```

Follow the URL in the output to complete authentication in your browser.

Enable route acceptance so your machine can reach the proxy:

```bash theme={"system"}
tailscale set --accept-routes=true
```

Verify the proxy is visible in your tailnet:

```bash theme={"system"}
tailscale status
```

The output includes the proxy nodes for your cluster:

```text theme={"system"}
100.104.110.46  [SERVICE-NAME]-proxy-0  tagged-devices  linux  -
100.103.104.80  [SERVICE-NAME]-proxy-1  tagged-devices  linux  -
```

For example: `cw123a-us-east-04a-my-cluster-proxy-0`.

The Tailscale service name for your cluster follows the pattern `[ORG-ID]-[ZONE]-[CLUSTER-NAME]`, where the zone is lowercase with hyphens (for example, `US-EAST-04A` becomes `us-east-04a`). Your organization ID prefix is visible in the Cloud Console.

### Configure DNS

The proxy is reachable by its Tailscale fully qualified domain name (FQDN), so your machine must be able to resolve Tailscale hostnames. The Tailscale DNS server address is `100.100.100.100`. You can confirm this address on the [Tailscale DNS settings page](https://login.tailscale.com/admin/dns).

On **macOS**, the Tailscale app configures DNS automatically when connected. No manual steps are required.

On **Linux**, add the DNS server to your resolvers manually. The exact method depends on your distribution's DNS manager. For example, on systems that use `systemd-resolved`:

```bash theme={"system"}
resolvectl dns tailscale0 100.100.100.100
```

To verify the DNS server is reachable:

```bash theme={"system"}
ping -c 1 100.100.100.100
```

> [!NOTE]
>
> On Linux, remove the Tailscale DNS entry from your resolvers when you finish your session.

Your machine is now connected to the tailnet and can reach the CKS proxy. The following section covers how to authenticate to the Kubernetes API server with your chosen authentication mode.

## Access the cluster

With your machine on the tailnet, configure `kubectl` to reach the API server through the proxy. How you connect to the cluster depends on the authentication mode you use. Follow the section that matches the mode you chose in [Authentication modes](#authentication-modes).

### Tailscale Managed Auth

With Tailscale Managed Auth, the proxy authenticates requests with your Tailscale client identity. Your Kubernetes username comes from your workstation's hostname. Your Kubernetes groups come from the Tailscale tags assigned to your device in the Tailscale admin console.

Before you begin, find your service name. You can get it in two ways:

* Run `tailscale status` and strip the `-proxy-0` suffix from either proxy node name. For example, `cw123a-us-east-04a-my-cluster-proxy-0` gives a service name of `cw123a-us-east-04a-my-cluster`.
* Go to the [Tailscale admin console Services page](https://login.tailscale.com/admin/services) and find the entry for your cluster.

To generate a kubeconfig, pass the service name for your cluster to `tailscale configure kubeconfig`:

```bash theme={"system"}
tailscale configure kubeconfig [SERVICE-NAME]
```

The command prints the FQDN of the service it configured, for example, where `[TAILNET-DOMAIN]` is your tailnet's name:

```text theme={"system"}
kubeconfig configured for "[SERVICE-NAME].[TAILNET-DOMAIN].ts.net" at URL "https://[SERVICE-NAME].[TAILNET-DOMAIN].ts.net"
```

Verify access:

```bash theme={"system"}
kubectl auth whoami
```

You should see output similar to the following:

```text theme={"system"}
ATTRIBUTE   VALUE
Username    [USERNAME]
Groups      [system:authenticated]
```

The username is your workstation's hostname in uppercase. The `Groups` field lists the Tailscale tags assigned to your device in the Tailscale admin console. If your device has no tags, only `system:authenticated` appears.

#### Configure RBAC

Tailscale Managed Auth maps Tailscale tags to Kubernetes groups so you can use standard Kubernetes RBAC to control what cluster access each tag grants. The proxy treats any device with a given Tailscale tag as a member of the corresponding Kubernetes group when it connects through the proxy.

For example, to grant read-only access to any device tagged `tag:view`:

```bash theme={"system"}
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tailscale-view
subjects:
  - kind: Group
    name: "tag:view"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
EOF
```

Verify that the binding exists:

```bash theme={"system"}
kubectl get clusterrolebinding tailscale-view
```

You should see output similar to the following:

```text theme={"system"}
NAME             ROLE               AGE
tailscale-view   ClusterRole/view   23s
```

#### Configure grants

Tailscale Managed Auth supports [grants](https://tailscale.com/docs/kubernetes-operator/api-server-access#impersonating-kubernetes-groups-with-grants), which let you impersonate Kubernetes groups based on Tailscale ACL (access control list) rules. Add a grant to your tailnet policy JSON so devices with `tag:admin` can impersonate the `system:masters` Kubernetes group:

```json theme={"system"}
{
  "src": ["tag:admin"],
  "dst": ["tag:coreweave"],
  "app": {
    "tailscale.com/cap/kubernetes": [{
      "impersonate": {
        "groups": ["system:masters"]
      }
    }]
  }
}
```

### CoreWeave Managed Auth

With CoreWeave Managed Auth, the proxy routes requests through the CoreWeave API gateway. Authentication uses the API access token embedded in the kubeconfig you download from the Cloud Console.

Download a kubeconfig from the Cloud Console for your cluster, then update the server address to the Tailscale FQDN on port `9443`. Use the FQDN from the `tailscale configure kubeconfig` output, or find it in the Tailscale admin console under **Services**.

To find the cluster name in your kubeconfig:

```bash theme={"system"}
kubectl config get-clusters
```

Then update the server address:

```bash theme={"system"}
kubectl config set-cluster [CLUSTER-NAME] \
  --server https://[SERVICE-NAME].[TAILNET-DOMAIN].ts.net:9443
```

Verify access:

```bash theme={"system"}
kubectl auth whoami
```

You should see output similar to the following:

```text theme={"system"}
ATTRIBUTE   VALUE
Username    cwtoken-[TOKEN-ID]-[USERNAME]
Groups      [admin read write system:authenticated]
```

The username corresponds to the Cloud Console token used to generate the kubeconfig: `[TOKEN-ID]` is the token's ID, and `[USERNAME]` is the token's name.

### Direct Auth

Direct Auth forwards raw packets directly to the Kubernetes API server. Use this mode with kubeconfigs that contain embedded `client-certificate-data` and `client-key-data` fields.

Set the server address to the short Tailscale service name on port `6443` (without the `.ts.net` suffix):

```bash theme={"system"}
kubectl config set-cluster [CLUSTER-NAME] \
  --server https://[SERVICE-NAME]:6443
```

Verify access:

```bash theme={"system"}
kubectl auth whoami
```
