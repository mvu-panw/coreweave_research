# Create capacity claim

Source: https://docs.coreweave.com/products/inference/reference/api-overview/capacityclaimservice/create-capacity-claim

# Create capacity claim

> Reserve GPU instances for inference deployments via a new CapacityClaim.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Reserves the requested number of `instanceId`-typed instances
across the listed `zones`. The order of `zones` implies an
allocation preference: earlier entries are preferred. The
available `instanceId` values per zone are returned by
`GET /v1alpha1/inference/capacityclaims/parameters`.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1alpha1/inference/capacityclaims \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml post /v1alpha1/inference/capacityclaims
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
  /v1alpha1/inference/capacityclaims:
    post:
      tags:
        - CapacityClaimService
      summary: Create capacity claim
      description: >-
        Creates a new CapacityClaim that reserves GPU hardware for inference
        deployments.
      operationId: CapacityClaimService_CreateCapacityClaim
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateCapacityClaimRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateCapacityClaimResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    CreateCapacityClaimRequest:
      description: Request to create a CapacityClaim
      type: object
      properties:
        id:
          description: The unique identifier of the CapacityClaim, UUID format
          type: string
        name:
          description: The human readable name of the CapacityClaim
          type: string
        resources:
          description: The specification for the resources to reserve
          allOf:
            - $ref: '#/components/schemas/CapacityClaimResources'
      required:
        - resources
    CreateCapacityClaimResponse:
      description: Response for CreateCapacityClaim
      type: object
      properties:
        capacityClaim:
          description: The created CapacityClaim
          allOf:
            - $ref: '#/components/schemas/CapacityClaim'
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
    CapacityClaimResources:
      description: Resources to reserve within a CapacityClaim
      type: object
      properties:
        instanceId:
          description: >-
            The instance type to reserve, by ID specifier (for example,
            `gb200-4x`). Identifiers are case-sensitive and must use the
            lowercase form. Must be a valid instance type within at least one of
            the specified `zones`.
          type: string
        instanceCount:
          description: The number of instances to reserve.
          type: integer
          format: uint32
        capacityType:
          description: >-
            The capacity type for the CapacityClaim. `CAPACITY_TYPE_MANAGED`
            reserves instances from CoreWeave's managed capacity pool and is the
            only value accepted when creating or updating a claim.
            `CAPACITY_TYPE_CUSTOMER` is deprecated; it is not accepted on create
            or update, but can still appear when reading older claims. This
            field cannot be changed after the claim is created.
          type: string
          format: enum
          enum:
            - CAPACITY_TYPE_CUSTOMER
            - CAPACITY_TYPE_MANAGED
        zones:
          description: >-
            The Availability Zones the CapacityClaim may use resources from.
            Zone identifiers are case-sensitive and must use the uppercase
            canonical form (for example, `US-WEST-04A`). The order of `zones`
            implies an allocation preference; earlier entries are preferred.
          type: array
          items:
            type: string
      required:
        - instanceId
        - instanceCount
        - capacityType
        - zones
    CapacityClaim:
      description: CapacityClaim object with specification and status fields
      type: object
      properties:
        spec:
          description: The specification of the CapacityClaim
          allOf:
            - $ref: '#/components/schemas/CapacityClaimSpec'
          readOnly: true
        status:
          description: The status of the CapacityClaim
          allOf:
            - $ref: '#/components/schemas/CapacityClaimStatus'
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
    CapacityClaimSpec:
      description: CapacityClaimSpec contains the specification for a CapacityClaim
      type: object
      properties:
        id:
          description: The unique identifier of the CapacityClaim, UUID format
          type: string
          readOnly: true
        name:
          description: The human readable name of the CapacityClaim
          type: string
          readOnly: true
        resources:
          description: The specification for the resources to reserve
          allOf:
            - $ref: '#/components/schemas/CapacityClaimResources'
          readOnly: true
        organizationId:
          description: The organization ID that owns the CapacityClaim
          type: string
          readOnly: true
    CapacityClaimStatus:
      description: CapacityClaimStatus contains the status fields for a CapacityClaim
      type: object
      properties:
        createdAt:
          description: The time at which the CapacityClaim was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time at which the CapacityClaim was last updated.
          type: string
          format: date-time
          readOnly: true
        status:
          description: >-
            The overall status of the CapacityClaim. `STATUS_UNSPECIFIED` means
            the status has not been set. See the [Inference API
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
        allocatedInstances:
          description: The number of instances currently allocated and available.
          type: integer
          format: uint32
          readOnly: true
        pendingInstances:
          description: >-
            The number of instances being provisioned to fulfill the capacity
            claim.
          type: integer
          format: uint32
          readOnly: true
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
