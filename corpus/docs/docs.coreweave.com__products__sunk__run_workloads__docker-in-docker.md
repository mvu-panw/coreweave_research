# Use Docker in SUNK

Source: https://docs.coreweave.com/products/sunk/run_workloads/docker-in-docker

# Use Docker in SUNK

> Enable Docker-in-Docker inside SUNK clusters by configuring AppArmor, privileged pods, and s6 services

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This guide explains how to use Docker inside a SUNK cluster with a technique known as Docker-in-Docker (DinD). This approach enables automated evaluations and lets you run benchmarks, [such as SWE-bench](https://docs.coreweave.com/products/sunk/tutorials/swe-bench-in-sunk.md), within your SUNK cluster.

This guide is for cluster administrators who need to enable container-based workflows inside SUNK compute nodes. Before you begin, review the [known security risks](#known-security-risks) section so you understand the trade-offs this configuration introduces.

> [!WARNING]
>
> The solution presented in this guide requires enabling privileged Pods and disabling the AppArmor profile recommended for use in SUNK. This process grants elevated kernel capabilities and weakens isolation guarantees. See the [known security risks](#known-security-risks) section for more details.
>
> You are responsible for verifying that third-party code is safe to execute alongside your other workloads.

## Enable Docker-in-Docker

To run Docker inside SUNK compute nodes, you must disable AppArmor and run privileged Pods. The following changes to the Slurm Helm chart install the Docker daemon on each compute node, mount storage for Docker that lasts for the lifetime of the Pod, and relax the security context so the daemon can operate.

To disable AppArmor and run privileged Pods, edit the `values.yaml` file of the Slurm Helm chart.

In the `compute` section of the `slurm` Helm chart:

1. Create an `s6` block to install and enable Docker. Because the Docker service is a `longrun`, set `timeoutUp`, `timeoutDown`, or both. SUNK rejects a `longrun` service that sets neither. See [Set timeouts for scripts](https://docs.coreweave.com/products/sunk/run_workloads/run-scripts-with-s6.md#set-timeouts-for-scripts).

2. Add a volume mount for Docker using the `volumeMounts` and `volumes` blocks.

3. Under `pyxis`, apply the following settings:

   * Set `pyxis.enabled` to `true`.
   * Set `pyxis.appArmorProfile` to `unconfined` to disable AppArmor confinement.
   * Set `pyxis.podSecurityContext.seccompProfile.type` to `Unconfined` to disable seccomp filtering.

   Use explicit `unconfined` settings. In SUNK v8, the operator restores the default profiles when these values are omitted or set to `null`.

4. Under `securityContext`, set `securityContext.privileged` to `true` for the `slurmd` container.

   The result should resemble the following:

   ```yaml theme={"system"}
   compute:
     s6:
       docker:
         type: longrun
         timeoutUp: 3600000 # 1 hour, in milliseconds
         script: |
           #!/bin/sh
           curl -fsSL https://get.docker.com | sh
           dockerd
     volumeMounts:
       - mountPath: /var/lib/docker
         name: docker-storage
     volumes:
       - name: docker-storage
         emptyDir: {}
     pyxis:
       enabled: true
       appArmorProfile: unconfined
       podSecurityContext:
         seccompProfile:
           type: Unconfined
     securityContext:
       privileged: true

   ```

5. Apply the values through your Helm deployment and wait for the compute Pods to roll out. For CPU-only testing, also set `compute.gpusd.enabled` to `false` to prevent the GPUSD installer from competing with Docker for the package-manager lock.

6. Verify the running Pod's security settings. This check requires `jq`. Replace `[SLURMD-POD-NAME]` with the name of your slurmd Pod and `[NAMESPACE]` with its namespace.

   ```bash theme={"system"}
   kubectl -n [NAMESPACE] get pod [SLURMD-POD-NAME] -o json | jq '
     . as $pod | .spec.containers[] | select(.name == "slurmd") | {
       privileged: .securityContext.privileged,
       appArmor: .securityContext.appArmorProfile,
       appArmorAnnotation: $pod.metadata.annotations["container.apparmor.security.beta.kubernetes.io/slurmd"],
       podSeccomp: $pod.spec.securityContext.seccompProfile
     }'
   ```

   Verify that `privileged` is `true`, `appArmorAnnotation` is `unconfined`, and `podSeccomp.type` is `Unconfined`. If the container has an `appArmor` field, its `type` must also be `Unconfined`.

7. After Docker finishes installing, verify that it can run a container:

   ```bash theme={"system"}
   kubectl -n [NAMESPACE] exec [SLURMD-POD-NAME] -c slurmd -- docker run --rm hello-world
   ```

   The output should include `Hello from Docker!`.

## Grant users Docker access

With the Helm chart changes applied, Docker is available on the compute nodes, but only `root` can use it by default. The next step grants non-root users the permissions they need to run Docker commands.

After you disable AppArmor and enable privileged Pods, grant users access to Docker.

If not running as `root`, users must belong to the `sudoers` group. If the SUNK cluster manages users with SUNK User Provisioning (SUP), set `nsscache.sudoGroups` to the groups that should have sudo privileges.

### SUP-based clusters

For SUP-based clusters, configure `nsscache:` to provision access through SCIM, and list the sudo-enabled groups under `sudoGroups:`. Group names must exactly match the group names in CoreWeave IAM or your upstream IdP. Refer to [the SUP documentation on creating user groups](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/sunk_user_provisioning.md#create-sunk-user-groups).

```yaml theme={"system"}
 nsscache:
  sudoGroups:
   - slurm-sudo
   - additional-group
```

### SSSD-based clusters

For SSSD-based clusters, set the `sudoGroups:` configuration in `directoryService:` to a list of Unix groups from all directories with sudo privileges.

* The group names are not fully qualified for the default directory. For example, the default directory's group name should be `group1` instead of `group1@example.com`.
* The group names are fully qualified for any additional directories.

```yaml theme={"system"}
directoryService:
  sudoGroups: ["slurm-sudo", "additional-group@example.com"]
```

## Known security risks

Enabling Docker-in-Docker requires loosening several of SUNK's default isolation guarantees. Before you apply the preceding configuration, review the risks in this section so you can decide whether the trade-offs are acceptable for your environment.

Kubernetes provides a list of [pod security standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). The following sections outline the subset most relevant to SUNK, but consider all of the standards listed in the Kubernetes documentation when assessing risk.

The setup described in this guide:

* Runs Docker inside a Pod.
* Requires privileged mode.
* Disables AppArmor protections.

> [!CAUTION]
>
> This setup grants full access to the `/proc` and `sys` directories, and allows kernel-level operations, including mounting, pivoting `root`, and process tracing.

### Item at risk: `cgroups`

`cgroups` handle management and monitoring of resources used by Slurm jobs. In privileged mode, users can bypass `cgroup` restrictions, reconfigure the resource limits set by Slurm, and move processes outside of their assigned `cgroups`. **This is critical to understand when providing support for multi-tenancy in a single CKS cluster. The same guardrails you depend on for isolation do not apply here.**

### Item at risk: System and security

Disabling AppArmor on a privileged Pod removes additional security features, including protections against kernel exploits. This allows unrestricted access to the `/proc` and `/sys` directories. Without AppArmor protections in place, users can gain access to and tamper with other containers in the Pod, or access other devices outside the intended allocation.
