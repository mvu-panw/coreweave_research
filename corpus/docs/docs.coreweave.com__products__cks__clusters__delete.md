# Delete a CKS cluster

Source: https://docs.coreweave.com/products/cks/clusters/delete

# Delete a CKS cluster

> Learn how to delete a CKS cluster using the Cloud Console, including state requirements and precautions

This guide explains how to delete a CoreWeave Kubernetes Service (CKS) cluster using the Cloud Console. Delete a cluster when you no longer need its compute resources, so you can stop incurring costs and free up project quota.

## Prerequisites

This guide assumes you have an active CoreWeave account.

## Delete a cluster with the Cloud Console

The cluster dashboard displays the cluster status. You can delete a cluster in the **Running**, **Failed**, or **Preempted** state. These labels correspond to `STATUS_RUNNING`, `STATUS_FAILED`, and `STATUS_PREEMPTED` in the CKS API. To delete a cluster, follow these steps:

1. Navigate to the [Clusters](https://console.coreweave.com/clusters) page.
2. Confirm the cluster is in the **Running**, **Failed**, or **Preempted** state.
3. Click the ellipsis on the far right of the screen next to the cluster, then select **Delete**.
4. To confirm deletion, enter the name of the cluster.
