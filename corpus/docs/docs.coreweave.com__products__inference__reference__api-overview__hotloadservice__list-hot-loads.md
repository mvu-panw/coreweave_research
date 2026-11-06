# List hot-loads

Source: https://docs.coreweave.com/products/inference/reference/api-overview/hotloadservice/list-hot-loads

# List hot-loads

> Fetch the caller's checkpoint hot-loads, newest first, with an optional deployment filter.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Use this endpoint to read a deployment's checkpoint update
history. Results are paginated: pass `nextPageToken` back as
`pageToken`, keeping `parentDeploymentId` identical across
the walk. A token minted under one filter and replayed under
another is rejected.

```bash title="Example request" theme={{"system"}}
curl -X GET "https://api.coreweave.com/v1alpha1/inference/hotLoads?parentDeploymentId={DEPLOYMENT_ID}" \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml get /v1alpha1/inference/hotLoads
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
  /v1alpha1/inference/hotLoads:
    get:
      tags:
        - HotLoadService
      summary: List hot-loads
      description: >-
        Returns the caller's hot-loads, newest first, optionally filtered to a
        single deployment.
      operationId: HotLoadService_ListHotLoads
      parameters:
        - name: parentDeploymentId
          in: query
          description: >-
            The ID of a deployment to filter by. When omitted, every hot-load in
            the caller's organization is returned.
          schema:
            type: string
        - name: maxPageSize
          in: query
          description: >-
            The maximum number of hot-loads to return. The service may return
            fewer than this value. If unspecified or 0, at
             most 50 hot-loads are returned. The maximum value is 1000; values above 1000 are coerced to 1000. A negative
             value is rejected with INVALID_ARGUMENT.
          schema:
            type: integer
            format: int32
        - name: pageToken
          in: query
          description: >-
            A page token received from a previous ListHotLoads call. Provide
            this to retrieve the subsequent page.
             Use the same parent_deployment_id filter, including leaving it unset if it was unset in the previous call.
             A token used with a different filter is rejected with INVALID_ARGUMENT.
             The token is opaque and must not be constructed by clients.
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
components:
  schemas:
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
          description: >-
            A token that can be sent as page_token to retrieve the next page.
            Empty when the final page has been reached.
          type: string
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
          description: >-
            The identity of the target snapshot within the deployment. Must be a
            single path segment.
             Multiple hot-load operations may target the same snapshot identity.
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
          description: >-
            The resolved snapshot chain, oldest first. The first element is
            always a full snapshot.
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
          description: >-
            The aggregate state of the hot-load. `HOT_LOAD_STATE_PENDING` means
            the operation was accepted but replica transitions have not started,
            and `HOT_LOAD_STATE_IN_PROGRESS` means they are underway.
            `HOT_LOAD_STATE_COMPLETED` means every replica serves the target
            snapshot identity. `HOT_LOAD_STATE_FAILED` and
            `HOT_LOAD_STATE_CANCELED` are terminal, and replicas may serve
            different snapshots until a later hot-load completes.
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
      description: >-
        Metadata describing how an incremental snapshot relates to its
        predecessor
      type: object
      properties:
        previousSnapshotIdentity:
          description: The identity of the snapshot this delta was computed against
          type: string
        compressionFormat:
          description: >-
            The compression format of the delta. `COMPRESSION_FORMAT_ZSTD` is a
            Zstandard-compressed XOR delta. This field is required, and
            `COMPRESSION_FORMAT_ZSTD` is the only accepted value.
          type: string
          format: enum
          enum:
            - COMPRESSION_FORMAT_ZSTD
        checksumFormat:
          description: >-
            The checksum format used to verify snapshot integrity. This field is
            required, and `CHECKSUM_FORMAT_ADLER32` is the only accepted value.
          type: string
          format: enum
          enum:
            - CHECKSUM_FORMAT_ADLER32
      required:
        - previousSnapshotIdentity
        - compressionFormat
        - checksumFormat
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
          description: >-
            The ID of the HotLoad operation that introduced this snapshot into
            the chain.
          type: string
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
