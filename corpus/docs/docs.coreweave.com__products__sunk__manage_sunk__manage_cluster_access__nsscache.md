# Manage users with nsscache on SUNK Standard

Source: https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache

# Manage users with nsscache on SUNK Standard

> Enable automatic user provisioning with nsscache on a SUNK Standard cluster

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

SUNK User Provisioning (SUP) uses [nsscache](https://github.com/google/nsscache), a lightweight directory service, to manage users across CoreWeave clusters. It supports two directory protocols: SCIM (System for Cross-domain Identity Management (SCIM) is an open standard protocol that automates user account provisioning and management across different systems.) and LDAP (Lightweight Directory Access Protocol (LDAP) is a protocol for accessing and managing distributed directory information services.). We recommend SCIM, because it enables automated user and group synchronization from your upstream identity provider (IdP) (An Identity Provider (IdP) is an entity that stores and verifies the identity of a user.) to SUNK. When you add or remove a user in your IdP, the change appears in your SUNK cluster within minutes, keeping access accurate and up to date.

Whether your users are managed in a third-party IdP or directly in CoreWeave IAM, SUP provisions, updates, and removes POSIX users in your cluster without manual intervention.

This guide demonstrates how to configure `nsscache` to support SUP with the following steps:

1. [Set up SUNK User Provisioning (SUP)](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md).
2. [Create user groups with CoreWeave IAM or your upstream IdP](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#create-sunk-user-groups).
3. [Create a Kubernetes Secret and add it to the `slurm` chart](#configure-a-kubernetes-secret-for-sup).

## Prerequisites

Before making any changes to the `nsscache` configuration, you must first do the following:

* [Set up SUP](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md). SUP is required to provision cluster access to users, whether you use a federated IdP or not.
* [Create user groups with CoreWeave IAM or your upstream IdP](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#create-sunk-user-groups). SUP provisions access to groups of users, rather than individual users. You must create these groups before you configure `nsscache`, and the group names must exactly match the group names specified in the `nsscache` configuration.

## Configure a Kubernetes Secret for SUP

With prerequisites in place, give `nsscache` the credentials it needs to authenticate with your directory service. Create a Kubernetes Secret that contains the configuration for your directory service, then add the Secret to the `slurm` chart's `values.yaml` file, as detailed in the following sections.

### Create a Kubernetes Secret

Create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that contains the configuration for your directory service.

> [!WARNING]
>
> CoreWeave discourages including sensitive information, such as plaintext user credentials, directly in your `values.yaml` configuration. Instead, use a Kubernetes Secret for added security and manageability. CoreWeave provides [encryption at rest](https://docs.coreweave.com/products/cks/clusters/secrets.md) for `etcd` data, which includes Secrets.

This Secret can be a SCIM token or an LDAP service account password. Be sure to follow the appropriate naming conventions detailed in the following sections when creating your Secret.

#### Naming conventions for SCIM Secrets

For a SCIM Secret, the suggested Secret name is `[RELEASE-NAME]-nsscache-scim-secret`.

Inside the Secret, the `key` under `data` must be named `nsscache-scim-auth-token`, as shown in the following example. This contains the base64-encoded SCIM token.

```yaml theme={"system"}
apiVersion: v1
kind: Secret
metadata:
  name: "[RELEASE-NAME]-nsscache-scim-secret"
data:
  nsscache-scim-auth-token: [BASE64-ENCODED-SCIM-TOKEN]
```

#### Naming conventions for LDAP Secrets

For an LDAP Secret, the suggested Secret name is `[RELEASE-NAME]-nsscache-ldap-secret`.

Inside the Secret, the `key` under `data` must be named `nsscache-ldap-password`. This contains the base64-encoded password for the LDAP service.

### Update the `slurm` chart with your Kubernetes Secret

After you create the Secret, update the `slurm` chart's `values.yaml` file so that `nsscache` references it.

Edit the `nsscache.existingSecret` parameter with the name of your Secret, as shown in [Provision cluster access to groups of users](#provision-cluster-access-to-groups-of-users). With the Secret in place and referenced from the chart, `nsscache` can authenticate against your directory service.

## Provision cluster access to groups of users

Once `nsscache` can authenticate to your directory service, configure it to provision specific users and groups into the cluster. [SUP](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md) provisions cluster access to **groups of users**, rather than individual users. You must [create the groups in CoreWeave IAM or your upstream IdP](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#create-sunk-user-groups) before you configure `nsscache`. The names of your created user groups must match the group names specified in the `nsscache` configuration exactly.

```yaml title="Example SCIM values" highlight={4} theme={"system"}
sssdContainer:
  enabled: false
# You may remove the `directoryService` key when using nsscache
directoryService:
nsscache:
  enabled: true
  existingSecret: "[RELEASE-NAME]-nsscache-scim-secret"
  sudoGroups:
    - sudo-users
  nsscacheConfig:
    default:
      source: scim
      scim_base_url: https://api.coreweave.com/scim/<org>
      scim_users_parameters: filter=active eq "true"&groups=slurm-users,sudo-users
      scim_groups_parameters: excludeInactiveUsers=true&includeVirtualUserGroups=slurm-users,sudo-users
```

The `values.yaml` file sets the suggested `nsscache` configuration for SCIM by default. For a full list of configuration options, see the [SCIM parameter reference](https://docs.coreweave.com/products/sunk/reference/nsscache_reference.md).

The following parameters configure the groups to provision:

* `sudoGroups` specifies the user groups that can run `sudo` commands on the nodes.
* `scim_users_endpoint` specifies the SCIM endpoint path for retrieving user data. The default value is `Users`.
* `scim_groups_endpoint` specifies the SCIM endpoint path for retrieving group data. The default value is `Groups`.
* `scim_users_parameters` specifies which **users** in these groups to provision, so they find their User ID in the cluster. By default, this filters out inactive users with `filter=active eq "true"`.
* `scim_groups_parameters` specifies the groups to provision. By default, this filters out inactive users with `excludeInactiveUsers=true`. If you specify no user groups, `nsscache` provisions all groups.

The groups you list in `scim_users_parameters` also determine which Slurm users SUP creates and deletes. If you drop a group from this parameter, the next sync run deletes the Slurm users whose cluster access came from that group. For more information, see [Slurm user and account lifecycle](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#slurm-user-and-account-lifecycle).

> [!NOTE]
>
> On SUNK 8.0 and later, set the group list in `nsscache.groups`. The operator writes it into the `groups=` parameter of `scim_users_parameters`, which is the value the sync process reads, and it overrides any `groups=` value you set yourself under `nsscache.nsscacheConfig`. On SUNK 7.x and earlier, set `groups=` in `scim_users_parameters` directly. SUP creates and deletes Slurm users the same way in both versions.

### Filter specific user groups

`scim_groups_parameters` and `scim_users_parameters` let you add optional parameters to the `groups` and `users` endpoints, respectively. `nsscache` automatically URL-encodes special characters such as spaces and quotes.

To provision access to specific user groups, list the group names in **both** the `scim_users_parameters` and `scim_groups_parameters` parameters, as follows:

```yaml theme={"system"}
scim_users_parameters: filter=active eq "true"&groups=slurm-users,sudo-users
scim_groups_parameters: excludeInactiveUsers=true&includeVirtualUserGroups=slurm-users,sudo-users
```

The previous example does the following:

* Filter out inactive users
* Provision access to the **users** in the `slurm-users` and `sudo-users` groups.
* Provision the virtual user groups `slurm-users` and `sudo-users`.

Specify the group names exactly as they appear in your IdP, and list them in both the `scim_users_parameters` and `scim_groups_parameters` parameters so that `nsscache` provisions the users and groups correctly.

#### Example: Authentik LDAP values

```yaml title="Example Authentik LDAP values" highlight={4} theme={"system"}
sssdContainer:
  enabled: false
# Remove the `directoryService` key
directoryService:
nsscache:
  enabled: true
  existingSecret: nsscache-ldap-secret
  nsscacheConfig:
    default:
      source: ldap
      ldap_uri: ldap://authentik-outpost-ldap-outpost
      ldap_base: dc=coreweave,dc=cloud
      ldap_bind_dn: cn=ldapsvc,dc=coreweave,dc=cloud
      ldap_bind_password:
      ldap_rfc2307bis: "1"
      ldap_default_shell: /bin/bash
      ldap_scope: sub
      ldap_uidattr: cn
    passwd:
      ldap_filter: (objectClass=user)
      ldap_override_home_dir: /mnt/home/%%u
    group:
      ldap_filter: (objectClass=group)
    shadow:
      ldap_filter: (objectClass=user)
    sshkey:
      ldap_filter: (objectClass=user)
```

## Verify and troubleshoot `nsscache`

After you configure `nsscache`, use the following checks to confirm that user and group data is syncing from your directory service into the cluster.

You don't need to sync data manually with `nsscache`. It takes about two minutes for data to sync from an identity provider to SUNK through `nsscache`. If user data isn't available, wait a few minutes and check again.

To validate that `nsscache` is working, follow these steps:

1. Log in to the [Login Pod](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md#connect-through-ssh) for your cluster, replacing `[LOGIN-POD]` with its Pod name.

   ```bash theme={"system"}
   kubectl exec -it [LOGIN-POD] -c sshd -- /bin/bash
   ```

2. Access the `/etc/nsscache` directory and list the files within:

   ```bash theme={"system"}
   cd /etc/nsscache && ls
   ```

   This should return the following files:

   ```text theme={"system"}
   group.cache passwd.cache shadow.cache sshkey.cache
   ```

3. Check the contents of the `group.cache`, `passwd.cache`, `shadow.cache`, and `sshkey.cache` files directly for information about the users and groups in your directory, as shown with the following `cat` command:

   ```bash theme={"system"}
   cat sshkey.cache
   ```

   Alternatively, use the `getent` command with the `group`, `passwd`, or `shadow` options to list the system users and groups in addition to the data pulled by `nsscache`, as shown in the following example:

   ```bash theme={"system"}
   getent passwd
   ```

   The `getent` command doesn't retrieve SSH keys directly. To view the contents of the `sshkey.cache` file, use the `cat` command, as shown in the preceding example.

## Migrate to `nsscache` from SSSD

> [!NOTE]
>
> In SUNK v7.0.0 and later, `nsscache` is the default directory service. The following steps only apply if you use an earlier version of SUNK and are migrating to `nsscache` for your directory service.

If you're upgrading from an earlier version of SUNK that used SSSD, the following sections describe how to disable SSSD and switch the relevant Helm charts to `nsscache`.

### Disable SSSD in the `slurm` and `slurm-login` charts

SSSD and `nsscache` are mutually exclusive, so you must turn off SSSD before `nsscache` can handle directory lookups. To enable `nsscache`, you must edit the `slurm` Helm chart. If you use [individual login Pods](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login.md), you must also edit the `slurm-login` Helm chart.

### Update the `slurm` chart

In the `slurm` chart's `values.yaml` file, update the `sssdContainer.enabled` parameter to `false` and remove the `directoryService` section, as shown in the following example:

```yaml highlight={4} theme={"system"}
sssdContainer:
  enabled: false
# Remove the `directoryService` key
directoryService:
```

This disables SSSD, which is incompatible with `nsscache`.

You may remove the `directoryCache.directoryService` section in the `values.yaml` of the `slurm` chart, because `nsscache` does not use this configuration.

> [!NOTE]
>
> **Disable SSSD**
>
> You must disable SSSD to use `nsscache`. For SUNK versions v6.x and earlier, SSSD is enabled by default.

### Update the `slurm-login` chart

If you use [individual login Pods](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login.md), you must also edit the `slurm-login` chart's `values.yaml` file.

Set the `directoryCache.source` parameter to `nsscache`, as shown in the following example:

```yaml highlight={4} theme={"system"}
directoryCache:
  source: nsscache
# Remove the `directoryService` key
  directoryService:
```

You may remove the `directoryCache.directoryService` section in the `values.yaml` of the `slurm-login` chart, because `nsscache` does not use this configuration.

At this point, both the `slurm` and `slurm-login` charts are configured to use `nsscache` as the directory service, and your cluster is ready to provision users through SUP.
