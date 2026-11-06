# Manage a SUNK Standard deployment with CI and GitOps

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/manage-deployment-with-ci

# Manage a SUNK Standard deployment with CI and GitOps

> Manage a SUNK Standard deployment with ArgoCD and GitOps-based CI workflows

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

SUNK incorporates continuous integration (CI) and GitOps principles to manage the deployment of SUNK and Slurm clusters. This guide outlines the common strategies used for the SUNK project. It covers how to configure ArgoCD to synchronize `NodeSet` resources, how to structure a GitOps repository with Helm charts and values files for SUNK and Slurm, and how to apply an app of apps pattern so a single ArgoCD `Application` manages the full deployment.

Use this guide if you maintain a SUNK environment and want declarative, repeatable cluster deployments that align with GitOps practices.

## ArgoCD for application management

SUNK uses ArgoCD, a GitOps continuous delivery tool, to manage Kubernetes applications declaratively. ArgoCD provides a streamlined deployment workflow that aligns with the GitOps model. This automates the deployment process to maintain consistency across different environments.

ArgoCD defines two main applications:

* **SUNK Application**: Manages the deployment of the SUNK cluster, including all necessary configurations and dependencies.
* **Slurm Application**: Handles the Slurm cluster deployment to manage and schedule compute resources properly.

Additional supporting applications expand Slurm's capabilities and manage specific requirements, such as:

* Persistent Volume Claims (PVCs) for storage.
* [Prolog and Epilog scripts](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md) for preparing and cleaning up compute nodes before and after job execution.

## NodeSet sync customization

Update the ArgoCD configuration to sync `NodeSet` definitions. The resource customization feature lets ArgoCD sync the `NodeSet` spec in the same manner as `PodSpec`. Without this customization, ArgoCD doesn't process `NodeSet` fields correctly, which can cause drift between the desired and actual state of the cluster.

The method for applying configuration changes varies depending on the cluster's ArgoCD installation. The following sections describe two ways to apply the customization: edit the `argocd-cm` ConfigMap directly, or patch it with `kubectl`.

### Apply configuration changes with a ConfigMap patch

To apply configuration changes with a ConfigMap patch, edit the `data` section of the ConfigMap.

To open the `argocd-cm` ConfigMap for editing, use the following command, replacing `[NAMESPACE]` with the namespace where ArgoCD is installed:

```bash theme={"system"}
kubectl edit configmap argocd-cm -n [NAMESPACE]
```

> [!NOTE]
>
> The `kubectl edit` command opens the entire ConfigMap and sends the entire modified YAML back to the API server to replace the existing ConfigMap with your newly modified version.

In the `data` section of the ConfigMap, add the following key-value pairs:

```yaml theme={"system"}
resource.customizations.knownTypeFields.sunk.coreweave.com_NodeSet: |
  - field: spec.template.spec
    type: core/v1/PodSpec
```

### Apply configuration changes with kubectl

To apply configuration changes with `kubectl`, use the following command:

```bash theme={"system"}
kubectl patch configmap argocd-cm -n [NAMESPACE] --type=merge \
  -p '{"data":{"resource.customizations.knownTypeFields.sunk.coreweave.com_NodeSet": "- field: spec.template.spec\n  type: core/v1/PodSpec\n"}}'
```

> [!NOTE]
>
> The `kubectl patch` command only updates the specific resources you've modified and merges them with the existing resource.

The `-p '...'` flag specifies the patch content. This example uses the `data`, `- field`, and `type` parameters.

The `"data":{...}` parameter specifies the section of the ConfigMap to modify. The `kubectl patch` command only modifies the specified section.

`" - field: spec.template.spec\n"` and `type: core/v1/PodSpec\n` are the specific key-value pair to add to the ConfigMap.

The `--type=merge` flag specifies the patch type as a [JSON Merge Patch](https://datatracker.ietf.org/doc/html/rfc7386), which operates on the following logic:

* If a field exists in the patch, it replaces the existing field in the target object.
* If a field exists in the patch with a `null` value, it deletes the field from the target object.
* If a field does not exist in the patch, it remains unchanged in the target object.
* If you provide a list, it replaces the entire existing list with the one provided in the patch.

## Configuration in git (GitOps)

This section shows an example of how to keep a git repository synced to ArgoCD with Helm and the app of apps pattern. The following subsections walk through the Helm chart and values files for SUNK and Slurm, optional custom configurations, and the ArgoCD `Application` definitions that tie everything together.

Create a git repository with the contents described in the following sections.

### SUNK

The following sections describe the SUNK Helm chart and values file used to manage the SUNK deployment in your GitOps repository.

> [!NOTE]
>
> The SUNK and Slurm charts are licensed. Reach out to CoreWeave at
> [sunk@coreweave.com](mailto:sunk@coreweave.com) for access instructions, then substitute the repository
> URL you receive for `COREWEAVE_HELM_REPO_URL` below.

#### SUNK Helm chart

```yaml title="sunk/Chart.yaml" theme={"system"}
apiVersion: v2
name: sunk-gitops
version: 0.1.0
dependencies:
  - name: sunk
    version: 5.x.x
    repository: [COREWEAVE_HELM_REPO_URL]
```

#### SUNK values file

Use the [SUNK Values Reference](https://docs.coreweave.com/products/sunk/reference/sunk-parameters.md) to customize this file. The following shows an example `sunk/values.yaml`.

> [!WARNING]
>
> This file must have a top-level `sunk` key.

```yaml title="sunk/values.yaml" theme={"system"}
sunk:
  operator:
    logLevel: debug
    resources:
      limits:
        cpu: 1
        memory: 200Mi
      requests:
        cpu: 1
        memory: 200Mi
    podMonitor:
      enabled: false
    replicas: 1
    leaderElection:
      enabled: true
  scheduler:
    podMonitor:
      enabled: false
  syncer:
    podMonitor:
      enabled: false
```

### Slurm

The following sections describe the Slurm Helm chart and values file used to manage the Slurm deployment in your GitOps repository.

> [!NOTE]
>
> The SUNK and Slurm charts are licensed. Reach out to CoreWeave at
> [sunk@coreweave.com](mailto:sunk@coreweave.com) for access instructions, then substitute the repository
> URL you receive for `COREWEAVE_HELM_REPO_URL` below.

#### Slurm Helm chart

```yaml title="slurm/Chart.yaml" theme={"system"}
apiVersion: v2
name: slurm-gitops
version: 0.1.0
dependencies:
  - name: slurm
    version: 5.x.x
    repository: [COREWEAVE_HELM_REPO_URL]
```

#### Slurm values file

Use the [Slurm Values Reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) to customize this file. The following shows an example `slurm/values.yaml`.

> [!WARNING]
>
> This file must have a top-level `slurm` key.

```yaml title="slurm/values.yaml" theme={"system"}
slurm:
  accounting:
    priorityClassName: ""
    resources:
      requests:
        cpu: 100m
        memory: 100Mi
  controller:
    priorityClassName: ""
    resources:
      requests:
        cpu: 100m
        memory: 100Mi
  rest:
    enabled: false
    priorityClassName: ""
    resources:
      requests:
        cpu: 100m
        memory: 100Mi
  login:
    priorityClassName: ""
    resources:
      requests:
        cpu: 10m
        memory: 100Mi
  munge:
    priorityClassName: ""
    resources:
      requests:
        cpu: 1m
        memory: 20Mi
  syncer:
    priorityClassName: ""
    resources:
      requests:
        cpu: 100m
        memory: 50Mi
  scheduler:
    priorityClassName: ""
    enabled: true
    resources:
      requests:
        cpu: 100m
        memory: 50Mi
  mysql:
    metrics:
      enabled: false
    primary:
      resources:
        requests:
          cpu: 100m
          memory: 500Mi
    initdbScriptsConfigMap: "{{ .Release.Name }}-mysql-initdb-scripts"
  compute:
    nodes:
      cpu-epyc:
        enabled: true
        replicas: 2 # Adjust to desired amount or scale manually after deploy
        definitions:
          - standard
        features:
          - test
        resources:
          requests:
            cpu: 500m
            memory: 400Mi
        priorityClassName: ""
        # This is a toleration for a test taint that can be applied to the desired nodes to keep
        # other workloads off
        tolerations:
          - key: sunk.coreweave.com/nodes
            operator: "Exists"
        # affinity for a test label to filter nodes on, nodes need to be labeled with this or remove
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
                - matchExpressions:
                    - key: sunk.coreweave.com/nodes
                      operator: Exists
```

### Optional: Custom configurations

This section shows an example of how to define custom Slurm deployment configurations and keep them synchronized with ArgoCD.

#### Slurm controller config

Use the following ConfigMap to customize the Slurm controller configurations.

> [!WARNING]
>
> To use this ConfigMap, add its name to the `slurm.slurmConfig.slurmCtld.etcConfigMap` key in the [Slurm values file](#slurm-values-file).

```text title="slurm/templates/etc-slurmctld-configmap.yaml" theme={"system"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-etc-slurmctld
data:
{{ (.Files.Glob "scripts/etc-slurmctld/*").AsConfig | indent 2 }}
```

#### Prolog and Epilog

For more configuration options, see the [Slurm Values Reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) and [Prolog and Epilog Scripts](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md) pages.

> [!WARNING]
>
> To use these ConfigMaps, add them to the respective `slurm.compute.prologConfigMap` or `slurm.compute.epilogConfigMap` keys in the [Slurm values file](#slurm-values-file).

The following is an example of a prolog ConfigMap, `slurm/templates/prolog-configmap.yaml`:

```text title="slurm/templates/prolog-configmap.yaml" theme={"system"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-prolog
data:
{{ (.Files.Glob "scripts/prolog.d/*.sh").AsConfig | indent 2 }}
```

The following is an example of an Epilog ConfigMap, `slurm/templates/epilog-configmap.yaml`:

```text title="slurm/templates/epilog-configmap.yaml" theme={"system"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-epilog
data:
{{ (.Files.Glob "scripts/epilog.d/*.sh").AsConfig | indent 2 }}
```

The following is a simple example of an Epilog script, `slurm/scripts/epilog.d/test.sh`, to use with the preceding Epilog ConfigMap:

```bash title="slurm/scripts/epilog.d/test.sh" theme={"system"}
#!/usr/bin/env bash

set -e

echo "Epilog test executed"
```

### ArgoCD app of apps

This section shows an example of how to define multiple ArgoCD `Application` resources to manage SUNK and Slurm with the app of apps pattern and GitOps principles. The following subsections define the individual SUNK and Slurm `Application` resources, then a parent `Application` that references both.

#### SUNK app definition

The `apps/sunk.yaml` file describes where ArgoCD can find and synchronize the Helm manifests for SUNK. Replace the `[REPO-URL]` placeholder with your GitOps repository URL. Follow the [ArgoCD Specs](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/) for more customization options.

```yaml title="apps/sunk.yaml" theme={"system"}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sunk
spec:
  destination:
    namespace: sunk
    server: https://kubernetes.default.svc
  source:
    repoURL: [REPO-URL]
    path: sunk
    targetRevision: HEAD
    helm:
      valueFiles:
        - values.yaml
  sources: []
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

#### Slurm app definition

The `apps/slurm.yaml` file describes where ArgoCD can find and synchronize the Helm manifests for Slurm. Replace the `[REPO-URL]` placeholder with your GitOps repository URL. Follow the [ArgoCD Specs](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/) for more customization options.

> [!NOTE]
>
> The `spec.ignoreDifferences` key contains recommended values to keep ArgoCD synchronized.

```yaml title="apps/slurm.yaml" theme={"system"}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: slurm
spec:
  destination:
    namespace: tenant-slurm
    server: https://kubernetes.default.svc
  source:
    repoURL: [REPO-URL]
    path: slurm
    targetRevision: HEAD
    helm:
      valueFiles:
        - values.yaml
  sources: []
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
  ignoreDifferences:
    - group: sunk.coreweave.com
      kind: Nodeset
      namespace: tenant-slurm
      jqPathExpressions:
        - '.spec.template.spec.tolerations[] | select(.key == "node.coreweave.cloud/reservation-policy" or .key == "node.coreweave.cloud/reserved")'
```

#### App of apps definition

The `app-of-apps.yaml` file describes where ArgoCD can find and synchronize the custom Helm charts defined for SUNK and Slurm in the preceding sections. Replace the `[REPO-URL]` placeholder with your GitOps repository URL. Follow the [ArgoCD Specs](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/) for more customization options.

```yaml title="app-of-apps.yaml" theme={"system"}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sunk-app-of-apps
  namespace: argocd
spec:
  destination:
    namespace: 'argocd'
    server: https://kubernetes.default.svc
  source:
    repoURL: [REPO-URL]
    path: apps
    targetRevision: HEAD
  sources: []
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Apply to ArgoCD

After you follow the preceding steps, your GitOps repository should be structured as follows:

```text theme={"system"}
.
├── app-of-apps.yaml
├── apps
│  ├── slurm.yaml
│  └── sunk.yaml
├── slurm
│  ├── Chart.yaml
│  ├── scripts
│  │  └── prolog.d
│  │     └── test.sh
│  ├── templates
│  │  ├── epilog-configmap.yaml
│  │  ├── etc-slurmctld-configmap.yaml
│  │  └── prolog-configmap.yaml
│  └── values.yaml
└── sunk
   ├── Chart.yaml
   └── values.yaml
```

To apply all of the resources defined in the preceding sections, run the following command:

```bash theme={"system"}
# pwd: root dir of GitOps repo
kubectl apply -f app-of-apps.yaml
```

You can now keep SUNK and Slurm synchronized with ArgoCD following GitOps principles.

## Additional notes

The following sections describe behaviors and recommendations to understand when operating SUNK and Slurm under ArgoCD. They cover how syncs affect running jobs, how to handle login node updates, and the lifecycle of the secret jobs created by the Slurm chart.

### ArgoCD impact on Slurm jobs

ArgoCD syncs are job-safe. Syncing in Argo doesn't affect running jobs in the cluster. The `RollingUpdate` strategy updates compute nodes, and you can configure the maximum percentage of nodes unavailable during an update with `compute.maxUnavailable` in the chart values. See the [Slurm Values Reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for details.

### Login node updates

The login nodes might contain user states that you might not want to delete during an update. We recommend setting `login.updateStrategy` to `OnDelete` in this case. This requires you to manually delete the existing pod before creating the updated login node so the user state isn't deleted during a sync in ArgoCD. See the [Slurm Values Reference](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for details.

### Secret job lifecycle

On each sync, the Slurm chart schedules two Kubernetes Jobs to create the secrets the Slurm cluster needs to operate. When you install or upgrade, the chart replaces any existing jobs and initiates new job runs. If a job succeeds, an Argo hook deletes the Job object, and ArgoCD reports `In Sync` to indicate the job is complete. If a job fails, the Job object remains in Argo as `Failed` until you resolve the issue with the job run or the next sync occurs, which then follows this same process.
