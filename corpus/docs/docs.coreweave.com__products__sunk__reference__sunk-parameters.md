# SUNK parameter reference

Source: https://docs.coreweave.com/products/sunk/reference/sunk-parameters

# SUNK parameter reference

> Complete parameter reference for the SUNK operator Helm chart, including image, MySQL, and NVIDIA plugin settings

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

## Requirements

| Repository | Name | Version |
| - | - | - |
| [https://cybozu-go.github.io/moco/](https://cybozu-go.github.io/moco/) | moco | 0.25.0 |
| oci://ghcr.io/coreweave/k8s-device-plugin/charts | nvidia-device-plugin | 0.17.0-5c8a50df |

## Parameters

<table>
  <thead>
    <th>Key & Description</th>
    <th>Type</th>
    <th>Default</th>
  </thead>

  <tbody>
    <tr>
      <td id="imagePullSecrets">
        **imagePullSecrets**\

        Image pull secrets to configure if using custom private images.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="moco">
        **moco**\

        Options for the MOCO MySQL Operator.
      </td>

      <td>object</td>
      <td>See individual settings below.</td>
    </tr>

    <tr>
      <td id="moco--enabled">
        **moco.enabled**\

        Enable the MOCO MySQL Operator.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--image--repository">
        **moco.image.repository**\

        The repository for the MOCO image.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "ghcr.io/cybozu-go/moco"
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--image--tag">
        **moco.image.tag**\

        The tag for the MOCO image.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--imagePullSecrets">
        **moco.imagePullSecrets**\

        Image pull secrets to configure if using custom private images.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--monitoring--podMonitors--enabled">
        **moco.monitoring.podMonitors.enabled**\

        Enable monitoring via the Prometheus operator `PodMonitor` CRD
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--monitoring--vmPodScrapes--enabled">
        **moco.monitoring.vmPodScrapes.enabled**\

        Enable monitoring via the VictoriaMetrics operator `VMPodScrape` CRD
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--priorityClassName">
        **moco.priorityClassName**\

        The priority class name for the MOCO pod.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "sunk-control-plane"
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--replicaCount">
        **moco.replicaCount**\

        The number of replicas of the MOCO instance to run.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="moco--resources">
        **moco.resources**\

        Resources for the MOCO container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits:
            memory: 4Gi
        requests:
            cpu: 100m
            memory: 256Mi

        ```
      </td>
    </tr>

    <tr>
      <td id="nvidia-device-plugin">
        **nvidia-device-plugin**\

        Options for [ the Coreweave fork of the Nvidia device plugin chart](https://github.com/coreweave/k8s-device-plugin/tree/coreweave/deployments/helm/nvidia-device-plugin). This chart builds on the default configuration provided by Nvidia, and uses these [default chart values](https://github.com/coreweave/k8s-device-plugin/tree/coreweave/deployments/helm/nvidia-device-plugin/values.yaml).
      </td>

      <td>object</td>
      <td>See default chart values.</td>
    </tr>

    <tr>
      <td id="operator--affinity">
        **operator.affinity**\

        The affinity for the operator deployment.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                    - matchExpressions:
                        - key: node.coreweave.cloud/class
                          operator: In
                          values:
                            - cpu

        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--failedPodsBackoffGCInterval">
        **operator.config.operator.nodeSet.failedPodsBackoffGCInterval**\

        The time that has to pass before next iteration of backoff GC is run for checking failed pods.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "1m"
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--forceScalingDeleteKnownConditionTimeout">
        **operator.config.operator.nodeSet.forceScalingDeleteKnownConditionTimeout**\

        The delay to wait before deleting a pod during nodeset scaling with a known Slurm state. "0" disables this feature.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        0
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--forceScalingDeleteUnknownConditionTimeout">
        **operator.config.operator.nodeSet.forceScalingDeleteUnknownConditionTimeout**\

        The delay to wait before deleting a pod during nodeset scaling with a unknown Slurm state. "0" disables this feature.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        0
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--maxBurstReplicas">
        **operator.config.operator.nodeSet.maxBurstReplicas**\

        A rate limiter for booting pods when there are a lot of pods. A too high of a value can cause registry DoS issues.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        250
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--scaleDownPriorityOrdering">
        **operator.config.operator.nodeSet.scaleDownPriorityOrdering**\

        Enable priority ordering for scale down. This ensures the following deletion order non-ready pods, drained pods without running workloads, idle pods, draining pods with running workloads, then running pods.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSet--statusUpdateBackoffGCInterval">
        **operator.config.operator.nodeSet.statusUpdateBackoffGCInterval**\

        The time that has to pass before next iteration of backoff GC is run for checking node status updates.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "1m"
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--config--operator--nodeSlice--maxNodesPerNodeSlice">
        **operator.config.operator.nodeSlice.maxNodesPerNodeSlice**\

        The maximum number of nodes that can be in a single nodeSlice.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        100
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--image">
        **operator.image**\

        The image to use for the operator. When repository is empty it defaults to images.coreweave.com/cluster-images/sunk/operator. When tag is empty it defaults to the chart appVersion.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="operator--leaderElection--enabled">
        **operator.leaderElection.enabled**\

        This forces the operator to use leader election even if the number of replicas is set to 1. \
        &#x20;Useful if planning to scale after deployment.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--leaderElection--leaderElectionID">
        **operator.leaderElection.leaderElectionID**\

        The string value to use as the leader election id.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--logLevel">
        **operator.logLevel**\

        The log level. \
        &#x20;Uses integers or [zap log level strings](https://pkg.go.dev/go.uber.org/zap#pkg-constants): <ul> <li>`debug`</li> <li>`info`</li> <li>`warn`</li> <li>`error`</li> <li>`dpanic`</li> <li>`panic`</li> <li>`fatal`</li> </ul>
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "info"
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--maxConcurrentReconciles">
        **operator.maxConcurrentReconciles**\

      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        50
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--priorityClassName">
        **operator.priorityClassName**\

        The priority class name for the operator.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "sunk-control-plane"
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--replicas">
        **operator.replicas**\

        The number of replicas of the operator pod to run. \
        &#x20;Leader election will be enabled if this is greater than 1 or leader election is explicitly enabled.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="operator--resources">
        **operator.resources**\

        The resource to request for the operator.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits:
            cpu: 16
            memory: 32Gi
        requests:
            cpu: 8
            memory: 32Gi

        ```
      </td>
    </tr>

    <tr>
      <td id="operator--tolerations">
        **operator.tolerations**\

        The tolerations for the operator deployment.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="priorityClass--enabled">
        **priorityClass.enabled**\

        Enable the priority class for the control plane components.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="priorityClass--value">
        **priorityClass.value**\

        The value of the priority class, generally should be high relative to other priority classes as these are critical components.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1000000000
        ```
      </td>
    </tr>
  </tbody>
</table>
