# Create a CoreWeave API access token

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens

# Create a CoreWeave API access token

> Get API access tokens for the CoreWeave Cloud Console

CoreWeave uses API access tokens to authenticate users and grant access to resources on the CoreWeave Cloud Console. This guide explains how to create and manage access tokens on the Cloud Console for Object Storage.

## Prerequisites

This guide assumes that you have an active CoreWeave account.

## Create a new API access token

API access tokens authenticate programmatic access to CoreWeave services. Create them in the CoreWeave Cloud Console.
To create a new access token, complete the following steps:

1. In Cloud Console, navigate to [Tokens](https://console.coreweave.com/tokens), and then click the **Create Token** button in the upper-right corner.

2. In the **Create API Token** dialog, complete the following fields to configure the token values, and then click **Create**:

   | **Field** | **Description** |
   | - | - |
   | **Name** | The name of the token. |
   | **Expiration** | How long the token remains valid. |
   | **Note** | A description for future reference. |

3. Select one of the following options:

   | **Option** | **Description** |
   | - | - |
   | **Token Secret** | Copy and store the token secret for use cases such as scraping metrics, scraping logs, self-hosted Grafana setup, or to add the token secret to an existing `kubeconfig`. |
   | **Kubeconfig** | Create and download a `kubeconfig` for a specific cluster, so you can interact with the cluster using commands like `kubectl`. A `kubeconfig` can access multiple clusters when you [switch contexts](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/). |

   > [!WARNING]
   >
   > Sensitive values such as token secrets and `kubeconfig` files are displayed in the Cloud Console modal **only once**, and they are never shown again after you close the modal. You must record them in a secure location.

   After you complete these steps, your new API access token is ready to use with CoreWeave services.

## Get a kubeconfig for a CKS cluster

To get a kubeconfig for an existing CKS cluster, complete the following steps:

1. In the Cloud Console, go to the [Clusters](https://console.coreweave.com/clusters) page.
2. Find the cluster, click the vertical ellipsis next to its name, and then click **Get kubeconfig**.
3. Save the kubeconfig file to your local machine.

After creating the token, the modal presents two options: **Token Secret** and **Kubeconfig**. For AI Object Storage API access, copy and store the **Token Secret**, which is the bearer token you pass in `Authorization: Bearer` headers when calling `api.coreweave.com`. The Token Secret is different from the S3-compatible Access Key and secret key used for bucket operations.

> [!NOTE]
>
> If you're connected to a Kubernetes cluster and need to retrieve an existing token secret, it's embedded in your `kubeconfig`. To read it, run the following command:
>
> ```bash theme={"system"}
> kubectl config view --raw -o jsonpath='{.users[0].user.token}'
> ```
