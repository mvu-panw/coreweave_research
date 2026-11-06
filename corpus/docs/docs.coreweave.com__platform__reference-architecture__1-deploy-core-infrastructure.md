# 1. Deploy core infrastructure

Source: https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure

# 1. Deploy core infrastructure

> Create a CoreWeave VPC and CKS cluster with Terraform (Phase 1)

Phase 1 provisions the foundational infrastructure for the CoreWeave reference architecture: a VPC and a CKS Kubernetes cluster. This phase is for platform engineers and infrastructure operators who are bootstrapping a new CoreWeave environment and want to follow the reference architecture end to end.

After this phase completes, you have a running cluster and can download its kubeconfig to proceed to [Phase 2](https://docs.coreweave.com/platform/reference-architecture/2-add-storage-and-workloads.md), which adds node pools and DFS storage.

> [!NOTE]
>
> Ensure you meet the [prerequisites](https://docs.coreweave.com/platform/reference-architecture.md) before starting, including the **CKS Admin** Identity and Access Management (IAM) role.

## Clone the repository

The reference architecture is distributed as a Terraform configuration in a public GitHub repository. Clone the [CoreWeave reference architecture repository](https://github.com/coreweave/reference-architecture), navigate to the `terraform/` folder, and copy the example Terraform variables file:

```bash theme={"system"}
git clone https://github.com/coreweave/reference-architecture.git
cd ./reference-architecture/terraform/
cp terraform.tfvars.example terraform.tfvars
```

The `terraform.tfvars.example` file contains example values you can use as a starting point. You'll edit `terraform.tfvars` to set your values in the next section.

## Configuration

In this section, you set your API token and configure your Terraform variables.

### Set your API token

Set the CoreWeave API token as an environment variable. Replace `[API-ACCESS-TOKEN]` with an [API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) for your organization:

```bash theme={"system"}
export TF_VAR_coreweave_api_token="[API-ACCESS-TOKEN]"
```

Setting the API token as an environment variable is the recommended approach because it keeps the token out of files that might be committed to version control.

### Configure variables

Edit `terraform.tfvars` and set the following values:

| Variable | Description |
| - | - |
| `zone` | Deployment zone, for example `US-EAST-02A`. |
| `vpc_name` | A name for your VPC. |
| `vpc_prefixes` | CIDR blocks for pod, service, and internal LB networks. See [VPC CIDR sizing](https://docs.coreweave.com/products/networking/vpc/vpc-cidr.md) for guidance. The example values in `terraform.tfvars.example` are valid defaults. |
| `cluster_name` | A name for your CKS cluster (maximum 30 characters). |

Leave `create_nodepool` and `create_dfs_pvc` as `false` for Phase 1. You enable these variables in Phase 2 when you add node pools and storage.

> [!WARNING]
>
> If you choose to add your CoreWeave API token to the `terraform.tfvars` file, **do not commit** `terraform.tfvars` to the repository. Add it to `.gitignore` or use environment variables exclusively for security.

## Create and verify your VPC and CKS cluster

In this section, you apply your Terraform configuration to create your VPC and CKS cluster, verify the outputs, and download the resulting kubeconfig.

### Apply your Terraform configuration

Initialize your Terraform configuration, preview the planned changes, and apply them to create your VPC and CKS cluster:

```bash theme={"system"}
terraform init
terraform plan
terraform apply
```

Cluster creation takes approximately 45 minutes. Terraform displays progress as it provisions the VPC and cluster.

### Verify outputs

After `terraform apply` completes, verify the core outputs to confirm Terraform created your VPC and CKS cluster successfully:

```bash theme={"system"}
terraform output vpc_id
terraform output cks_cluster_id
terraform output cks_api_server_endpoint
terraform output cks_status
```

The `cks_status` output shows the cluster as `running`.

### Download kubeconfig

Download the kubeconfig for your new cluster from the [CoreWeave Console](https://console.coreweave.com/). The kubeconfig authenticates `kubectl` to your cluster, and you also need it for Phase 2, which covers node pools and DFS.

1. Log in to the [CoreWeave Console](https://console.coreweave.com/clusters).
2. On the [Clusters](https://console.coreweave.com/clusters) page, find your new cluster and click the vertical ellipsis (**More options**) next to the cluster name.
3. Click **Get kubeconfig**.
4. Save the kubeconfig file to your local machine.

After downloading, set the `KUBECONFIG` environment variable to the path to the downloaded kubeconfig and verify connectivity. Replace `[PATH-TO-DOWNLOADED-KUBECONFIG]` with that path:

```bash theme={"system"}
export KUBECONFIG=[PATH-TO-DOWNLOADED-KUBECONFIG]
kubectl cluster-info
```

## Next steps

You now have a running CKS cluster in a CoreWeave VPC, with `kubectl` configured to access it. Continue to Phase 2, [Add node pools and storage](https://docs.coreweave.com/platform/reference-architecture/2-add-storage-and-workloads.md), to add node pools and DFS storage.
