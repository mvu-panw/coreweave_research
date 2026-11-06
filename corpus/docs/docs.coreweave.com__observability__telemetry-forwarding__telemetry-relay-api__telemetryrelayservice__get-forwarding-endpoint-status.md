# Get forwarding endpoint status

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-forwarding-endpoint-status

# Get forwarding endpoint status

> Returns the last-known `ForwardingEndpointStatus` for a forwarding endpoint identified by `ref.slug`. This reads persisted state. It is not a live connectivity probe and does not verify TLS, authentication, or reachability against the destination. Live liveness checking is planned for a future release. The `zones_active` field in the response may be empty regardless of actual endpoint usage.



## OpenAPI

````yaml /openapi/o11y/openapi.yaml get /v1beta1/telemetryrelay/endpoints/{ref.slug}:check
openapi: 3.0.3
info:
  title: CoreWeave Telemetry Relay API
  version: 0.0.1
  description: >-
    The CoreWeave Telemetry Relay API provides programmatic control over
    Telemetry Relay, CoreWeave's managed solution for forwarding telemetry to
    destinations outside the CoreWeave observability platform.
servers:
  - url: https://api.coreweave.com
security:
  - bearerAuth: []
tags:
  - name: TelemetryRelayService
    description: >-
      Endpoints for managing forwarding endpoints, forwarding pipelines, and
      reading available telemetry streams. Use these endpoints to configure how
      CoreWeave platform telemetry is forwarded to destinations outside the
      CoreWeave observability platform. For Cloud Console procedures, see the
      [Telemetry Relay configure
      guide](/observability/telemetry-forwarding/configure).


      With self-service, you can forward only supported audit logs to HTTPS
      endpoints or AWS S3 destinations. To forward other telemetry or use a
      different destination type, [contact Support](/support).


      Write operations (`POST`, `PATCH`, `DELETE`) require the `Telemetry Relay
      Admin` role; read operations (`GET`) require the `Telemetry Relay Reader`
      role.
paths:
  /v1beta1/telemetryrelay/endpoints/{ref.slug}:check:
    get:
      tags:
        - TelemetryRelayService
      summary: Get forwarding endpoint status
      description: >-
        Returns the last-known `ForwardingEndpointStatus` for a forwarding
        endpoint identified by `ref.slug`. This reads persisted state. It is not
        a live connectivity probe and does not verify TLS, authentication, or
        reachability against the destination. Live liveness checking is planned
        for a future release. The `zones_active` field in the response may be
        empty regardless of actual endpoint usage.
      operationId: TelemetryRelayService_CheckEndpoint
      parameters:
        - name: ref.slug
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CheckEndpointResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.CheckEndpointResponse:
      type: object
      properties:
        status:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus
    google.rpc.Status:
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
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
            $ref: '#/components/schemas/google.protobuf.Any'
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus:
      description: >-
        ForwardingEndpointStatus reflects the current operational state of an
        endpoint.

         Status is managed by the system and includes connection state, timestamps,
         and information about which zones/clusters are actively using the endpoint.
      type: object
      properties:
        createdAt:
          description: created_at is when the endpoint was first created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: updated_at is when the endpoint configuration was last modified.
          type: string
          format: date-time
          readOnly: true
        state:
          description: >-
            Current operational state of the endpoint. `PENDING` while the
            endpoint is being provisioned, `CONNECTED` once the endpoint is
            operational and receiving data, `ERROR` when the endpoint
            encountered an error and is not operational, `UNSPECIFIED` when the
            state has not been set.
          type: string
          format: enum
          enum:
            - FORWARDING_ENDPOINT_STATE_UNSPECIFIED
            - FORWARDING_ENDPOINT_STATE_PENDING
            - FORWARDING_ENDPOINT_STATE_CONNECTED
            - FORWARDING_ENDPOINT_STATE_ERROR
          readOnly: true
        stateMessage:
          description: |-
            state_message provides additional context about the current state.
             Especially useful when state is ERROR to describe what went wrong.
          type: string
          readOnly: true
        zonesActive:
          description: |-
            zones_active lists which zones and clusters are actively forwarding
             data to this endpoint.
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ZoneClusterStatus
          readOnly: true
        credentialsConfigured:
          description: >-
            credentials_configured indicates whether credentials have been set
            for this endpoint.
             Does not indicate if the credentials are valid, only that they exist.
          type: boolean
          readOnly: true
        credentialsUpdatedAt:
          description: |-
            credentials_updated_at is when credentials were last set or updated.
             Unset if credentials have never been configured.
          type: string
          format: date-time
          readOnly: true
    google.protobuf.Any:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ZoneClusterStatus:
      description: ZoneClusterStatus groups clusters by zone that are using this endpoint.
      type: object
      properties:
        zoneSlug:
          description: zone_slug identifies the zone.
          type: string
        clusters:
          description: clusters is the list of clusters in this zone using the endpoint.
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ClusterStatus
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ClusterStatus:
      description: ClusterStatus identifies a single cluster using this endpoint.
      type: object
      properties:
        id:
          description: id is the cluster's unique identifier.
          type: string
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [CW-API-TOKEN]

````
