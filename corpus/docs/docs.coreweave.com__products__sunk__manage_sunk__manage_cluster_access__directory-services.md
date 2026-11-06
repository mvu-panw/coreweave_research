# Manage users with a directory service on SUNK Standard

Source: https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/directory-services

# Manage users with a directory service on SUNK Standard

> Manage user accounts on a SUNK Standard cluster with an external directory service

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

If you're using SUNK, you may want to manage user accounts using an external directory service. This guide shows you how to connect SUNK to a directory service for user management. It's intended for SUNK administrators who manage user authentication and want to centralize account management with an external identity provider such as Active Directory, OpenLDAP, Authentik, or Google Secure LDAP.

The following sections describe how to create a Kubernetes Secret to hold your directory service credentials, reference that Secret from Slurm's `values.yaml`, and configure SUNK for several common directory service providers.

## Set up a Kubernetes Secret

Before configuring SUNK to use a directory service, you must create a Kubernetes Secret that stores the bind credentials SUNK uses to query your directory.

> [!NOTE]
>
> Google Secure LDAP users should skip this step and [follow the instructions in that section](#create-a-secret-for-google-secure-ldap) to create the Secret using a TLS certificate instead.

### Create a Kubernetes Secret

> [!WARNING]
>
> CoreWeave discourages including sensitive information, such as plaintext user credentials, directly in your `values.yaml` configuration. Instead, use a Kubernetes Secret for added security and manageability. CoreWeave provides [encryption at rest](https://docs.coreweave.com/products/cks/clusters/secrets.md) for etcd data, which includes Secrets.

First, create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that contains the configuration for your directory service.

The Secret must meet the following criteria:

* The key name in the Secret must end with `.conf`.
* The Secret's data should include a full and correct SSSD configuration snippet. This snippet must include the domain and `ldap_default_authtok` parameter. This is not a user password.

Here's an example of a Secret that meets these criteria:

```yaml theme={"system"}
apiVersion: v1
kind: Secret
metadata:
  name: bind-user-sssd-config
type: Opaque
stringData:
  ldap-password.conf: |-
    [domain/default]
    ldap_default_authtok = [CREDENTIALS]
```

Replace `[CREDENTIALS]` with the actual credentials for your directory service.

> [!WARNING]
>
> The `ldap_default_authtok` parameter contains the bind password that SSSD uses to connect to the LDAP server and perform lookups. This parameter should not contain individual user credentials.

In this example, the `name` of the Secret is `bind-user-sssd-config`.

The example also adds a secret key with the `ldap-password.conf` parameter and inserts the SSSD configuration snippet within.

### Reference the Secret in `values.yaml`

Next, [update Slurm's `values.yaml` file](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) to reference the Secret you just created.

Add the `name` of your Secret to the `existingSecret` field.

Add the secret key to the `existingSecretFileName` field.

Ensure that the values in these fields match your created Secret exactly.

The following example uses the Secret `name` and secret key created in the [previous step](#create-a-kubernetes-secret):

```yaml theme={"system"}
directoryService:
  directories:
  - name: default
    user:
      existingSecret: bind-user-sssd-config
      existingSecretFileName: ldap-password.conf
```

## Create a Secret for Google Secure LDAP

Google Secure LDAP requires a TLS certificate instead of a bind password, so the Secret takes a different form than the SSSD configuration Secret described in the previous section.

If you want to use Google Secure LDAP, follow [Google's instructions](https://knowledge.workspace.google.com/admin/apps/add-ldap-clients) to add a new LDAP client. As part of the setup, you generate certificates and download them.

Then, create a Kubernetes Secret of type `tls` using the certificate files you downloaded:

```bash theme={"system"}
kubectl create secret tls google-ldaps-cert \
--cert=[YOUR-CERTIFICATE].crt \
--key=[YOUR-PRIVATE-KEY].key
```

Replace `[YOUR-CERTIFICATE].crt` and `[YOUR-PRIVATE-KEY].key` with your downloaded certificate and key.

Modify `values.yaml` to include the Google Secure LDAP configuration in the `directoryService` section:

```yaml theme={"system"}
directoryService:
  sudoGroups:
    - group1
  directories:
  - name: google-example
    enabled: true
    debugLevel: 0x0200
    ldapUri: ldaps://ldap.google.com:636
    user:
      canary: user@example.com
    defaultShell: "/bin/bash"
    fallbackHomeDir: "/home/%u"
    overrideHomeDir: /mnt/nvme/home/%u
    ldapsCert: google-ldaps-cert
    # For Google Secure LDAP, set schema: rfc2307bis
    schema: rfc2307bis
```

### Optional: Enable SSH with Google Secure LDAP

To let users sign in using an SSH key, add a multi-value attribute to your Google directory. Follow the [Google guide](https://knowledge.workspace.google.com/admin/users/create-custom-attributes-for-user-profiles) to create a custom attribute named `sshPublicKey`.

For each user, enter their SSH public key into the `sshPublicKey` attribute field.

> [!NOTE]
>
> Google's custom attribute values have a 500-character limit, so use a shorter key type like `ssh-ed25519`.

After completing these steps, SUNK is integrated with Google Secure LDAP, and users can authenticate through SSH keys tied to their Google accounts.

## Configuration examples

The following examples show `directoryService` configuration snippets for common directory service providers. Use them as a starting point and adjust the values to match your environment.

### Active Directory

```yaml theme={"system"}
directories:
  - name: active-directory-example
    enabled: true
    ldapUri: ldap://domaincontroller.tenant-my-tenant.coreweave.cloud
    user:
      bindDn: CN=binduser,CN=Users,DC=contoso,DC=com
      searchBase: DC=contoso,DC=com
      existingSecret: bind-user-sssd-config
      canary: binduser
    defaultShell: "/bin/bash"
    fallbackHomeDir: "/home/%u"
    schema: AD
```

### OpenLDAP

```yaml theme={"system"}
directories:
  - name: openldap-example
    enabled: true
    ldapUri: ldap://openldap
    user:
      bindDn: cn=admin,dc=coreweave,dc=cloud
      searchBase: dc=coreweave,dc=cloud
      existingSecret: bind-user-sssd-config
      canary: admin
    defaultShell: "/bin/bash"
    fallbackHomeDir: "/home/%u"
    schema: rfc2307
```

### Authentik

```yaml theme={"system"}
 directories:
  - name: authentik-example
    enabled: true
    ldapUri: ldap://authentik-outpost-ldap-outpost
    user:
      bindDn: cn=ldapsvc,dc=coreweave,dc=cloud
      searchBase: dc=coreweave,dc=cloud
      existingSecret: bind-user-sssd-config
      canary: ldapsvc
    startTLS: true
    userObjectClass: user
    groupObjectClass: group
    userNameAttr: cn
    groupNameAttr: cn
    schema: rfc2307bis
```

## General directory service configuration

The following sections list the configuration keys available in the `directoryService` section of `values.yaml`, with links to the full parameter reference.

For general configuration, see these keys in the `directoryService` section of `values.yaml`.

* [`debugLevel`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`directories`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`name`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`negativeCacheTimeout`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`sudoGroups`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)

## Directory service-specific configuration

Each named directory service has its own configuration section. See these keys in the
`directoryService.directories[*]` section of `values.yaml`.

* [`additionalConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`defaultShell`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`fallbackHomeDir`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`ldapUri`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`ldapsCert`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`overrideGidAttr`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`overrideHomeDir`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`overrideUidAttr`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`overrideUserNameAttr`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`schema`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`user.bindDn`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`user.canary`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`user.existingSecret`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`user.password`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
* [`user.searchBase`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters)
