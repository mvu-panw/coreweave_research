# Delete deployment

Source: https://docs.coreweave.com/products/inference/reference/api-overview/deploymentservice/delete-deployment

# Delete deployment

> Delete a CoreWeave inference deployment by its ID.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

A successful response returns the deleted deployment
object, including its final state at the moment of deletion.

```bash title="Example request" theme={"system"}
curl -X DELETE https://api.coreweave.com/v1alpha1/inference/deployments/{id} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml delete /v1alpha1/inference/deployments/{id}
openapi: 3.0.3
info:
  title: CoreWeave Inference API
  version: 0.0.1
  description: >-
    The CoreWeave Inference API provides programmatic control over inference
    gateways, model deployments, and capacity claims.
servers:
  - url: https://api.coreweave.com
    description: CoreWeave production API.
security:
  - bearerAuth: []
tags:
  - name: CapacityClaimService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting
      CapacityClaim reservations of GPU hardware for inference deployments.
  - name: DeploymentService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting model
      deployments. Each deployment associates a model with one or more gateways
      and configures runtime, resources, autoscaling, and traffic.
  - name: GatewayService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting inference
      gateways. Gateways provide authentication, request routing, load
      balancing, and traffic splitting for one or more deployments.
  - name: HotLoadService
    description: >-
      Endpoints for creating, listing, getting, and canceling checkpoint
      hot-loads. A hot-load loads a new set of model weights into a running
      deployment's replicas without restarting the inference processes or
      recreating the replicas.
paths:
  /v1alpha1/inference/deployments/{id}:
    delete:
      tags:
        - DeploymentService
      summary: Delete deployment
      description: Deletes a deployment by ID. Returns the deleted deployment.
      operationId: DeploymentService_DeleteDeployment
      parameters:
        - name: id
          in: path
          description: The ID of the deployment to delete
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteDeploymentResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    DeleteDeploymentResponse:
      description: Response for DeleteDeployment
      type: object
      properties:
        deployment:
          description: The deployment that was deleted
          allOf:
            - $ref: '#/components/schemas/Deployment'
          readOnly: true
    Status:
      description: >-
        Standard error response. `code` is a
        [`google.rpc.Code`](https://cloud.google.com/apis/design/errors#error_codes);
        `message` is human-readable English; `details` carries machine-readable
        error details when present.
      type: object
      properties:
        code:
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
          type: string
        details:
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    Deployment:
      description: Deployment object with specification and status fields
      type: object
      properties:
        spec:
          description: The specification of the deployment
          allOf:
            - $ref: '#/components/schemas/DeploymentSpec'
          readOnly: true
        status:
          description: The status of the deployment
          allOf:
            - $ref: '#/components/schemas/DeploymentStatus'
          readOnly: true
    GoogleProtobufAny:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    DeploymentSpec:
      description: DeploymentSpec object with configuration fields
      type: object
      properties:
        id:
          description: The ID of the deployment
          type: string
          readOnly: true
        name:
          description: The name of the deployment
          type: string
          readOnly: true
        gatewayIds:
          description: >-
            The IDs of the gateways the deployment is associated with. A
            deployment may be attached to multiple gateways; traffic from each
            gateway is routed by that gateway's strategy.
          type: array
          items:
            type: string
          readOnly: true
        runtime:
          description: >-
            Runtime selection and configuration. The available engines,
            versions, and per-engine config keys are returned by `GET
            /v1alpha1/inference/deployments/parameters`.
          allOf:
            - $ref: '#/components/schemas/DeploymentRuntime'
          readOnly: true
        resources:
          description: >-
            Resource configuration for the deployment. CPU and RAM are
            automatically assigned based on `gpuCount` for the chosen
            `instanceType`.
          allOf:
            - $ref: '#/components/schemas/DeploymentResources'
          readOnly: true
        model:
          description: >-
            The model configuration. The model is loaded from a path in a
            CoreWeave AI Object Storage (CAIOS) bucket.
          allOf:
            - $ref: '#/components/schemas/DeploymentModel'
          readOnly: true
        autoscaling:
          description: >-
            Autoscaling configuration. CoreWeave manages scaling within the
            configured `min` and `max` bounds; scale-to-zero is not supported.
          allOf:
            - $ref: '#/components/schemas/DeploymentAutoscaling'
          readOnly: true
        traffic:
          description: >-
            Traffic configuration for the deployment. When multiple deployments
            share a model name on the same gateway, `traffic.weight` controls
            the share of traffic each deployment receives.
          allOf:
            - $ref: '#/components/schemas/DeploymentTraffic'
          readOnly: true
        organizationId:
          description: The organization ID that owns the deployment.
          type: string
          readOnly: true
        disabled:
          description: >-
            When `true`, the deployment does not receive traffic and is not
            scaled.
          type: boolean
          readOnly: true
        hotLoad:
          description: The hot-load configuration for the deployment
          allOf:
            - $ref: '#/components/schemas/DeploymentHotLoad'
          readOnly: true
        pd:
          description: >-
            Prefill/Decode disaggregation configuration. When set, the
            deployment renders two worker
             pools — prefill (compute-bound, sized on TTFT) and decode (memory-bound, sized on
             concurrent streams) — with NIXL/RDMA KV transfer between them. Top-level `resources` and
             `autoscaling` describe the DECODE pool; `pd.prefill_*` describes the PREFILL pool. Only
             valid when runtime.engine = "dynamo-vllm" and the pdDisaggEnabled feature flag is on.
          allOf:
            - $ref: '#/components/schemas/DeploymentPD'
          readOnly: true
    DeploymentStatus:
      description: DeploymentStatus object for status fields
      type: object
      properties:
        createdAt:
          description: The time at which the deployment was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time at which the deployment was last updated.
          type: string
          format: date-time
          readOnly: true
        status:
          description: >-
            The overall status of the deployment. `STATUS_UNSPECIFIED` means the
            status has not been set. See the [Inference API
            overview](https://docs.coreweave.com/products/inference/reference/api-overview#status-values)
            for the meaning of each value.
          type: string
          format: enum
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_CREATING
            - STATUS_UPDATING
            - STATUS_DELETING
            - STATUS_ERROR
            - STATUS_FAILED
            - STATUS_READY
          readOnly: true
        conditions:
          description: List of conditions representing detailed status information
          type: array
          items:
            $ref: '#/components/schemas/Condition'
          readOnly: true
        specRevision:
          description: >-
            The revision of the deployment specification. It increases when the
            configuration changes.
          type: string
          readOnly: true
    DeploymentRuntime:
      description: Runtime selection and configuration for deployments
      type: object
      properties:
        engine:
          description: >-
            The inference engine to use (for example, `vllm`). The available
            engines are returned by `GET
            /v1alpha1/inference/deployments/parameters`.
          type: string
        version:
          description: >-
            The version of the engine. Required. Must be one of the engine's
            available versions returned by the parameters endpoint.
          type: string
        engineConfig:
          description: >-
            Engine-specific configuration arguments. The parameters endpoint
            returns the allowed keys for each engine and version in
            `runtimeParameters.runtimeEngineOptions[engine].versions[version].configOptions`.
          type: object
          additionalProperties:
            type: string
        engineEnv:
          description: >-
            Map of engine-specific environment variables to inject into the
            model runtime container
          type: object
          additionalProperties:
            type: string
      required:
        - engine
        - version
    DeploymentResources:
      description: Resource configuration for the deployment
      type: object
      properties:
        instanceType:
          description: >-
            The instance type to use for the deployment. The available values
            are returned by `GET /v1alpha1/inference/deployments/parameters`.
          type: string
        gpuCount:
          description: >-
            Number of GPUs needed per instance. CPU and RAM are automatically
            assigned based on the chosen GPU count.
          type: integer
          format: uint32
      required:
        - instanceType
        - gpuCount
    DeploymentModel:
      description: Configuration of the model
      type: object
      properties:
        name:
          description: >-
            The model name used in inference requests (and returned by the
            gateway's `/models` endpoint). When multiple deployments on the same
            gateway share a name, traffic is split between them by
            `traffic.weight`.
          type: string
        bucket:
          description: >-
            The CoreWeave AI Object Storage (CAIOS) bucket the model is stored
            in.
          type: string
        path:
          description: The path within `bucket` to the model and its configuration files.
          type: string
      required:
        - name
        - bucket
        - path
    DeploymentAutoscaling:
      description: Autoscaling configuration for the deployment
      type: object
      properties:
        min:
          description: >-
            The minimum number of replicas. Must be at least `1`; scale-to-zero
            is not supported.
          type: integer
          format: uint32
        max:
          description: >-
            The maximum number of replicas. Must be greater than or equal to
            `min`. Set equal to `min` to disable autoscaling.
          type: integer
          format: uint32
        priority:
          description: >-
            Scaling priority relative to other deployments, from `0` to `1000`.
            Higher values receive scaling preference during resource contention.
          type: integer
          format: uint32
        capacityClasses:
          description: >-
            The capacity classes the autoscaler may use for this deployment. Set
            `CAPACITY_CLASS_RESERVED` to schedule replicas onto capacity
            reserved by a CapacityClaim; set `CAPACITY_CLASS_ON_DEMAND` to use
            shared on-demand capacity. Omit the zero value
            `CAPACITY_CLASS_UNSPECIFIED` rather than sending it.
          type: array
          items:
            type: string
            format: enum
            enum:
              - CAPACITY_CLASS_RESERVED
              - CAPACITY_CLASS_ON_DEMAND
        concurrency:
          description: >-
            Target concurrent requests per replica. Lower values reduce latency;
            higher values increase throughput. Must be at least `1`.
          type: integer
          format: uint32
        claims:
          description: >-
            Optional `CapacityClaim` IDs to use for reserved capacity, in
            preference order. If omitted, any available reserved capacity may be
            used. Replace released or deleted claims because they no longer
            provide reserved capacity.
          type: array
          items:
            type: string
      required:
        - min
        - max
    DeploymentTraffic:
      description: Configuration for traffic control to the deployment
      type: object
      properties:
        weight:
          description: >-
            The relative weight of traffic routed to this deployment compared to
            other deployments with the same model name on the same gateway.
            Weights are normalized into percentages.
          type: integer
          format: uint32
    DeploymentHotLoad:
      description: >-
        DeploymentHotLoad configures checkpoint hot-loading for the deployment.
        Set it at deployment creation to enable
         hot-loading, or omit it to disable hot-loading. This configuration cannot be changed after creation.
      type: object
      properties:
        bucket:
          description: The CoreWeave Object Storage bucket that holds checkpoint snapshots
          type: string
        pathPrefix:
          description: >-
            The path prefix within the bucket that holds checkpoint snapshots.
            Append the snapshot identity to this
             prefix to locate the snapshot's weights and metadata.
             Example: with bucket "my-model" and path_prefix "my-checkpoints", the weights and metadata of the
             snapshot with identity "weight_v001" should live under "s3://my-model/my-checkpoints/weight_v001/"
          type: string
        transitionMode:
          description: >-
            How requests are handled while a checkpoint swap is in progress on a
            replica. `TRANSITION_MODE_ASYNC` pauses in-flight requests and
            resumes them after the swap, and queues new requests until the swap
            completes. This field is required, and `TRANSITION_MODE_ASYNC` is
            the only accepted value.
          type: string
          format: enum
          enum:
            - TRANSITION_MODE_ASYNC
      required:
        - bucket
        - transitionMode
    DeploymentPD:
      description: >-
        DeploymentPD carries per-pool configuration for prefill/decode
        disaggregated serving. The
         decode pool is described by the enclosing DeploymentSpec's top-level `resources` and
         `autoscaling` fields; DeploymentPD contributes the prefill-pool overrides.
      type: object
      properties:
        prefillResources:
          description: Resource configuration for the prefill worker pool
          allOf:
            - $ref: '#/components/schemas/DeploymentResources'
        prefillAutoscaling:
          description: >-
            Autoscaling configuration for the prefill worker pool.
            Deployment-wide priority is inherited
             from the top-level autoscaling configuration and is therefore not repeated here.
          allOf:
            - $ref: '#/components/schemas/DeploymentPDPoolAutoscaling'
      required:
        - prefillResources
        - prefillAutoscaling
    Condition:
      description: Condition represents a detailed status condition for resources
      type: object
      properties:
        type:
          description: Type of condition
          type: string
          readOnly: true
        status:
          description: >-
            The status of the condition: `STATUS_TRUE` or `STATUS_FALSE`, or
            `STATUS_UNSPECIFIED` when the status has not been set.
          type: string
          format: enum
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_FALSE
            - STATUS_TRUE
          readOnly: true
        lastUpdateTime:
          description: Last time the condition was updated
          type: string
          format: date-time
          readOnly: true
        reason:
          description: Reason for the condition's last transition
          type: string
          readOnly: true
        message:
          description: Human-readable message indicating details about the condition
          type: string
          readOnly: true
        zone:
          description: Zone associated with the condition
          type: string
          readOnly: true
    DeploymentPDPoolAutoscaling:
      description: >-
        Autoscaling configuration for a worker pool in a
        Prefill/Decode-disaggregated deployment.
         Deployment-wide settings such as priority remain on DeploymentSpec.autoscaling.
      type: object
      properties:
        min:
          description: >-
            The minimum number of instances to scale down to, scale to zero is
            not supported
          type: integer
          format: uint32
        max:
          description: >-
            The maximum number of instances to scale up to, setting equal to min
            disables autoscaling
          type: integer
          format: uint32
        capacityClasses:
          description: >-
            The capacity classes the autoscaler may use for the prefill worker
            pool. Set `CAPACITY_CLASS_RESERVED` to schedule replicas onto
            capacity reserved by a CapacityClaim; set `CAPACITY_CLASS_ON_DEMAND`
            to use shared on-demand capacity. Omit the zero value
            `CAPACITY_CLASS_UNSPECIFIED` rather than sending it; the API rejects
            it.
          type: array
          items:
            type: string
            format: enum
            enum:
              - CAPACITY_CLASS_RESERVED
              - CAPACITY_CLASS_ON_DEMAND
        concurrency:
          description: >-
            The concurrency per instance to target/limit, used to control
            latency vs throughput tradeoffs
          type: integer
          format: uint32
        claims:
          description: >-
            Optional `CapacityClaim` IDs to use for reserved capacity, in
            preference order. If omitted, any available reserved capacity may be
            used. Replace released or deleted claims because they no longer
            provide reserved capacity.
          type: array
          items:
            type: string
      required:
        - min
        - max
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
