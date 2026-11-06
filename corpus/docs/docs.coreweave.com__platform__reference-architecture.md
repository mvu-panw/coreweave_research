# Terraform reference architecture

Source: https://docs.coreweave.com/platform/reference-architecture

# Terraform reference architecture

> Deploy CoreWeave infrastructure as code with Terraform using a modular, two-phase approach

This reference architecture helps platform engineers and infrastructure teams deploy a production-ready CoreWeave environment with Terraform. It uses a modular repository that provisions a VPC, CoreWeave Kubernetes Service (CKS) cluster, Node Pools, and Distributed File Storage (DFS) in two phases. Phase 1 creates the networking and cluster. Phase 2 adds Node Pools and DFS volumes after the cluster runs and you have kubeconfig. CoreWeave AI Object Storage is an optional add-on you can include at any point.

Use this page to understand what the architecture deploys, the prerequisites you must meet, and how the repository is organized before you begin Phase 1.

## What this deploys

The reference architecture uses a single Terraform root with separate modules for each resource. The two-phase apply exists because Node Pools and DFS volumes are Kubernetes manifests, which need a running cluster and kubeconfig before Terraform can create them.

### Phase 1: Networking and cluster

| Resource | Description |
| - | - |
| **VPC** | CoreWeave VPC with host prefixes and named CIDR prefixes for CKS (pod, service, internal LB). |
| **CKS cluster** | CKS cluster in the VPC. Supports OIDC configuration for external IdPs. |

### Phase 2: Node Pools and storage

| Resource | Description |
| - | - |
| **Node Pools** | One or more CKS Node Pools (Kubernetes manifest). Requires kubeconfig from Phase 1. |
| **DFS PVCs** | One or more Distributed File Storage PVCs (`shared-vast`, `ReadWriteMany`). Requires kubeconfig from Phase 1. |

### Optional: Object Storage add-on

Object Storage is independent of the two-phase apply, and you can add it at any point.

| Resource | Description |
| - | - |
| **Object Storage org access policy** | Organization-wide access policy for Object Storage. At least one must exist before creating buckets. |
| **Object Storage bucket** | Object Storage (S3-compatible) bucket. |
| **Object Storage bucket policy** | Per-bucket S3-compatible access policy for fine-grained control. |

> [card] Phase 1: Deploy core infrastructure
>
> Create a VPC and CKS cluster, then download kubeconfig.
>
> [Deploy core infrastructure](https://docs.coreweave.com/platform/reference-architecture/1-deploy-core-infrastructure.md)

> [card] Phase 2: Add Node Pools and storage
>
> Add Node Pools, DFS volumes, and optionally Object Storage.
>
> [Add Node Pools and storage](https://docs.coreweave.com/platform/reference-architecture/2-add-storage-and-workloads.md)

## Prerequisites

Before you begin, ensure you have the required tools and Identity and Access Management (IAM) roles described in the following sections.

### Tools

* [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.2.
* A [CoreWeave account](https://console.coreweave.com/) with a **CoreWeave API token** ([create one in Console](https://console.coreweave.com/tokens)).
* `kubectl` (required for Phase 2 and ongoing cluster interaction).

### IAM roles

Your CoreWeave user or API access token must have the appropriate [IAM roles](https://docs.coreweave.com/security/iam/access-policies/roles.md) and product-specific permissions for each phase. The following table lists the minimum required access.

| Phase | Required access |
| - | - |
| Phase 1 (VPC and CKS cluster) | **CKS Admin** to create, update, and delete clusters and VPC resources. |
| Phase 2 (Node Pool and DFS) | **CKS Admin** and a kubeconfig file for the cluster. |
| Object Storage add-on (optional) | **Object Storage Admin** or the required granular `cwobject:` permissions for [Object Storage control-plane actions](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md), plus the applicable `s3:` permissions in an [organization or bucket access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md) for bucket operations. |
| OIDC WIF setup (optional) | **IAM Admin** to configure identity integrations, including Workload Identity Federation. |

> [!NOTE]
>
> If you're using [legacy group role assignments](https://docs.coreweave.com/security/iam/access-policies/roles.md#legacy-group-role-assignments), users in the `admin` or `write` groups already have the CKS Admin and Object Storage Admin roles. The Object Storage Admin role doesn't include the `s3:` permissions required for bucket operations.

## Repository structure

Review the repository layout before you start to locate the files you edit during each phase. The reference architecture repository organizes all resources as **modules**. The root `main.tf` wires them together.

```text theme={"system"}
.
├── README.md
├── .gitignore
├── .terraform.lock.hcl       # Committed for reproducible provider versions
├── terraform.tfvars.example  # Copy to terraform.tfvars and fill in your values
├── providers.tf              # CoreWeave + Kubernetes providers, token variable
├── main.tf                   # Calls all modules (network, cks, object_storage, nodepool, dfs)
├── variables.tf              # Root variables (passed into modules)
├── outputs.tf                # Outputs from each module
└── modules/
    ├── network/              # VPC (coreweave_networking_vpc)
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    ├── cks/                  # CKS cluster (coreweave_cks_cluster)
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    ├── object_storage/       # Optional AI Object Storage bucket + policies
    │   ├── main.tf           # Bucket, org access policy, bucket policy
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    ├── nodepool/             # CKS NodePool (kubernetes_manifest, Phase 2)
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    └── dfs/                  # DFS PVC (shared-vast, kubernetes_manifest, Phase 2)
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── versions.tf
```

* Don't commit `terraform.tfvars`. Create it from `terraform.tfvars.example`.
* Don't commit state files (`*.tfstate`). Use a [remote backend](https://developer.hashicorp.com/terraform/language/backend) for production environments.

## Outputs

After apply, Terraform outputs include:

| Output | Source | Description |
| - | - | - |
| `vpc_id` | `module.network` | Created VPC ID. |
| `cks_cluster_id` | `module.cks` | CKS cluster ID. |
| `cks_cluster_name` | `module.cks` | CKS cluster name. |
| `cks_api_server_endpoint` | `module.cks` | Kubernetes API server endpoint. |
| `cks_status` | `module.cks` | Current cluster status. |
| `cks_service_account_oidc_issuer_url` | `module.cks` | OIDC issuer URL for CKS service account tokens (use for WIF). |
| `nodepools` | `module.nodepool` | Map of created Node Pool names. |
| `dfs_pvcs` | `module.dfs` | Map of created DFS PVCs. |

If you include the Object Storage add-on, the following outputs are also available.

| Output | Source | Description |
| - | - | - |
| `object_storage_bucket_name` | `module.object_storage` | Bucket name, if created. |
| `object_storage_org_access_policy_names` | `module.object_storage` | Map of created org access policy names. |
| `object_storage_bucket_policy_json` | `module.object_storage` | Bucket policy JSON, if applied. |

## Related resources

* [CoreWeave Cloud Console](https://console.coreweave.com/)
* [CoreWeave Terraform Provider](https://docs.coreweave.com/platform/terraform.md)
* [CoreWeave Terraform Provider on the Terraform Registry](https://registry.terraform.io/providers/coreweave/coreweave/latest/docs)
* [CKS cluster documentation](https://docs.coreweave.com/products/cks/clusters/introduction.md)
* [VPC CIDR sizing](https://docs.coreweave.com/products/networking/vpc/vpc-cidr.md)
* [Object Storage access policies](https://docs.coreweave.com/platform/terraform/resources/object_storage_organization_access_policy.md)
* [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md)
* [DFS - Create volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md)
