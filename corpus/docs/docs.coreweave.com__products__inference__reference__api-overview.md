# Dedicated Inference API reference

Source: https://docs.coreweave.com/products/inference/reference/api-overview

# Dedicated Inference API reference

> Authentication, protocols, status values, and error formats for the Dedicated Inference API

The Dedicated Inference API, published as the CoreWeave Inference API, provides programmatic control over inference [gateways](https://docs.coreweave.com/products/inference/gateways.md), model [deployments](https://docs.coreweave.com/products/inference/models.md), [capacity claims](https://docs.coreweave.com/products/inference/scaling.md#capacity-claims), and checkpoint hot-loads for RL Rollouts. The API is available at `api.coreweave.com`.

> [!NOTE]
>
> This API manages Dedicated Inference resources. To call catalog models or LoRA adapters hosted by Serverless Inference, see the [Serverless Inference API reference](https://docs.coreweave.com/products/inference/serverless/api-reference.md). To compare Serverless Inference, Dedicated Inference, and Inference on CKS, see [About CoreWeave Inference](https://docs.coreweave.com/products/inference.md#choose-a-deployment-option).

This page covers cross-cutting topics: authentication, protocols, status values, error formats, and the OpenAI-compatible inference endpoint. For per-endpoint request and response schemas, see the per-operation pages under each service in the left sidebar:

* [CapacityClaimService](https://docs.coreweave.com/products/inference/reference/api-overview/capacityclaimservice/list-capacity-claims.md)
* [DeploymentService](https://docs.coreweave.com/products/inference/reference/api-overview/deploymentservice/list-deployments.md)
* [GatewayService](https://docs.coreweave.com/products/inference/reference/api-overview/gatewayservice/list-gateways.md)

> [!NOTE]
>
> The Dedicated Inference API is versioned as `v1alpha1`. APIs may change before general availability.

## Authentication

The Dedicated Inference API uses bearer token authentication to identify the caller and authorize each request. All API requests must include a CoreWeave API access token in the `Authorization` header as a Bearer token. The token must belong to a user with the [Inference Viewer or Inference Admin role](https://docs.coreweave.com/security/iam/access-policies.md), depending on the operation.

Replace `[API-TOKEN]` with your CoreWeave API access token.

```bash theme={"system"}
curl "https://api.coreweave.com/v1alpha1/inference/gateways" \
  -H "Authorization: Bearer [API-TOKEN]"
```

For details on obtaining an API token, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

## Protocol support

You can call the Dedicated Inference API over several transport protocols, depending on your client tooling and performance needs:

| Protocol | Description |
| - | - |
| REST/JSON | Standard HTTP/1.1 with JSON request and response bodies. All examples in this documentation use REST. |
| gRPC | Protocol buffers over HTTP/2 for high-performance programmatic access. |
| Connect | gRPC-compatible protocol with improved browser and HTTP/1.1 support. |

## Schema and SDKs

The Dedicated Inference API is defined in Protobuf and published to CoreWeave's public Buf Schema Registry, so you can install a generated client instead of writing HTTP calls by hand.

* **Public BSR module**: [buf.build/coreweave/inference](https://buf.build/coreweave/inference) (module name `buf.build/coreweave/inference`).
* **Generated SDKs**: [Inference SDKs on the Buf Schema Registry](https://buf.build/coreweave/inference/sdks/main%3Aconnectrpc). Clients are available for the Connect, gRPC, and Protobuf ecosystems across languages including Go, Python, TypeScript, Java, Kotlin, Rust, and Swift.
* **Services**: `GatewayService`, `DeploymentService`, `CapacityClaimService`, and `HotLoadService` (package `coreweave.inference.v1alpha1`).

Select an ecosystem and language on the Buf Schema Registry to get the install command for your package manager. Generated clients target the same API host and Bearer token authentication described in [Authentication](#authentication).

> [!NOTE]
>
> Generated clients cover the Dedicated Inference API, which is what you use to create and manage gateways, deployments, capacity claims, and hot-loads. To send inference requests to a deployed model, use any OpenAI-compatible client against your gateway endpoint. See [OpenAI-compatible endpoint](#openai-compatible-endpoint).

## Query parameters

List endpoints support the following query parameter:

| Parameter | Type | Description |
| - | - | - |
| `updatedAfter` | `date-time` | Filter resources to those updated after the specified timestamp (ISO 8601 format). |

## Status values

Use these status values to determine the lifecycle state of a resource when polling or reconciling state in your application. All resources share a common set of status values:

| Status | Description |
| - | - |
| `STATUS_UNSPECIFIED` | Status has not been set. |
| `STATUS_CREATING` | Resource is being provisioned. |
| `STATUS_READY` | Resource is active and operational. |
| `STATUS_UPDATING` | Resource configuration is being updated. |
| `STATUS_DELETING` | Resource is being removed. |
| `STATUS_ERROR` | Resource has an error that isn't terminal. Either CoreWeave temporarily couldn't check the resource's readiness, which clears on its own, or a deployment that runs only on reserved capacity has none allocated in its zone, which clears once capacity is allocated. Check `status.conditions` for the cause. |
| `STATUS_FAILED` | Resource encountered a terminal error. |

Each resource includes a `conditions` array in its status with detailed information about the current state, including timestamps, reasons, and human-readable messages. Each condition's `status` field is `STATUS_TRUE`, `STATUS_FALSE`, or `STATUS_UNSPECIFIED` when it has not been set.

## Error responses

When a request fails, the API returns a structured error body that your client can parse to surface details to users or trigger retries. Error responses follow the standard format:

```json theme={"system"}
{
  "code": 400,
  "message": "name is required",
  "details": []
}
```

## OpenAI-compatible endpoint

Deployed models expose an OpenAI-compatible completions endpoint through their associated gateway. The endpoint URL depends on the gateway's routing strategy. See [Gateways](https://docs.coreweave.com/products/inference/gateways.md#routing-strategies) for details on how each routing strategy constructs the request URL.

For a complete walkthrough, see the [Getting started](https://docs.coreweave.com/products/inference/getting-started.md) guide.

## OpenAPI specification

The complete OpenAPI 3.0 specification for the Dedicated Inference API is embedded below. Expand the code block by clicking "See all" at the bottom, or use the download and copy buttons in the title bar.

```yaml expandable title="Inference OpenAPI" theme={"system"}
openapi: 3.0.3
info:
  title: CoreWeave Inference API
  version: 0.0.1
  description: The CoreWeave Inference API provides programmatic control over inference gateways, model
    deployments, and capacity claims.
servers:
- url: https://api.coreweave.com
  description: CoreWeave production API.
paths:
  /v1alpha1/inference/capacityclaims:
    get:
      operationId: CapacityClaimService_ListCapacityClaims
      summary: List capacity claims
      description: Returns every CapacityClaim that the caller can read.
      parameters:
      - name: updatedAfter
        in: query
        description: Filter by those updated after this timestamp
        schema:
          type: string
          format: date-time
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListCapacityClaimsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CapacityClaimService
    post:
      operationId: CapacityClaimService_CreateCapacityClaim
      summary: Create capacity claim
      description: Creates a new CapacityClaim that reserves GPU hardware for inference deployments.
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
      tags:
      - CapacityClaimService
  /v1alpha1/inference/capacityclaims/parameters:
    get:
      operationId: CapacityClaimService_GetCapacityClaimParameters
      summary: Get capacity claim parameters
      description: Returns the available instance types per Availability Zone for use when creating a
        CapacityClaim.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetCapacityClaimParametersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CapacityClaimService
  /v1alpha1/inference/capacityclaims/{id}:
    get:
      operationId: CapacityClaimService_GetCapacityClaim
      summary: Get capacity claim
      description: Retrieves a single CapacityClaim by its UUID.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the CapacityClaim to get, UUID format
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetCapacityClaimResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CapacityClaimService
    delete:
      operationId: CapacityClaimService_DeleteCapacityClaim
      summary: Delete capacity claim
      description: Deletes a CapacityClaim by ID. Returns the deleted CapacityClaim.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the CapacityClaim to delete, UUID format
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteCapacityClaimResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CapacityClaimService
    patch:
      operationId: CapacityClaimService_UpdateCapacityClaim
      summary: Update capacity claim
      description: Updates an existing CapacityClaim. The full `resources` block is required and replaces
        the existing reservation.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the CapacityClaim to update, UUID format
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateCapacityClaimRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateCapacityClaimResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CapacityClaimService
  /v1alpha1/inference/deployments:
    get:
      operationId: DeploymentService_ListDeployments
      summary: List deployments
      description: Returns every deployment that the caller can read, optionally filtered by parent gateway
        or update timestamp.
      parameters:
      - name: parentGatewayId
        in: query
        description: The ID of the parent gateway to filter deployments by
        schema:
          type: string
      - name: updatedAfter
        in: query
        description: Filter by those updated after this timestamp
        schema:
          type: string
          format: date-time
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListDeploymentsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - DeploymentService
    post:
      operationId: DeploymentService_CreateDeployment
      summary: Create deployment
      description: Creates a new model deployment associated with one or more gateways.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateDeploymentRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateDeploymentResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - DeploymentService
  /v1alpha1/inference/deployments/parameters:
    get:
      operationId: DeploymentService_GetDeploymentParameters
      summary: Get deployment parameters
      description: Returns the available gateways, runtime engines and versions, runtime config keys,
        and instance types for use when creating a deployment.
      parameters:
      - name: gatewayIds
        in: query
        description: "Optional set of gateway IDs to scope the returned parameters to. When provided,\
          \ the response\n enumerates only the values valid across every listed gateway, so a deployment\
          \ targeting this\n exact set and using only the returned values passes validation. Empty means\
          \ all of the\n organization's gateways (the values are enumerated across them without the cross-gateway\n\
          \ intersection)."
        schema:
          type: array
          items:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetDeploymentParametersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - DeploymentService
  /v1alpha1/inference/deployments/{id}:
    get:
      operationId: DeploymentService_GetDeployment
      summary: Get deployment
      description: Retrieves a single deployment by ID.
      parameters:
      - name: id
        in: path
        description: The ID of the deployment to get
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetDeploymentResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - DeploymentService
    delete:
      operationId: DeploymentService_DeleteDeployment
      summary: Delete deployment
      description: Deletes a deployment by ID. Returns the deleted deployment.
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
      tags:
      - DeploymentService
    patch:
      operationId: DeploymentService_UpdateDeployment
      summary: Update deployment
      description: Updates an existing deployment. The request body replaces the deployment's spec; this
        endpoint does not accept a field mask.
      parameters:
      - name: id
        in: path
        description: The ID of the deployment to update
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateDeploymentRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateDeploymentResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - DeploymentService
  /v1alpha1/inference/gateways:
    get:
      operationId: GatewayService_ListGateways
      summary: List gateways
      description: Returns every inference gateway that the caller can read, optionally filtered by update
        timestamp.
      parameters:
      - name: updatedAfter
        in: query
        description: Filter by those updated after this timestamp
        schema:
          type: string
          format: date-time
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListGatewaysResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
    post:
      operationId: GatewayService_CreateGateway
      summary: Create gateway
      description: Creates a new inference gateway. Each gateway must be configured with exactly one authentication
        type and exactly one routing strategy.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateGatewayRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateGatewayResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
  /v1alpha1/inference/gateways/parameters:
    get:
      operationId: GatewayService_GetGatewayParameters
      summary: Get gateway parameters
      description: Returns the available Availability Zones for use when creating a gateway.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetGatewayParametersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
  /v1alpha1/inference/gateways/{id}:
    get:
      operationId: GatewayService_GetGateway
      summary: Get gateway
      description: Retrieves a single gateway by its UUID.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the reservation to get, UUID format
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetGatewayResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
    delete:
      operationId: GatewayService_DeleteGateway
      summary: Delete gateway
      description: Deletes a gateway by ID. Returns the deleted gateway.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the gateway to delete, UUID format
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteGatewayResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
    patch:
      operationId: GatewayService_UpdateGateway
      summary: Update gateway
      description: Updates an existing gateway. The request body replaces the gateway's spec; this endpoint
        does not accept a field mask.
      parameters:
      - name: id
        in: path
        description: The unique identifier of the gateway to update, UUID format
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateGatewayRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateGatewayResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - GatewayService
  /v1alpha1/inference/hotLoads:
    get:
      operationId: HotLoadService_ListHotLoads
      summary: List hot-loads
      description: Returns the caller's hot-loads, newest first, optionally filtered to a single deployment.
      parameters:
      - name: parentDeploymentId
        in: query
        description: The ID of a deployment to filter by. When omitted, every hot-load in the caller's
          organization is returned.
        schema:
          type: string
      - name: maxPageSize
        in: query
        description: "The maximum number of hot-loads to return. The service may return fewer than this\
          \ value. If unspecified or 0, at\n most 50 hot-loads are returned. The maximum value is 1000;\
          \ values above 1000 are coerced to 1000. A negative\n value is rejected with INVALID_ARGUMENT."
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        description: "A page token received from a previous ListHotLoads call. Provide this to retrieve\
          \ the subsequent page.\n Use the same parent_deployment_id filter, including leaving it unset\
          \ if it was unset in the previous call.\n A token used with a different filter is rejected with\
          \ INVALID_ARGUMENT.\n The token is opaque and must not be constructed by clients."
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListHotLoadsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - HotLoadService
    post:
      operationId: HotLoadService_CreateHotLoad
      summary: Create hot-load
      description: Triggers a checkpoint hot-load on a deployment. The operation runs asynchronously,
        so a successful response means the request was accepted, not that the weights are loaded.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateHotLoadRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateHotLoadResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - HotLoadService
  /v1alpha1/inference/hotLoads/{hotLoadId}/replicas:
    get:
      operationId: HotLoadService_ListHotLoadReplicas
      summary: List hot-load replicas
      description: Returns the replicas of one hot-load, ordered by zone and name, in pages.
      parameters:
      - name: hotLoadId
        in: path
        description: The ID of the hot-load whose replicas to list
        required: true
        schema:
          type: string
      - name: maxPageSize
        in: query
        description: "The maximum number of replicas to return. The service may return fewer than this\
          \ value. If unspecified or 0,\n at most 50 replicas are returned. The maximum value is 1000;\
          \ values above 1000 are coerced to 1000. A\n negative value is rejected with INVALID_ARGUMENT."
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        description: "A page token received from a previous ListHotLoadReplicas call. Provide this to\
          \ retrieve the subsequent page.\n Use the same hot_load_id and organization as the previous\
          \ call; otherwise, the token is rejected with\n INVALID_ARGUMENT. The token is opaque and must\
          \ not be constructed by clients."
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListHotLoadReplicasResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - HotLoadService
  /v1alpha1/inference/hotLoads/{id}:
    get:
      operationId: HotLoadService_GetHotLoad
      summary: Get hot-load
      description: Returns a hot-load by ID, including its resolved snapshot chain and aggregate state.
      parameters:
      - name: id
        in: path
        description: The ID of the hot-load
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetHotLoadResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - HotLoadService
  /v1alpha1/inference/hotLoads/{id}:cancel:
    post:
      operationId: HotLoadService_CancelHotLoad
      summary: Cancel hot-load
      description: Cancels a hot-load. This operation is not yet implemented and currently returns an
        `Unimplemented` error.
      parameters:
      - name: id
        in: path
        description: The ID of the hot-load to cancel
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CancelHotLoadRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CancelHotLoadResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - HotLoadService
components:
  schemas:
    BodyBasedRouting:
      description: Body based routing configuration
      type: object
      properties:
        apiType:
          description: Well-known API type for routing. `API_TYPE_OPENAI` extracts the model name from
            the `model` field in the JSON request body (OpenAI-compatible behavior). The zero value `API_TYPE_UNSPECIFIED`
            is never valid to send.
          type: string
          format: enum
          enum:
          - API_TYPE_OPENAI
      required:
      - apiType
    CancelHotLoadRequest:
      description: Request for CancelHotLoad
      type: object
      properties:
        id:
          description: The ID of the hot-load to cancel
          type: string
      required:
      - id
    CancelHotLoadResponse:
      description: Response for CancelHotLoad
      type: object
      properties:
        hotLoad:
          description: The canceled hot-load
          allOf:
          - $ref: '#/components/schemas/HotLoad'
          readOnly: true
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
    CapacityClaimResources:
      description: Resources to reserve within a CapacityClaim
      type: object
      properties:
        instanceId:
          description: The instance type to reserve, by ID specifier (for example, `gb200-4x`). Identifiers
            are case-sensitive and must use the lowercase form. Must be a valid instance type within at
            least one of the specified `zones`.
          type: string
        instanceCount:
          description: The number of instances to reserve.
          type: integer
          format: uint32
        capacityType:
          description: The capacity type for the CapacityClaim. `CAPACITY_TYPE_MANAGED` reserves instances
            from CoreWeave's managed capacity pool and is the only value accepted when creating or updating
            a claim. `CAPACITY_TYPE_CUSTOMER` is deprecated; it is not accepted on create or update, but
            can still appear when reading older claims. This field cannot be changed after the claim is
            created.
          type: string
          format: enum
          enum:
          - CAPACITY_TYPE_CUSTOMER
          - CAPACITY_TYPE_MANAGED
        zones:
          description: The Availability Zones the CapacityClaim may use resources from. Zone identifiers
            are case-sensitive and must use the uppercase canonical form (for example, `US-WEST-04A`).
            The order of `zones` implies an allocation preference; earlier entries are preferred.
          type: array
          items:
            type: string
      required:
      - instanceId
      - instanceCount
      - capacityType
      - zones
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
          description: The overall status of the CapacityClaim. `STATUS_UNSPECIFIED` means the status
            has not been set. See the [Inference API overview](https://docs.coreweave.com/products/inference/reference/api-overview#status-values)
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
          description: The number of instances being provisioned to fulfill the capacity claim.
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
          description: 'The status of the condition: `STATUS_TRUE` or `STATUS_FALSE`, or `STATUS_UNSPECIFIED`
            when the status has not been set.'
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
    CoreWeaveAuth:
      description: Use CoreWeave Identity and Access Management (IAM) authentication.
      type: object
      properties:
        organizations:
          description: The organizations allowed to authenticate. If omitted, the organization that owns
            the gateway is used. Only one organization is supported.
          type: array
          items:
            type: string
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
    CreateDeploymentRequest:
      description: Request for CreateDeployment
      type: object
      properties:
        id:
          description: The unique identifier of the deployment, UUID format
          type: string
        name:
          description: The name of the deployment
          type: string
        gatewayIds:
          description: The gateways to associate the deployment with
          type: array
          items:
            type: string
        runtime:
          description: Runtime selection and configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentRuntime'
        resources:
          description: Resource configuration for the deployment
          allOf:
          - $ref: '#/components/schemas/DeploymentResources'
        model:
          description: The model configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentModel'
        autoscaling:
          description: The autoscaling configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentAutoscaling'
        traffic:
          description: The traffic configuration for the deployment
          allOf:
          - $ref: '#/components/schemas/DeploymentTraffic'
        disabled:
          description: Disable the deployment
          type: boolean
        hotLoad:
          description: "The hot-load configuration for the deployment. Set it to enable checkpoint hot-loading;\
            \ it is immutable\n after creation."
          allOf:
          - $ref: '#/components/schemas/DeploymentHotLoad'
        pd:
          description: "Prefill/Decode disaggregation configuration. Top-level resources and autoscaling\
            \ configure\n the decode pool; this field configures the prefill pool. Only supported by dynamo-vllm\
            \ when\n the pdDisaggEnabled feature flag is enabled."
          allOf:
          - $ref: '#/components/schemas/DeploymentPD'
      required:
      - name
      - gatewayIds
      - runtime
      - resources
      - model
      - autoscaling
      - traffic
    CreateDeploymentResponse:
      description: Response for CreateDeployment
      type: object
      properties:
        deployment:
          description: The deployment that was created
          allOf:
          - $ref: '#/components/schemas/Deployment'
          readOnly: true
    CreateGatewayRequest:
      description: Request for CreateGateway
      type: object
      properties:
        id:
          description: The unique identifier of the gateway, UUID format
          type: string
        name:
          description: "The human readable name of the gateway. Capped at 38 characters so the derived\n\
            \ production FQDN (<name>.<orgId>.gw.cwinference.com) fits within the 64-character\n X.509\
            \ Common Name limit."
          type: string
        zones:
          description: "The zones to make the gateway available in, limits where deployments associated\
            \ with the gateway may exist, no\n zones means all may be used."
          type: array
          items:
            type: string
        coreWeaveAuth:
          description: CoreWeave IAM
          allOf:
          - $ref: '#/components/schemas/CoreWeaveAuth'
        weightsAndBiasesAuth:
          description: Weights & Biases
          allOf:
          - $ref: '#/components/schemas/WeightsAndBiasesAuth'
        endpointConfiguration:
          description: Additional endpoint configuration options
          allOf:
          - $ref: '#/components/schemas/EndpointConfiguration'
        bodyBasedRouting:
          description: Body based routing
          allOf:
          - $ref: '#/components/schemas/BodyBasedRouting'
        headerBasedRouting:
          description: Header based routing
          allOf:
          - $ref: '#/components/schemas/HeaderBasedRouting'
        pathBasedRouting:
          description: Path based routing
          allOf:
          - $ref: '#/components/schemas/PathBasedRouting'
      required:
      - name
    CreateGatewayResponse:
      description: Response for CreateGateway
      type: object
      properties:
        gateway:
          description: The gateway that was created
          allOf:
          - $ref: '#/components/schemas/Gateway'
          readOnly: true
    CreateHotLoadRequest:
      description: Request for CreateHotLoad
      type: object
      properties:
        deploymentId:
          description: The ID of the deployment to hot-load
          type: string
        hotLoadId:
          description: "The ID to use for the hot-load, which becomes its permanent identifier. Must be\
            \ a UUID. If omitted, one is\n generated. Creating a second hot-load with an ID that already\
            \ exists in the caller's organization fails with\n ALREADY_EXISTS; an ID that is unavailable\
            \ for any other reason fails with INVALID_ARGUMENT."
          type: string
        identity:
          description: "The identity of the target snapshot within the deployment. Must be a single path\
            \ segment.\n Multiple hot-load operations may target the same snapshot identity."
          type: string
        type:
          description: The type of the target snapshot. `SNAPSHOT_TYPE_FULL` carries a complete set of
            model weights and starts a new snapshot chain. `SNAPSHOT_TYPE_INCREMENTAL` is a delta against
            an earlier snapshot and requires `incrementalSnapshotMetadata`. This field is required; the
            zero value is rejected.
          type: string
          format: enum
          enum:
          - SNAPSHOT_TYPE_FULL
          - SNAPSHOT_TYPE_INCREMENTAL
        incrementalSnapshotMetadata:
          description: Delta metadata, required when type is SNAPSHOT_TYPE_INCREMENTAL
          allOf:
          - $ref: '#/components/schemas/IncrementalSnapshotMetadata'
        promptCachePolicy:
          description: How the prompt cache is handled once the swap completes. `PROMPT_CACHE_POLICY_RESET_ALL`
            prevents reuse of any entry computed before the swap. `PROMPT_CACHE_POLICY_PRESERVE` allows
            reuse, knowingly stale under the new weights. The policy applies to requests admitted after
            the transition, not to requests already in flight. If you omit the field or send `PROMPT_CACHE_POLICY_UNSPECIFIED`,
            `PROMPT_CACHE_POLICY_PRESERVE` applies.
          type: string
          format: enum
          enum:
          - PROMPT_CACHE_POLICY_UNSPECIFIED
          - PROMPT_CACHE_POLICY_RESET_ALL
          - PROMPT_CACHE_POLICY_PRESERVE
      required:
      - deploymentId
      - identity
      - type
    CreateHotLoadResponse:
      description: Response for CreateHotLoad
      type: object
      properties:
        hotLoad:
          description: The created hot-load
          allOf:
          - $ref: '#/components/schemas/HotLoad'
          readOnly: true
    DeleteCapacityClaimResponse:
      description: Response for DeleteCapacityClaim
      type: object
      properties:
        capacityClaim:
          description: The deleted CapacityClaim
          allOf:
          - $ref: '#/components/schemas/CapacityClaim'
          readOnly: true
    DeleteDeploymentResponse:
      description: Response for DeleteDeployment
      type: object
      properties:
        deployment:
          description: The deployment that was deleted
          allOf:
          - $ref: '#/components/schemas/Deployment'
          readOnly: true
    DeleteGatewayResponse:
      description: Response for DeleteGateway
      type: object
      properties:
        gateway:
          description: The gateway that was deleted
          allOf:
          - $ref: '#/components/schemas/Gateway'
          readOnly: true
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
    DeploymentAutoscaling:
      description: Autoscaling configuration for the deployment
      type: object
      properties:
        min:
          description: The minimum number of replicas. Must be at least `1`; scale-to-zero is not supported.
          type: integer
          format: uint32
        max:
          description: The maximum number of replicas. Must be greater than or equal to `min`. Set equal
            to `min` to disable autoscaling.
          type: integer
          format: uint32
        priority:
          description: Scaling priority relative to other deployments, from `0` to `1000`. Higher values
            receive scaling preference during resource contention.
          type: integer
          format: uint32
        capacityClasses:
          description: The capacity classes the autoscaler may use for this deployment. Set `CAPACITY_CLASS_RESERVED`
            to schedule replicas onto capacity reserved by a CapacityClaim; set `CAPACITY_CLASS_ON_DEMAND`
            to use shared on-demand capacity. Omit the zero value `CAPACITY_CLASS_UNSPECIFIED` rather
            than sending it.
          type: array
          items:
            type: string
            format: enum
            enum:
            - CAPACITY_CLASS_RESERVED
            - CAPACITY_CLASS_ON_DEMAND
        concurrency:
          description: Target concurrent requests per replica. Lower values reduce latency; higher values
            increase throughput. Must be at least `1`.
          type: integer
          format: uint32
        claims:
          description: Optional `CapacityClaim` IDs to use for reserved capacity, in preference order.
            If omitted, any available reserved capacity may be used. Replace released or deleted claims
            because they no longer provide reserved capacity.
          type: array
          items:
            type: string
      required:
      - min
      - max
    DeploymentHotLoad:
      description: "DeploymentHotLoad configures checkpoint hot-loading for the deployment. Set it at\
        \ deployment creation to enable\n hot-loading, or omit it to disable hot-loading. This configuration\
        \ cannot be changed after creation."
      type: object
      properties:
        bucket:
          description: The CoreWeave Object Storage bucket that holds checkpoint snapshots
          type: string
        pathPrefix:
          description: "The path prefix within the bucket that holds checkpoint snapshots. Append the\
            \ snapshot identity to this\n prefix to locate the snapshot's weights and metadata.\n Example:\
            \ with bucket \"my-model\" and path_prefix \"my-checkpoints\", the weights and metadata of\
            \ the\n snapshot with identity \"weight_v001\" should live under \"s3://my-model/my-checkpoints/weight_v001/\""
          type: string
        transitionMode:
          description: How requests are handled while a checkpoint swap is in progress on a replica. `TRANSITION_MODE_ASYNC`
            pauses in-flight requests and resumes them after the swap, and queues new requests until the
            swap completes. This field is required, and `TRANSITION_MODE_ASYNC` is the only accepted value.
          type: string
          format: enum
          enum:
          - TRANSITION_MODE_ASYNC
      required:
      - bucket
      - transitionMode
    DeploymentModel:
      description: Configuration of the model
      type: object
      properties:
        name:
          description: The model name used in inference requests (and returned by the gateway's `/models`
            endpoint). When multiple deployments on the same gateway share a name, traffic is split between
            them by `traffic.weight`.
          type: string
        bucket:
          description: The CoreWeave AI Object Storage (CAIOS) bucket the model is stored in.
          type: string
        path:
          description: The path within `bucket` to the model and its configuration files.
          type: string
      required:
      - name
      - bucket
      - path
    DeploymentPD:
      description: "DeploymentPD carries per-pool configuration for prefill/decode disaggregated serving.\
        \ The\n decode pool is described by the enclosing DeploymentSpec's top-level `resources` and\n\
        \ `autoscaling` fields; DeploymentPD contributes the prefill-pool overrides."
      type: object
      properties:
        prefillResources:
          description: Resource configuration for the prefill worker pool
          allOf:
          - $ref: '#/components/schemas/DeploymentResources'
        prefillAutoscaling:
          description: "Autoscaling configuration for the prefill worker pool. Deployment-wide priority\
            \ is inherited\n from the top-level autoscaling configuration and is therefore not repeated\
            \ here."
          allOf:
          - $ref: '#/components/schemas/DeploymentPDPoolAutoscaling'
      required:
      - prefillResources
      - prefillAutoscaling
    DeploymentPDPoolAutoscaling:
      description: "Autoscaling configuration for a worker pool in a Prefill/Decode-disaggregated deployment.\n\
        \ Deployment-wide settings such as priority remain on DeploymentSpec.autoscaling."
      type: object
      properties:
        min:
          description: The minimum number of instances to scale down to, scale to zero is not supported
          type: integer
          format: uint32
        max:
          description: The maximum number of instances to scale up to, setting equal to min disables autoscaling
          type: integer
          format: uint32
        capacityClasses:
          description: The capacity classes the autoscaler may use for the prefill worker pool. Set `CAPACITY_CLASS_RESERVED`
            to schedule replicas onto capacity reserved by a CapacityClaim; set `CAPACITY_CLASS_ON_DEMAND`
            to use shared on-demand capacity. Omit the zero value `CAPACITY_CLASS_UNSPECIFIED` rather
            than sending it; the API rejects it.
          type: array
          items:
            type: string
            format: enum
            enum:
            - CAPACITY_CLASS_RESERVED
            - CAPACITY_CLASS_ON_DEMAND
        concurrency:
          description: The concurrency per instance to target/limit, used to control latency vs throughput
            tradeoffs
          type: integer
          format: uint32
        claims:
          description: Optional `CapacityClaim` IDs to use for reserved capacity, in preference order.
            If omitted, any available reserved capacity may be used. Replace released or deleted claims
            because they no longer provide reserved capacity.
          type: array
          items:
            type: string
      required:
      - min
      - max
    DeploymentResourceParameters:
      description: The available parameters for resource configuration
      type: object
      properties:
        instanceTypes:
          description: "Available instance types. May be empty — e.g. when a gateway_ids filter selects\
            \ gateways that\n share no common instance type, or when the organization has no gateways."
          type: array
          items:
            type: string
          readOnly: true
    DeploymentResources:
      description: Resource configuration for the deployment
      type: object
      properties:
        instanceType:
          description: The instance type to use for the deployment. The available values are returned
            by `GET /v1alpha1/inference/deployments/parameters`.
          type: string
        gpuCount:
          description: Number of GPUs needed per instance. CPU and RAM are automatically assigned based
            on the chosen GPU count.
          type: integer
          format: uint32
      required:
      - instanceType
      - gpuCount
    DeploymentRuntime:
      description: Runtime selection and configuration for deployments
      type: object
      properties:
        engine:
          description: The inference engine to use (for example, `vllm`). The available engines are returned
            by `GET /v1alpha1/inference/deployments/parameters`.
          type: string
        version:
          description: The version of the engine. Required. Must be one of the engine's available versions
            returned by the parameters endpoint.
          type: string
        engineConfig:
          description: Engine-specific configuration arguments. The parameters endpoint returns the allowed
            keys for each engine and version in `runtimeParameters.runtimeEngineOptions[engine].versions[version].configOptions`.
          type: object
          additionalProperties:
            type: string
        engineEnv:
          description: Map of engine-specific environment variables to inject into the model runtime container
          type: object
          additionalProperties:
            type: string
      required:
      - engine
      - version
    DeploymentRuntimeParameters:
      description: The available parameters for runtime configuration
      type: object
      properties:
        runtimeVersions:
          description: Deprecated. Use `runtimeEngineOptions` instead. Lists the available runtime versions
            for each engine.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_RuntimeVersions'
          readOnly: true
        runtimeConfigOptions:
          description: Deprecated. Use `runtimeEngineOptions` instead. Lists the available configuration
            options for each engine.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_RuntimeConfigOptions'
          readOnly: true
        engineEnvOptions:
          description: Deprecated. Use `runtimeEngineOptions` instead. Lists the available environment
            variables for each engine.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_EngineEnvOptions'
          readOnly: true
        runtimeEngineOptions:
          description: The available runtime parameters, grouped by engine name and version.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_RuntimeEngineOptions'
          readOnly: true
    DeploymentRuntimeParameters_EngineEnvOptions:
      description: The available engine environment variable options
      type: object
      properties:
        allowedNames:
          description: The allowed engine environment variable names.
          type: array
          items:
            type: string
          readOnly: true
    DeploymentRuntimeParameters_RuntimeConfigOptions:
      description: The available runtime config options
      type: object
      properties:
        allowedKeys:
          description: The allowed engine config keys
          type: array
          items:
            type: string
          readOnly: true
    DeploymentRuntimeParameters_RuntimeEngineOptions:
      description: The available runtime parameters for an engine.
      type: object
      properties:
        versions:
          description: The available runtime parameters, grouped by version.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/RuntimeEngineOptions_VersionOptions'
          readOnly: true
    DeploymentRuntimeParameters_RuntimeVersions:
      description: List of runtime versions
      type: object
      properties:
        versions:
          description: The version strings
          type: array
          items:
            type: string
          readOnly: true
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
          description: The IDs of the gateways the deployment is associated with. A deployment may be
            attached to multiple gateways; traffic from each gateway is routed by that gateway's strategy.
          type: array
          items:
            type: string
          readOnly: true
        runtime:
          description: Runtime selection and configuration. The available engines, versions, and per-engine
            config keys are returned by `GET /v1alpha1/inference/deployments/parameters`.
          allOf:
          - $ref: '#/components/schemas/DeploymentRuntime'
          readOnly: true
        resources:
          description: Resource configuration for the deployment. CPU and RAM are automatically assigned
            based on `gpuCount` for the chosen `instanceType`.
          allOf:
          - $ref: '#/components/schemas/DeploymentResources'
          readOnly: true
        model:
          description: The model configuration. The model is loaded from a path in a CoreWeave AI Object
            Storage (CAIOS) bucket.
          allOf:
          - $ref: '#/components/schemas/DeploymentModel'
          readOnly: true
        autoscaling:
          description: Autoscaling configuration. CoreWeave manages scaling within the configured `min`
            and `max` bounds; scale-to-zero is not supported.
          allOf:
          - $ref: '#/components/schemas/DeploymentAutoscaling'
          readOnly: true
        traffic:
          description: Traffic configuration for the deployment. When multiple deployments share a model
            name on the same gateway, `traffic.weight` controls the share of traffic each deployment receives.
          allOf:
          - $ref: '#/components/schemas/DeploymentTraffic'
          readOnly: true
        organizationId:
          description: The organization ID that owns the deployment.
          type: string
          readOnly: true
        disabled:
          description: When `true`, the deployment does not receive traffic and is not scaled.
          type: boolean
          readOnly: true
        hotLoad:
          description: The hot-load configuration for the deployment
          allOf:
          - $ref: '#/components/schemas/DeploymentHotLoad'
          readOnly: true
        pd:
          description: "Prefill/Decode disaggregation configuration. When set, the deployment renders\
            \ two worker\n pools — prefill (compute-bound, sized on TTFT) and decode (memory-bound, sized\
            \ on\n concurrent streams) — with NIXL/RDMA KV transfer between them. Top-level `resources`\
            \ and\n `autoscaling` describe the DECODE pool; `pd.prefill_*` describes the PREFILL pool.\
            \ Only\n valid when runtime.engine = \"dynamo-vllm\" and the pdDisaggEnabled feature flag\
            \ is on."
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
          description: The overall status of the deployment. `STATUS_UNSPECIFIED` means the status has
            not been set. See the [Inference API overview](https://docs.coreweave.com/products/inference/reference/api-overview#status-values)
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
          description: The revision of the deployment specification. It increases when the configuration
            changes.
          type: string
          readOnly: true
    DeploymentTraffic:
      description: Configuration for traffic control to the deployment
      type: object
      properties:
        weight:
          description: The relative weight of traffic routed to this deployment compared to other deployments
            with the same model name on the same gateway. Weights are normalized into percentages.
          type: integer
          format: uint32
    EndpointConfiguration:
      description: Configuration options for the gateway endpoint, DNS, TLS, etc.
      type: object
      properties:
        additionalDns:
          description: Additional DNS configurations, these DNS need to be configured to point to the
            gateway endpoint manually
          type: array
          items:
            type: string
        edgeProxyMode:
          description: 'How client traffic reaches the gateway. `EDGE_PROXY_MODE_MANAGED` proxies traffic
            through CoreWeave''s managed edge network: DDoS mitigation and WAF, with TLS terminated at
            the edge and the origin address kept out of public DNS. `EDGE_PROXY_MODE_DIRECT` connects
            clients straight to the gateway''s load balancer, with no edge filtering and the load balancer
            address published in DNS. `EDGE_PROXY_MODE_UNSPECIFIED` (or omitting the field) applies the
            platform default, currently managed.'
          type: string
          format: enum
          enum:
          - EDGE_PROXY_MODE_UNSPECIFIED
          - EDGE_PROXY_MODE_MANAGED
          - EDGE_PROXY_MODE_DIRECT
        allowedSourceIpRanges:
          description: "Client source IP ranges permitted to reach the gateway, in CIDR notation (IPv4\
            \ or IPv6), up to\n 50 entries. An empty list applies no source restriction. Use a full-length\
            \ prefix for a single\n address (e.g. \"203.0.113.5/32\")."
          type: array
          items:
            type: string
    Gateway:
      description: Gateway object with specification and status fields
      type: object
      properties:
        spec:
          description: The specification of the gateway
          allOf:
          - $ref: '#/components/schemas/GatewaySpec'
          readOnly: true
        status:
          description: The status of the gateway
          allOf:
          - $ref: '#/components/schemas/GatewayStatus'
          readOnly: true
    GatewaySpec:
      description: GatewaySpec contains the specification for a Gateway
      type: object
      properties:
        id:
          description: The unique identifier of the gateway, UUID format
          type: string
          readOnly: true
        name:
          description: "The human readable name of the gateway. Combined with organization_id and the\n\
            \ deployment base domain it forms the gateway's public FQDN\n (<name>.<orgId>.gw.<baseDomain>).\
            \ See CreateGatewayRequest.name and\n UpdateGatewayRequest.name for the length cap applied\
            \ on write."
          type: string
          readOnly: true
        zones:
          description: The Availability Zones the gateway is deployed in. The field accepts an array,
            but gateways are currently limited to one zone. The available zones are returned by `GET /v1alpha1/inference/gateways/parameters`.
          type: array
          items:
            type: string
          readOnly: true
        coreWeaveAuth:
          description: CoreWeave IAM authentication. Validates inference requests using the same CoreWeave
            API access tokens used to call the management API.
          allOf:
          - $ref: '#/components/schemas/CoreWeaveAuth'
        weightsAndBiasesAuth:
          description: Weights & Biases authentication. Validates inference requests using W&B SaaS credentials.
            W&B self-hosted is not currently supported.
          allOf:
          - $ref: '#/components/schemas/WeightsAndBiasesAuth'
        organizationId:
          description: The organization ID that owns the gateway
          type: string
          readOnly: true
        endpointConfiguration:
          description: Optional endpoint configuration. Use `additionalDns` to register additional DNS
            names that you point at the gateway endpoint manually.
          allOf:
          - $ref: '#/components/schemas/EndpointConfiguration'
        bodyBasedRouting:
          description: Body based routing
          allOf:
          - $ref: '#/components/schemas/BodyBasedRouting'
        headerBasedRouting:
          description: Header based routing
          allOf:
          - $ref: '#/components/schemas/HeaderBasedRouting'
        pathBasedRouting:
          description: Path based routing
          allOf:
          - $ref: '#/components/schemas/PathBasedRouting'
    GatewayStatus:
      description: GatewayStatus contains the status fields for a Gateway
      type: object
      properties:
        createdAt:
          description: The time at which the gateway was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time at which the gateway was last updated.
          type: string
          format: date-time
          readOnly: true
        status:
          description: The overall status of the gateway. `STATUS_UNSPECIFIED` means the status has not
            been set. See the [Inference API overview](https://docs.coreweave.com/products/inference/reference/api-overview#status-values)
            for the meaning of each value. Once `STATUS_READY`, the gateway exposes one or more endpoint
            URLs in `endpoints`.
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
        endpoints:
          description: The endpoint URLs for the gateway. The default endpoint follows the pattern `https://[GATEWAY-NAME].[ORG-ID].gw.cwinference.com`;
            additional entries appear when `endpointConfiguration.additionalDns` is set.
          type: array
          items:
            type: string
          readOnly: true
    GetCapacityClaimParametersResponse:
      description: Response for GetCapacityClaimParameters
      type: object
      properties:
        zoneInstanceTypes:
          description: Map keyed by Availability Zone (for example, `US-WEST-04A`) whose values list the
            `instanceId` strings that are valid for a CapacityClaim in that zone.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/GetCapacityClaimParametersResponse_InstanceTypes'
          readOnly: true
    GetCapacityClaimParametersResponse_InstanceTypes:
      description: List of available instance types
      type: object
      properties:
        instanceIds:
          description: List of instance type IDs
          type: array
          items:
            type: string
          readOnly: true
    GetCapacityClaimResponse:
      description: Response for GetCapacityClaim
      type: object
      properties:
        capacityClaim:
          description: The CapacityClaim
          allOf:
          - $ref: '#/components/schemas/CapacityClaim'
          readOnly: true
    GetDeploymentParametersResponse:
      description: Response for GetDeploymentParameters
      type: object
      properties:
        gatewayIds:
          description: The gateway IDs in the caller's organization that can be referenced by a new deployment.
          type: array
          items:
            type: string
        runtimeParameters:
          description: The available runtime parameters for the deployments
          allOf:
          - $ref: '#/components/schemas/DeploymentRuntimeParameters'
          readOnly: true
        resourceParameters:
          description: The available resource parameters for the deployments
          allOf:
          - $ref: '#/components/schemas/DeploymentResourceParameters'
          readOnly: true
      required:
      - gatewayIds
    GetDeploymentResponse:
      description: Response for GetDeployment
      type: object
      properties:
        deployment:
          description: The deployment
          allOf:
          - $ref: '#/components/schemas/Deployment'
          readOnly: true
    GetGatewayParametersResponse:
      description: Response for GetGatewayParameters
      type: object
      properties:
        zones:
          description: The Availability Zone identifiers that are valid in a gateway's `zones` field.
          type: array
          items:
            type: string
      required:
      - zones
    GetGatewayResponse:
      description: Response for GetGateway
      type: object
      properties:
        gateway:
          description: The gateway
          allOf:
          - $ref: '#/components/schemas/Gateway'
          readOnly: true
    GetHotLoadResponse:
      description: Response for GetHotLoad
      type: object
      properties:
        hotLoad:
          description: The requested hot-load
          allOf:
          - $ref: '#/components/schemas/HotLoad'
          readOnly: true
    GoogleProtobufAny:
      description: Contains an arbitrary serialized message along with a @type that describes the type
        of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    HeaderBasedRouting:
      description: Header based routing configuration, uses a header value to route requests to the model
        by name
      type: object
      properties:
        headerName:
          description: The HTTP header to read the model name from on each inference request. Must be
            1-100 characters.
          type: string
      required:
      - headerName
    HotLoad:
      description: HotLoad object with specification and status fields
      type: object
      properties:
        spec:
          description: The specification of the hot-load
          allOf:
          - $ref: '#/components/schemas/HotLoadSpec'
          readOnly: true
        status:
          description: The status of the hot-load
          allOf:
          - $ref: '#/components/schemas/HotLoadStatus'
          readOnly: true
    HotLoadReplicaStatus:
      description: The per-replica progress of a hot-load
      type: object
      properties:
        name:
          description: The name of the replica
          type: string
          readOnly: true
        currentSnapshotIdentity:
          description: The snapshot identity the replica currently serves
          type: string
          readOnly: true
        state:
          description: The state of this replica's checkpoint transition. `PENDING_UPDATE` means the replica
            serves a different snapshot identity and its transition has not started. `UPDATING` means
            the transition is in progress. `READY` means the replica serves the target snapshot identity.
            `ERROR` means the transition failed, and `errorReason` carries the cause.
          type: string
          format: enum
          enum:
          - REPLICA_STATE_UNSPECIFIED
          - PENDING_UPDATE
          - UPDATING
          - READY
          - ERROR
          readOnly: true
        errorReason:
          description: The reason for an error state
          type: string
          readOnly: true
        transitionedAt:
          description: The last time the replica state changed
          type: string
          format: date-time
          readOnly: true
        zone:
          description: The zone where the replica runs
          type: string
          readOnly: true
        startedAt:
          description: "The time the replica began transitioning to the target snapshot, set when it first\
            \ enters UPDATING. Unset\n while the replica is still PENDING_UPDATE."
          type: string
          format: date-time
          readOnly: true
        finishedAt:
          description: "The time the replica reached a terminal state (READY or ERROR). Unset until then,\
            \ and unset again if a retry\n moves the replica back out of a terminal state."
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time the replica status was last updated, whether or not its state changed
          type: string
          format: date-time
          readOnly: true
    HotLoadSpec:
      description: HotLoadSpec describes one immutable checkpoint hot-load operation
      type: object
      properties:
        id:
          description: The ID of the hot-load
          type: string
          readOnly: true
        deploymentId:
          description: The ID of the deployment this hot-load targets
          type: string
          readOnly: true
        organizationId:
          description: The organization ID that owns the hot-load
          type: string
          readOnly: true
        identity:
          description: "The identity of the target snapshot within the deployment. Must be a single path\
            \ segment.\n Multiple hot-load operations may target the same snapshot identity."
          type: string
          readOnly: true
        type:
          description: The type of the target snapshot.
          type: string
          format: enum
          enum:
          - SNAPSHOT_TYPE_UNSPECIFIED
          - SNAPSHOT_TYPE_FULL
          - SNAPSHOT_TYPE_INCREMENTAL
          readOnly: true
        incrementalSnapshotMetadata:
          description: Delta metadata, required when type is SNAPSHOT_TYPE_INCREMENTAL
          allOf:
          - $ref: '#/components/schemas/IncrementalSnapshotMetadata'
          readOnly: true
        promptCachePolicy:
          description: How the prompt cache was handled once the swap completed.
          type: string
          format: enum
          enum:
          - PROMPT_CACHE_POLICY_UNSPECIFIED
          - PROMPT_CACHE_POLICY_RESET_ALL
          - PROMPT_CACHE_POLICY_PRESERVE
          readOnly: true
        snapshotChain:
          description: The resolved snapshot chain, oldest first. The first element is always a full snapshot.
          type: array
          items:
            $ref: '#/components/schemas/SnapshotRef'
          readOnly: true
    HotLoadStatus:
      description: HotLoadStatus describes the observed state of a hot-load
      type: object
      properties:
        createdAt:
          description: The time the hot-load was created
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time the hot-load status last changed
          type: string
          format: date-time
          readOnly: true
        finishedAt:
          description: The time the hot-load reached a terminal state
          type: string
          format: date-time
          readOnly: true
        state:
          description: The aggregate state of the hot-load. `HOT_LOAD_STATE_PENDING` means the operation
            was accepted but replica transitions have not started, and `HOT_LOAD_STATE_IN_PROGRESS` means
            they are underway. `HOT_LOAD_STATE_COMPLETED` means every replica serves the target snapshot
            identity. `HOT_LOAD_STATE_FAILED` and `HOT_LOAD_STATE_CANCELED` are terminal, and replicas
            may serve different snapshots until a later hot-load completes.
          type: string
          format: enum
          enum:
          - HOT_LOAD_STATE_UNSPECIFIED
          - HOT_LOAD_STATE_PENDING
          - HOT_LOAD_STATE_IN_PROGRESS
          - HOT_LOAD_STATE_COMPLETED
          - HOT_LOAD_STATE_FAILED
          - HOT_LOAD_STATE_CANCELED
          readOnly: true
        conditions:
          description: Detailed status conditions
          type: array
          items:
            $ref: '#/components/schemas/Condition'
          readOnly: true
        canceledAt:
          description: The time cancellation was requested; set only for canceled hot-loads
          type: string
          format: date-time
          readOnly: true
    IncrementalSnapshotMetadata:
      description: Metadata describing how an incremental snapshot relates to its predecessor
      type: object
      properties:
        previousSnapshotIdentity:
          description: The identity of the snapshot this delta was computed against
          type: string
        compressionFormat:
          description: The compression format of the delta. `COMPRESSION_FORMAT_ZSTD` is a Zstandard-compressed
            XOR delta. This field is required, and `COMPRESSION_FORMAT_ZSTD` is the only accepted value.
          type: string
          format: enum
          enum:
          - COMPRESSION_FORMAT_ZSTD
        checksumFormat:
          description: The checksum format used to verify snapshot integrity. This field is required,
            and `CHECKSUM_FORMAT_ADLER32` is the only accepted value.
          type: string
          format: enum
          enum:
          - CHECKSUM_FORMAT_ADLER32
      required:
      - previousSnapshotIdentity
      - compressionFormat
      - checksumFormat
    ListCapacityClaimsResponse:
      description: Response for ListCapacityClaims
      type: object
      properties:
        capacityClaims:
          description: The list of CapacityClaims
          type: array
          items:
            $ref: '#/components/schemas/CapacityClaim'
          readOnly: true
    ListDeploymentsResponse:
      description: Response for ListDeployments
      type: object
      properties:
        items:
          description: The list of deployments
          type: array
          items:
            $ref: '#/components/schemas/Deployment'
          readOnly: true
    ListGatewaysResponse:
      description: Response for ListGateways
      type: object
      properties:
        items:
          description: The list of gateways
          type: array
          items:
            $ref: '#/components/schemas/Gateway'
          readOnly: true
    ListHotLoadReplicasResponse:
      description: Response for ListHotLoadReplicas
      type: object
      properties:
        replicas:
          description: The replicas of the hot-load, ordered by (zone, name)
          type: array
          items:
            $ref: '#/components/schemas/HotLoadReplicaStatus'
          readOnly: true
        nextPageToken:
          description: A token that can be sent as page_token to retrieve the next page. Empty when the
            final page has been reached.
          type: string
          readOnly: true
    ListHotLoadsResponse:
      description: Response for ListHotLoads
      type: object
      properties:
        hotLoads:
          description: The hot-loads matching the request, newest first
          type: array
          items:
            $ref: '#/components/schemas/HotLoad'
          readOnly: true
        nextPageToken:
          description: A token that can be sent as page_token to retrieve the next page. Empty when the
            final page has been reached.
          type: string
          readOnly: true
    PathBasedRouting:
      description: Path-based routing configuration. The model name is read from the first segment of
        the URL path (for example, `/my-model/v1/chat/completions`). URL-encode model names that contain
        special characters.
      type: object
      properties: {}
    RuntimeEngineOptions_VersionOptions:
      description: The available runtime parameters for an engine version.
      type: object
      properties:
        configOptions:
          description: The available engine configuration options, grouped by configuration name.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/VersionOptions_ParameterOptions'
          readOnly: true
        envOptions:
          description: The available engine environment variables, grouped by variable name.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/VersionOptions_ParameterOptions'
          readOnly: true
        lifecycle:
          description: The lifecycle state of this runtime engine version. `LIFECYCLE_STABLE` is stable
            and available for new and existing deployments. `LIFECYCLE_UNSTABLE` is available for use
            but isn't yet stable. `LIFECYCLE_DEPRECATED` is available only to existing deployments already
            using the version. `LIFECYCLE_UNSPECIFIED` means the lifecycle state hasn't been set.
          type: string
          format: enum
          enum:
          - LIFECYCLE_UNSPECIFIED
          - LIFECYCLE_STABLE
          - LIFECYCLE_UNSTABLE
          - LIFECYCLE_DEPRECATED
          readOnly: true
    SnapshotRef:
      description: One element of a resolved snapshot chain
      type: object
      properties:
        identity:
          description: The identity of the snapshot
          type: string
          readOnly: true
        type:
          description: The type of this snapshot in the resolved chain.
          type: string
          format: enum
          enum:
          - SNAPSHOT_TYPE_UNSPECIFIED
          - SNAPSHOT_TYPE_FULL
          - SNAPSHOT_TYPE_INCREMENTAL
          readOnly: true
        compressionFormat:
          description: The compression format, set for incremental snapshots.
          type: string
          format: enum
          enum:
          - COMPRESSION_FORMAT_UNSPECIFIED
          - COMPRESSION_FORMAT_ZSTD
          readOnly: true
        checksumFormat:
          description: The checksum format, set for incremental snapshots.
          type: string
          format: enum
          enum:
          - CHECKSUM_FORMAT_UNSPECIFIED
          - CHECKSUM_FORMAT_ADLER32
          readOnly: true
        hotLoadId:
          description: The ID of the HotLoad operation that introduced this snapshot into the chain.
          type: string
          readOnly: true
    Status:
      description: Standard error response. `code` is a [`google.rpc.Code`](https://cloud.google.com/apis/design/errors#error_codes);
        `message` is human-readable English; `details` carries machine-readable error details when present.
      type: object
      properties:
        code:
          description: The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: A developer-facing error message, which should be in English. Any user-facing error
            message should be localized and sent in the [google.rpc.Status.details][google.rpc.Status.details]
            field, or localized by the client.
          type: string
        details:
          description: A list of messages that carry the error details.  There is a common set of message
            types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    UpdateCapacityClaimRequest:
      description: Request to update a CapacityClaim
      type: object
      properties:
        id:
          description: The unique identifier of the CapacityClaim to update, UUID format
          type: string
        resources:
          description: The specification for the resources to reserve
          allOf:
          - $ref: '#/components/schemas/CapacityClaimResources'
      required:
      - id
      - resources
    UpdateCapacityClaimResponse:
      description: Response for UpdateCapacityClaim
      type: object
      properties:
        capacityClaim:
          description: The updated CapacityClaim
          allOf:
          - $ref: '#/components/schemas/CapacityClaim'
          readOnly: true
    UpdateDeploymentRequest:
      description: Request for UpdateDeployment
      type: object
      properties:
        id:
          description: The ID of the deployment to update
          type: string
        name:
          description: The name of the deployment
          type: string
        gatewayIds:
          description: The gateways to associate the deployment with
          type: array
          items:
            type: string
        runtime:
          description: Runtime selection and configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentRuntime'
        resources:
          description: Resource configuration for the deployment
          allOf:
          - $ref: '#/components/schemas/DeploymentResources'
        model:
          description: The model configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentModel'
        autoscaling:
          description: The autoscaling configuration
          allOf:
          - $ref: '#/components/schemas/DeploymentAutoscaling'
        traffic:
          description: The traffic configuration for the deployment
          allOf:
          - $ref: '#/components/schemas/DeploymentTraffic'
        disabled:
          description: Disable the deployment
          type: boolean
        hotLoad:
          description: 'The hot-load configuration for the deployment. Immutable: it must match the value
            set at creation.'
          allOf:
          - $ref: '#/components/schemas/DeploymentHotLoad'
        pd:
          description: "Prefill/Decode disaggregation configuration. Top-level resources and autoscaling\
            \ configure\n the decode pool; this field configures the prefill pool. Only supported by dynamo-vllm\
            \ when\n the pdDisaggEnabled feature flag is enabled."
          allOf:
          - $ref: '#/components/schemas/DeploymentPD'
      required:
      - id
      - name
      - gatewayIds
      - runtime
      - resources
      - model
      - autoscaling
      - traffic
    UpdateDeploymentResponse:
      description: Response for UpdateDeployment
      type: object
      properties:
        deployment:
          description: The updated deployment
          allOf:
          - $ref: '#/components/schemas/Deployment'
          readOnly: true
    UpdateGatewayRequest:
      description: Request for UpdateGateway
      type: object
      properties:
        id:
          description: The unique identifier of the gateway to update, UUID format
          type: string
        name:
          description: "The human readable name of the gateway. Capped at 38 characters, matching\n CreateGatewayRequest.name."
          type: string
        zones:
          description: "The zones to make the gateway available in, limits where deployments associated\
            \ with the gateway may exist, no\n zones means all may be used."
          type: array
          items:
            type: string
        coreWeaveAuth:
          description: CoreWeave IAM
          allOf:
          - $ref: '#/components/schemas/CoreWeaveAuth'
        weightsAndBiasesAuth:
          description: Weights & Biases
          allOf:
          - $ref: '#/components/schemas/WeightsAndBiasesAuth'
        endpointConfiguration:
          description: Additional endpoint configuration options
          allOf:
          - $ref: '#/components/schemas/EndpointConfiguration'
        bodyBasedRouting:
          description: Body based routing
          allOf:
          - $ref: '#/components/schemas/BodyBasedRouting'
        headerBasedRouting:
          description: Header based routing
          allOf:
          - $ref: '#/components/schemas/HeaderBasedRouting'
        pathBasedRouting:
          description: Path based routing
          allOf:
          - $ref: '#/components/schemas/PathBasedRouting'
      required:
      - id
      - name
    UpdateGatewayResponse:
      description: Response for UpdateGateway
      type: object
      properties:
        gateway:
          description: The updated gateway
          allOf:
          - $ref: '#/components/schemas/Gateway'
          readOnly: true
    VersionOptions_ParameterOptions:
      description: Metadata for a runtime configuration parameter.
      type: object
      properties: {}
    WeightsAndBiasesAuth:
      description: Use W&B auth
      type: object
      properties:
        apiKey:
          description: The W&B organization API key. Required if `serverUrl` is set.
          type: string
        serverUrl:
          description: Optional W&B server URL. Defaults to the W&B shared SaaS instance.
          type: string
        enableUsageReports:
          description: Send inference usage data to W&B for tracking.
          type: boolean
        enableRateLimiting:
          description: Enable W&B-controlled rate limiting for inference requests.
          type: boolean
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}
tags:
- name: CapacityClaimService
  description: Endpoints for creating, listing, getting, updating, and deleting CapacityClaim reservations
    of GPU hardware for inference deployments.
- name: DeploymentService
  description: Endpoints for creating, listing, getting, updating, and deleting model deployments. Each
    deployment associates a model with one or more gateways and configures runtime, resources, autoscaling,
    and traffic.
- name: GatewayService
  description: Endpoints for creating, listing, getting, updating, and deleting inference gateways. Gateways
    provide authentication, request routing, load balancing, and traffic splitting for one or more deployments.
- name: HotLoadService
  description: Endpoints for creating, listing, getting, and canceling checkpoint hot-loads. A hot-load
    loads a new set of model weights into a running deployment's replicas without restarting the inference
    processes or recreating the replicas.
security:
- bearerAuth: []
```
