# Node lifecycle

Source: https://docs.coreweave.com/platform/fleet-management/node-lifecycle

# Node lifecycle

> CoreWeave's full Node lifecycle management from Day 0 initialization through Day 2+ ongoing operations

Managing specialized infrastructure at CoreWeave's scale is complex. It requires automation to set up infrastructure, validate Nodes before deployment, tune their performance, and oversee their operation throughout their lifecycle.

CoreWeave Nodes operate as stateless entities, without any local data storage. When they boot, the Nodes require programming to get their specific configurations. CoreWeave automation applies these configurations and also identifies and resolves issues before they impact customers.

> [!NOTE]
>
> [Learn why Node lifecycle management is critical for AI applications](https://www.coreweave.com/blog/what-is-node-lifecycle-management-ml-training-and-inference) in our interview with Navarre Pratt, a Solutions Architect at CoreWeave.

CoreWeave manages and optimizes the full lifecycle of each Node, from Day 0 to Day 2 and beyond:

* **Day 0**: Initial configuration of a new Node at power-on.
* **Day 1**: Preparation of the Node for entry into the production fleet.
* **Day 2+**: Continual assurance that the production fleet always operates within set specifications.

The following sections describe each phase at a high level. Each Day 1 and Day 2+ section links to a dedicated page for deeper detail.

CoreWeave's automation across the lifecycle minimizes the time to bring new Nodes into the production fleet, improves the reliability of the Nodes in a fleet, and reduces the disruption and downtime to the fleet if and when a Node fails.

## Day 0: Initialization

Day 0 (The phase in the lifecycle of a CoreWeave Node where it is initially configured after powering on.) is when CoreWeave executes all the necessary initialization steps to prepare the Node for Day 1 activities.

After a Node powers on, the Node enters CoreWeave's management cluster where it receives configuration details such as its boot image and network setup.
It also fetches cloud-init data, including the Kubernetes API server's IP address and the Node's join token.
When complete, the Node automatically transitions to the **Onboard** state.

## Day 1: Preparation for production

Day 1 (The phase in the lifecycle of a CoreWeave Node where it is intensively validated before delivery to a customer.) is the pre-production phase, where CoreWeave automatically moves Nodes through a series of stages including firmware updates, validation testing, cable verification, and reliability assessments. This process ensures each Node meets CoreWeave's standards for performance and reliability before it joins the production fleet.

[Learn more about Day 1 validation automation](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day1.md).

## Day 2+: Continuous production monitoring

Day 2+ (The phase in the lifecycle of a CoreWeave Node once it has been delivered to a customer, and is continuously monitored and validated by CoreWeave.) is the period when a Node is in production and available to you. CoreWeave continuously verifies that Nodes operate within set specifications, combining active HPC Verification tests, passive monitoring, and automated InfiniBand validation to keep fleets reliable and performant.

[Learn more about Day 2+ validation automation](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md).

## Non-CoreWeave-managed Nodes

This section describes which lifecycle automation and validation services are available for Nodes that aren't managed by CoreWeave's Kubernetes services.

For Nodes not running CKS (CoreWeave Kubernetes Service (CKS) is CoreWeave's managed Kubernetes service.) or SUNK, CoreWeave's lifecycle automation and validation services offer these features:

* **Node lifecycle management**: Initial onboarding and the Zap process are available at first delivery.
  This includes automatic upgrades and configurations for various components such as BMC, BIOS, HMC, and GPUs.
  However, upgrades for InfiniBand HCA aren't supported.
* **Passive InfiniBand fault detection**: The system monitors InfiniBand fabric events, transceiver status, and fabric and Node topology.
  Node link flap events are tracked, but automatic lifecycle actions in response to these detections aren't performed.
* **InfiniBand layout and connectivity checks**: Validation for InfiniBand fabric, including leaf-to-Node cabling and topology integrity, is supported.
* **Manual InfiniBand connectivity validation**: CoreWeave also performs manual, weekly validation checks to confirm continuous InfiniBand connectivity and performance.

These services ensure that Nodes outside the CoreWeave-managed ecosystem benefit from lifecycle and connectivity validations.
