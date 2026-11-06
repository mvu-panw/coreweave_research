# Pod Controller

Source: https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller

# Pod Controller

> How the SUNK Pod Controller synchronizes data from Kubernetes Nodes to Pods for cordon and lock state

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The Pod Controller is responsible for managing data synchronized to the Pods from the Kubernetes Nodes. The Pod Controller is deployed cluster-wide as part of the `sunk-controller-manager`, and performs operations that are not specifically tied to an instance of a Slurm cluster. In contrast, the [Syncer](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) performs synchronization of information between Pods and an associated Slurm cluster instance.

## Information flow and operations

The Pod Controller handles the flow of information from the Nodes to the Pods. The following sections describe some possible information flows.

### Node cordon

When a Node is marked as unschedulable, the Pod Controller propagates this information through an annotation to the respective `slurmd` Pod.

The Pod Controller extracts the reason from the Node annotation `node.coreweave.cloud/cordonReason`.

### Node lock

The [Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md#node-lock) handles most of the logic for the lock operation. The Pod Controller is only responsible for copying the lock annotation, `sunk.coreweave.com/lock`, from the associated Node to the Pod.

### Features

The Pod Controller is responsible for propagating the defined NodeSet features to the Pod. When you change the feature spec or, in the case of dynamic features, the feature values change, the Pod Controller updates the feature annotations on the Pod. The Syncer uses these annotations to propagate the features onto the Slurm nodes.

The features are specified in the NodeSet spec:

```yaml theme={"system"}
spec:
  features:
    staticFeatures:
      - example
    dynamicFeatures:
      gpu.nvidia.com/class: {}
      gpu.coreweave.cloud/driver-version:
        prefix: "driver-"
```

`staticFeatures` and `dynamicFeatures` are feature strings applied to the Slurm nodes.

`staticFeatures` is a list of feature strings updated through the NodeSet spec.

`dynamicFeatures` is a map where the key is a reference to the Node label, which contains the feature string. The value contains the additional configuration options for the feature. The Pod Controller updates this feature string either from changes to the NodeSet spec or when the labels on the associated Node change.

The Pod Controller creates two annotations on the Pod to reflect these feature lists:

* `sunk.coreweave.com/dynamic-features`
* `sunk.coreweave.com/static-features`

The lists are sorted, deduplicated, and comma-separated.

### Conditions

The Pod Controller copies a select set of conditions from the associated Node to the Pod and keeps them updated on changes. These conditions facilitate the propagation of Node information into Slurm later through the Syncer.
