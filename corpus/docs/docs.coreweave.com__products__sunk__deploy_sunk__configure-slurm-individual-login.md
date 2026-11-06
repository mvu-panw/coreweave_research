# Configure individual login Pods

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/configure-slurm-individual-login

# Configure individual login Pods

> Configure per-user Slurm login Pods on SUNK 7.x and earlier through the slurm-login subchart

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

Individual login Pods give each user their own Slurm login Pod. They isolate each user's session, simplify access control, and let a directory service manage user identities centrally.

Where you configure login Pods depends on your SUNK version. If you use version 8.0 or later, it also depends on how you deploy:

* **SUNK 7.x and earlier**: Configure individual login Pods through the `slurm-login` subchart of the Slurm chart, as described on this page.
* **SUNK 8.0 and later**
  * **Deployed with Helm (SUNK Standard)**: The `slurm-login` subchart no longer exists. This functionality has been added to the SUNK operator, and you configure it in the `slurm` chart under `login`. `login.common` sets the base for both kinds of Pod, `login.userPods` and `login.groupPods` override that base per kind, and each entry in `login.groups` picks which kinds a group gets. See [Login capacity is provisioned per user and per group](https://docs.coreweave.com/release-notes/sunk-8-0.md#login-capacity-is-provisioned-per-user-and-per-group).
  * **Deployed with the `SunkCluster` CR (SUNK Self-Service only)**: Configure login Pods declaratively on the `SunkCluster` resource under `spec.login`, where `userPods` creates a per-user login Pod for each member of a group and `groupPod` creates a shared per-group Pod. See [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md) and the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#loginconfig).

> [!NOTE]
>
> The `slurm-login` parameters on this page apply to SUNK 7.x and earlier. SUNK 8.0 deleted that subchart, along with its `directoryCache` and its SSSD support. The sections on [SSH exposure](#expose-ssh-access), [the default shell](#set-the-default-shell), and [conda](#avoid-conda-breaking-system-binaries) apply to every version and deployment path.

The rest of this page shows administrators how to enable per-user Slurm login Pods, integrate them with a directory service, verify the resulting resources, and avoid the access and shell pitfalls that generate the most support requests. For the `slurm-login` path, pass these configuration values from the `values.yaml` of the Slurm chart to define how `slurm-login` integrates and functions.

## Prerequisites

Before you configure individual login Pods, make sure you have:

* A SUNK 7.x or earlier cluster deployed and managed through the Slurm Helm charts. SUNK 8.0 and later use the paths listed in the preceding note.
* Access to edit the Slurm chart's `values.yaml`, where you set the `slurm-login` parameters.
* A directory service configured for user identities, either `nsscache` for SCIM or SSSD for LDAP. See [manage users with `nsscache`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache) and [manage users with a directory service](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/directory-services.md).
* The user groups you want to grant access to, defined in that directory service, so you can reference them in `slurm-login.directoryCache.selectGroups`.
* `kubectl` access to the cluster to verify the resulting StatefulSets and Services.

## Manage individual login Pods

You can enable, reboot, and access individual login Pods using the following capabilities:

* **Enable the deployment of the subchart**: To enable the `slurm-login` capability as part of the Slurm chart, set the `slurm-login.enabled` parameter to `true`.

* **Reboot individual login Pods**: If an individual login Pod is out of sync with the underlying StatefulSet, run the `reboot` command from within the Pod. This command deletes and recreates the Pod using the updated version. If the Pod is out of sync, a Message of the Day (MOTD) appears at SSH login with instructions to reboot:

  ```text theme={"system"}
  **********************************************************************
  *                                                                    *
  * The login statefulset has been updated, please restart your login  *
  * pod to get the latest changes.                                     *
  *                                                                    *
  * To restart the login pod, issue the command "reboot".              *
  **********************************************************************
  ```

* **Access individual login Pods**: For instructions on accessing each individual Slurm login Pod and running Slurm jobs, refer to [Connect to a Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

## Expose SSH access

You can expose login Pod SSH access two ways, with a security tradeoff:

* **Public LoadBalancer**: The login Pod gets a public, internet-routable IP. This is the simplest connectivity, but it exposes SSH to internet scanning and brute-force attempts. On SUNK Standard, harden it, for example, by disabling password authentication through `login.sshdConfig`. Note that a NetworkPolicy doesn't filter traffic arriving through the LoadBalancer, so it can't be used to restrict which addresses reach the Pod.
* **Tailscale**: The login Pod stays on a private overlay network with no public exposure. This is the more secure posture, at the cost of running and managing Tailscale. On SUNK Standard, see the [Tailscale sidecar example](https://docs.coreweave.com/products/sunk/manage_sunk/add-sidecars-to-slurm-nodes.md#sidecar-example-tailscale). On SUNK Self-Service, you can't run Tailscale as a sidecar in the login Pod. Run your own Tailscale outside the login Pods, and add any annotations it needs through your `SunkCluster` configuration. [Contact CoreWeave Support](https://docs.coreweave.com/support.md) for integration guidance.

Sustained scanning against a public login Pod can exhaust Pod resources even when every login attempt fails, so treat a private path as the stronger control and `sshd` hardening as defense in depth.

## Set the default shell

Set the default shell through your directory service rather than `chsh`. A directory service provisions login Pod users, not local `/etc/passwd`, so `chsh` doesn't work.

A user who wants a different interactive shell can `exec` it from their `~/.bashrc` as a self-service workaround. The `exec` line must come after the interactive-shell guard. Placed before it, it hangs SCP, SFTP, rsync, and git-over-SSH, because those sessions source `~/.bashrc` and then wait forever on the new shell:

```bash theme={"system"}
# Guard first. Everything below this line runs only in interactive shells.
[[ $- != *i* ]] && return
exec zsh
```

## Avoid conda breaking system binaries

A common support pattern: After a user activates a conda environment, system tools such as `git`, `ssh`, and `curl` fail with errors such as an OpenSSL version mismatch or "Could not read from remote repository." This looks like a network or authentication problem but is a library conflict.

The cause is that conda's activation prepends conda's `lib` directory to `LD_LIBRARY_PATH`, so system binaries load conda's libraries instead of the system ones. `conda deactivate` doesn't always clean it up.

Recommend that users keep conda opt-in inside compute jobs rather than autoactivating it in `~/.bashrc` on the login Pod, which would break system binaries for every interactive shell. Workarounds for an affected command include installing the tool into the conda environment (`conda install -n [ENV] git`), or running the system binary with a cleared path (`LD_LIBRARY_PATH= /usr/bin/git ...`).

> [!NOTE]
>
> A shared login Pod is a single memory cgroup shared by every user's interactive processes. Heavy interactive work, such as an IDE remote-server process plus interactive Python, can OOM-kill the whole sshd tree and drop every session at once. Prefer per-user Pods and direct heavy work to `srun` and `sbatch` rather than the login Pod. For memory accounting and limits on compute nodes, see [Diagnose unexplained memory pressure on a SUNK node](https://docs.coreweave.com/products/sunk/optimize_workloads/memory-accounting.md).

## Manage user identities and provision resources

The `slurm-login.directoryCache` parameter defines the directory service configuration used for managing user identities and provisioning resources. The following sections describe its key sub-values.

### Select users by group

`slurm-login.directoryCache.selectGroups` provides a list of user groups, from which the `slurm-login` chart retrieves all associated users. This acts as a filter, so it includes only users that belong to one of the specified groups. It uses OR logic, so a user must be in at least one of the listed groups to be selected.

### Define the polling interval

`slurm-login.directoryCache.interval` defines the polling interval for detecting changes to users and user groups and applying the corresponding resource updates. The value is a duration with a unit, such as `30s` or `1m`, and defaults to 90 seconds when unset. For more information, see [`directoryCache.interval`](https://docs.coreweave.com/products/sunk/reference/slurm-login-parameters#directoryCache--interval) in the Slurm login parameter reference.

### List directory services

`slurm-login.directoryCache.directoryService.directories` specifies a list of directory services to configure. This is similar to the `directoryService` configuration in Slurm and can be duplicated or referenced using a YAML anchor for reuse.

#### Example nsscache configuration

The following shows a typical nsscache configuration:

```yaml theme={"system"}
slurm-login:
  enabled: true
  directoryCache:
    source: nsscache
    selectGroups: ["group1", "group2"]
```

See [manage users with `nsscache`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/nsscache) for instructions on configuring `nsscache`.

#### Example SSSD configuration

The following shows a typical SSSD configuration:

```yaml theme={"system"}
slurm-login:
  enabled: true
  directoryCache:
    source: sssd
    selectGroups: ["group1", "group2"]
    interval: 1m
    directoryService:
      # Google Secure LDAP
      directories:
        - name: google-example.com
          enabled: true
          ldapUri: ldaps://ldap.google.com:636
          user:
            canary: user@google-example.com
          defaultShell: "/bin/bash"
          fallbackHomeDir: "/home/%u"
          overrideHomeDir: /mnt/nvme/home/%u
          ldapsCert: google-ldaps-cert
          schema: rfc2307bis
```

For more information about configuring SSSD, see [manage users with a directory service](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/directory-services.md).

## Verify individual Slurm login resources

To verify created resources, use the StatefulSets and Services as shown in the following commands.

```bash theme={"system"}
kubectl get sts
```

The output is similar to the following:

```text theme={"system"}
NAME                             READY   AGE
slurm-login                      1/1     20d
slurm-login-slurmuser1-7fcd49e   1/1     31d
slurm-login-slurmuser2-a19c153   1/1     31d
slurm-login-slurmuser3-4fe7f1d   1/1     31d
slurm-login-slurmuser4-4f705de   1/1     31d
slurm-login-slurmuser5-5e909b3   1/1     31d
```

```bash theme={"system"}
kubectl get svc
```

The output is similar to the following:

```text theme={"system"}
NAME                             TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
slurm-login                      LoadBalancer   10.96.46.53     <pending>     22:31408/TCP   35d
slurm-login-0                    LoadBalancer   10.96.146.233   <pending>     22:31276/TCP   35d
slurm-login-slurmuser1-7fcd49e   ClusterIP      10.96.61.246    <none>        22/TCP         32d
slurm-login-slurmuser2-a19c153   ClusterIP      10.96.160.110   <none>        22/TCP         32d
slurm-login-slurmuser3-4fe7f1d   ClusterIP      10.96.2.45      <none>        22/TCP         32d
slurm-login-slurmuser4-4f705de   ClusterIP      10.96.203.63    <none>        22/TCP         32d
slurm-login-slurmuser5-5e909b3   ClusterIP      10.96.184.148   <none>        22/TCP         32d
```

These commands confirm that the per-user StatefulSets and Services exist for each selected user.

Optionally, to ensure that users only use their designated Pods, you can disable the shared Slurm login StatefulSet and `slurm-login` Service.

## Parameter reference table

The following table summarizes the `slurm-login` parameters described in the preceding sections for quick reference.

| Parameter | Description |
| - | - |
| `slurm-login.enabled` | Set this value to `true` in the Slurm chart to enable the `slurm-login` chart. |
| `slurm-login.directoryCache` | Defines the directory service configuration used for managing user identities and provisioning resources. |
| `slurm-login.directoryCache.selectGroups` | Provides a list of user groups that the `slurm-login` chart uses to retrieve all associated users. This acts as a filter, meaning only users belonging to any of the specified groups are included. It uses OR logic, so a user must be in at least one of the listed groups to be selected. |
| `slurm-login.directoryCache.interval` | Defines the polling interval for detecting changes to users and user groups, as a duration such as `1m`. Defaults to 90 seconds when unset. |
| `slurm-login.directoryCache.directoryService.directories` | Specifies a list of directory services to configure. This is similar to the `directoryService` configuration in Slurm and can be duplicated or referenced using a YAML anchor for reuse. |

For the full list of `slurm-login` parameters, see the [Slurm login parameter reference](https://docs.coreweave.com/products/sunk/reference/slurm-login-parameters.md).
