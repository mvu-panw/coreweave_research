# List hot-load replicas

Source: https://docs.coreweave.com/products/inference/reference/api-overview/hotloadservice/list-hot-load-replicas

# List hot-load replicas

> Read per-replica progress for a hot-load, including the checkpoint each replica serves.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Per-replica progress is a sub-resource: `GetHotLoad` returns
the aggregate state only and does not embed replica status,
so poll this endpoint separately. A replica is caught up when
its `state` is `READY` and its `currentSnapshotIdentity`
matches the hot-load's target identity.

```bash title="Example request" theme={{"system"}}
curl -X GET https://api.coreweave.com/v1alpha1/inference/hotLoads/{HOT_LOAD_ID}/replicas \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml get /v1alpha1/inference/hotLoads/{hotLoadId}/replicas
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
  /v1alpha1/inference/hotLoads/{hotLoadId}/replicas:
    get:
      tags:
        - HotLoadService
      summary: List hot-load replicas
      description: >-
        Returns the replicas of one hot-load, ordered by zone and name, in
        pages.
      operationId: HotLoadService_ListHotLoadReplicas
      parameters:
        - name: hotLoadId
          in: path
          description: The ID of the hot-load whose replicas to list
          required: true
          schema:
            type: string
        - name: maxPageSize
          in: query
          description: >-
            The maximum number of replicas to return. The service may return
            fewer than this value. If unspecified or 0,
             at most 50 replicas are returned. The maximum value is 1000; values above 1000 are coerced to 1000. A
             negative value is rejected with INVALID_ARGUMENT.
          schema:
            type: integer
            format: int32
        - name: pageToken
          in: query
          description: >-
            A page token received from a previous ListHotLoadReplicas call.
            Provide this to retrieve the subsequent page.
             Use the same hot_load_id and organization as the previous call; otherwise, the token is rejected with
             INVALID_ARGUMENT. The token is opaque and must not be constructed by clients.
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
components:
  schemas:
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
          description: >-
            The state of this replica's checkpoint transition. `PENDING_UPDATE`
            means the replica serves a different snapshot identity and its
            transition has not started. `UPDATING` means the transition is in
            progress. `READY` means the replica serves the target snapshot
            identity. `ERROR` means the transition failed, and `errorReason`
            carries the cause.
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
          description: >-
            The time the replica began transitioning to the target snapshot, set
            when it first enters UPDATING. Unset
             while the replica is still PENDING_UPDATE.
          type: string
          format: date-time
          readOnly: true
        finishedAt:
          description: >-
            The time the replica reached a terminal state (READY or ERROR).
            Unset until then, and unset again if a retry
             moves the replica back out of a terminal state.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: >-
            The time the replica status was last updated, whether or not its
            state changed
          type: string
          format: date-time
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
