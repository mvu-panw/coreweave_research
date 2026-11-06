# Provision users in SUNK

Source: https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning

# Provision users in SUNK

> Set up SUNK User Provisioning (SUP) with CoreWeave IAM

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

## Overview

This page explains how to provision users in CoreWeave Identity and Access Management (IAM) for SUNK so they receive POSIX identities, SSH keys, and Slurm accounts in your cluster. It also explains how SUP keeps Slurm users in step with IAM afterward, including when it deletes them. After you complete the steps here, you can continue to [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache) so those identities are available on the cluster.

For the relationship between identity provisioning, authentication, platform IAM, and SUNK-specific authorization, see the [CoreWeave authorization model](https://docs.coreweave.com/security/iam.md#authorization-model).

SUNK access management refers to the provisioning of users in your SUNK cluster. Provisioned users can connect over SSH to Login Nodes and Individual Login Pods, manage Slurm settings, and use Slurm commands to run experiments. At CoreWeave, this encompasses the flow of user identities from its source of truth to the creation of POSIX and Slurm identities in your SUNK cluster. This end-to-end flow is implemented by Automated User Provisioning (AUP) and SUNK User Provisioning (SUP). You can use SUP alongside or independently of AUP.

AUP connects your organization's identity provider (IdP) (An Identity Provider (IdP) is an entity that stores and verifies the identity of a user.) to CoreWeave IAM through [SCIM](https://scim.cloud/), the modern standard for secure identity synchronization. AUP continuously syncs users and groups from an upstream IdP, such as Okta or Microsoft Entra. Any upstream changes, such as new users, role updates, or deletions, propagate automatically to CoreWeave IAM.

SUP provisions CoreWeave IAM data into SUNK, whether that data was federated from an IdP through AUP or manually created in the CoreWeave Cloud Console. The exception is users marked [exempt from SCIM](https://docs.coreweave.com/security/automated-user-provisioning.md#exempt-a-user-from-scim), which SUP doesn't provision. SUP automatically creates POSIX users and groups, SSH keys, and Slurm users and accounts in your SUNK clusters as soon as a user is added directly to CoreWeave IAM or to an upstream IdP.

The following diagram shows how all three provisioning paths (IdP federation via AUP, manual user and group management, and user SSH keys) flow through CoreWeave IAM and into SUNK clusters via SUP:

![Diagram showing three provisioning paths into CW IAM: an identity provider through AUP and SCIM, manual user and group management, and user SSH keys. CW IAM then flows through SCIM and SUP to Slurm Cluster A and Slurm Cluster B.](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/security/_media/aup-sup-flow-diagram.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=793b038388d6b816cbedeab06771281c)

User provisioning flow from identity sources through CoreWeave IAM to SUNK clusters

## Provision users in CoreWeave IAM

The following sections describe how to get users into CoreWeave IAM. You can federate from an IdP with AUP, create users manually in the Cloud Console, or create them programmatically through the SCIM API. Follow the instructions for one of these methods before configuring SUP so that SUP has IAM data to sync into the cluster.

### Prerequisites

Before you provision users in CoreWeave IAM, enable the following settings on the [**SCIM Configuration** page](https://console.coreweave.com/organization/iam/scim):

* **Enable SCIM API**
* **Enable SUNK user provisioning**

![SCIM Configuration page with the prerequisite toggles enabled](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_toggles_no_aup.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=6f4580cc76f227aadae7096260ec8a61)

### Provision users from an IdP into CoreWeave IAM

This section assumes you're federating users from an IdP with AUP. Complete [configure AUP with Okta](https://docs.coreweave.com/security/automated-user-provisioning/configure-okta.md) or [configure AUP with Microsoft Entra](https://docs.coreweave.com/security/automated-user-provisioning/configure-microsoft-entra.md) first so users and groups exist in CoreWeave IAM before you continue with the steps in this section.

1. In the Cloud Console, navigate to the [SCIM Configuration](https://console.coreweave.com/organization/iam/scim) page.

   ![SCIM option in the IAM sidebar](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_sidebar.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=ec72e688d0c5c78e99886b41d73a9a66)

2. If **Enable automated user provisioning** isn't already enabled, click the toggle to enable it. All three toggles must be enabled if you're federating from an IdP.

   ![SCIM Configuration page with the toggles enabled](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_toggles.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=2f8600d4dbb11e7defc88ec838fa9298)

3. In your IdP, create custom attributes for the SUNK user attributes and map them to CoreWeave's SCIM endpoint. CoreWeave IAM needs the SSH key mapping so SUP can install the correct keys on the cluster. The POSIX attributes are optional. Map them only if you want to set POSIX identities from your IdP instead of letting CoreWeave IAM generate them, as described in [Slurm user attributes](#slurm-user-attributes).

   All attributes use the SCIM namespace `urn:coreweave:params:scim:schemas:extension:coreweave:2.0:CoreWeaveUser`, and the target attribute names must match exactly:

   | Target attribute | Data type | Required |
   | - | - | - |
   | `sunkSshKeys` | String, multi-valued (a list of keys) | Yes |
   | `sunkPosixUsername` | String | No |
   | `sunkPosixUserId` | Integer | No |
   | `sunkPosixGroupId` | Integer | No |

   For the full list of SUNK attributes, see [SUNK SCIM attribute reference](#sunk-scim-attribute-reference). For IdP-specific setup instructions, see:

   * [Map SSH keys for SUNK with Microsoft Entra](https://docs.coreweave.com/security/automated-user-provisioning/configure-microsoft-entra.md#map-ssh-keys-for-sunk)
   * [Map SSH keys for SUNK with Okta](https://docs.coreweave.com/security/automated-user-provisioning/configure-okta.md#map-sunk-attributes)

4. In your IdP, navigate to the target user's profile and add their SSH public key to the custom attribute you created.

5. In the Provisioning section of your IdP, verify that the SSH key attribute is included in the attribute mappings for the CoreWeave application.

6. In the Cloud Console, navigate to the [Users](https://console.coreweave.com/organization/users) page to view a list of all users in your organization. Click the three-dot menu icon to the right of the target user's name, and then click **View Details**.

   ![View Details option for a user](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_details.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=e356b60548a8c1ef3eccf58322bcf0ce)

7. Verify that **SSH keys** in the **SUNK cluster access** section contains the SUNK public SSH key that you added in your IdP. When you use AUP, this field automatically synchronizes with CoreWeave IAM whenever changes are made in your IdP. Users can edit their own keys in the Cloud Console, but the next synchronization overwrites the change. Don't rely on manual updates for persistent SSH key configuration when using AUP.

8. Continue to [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache). At this point, federated users should appear in CoreWeave IAM with SSH keys that SUP can propagate to SUNK.

   For more information about AUP and integrating it with other CoreWeave services, see the [Automated User Provisioning guide](https://docs.coreweave.com/security/automated-user-provisioning.md).

### Provision users directly in CoreWeave IAM

1. In the Cloud Console, navigate to the [SCIM Configuration](https://console.coreweave.com/organization/iam/scim) page.

   ![SCIM option in the IAM sidebar](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_sidebar.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=ec72e688d0c5c78e99886b41d73a9a66)

2. If they aren't already enabled, click the toggle buttons to enable the following settings:

   * **Enable SCIM API**
   * **Enable SUNK user provisioning**

   On the SCIM Configuration page, you don't need to toggle **Enable automated user provisioning** if you aren't federating from an IdP.

   ![SCIM Configuration page with the toggles enabled](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_toggles_no_aup.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=6f4580cc76f227aadae7096260ec8a61)

3. Each user who needs cluster access must add at least one public SSH key in [their **User settings** page](https://console.coreweave.com/account/settings), also accessible from the profile icon at the top right of the Cloud Console.

   1. In the **SUNK cluster access** section, click **Add SSH key**. If the user already has keys, the button reads **Manage SSH keys**.
   2. In **SSH public keys**, paste one public key per line (newline-separated), not comma-separated. To print a key, run `cat ~/.ssh/id_ed25519.pub`, replacing the filename if the key is stored elsewhere.
   3. Click **Save SSH keys**.

   The **SUNK cluster access** section also shows the user's POSIX username for logging in. If the section indicates that the SSH keys are unavailable, verify that **Enable SUNK user provisioning** is enabled on the [**SCIM Configuration** page](https://console.coreweave.com/organization/iam/scim).

   > [!TIP]
   >
   > When SUP is enabled and a user without an SSH key opens the SUNK cluster list in the Cloud Console, a warning appears with an **Add SSH key** link. Users can also search for `ssh` in the Cloud Console command palette to open the SSH keys panel.

4. Continue to [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache). Users who added SSH keys in their User settings page are ready for SUP to create matching POSIX and Slurm identities on the cluster.

### Provision users programmatically through the SCIM API

You can call CoreWeave's SCIM API directly with a SCIM API token, without an IdP. Use this path to script user and group management, for example to create many users at once or to set POSIX attributes that the Cloud Console displays as read-only. The API implements the [SCIM 2.0 protocol (RFC 7644)](https://datatracker.ietf.org/doc/html/rfc7644), with the CoreWeave extension described in [SUNK SCIM attribute reference](#sunk-scim-attribute-reference).

> [!WARNING]
>
> If you also federate users from an IdP with AUP, the next synchronization from your IdP can overwrite values you set through the API. Manage each user from one source.

1. In the Cloud Console, navigate to the [SCIM Configuration](https://console.coreweave.com/organization/iam/scim) page and confirm that **Enable SCIM API** and **Enable SUNK user provisioning** are enabled.

2. Copy the URL under **SCIM base URL**. It has the form `https://api.coreweave.com/scim/[ORG-ID]`, where `[ORG-ID]` is your [organization ID](https://docs.coreweave.com/security/authn-authz/orgs-users.md#organization-ids).

3. Under **SCIM API tokens**, click **Create Token**, and then set the following:

   * **Token name**: up to 20 characters, using letters, numbers, and hyphens.
   * **Permissions**: **Read and write**. A **Read** token can't create or change users and groups.
   * **Expiration**: how long the token stays valid, up to 365 days.

4. Click **Create Token**, and then copy the token. The Cloud Console shows the token only once. Treat it like a password.

5. Export the base URL and the token as environment variables:

   ```bash theme={"system"}
   export SCIM_BASE_URL="https://api.coreweave.com/scim/[ORG-ID]"
   export SCIM_TOKEN="[SCIM-TOKEN]"
   ```

6. Create a user. The request must include both the core SCIM `User` schema and the CoreWeave user extension schema, and `userName` must be the user's email address. Only `sunkSshKeys` is needed for cluster access. Omit the POSIX attributes to let CoreWeave IAM generate them, as described in [Slurm user attributes](#slurm-user-attributes).

   ```bash theme={"system"}
   curl -X POST "$SCIM_BASE_URL/Users" \
     -H "Authorization: Bearer $SCIM_TOKEN" \
     -H "Content-Type: application/scim+json" \
     -d '{
       "schemas": [
         "urn:ietf:params:scim:schemas:core:2.0:User",
         "urn:coreweave:params:scim:schemas:extension:coreweave:2.0:CoreWeaveUser"
       ],
       "userName": "jane.doe@example.com",
       "name": {
         "givenName": "Jane",
         "familyName": "Doe"
       },
       "emails": [
         {
           "primary": true,
           "value": "jane.doe@example.com",
           "type": "work"
         }
       ],
       "active": true,
       "urn:coreweave:params:scim:schemas:extension:coreweave:2.0:CoreWeaveUser": {
         "sunkSshKeys": ["[SSH-PUBLIC-KEY]"],
         "sunkPosixUsername": "janedoe",
         "sunkPosixUserId": 100500,
         "sunkPosixGroupId": 100500
       }
     }'
   ```

   The response contains the user's `id`. Save it for the following steps:

   ```bash theme={"system"}
   export USER_ID="[USER-ID]"
   ```

7. Create a group. Use a group name that your cluster grants access to, so SUP provisions its members on the cluster: on SUNK Standard, a group in your [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache#provision-cluster-access-to-groups-of-users); on a `SunkCluster` CR, a group in `spec.login.groups`.

   ```bash theme={"system"}
   curl -X POST "$SCIM_BASE_URL/Groups" \
     -H "Authorization: Bearer $SCIM_TOKEN" \
     -H "Content-Type: application/scim+json" \
     -d '{
       "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
       "displayName": "slurm-users",
       "members": []
     }'
   ```

   The response contains the group's `id`. Save it:

   ```bash theme={"system"}
   export GROUP_ID="[GROUP-ID]"
   ```

8. Add the user to the group:

   ```bash theme={"system"}
   curl -X PATCH "$SCIM_BASE_URL/Groups/$GROUP_ID" \
     -H "Authorization: Bearer $SCIM_TOKEN" \
     -H "Content-Type: application/scim+json" \
     -d '{
       "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
       "Operations": [
         {
           "op": "add",
           "path": "members",
           "value": [{ "value": "'"$USER_ID"'" }]
         }
       ]
     }'
   ```

   The `'"$USER_ID"'` sequence ends the single-quoted JSON body, inserts the value of `$USER_ID`, and then resumes the body. The request body then contains the user's ID as a JSON string.

To change a user's attributes later, including their SSH keys or POSIX IDs, send `PUT "$SCIM_BASE_URL/Users/$USER_ID"` with the user resource in the same format as the create request. The API updates the attributes you include and keeps the stored value of any attribute you leave out. To read a user's current attributes, send `GET "$SCIM_BASE_URL/Users/$USER_ID"`. To remove a user, send `DELETE "$SCIM_BASE_URL/Users/$USER_ID"`. This permanently deletes the user from your CoreWeave organization, not only from SUNK, and revokes their CoreWeave AI Object Storage access keys. SUP then removes the user from the cluster, as described in [When SUP deletes a Slurm user](#when-sup-deletes-a-slurm-user). To remove cluster access without deleting the user, set `"active": false` instead.

## Create a SCIM API token for a SUNK cluster

`nsscache` on each SUNK cluster reads users and groups from CoreWeave IAM through the SCIM API. It authenticates with a SCIM API token stored in a Kubernetes Secret. How you create that token depends on how you deploy the cluster:

* **Cloud Console**: when you [create a SUNK cluster in the Cloud Console](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md), the form requires **Enable SCIM API** and **Enable SUNK user provisioning** to be enabled, and an organization admin can turn them on from the form. The Cloud Console then creates a **Read** token named `[PREFIX]-scim-[N]` that expires after 364 days, and stores it in a Secret named `[CLUSTER-NAME]-nsscache-scim-secret` in the `tenant-slurm` namespace. You don't need to do anything else until the token nears expiry. See [Replace a SCIM API token before it expires](#replace-a-scim-api-token-before-it-expires).
* **`SunkCluster` CR**: you create the token and the Secret yourself, as described in the following steps.
* **Helm charts**: create the Secret described in [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache).

To create the token and Secret for a `SunkCluster` CR:

1. In the Cloud Console, navigate to the [SCIM Configuration](https://console.coreweave.com/organization/iam/scim) page and enable **Enable SCIM API** and **Enable SUNK user provisioning**.

2. Under **SCIM API tokens**, click **Create Token**. Enter a token name of up to 20 characters, using letters, numbers, and hyphens. Set **Permissions** to **Read**, because `nsscache` only reads from the API. Choose an **Expiration**, and then click **Create Token**.

3. Copy the token. The Cloud Console shows the token only once.

4. Store the token in a Secret named `[CLUSTER-NAME]-nsscache-scim-secret`, in the same namespace as the `SunkCluster`, under the key `nsscache-scim-auth-token`. Replace `[CLUSTER-NAME]` with the name of the `SunkCluster`, `[NAMESPACE]` with its namespace, and `[SCIM-TOKEN]` with the token:

   ```bash theme={"system"}
   kubectl create secret generic [CLUSTER-NAME]-nsscache-scim-secret \
     --namespace [NAMESPACE] \
     --from-literal=nsscache-scim-auth-token=[SCIM-TOKEN]
   ```

   The out-of-band operator finds the Secret by its name, so you don't reference it from the `SunkCluster` manifest. You can create the Secret before or after you apply the manifest. For the full walkthrough, see [Get started with SUNK Self-Service using the SunkCluster CR](https://docs.coreweave.com/products/sunk/tutorials/get-started-with-sunkcluster-cr.md#step-4-store-the-scim-token-as-a-kubernetes-secret).

   The token expires on the date you chose. To keep users in sync after that, see [Replace a SCIM API token before it expires](#replace-a-scim-api-token-before-it-expires).

### Replace a SCIM API token before it expires

SCIM API tokens expire, including the token the Cloud Console creates for you. When the token expires, `nsscache` can't read from CoreWeave IAM, so new users, SSH key changes, and group membership changes stop reaching the cluster. Replace the token before it expires, whichever way you deployed the cluster:

1. On the [SCIM Configuration](https://console.coreweave.com/organization/iam/scim) page, under **SCIM API tokens**, click **Create Token** and create a token with **Permissions** set to **Read**. Copy the new token.

2. Replace the value of `nsscache-scim-auth-token` in the cluster's SCIM Secret. Replace `[SECRET-NAME]` with the Secret's name, such as `[CLUSTER-NAME]-nsscache-scim-secret`, `[NAMESPACE]` with its namespace, such as `tenant-slurm` for a cluster created in the Cloud Console, and `[SCIM-TOKEN]` with the new token:

   ```bash theme={"system"}
   kubectl create secret generic [SECRET-NAME] \
     --namespace [NAMESPACE] \
     --from-literal=nsscache-scim-auth-token=[SCIM-TOKEN] \
     --dry-run=client --output yaml | kubectl apply --filename -
   ```

3. Restart `nsscache`. It reads the token when its Pod starts, so it keeps using the old token until the Pod restarts. Find the `nsscache` Deployment, and then restart it, replacing `[NSSCACHE-DEPLOYMENT]` with its name:

   ```bash theme={"system"}
   kubectl get deployments --namespace [NAMESPACE] | grep nsscache
   kubectl rollout restart deployment/[NSSCACHE-DEPLOYMENT] --namespace [NAMESPACE]
   ```

   On SUNK 7.x and earlier, `nsscache` runs as a CronJob instead of a Deployment. Each run starts a new Pod that reads the updated Secret, so you don't need to restart anything.

## Slurm user attributes

SUP automatically creates a POSIX User ID (UID), POSIX Group ID (GID), and POSIX username when a user is provisioned in CoreWeave IAM through AUP, the SCIM API, or manual creation. Only an SSH key is required for cluster access. CoreWeave IAM generates the other values when you don't set them:

| Attribute | Generated value |
| - | - |
| POSIX username | Derived from the part of the email address before the `@`, in lowercase. Characters other than letters, digits, `.`, `_`, and `-` are replaced. If the name is already taken in the organization, a numbered suffix is added. For example, `John.Doe+Tag@example.com` becomes `john.doe_tag`. |
| POSIX UID | An ID that CoreWeave IAM assigns. |
| POSIX GID | The same value as the UID. |

To use specific values instead, such as existing IDs from another POSIX environment, set `sunkPosixUsername`, `sunkPosixUserId`, and `sunkPosixGroupId` from your IdP or through the [SCIM API](#provision-users-programmatically-through-the-scim-api). See [SUNK SCIM attribute reference](#sunk-scim-attribute-reference). Users and admins can't change these values in the Cloud Console.

These IDs belong to the CoreWeave user, not the email address. Don't change a user's email address only in your identity provider. If your IdP identifies users by email, that creates a second user with new IDs and breaks SSH access and file ownership. To change an email address without getting new IDs, see [Change a user's email address](https://docs.coreweave.com/security/authn-authz/manage-users.md#change-a-users-email-address).

> [!WARNING]
>
> If you're migrating users from an existing POSIX environment, such as Authentik or another LDAP directory, set `sunkPosixUserId` and `sunkPosixGroupId` in your IdP before AUP synchronizes the users. Use each user's existing UID and GID. Otherwise, CoreWeave IAM assigns new values, and users can lose access to files owned by their previous numeric IDs. For the Okta migration procedure, follow [Preserve POSIX identities during migration](https://docs.coreweave.com/security/automated-user-provisioning/configure-okta.md#preserve-posix-identities-during-migration).

Users can view these values in the **SUNK cluster access** section of [their **User settings** page](https://console.coreweave.com/account/settings), and under **Slurm identity** in the SSH keys panel. They can open this page through the profile icon at the top right of the Cloud Console.

Admins can view these values on the [Users](https://console.coreweave.com/organization/users) page of the Cloud Console. Click the vertical dot menu icon to the right of a user's name, click **View Details**, and then find the **SUNK cluster access** section.

## Slurm user and account lifecycle

SUP keeps the Slurm accounting database consistent with the POSIX users that `nsscache` resolves on the cluster. A sync process in the `slurmctld` Pod reconciles the two about every 60 seconds.

A Slurm user and a Slurm account are separate records. A Slurm user is an individual identity, and a Slurm account is a group that Slurm users are associated with for usage tracking and limits. SUP creates and deletes Slurm users, but it only creates Slurm accounts.

Each sync run does the following:

1. Creates the default SUP Slurm account if it doesn't already exist on the cluster. The account name comes from [`nsscache.slurmUserProvisioning.defaultSlurmAccount`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#nsscache--slurmUserProvisioning--defaultSlurmAccount), which is `cw-sup` unless you override it.

2. Creates a Slurm user for every POSIX user who belongs to a provisioned group. The default account for each new Slurm user is the account from the preceding step. Provisioned groups are the groups you list in `scim_users_parameters` in the [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache#provision-cluster-access-to-groups-of-users). If you list no groups there, SUP uses `slurm-users`.

3. Deletes Slurm users that no longer map to a provisioned POSIX user, as described in [When SUP deletes a Slurm user](#when-sup-deletes-a-slurm-user).

> [!NOTE]
>
> On SUNK 8.0 and later, set the group list in `nsscache.groups`. The operator writes it into the `groups=` parameter of `scim_users_parameters`, which is the value the sync process reads, and it overrides any `groups=` value you set yourself under `nsscache.nsscacheConfig`. On SUNK 7.x and earlier, set `groups=` in `scim_users_parameters` directly. SUP creates and deletes Slurm users the same way in both versions.

SUP never deletes Slurm accounts. The default account and any accounts you create yourself remain in place even after SUP deletes the last user associated with them.

To stop SUP from managing Slurm users, set [`nsscache.slurmUserProvisioning.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#nsscache--slurmUserProvisioning--enabled) to `false`. Slurm users that SUP already created stay in the accounting database, because the sync run is the only process that deletes them. POSIX user and group provisioning continues, and you manage Slurm users yourself with `sacctmgr`.

### When SUP deletes a Slurm user

SUP deletes a Slurm user on the next sync run when either of the following is true:

* The POSIX user no longer resolves on the cluster. This happens after you remove or deactivate the user in CoreWeave IAM or in your upstream IdP, and `nsscache` stops publishing them.
* The POSIX user still resolves, but belongs to none of the provisioned groups. If you drop a group from `scim_users_parameters`, every user whose cluster access came from that group meets this condition.

If the user has non-terminal job records in the Slurm accounting database, such as a job stuck after a node failure, the delete attempt fails and SUP retries on the next sync run. The user remains in the accounting database until you clear the stuck job records.

SUP removes the user from the Slurm accounting database, not only from the default Slurm account. It also removes the user's admin level and every account association the user held on the cluster, including any you added manually with `sacctmgr`. To restore access, provision the user again and reapply those changes.

> [!WARNING]
>
> SUP deletes any Slurm user on the cluster that doesn't map to a POSIX user in a provisioned group, including users you created manually with `sacctmgr`. The `root` user is exempt. Don't rely on a manually created Slurm user surviving on a cluster where SUP manages Slurm users.

## Create SUNK user groups

Group names in CoreWeave IAM must match the names you reference in the [`nsscache` configuration](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache).

If you're federating users from an IdP, you can create your user groups there. AUP automatically syncs groups into CoreWeave IAM.

If you aren't federating users from an IdP, create your user groups in the CoreWeave Cloud Console:

1. In the [CoreWeave Cloud Console](https://console.coreweave.com), navigate to [the **Groups** tab](https://console.coreweave.com/organization/groups) in the left sidebar.

   ![Groups option in the IAM sidebar](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/scim_groups.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=7e2db80b6d52051457fb0c258f70d441)

2. Click the **Create Group** button at the top right of the page.

   ![Create Group button](https://mintcdn.com/coreweave-dbfa0e8d/AMJ2Ia-aOiGUfdv1/products/sunk/_media/scim_create_group.png?fit=max\&auto=format\&n=AMJ2Ia-aOiGUfdv1\&q=85\&s=457efa43c9a679fc0a5b687770d4c733)

3. Enter the group name and click **Create**. These group names must match the names of the groups specified in the `nsscache` configuration. Each new group automatically receives a GID.

## SUNK SCIM attribute reference

CoreWeave's SCIM API accepts the following SUNK attributes, whether they come from an IdP through AUP or from direct [SCIM API](#provision-users-programmatically-through-the-scim-api) calls.

### User attributes

User attributes belong to the CoreWeave user extension schema, `urn:coreweave:params:scim:schemas:extension:coreweave:2.0:CoreWeaveUser`. Every `/Users` request must include this schema.

| Attribute | Type | Required | Description |
| - | - | - | - |
| `sunkSshKeys` | String, multi-valued | Yes, for cluster access | The user's SSH public keys, used to log in to SUNK clusters. |
| `sunkPosixUsername` | String | No | The POSIX username the user logs in as. Generated from the email address if not set. Must be unique in the organization. A create request that sets a username already in use fails with a `409` error. Update requests don't check this, so don't set a username that's already in use when you update a user. |
| `sunkPosixUserId` | Integer | No | The user's POSIX UID. Generated if not set. |
| `sunkPosixGroupId` | Integer | No | The user's primary POSIX GID. Defaults to the UID if not set. |
| `sunkPreferredHomeDirectory` | String | No | The user's home directory. SUNK ignores this value by default, because `nsscache` sets every user's home directory to `/mnt/home/[USERNAME]` through [`scim_override_home_directory`](https://docs.coreweave.com/products/sunk/reference/nsscache_reference). |
| `sunkLoginShell` | String | No | The user's login shell. If not set, `nsscache` uses [`scim_default_shell`](https://docs.coreweave.com/products/sunk/reference/nsscache_reference), which defaults to `/bin/bash`. |

### Group attributes

Groups use the core SCIM `Group` schema at the `/Groups` endpoint. The SUNK group attributes are available at a separate `/CoreWeaveGroups` endpoint, with the schema `urn:coreweave:params:scim:schemas:core:coreweave:2.0:CoreWeaveGroup`. You can update them with a `PATCH` request to `/CoreWeaveGroups/[GROUP-ID]`.

| Attribute | Type | Description |
| - | - | - |
| `sunkPosixGroupId` | Integer | The group's POSIX GID. Generated when the group is created. |
| `sunkPosixGroupName` | String | The group's POSIX group name. |
