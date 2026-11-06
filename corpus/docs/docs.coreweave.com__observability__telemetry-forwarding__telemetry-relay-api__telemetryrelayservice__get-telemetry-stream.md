# Get telemetry stream

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-telemetry-stream

# Get telemetry stream

> Returns a single telemetry stream by its `ref.slug`. Includes the stream's `spec` (display name, kind, label-selector filter) and `status` (current state and active zones).



## OpenAPI

````yaml /openapi/o11y/openapi.yaml get /v1beta1/telemetryrelay/streams/{ref.slug}
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
  /v1beta1/telemetryrelay/streams/{ref.slug}:
    get:
      tags:
        - TelemetryRelayService
      summary: Get telemetry stream
      description: >-
        Returns a single telemetry stream by its `ref.slug`. Includes the
        stream's `spec` (display name, kind, label-selector filter) and `status`
        (current state and active zones).
      operationId: TelemetryRelayService_GetStream
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
                  #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.GetStreamResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.GetStreamResponse:
      type: object
      properties:
        stream:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStream
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
    coreweave.telemetryrelay.types.v1beta1.TelemetryStream:
      type: object
      properties:
        ref:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef
        spec:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamSpec
        status:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus
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
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef:
      type: object
      properties:
        slug:
          type: string
          maxLength: 32
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamSpec:
      description: >-
        Configuration for a telemetry stream. `displayName` is a human-readable
        label; `filter` narrows the stream by label selectors; `kind` declares
        the category of telemetry the stream carries.
      type: object
      properties:
        displayName:
          type: string
        filter:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.LabelSelector
        kind:
          description: >-
            Category of telemetry carried by the stream. The API forwards audit
            logs, so `STREAM_KIND_LOGS` is the only available kind. The
            underlying enum also defines `STREAM_KIND_METRICS`, but metrics
            streams are not supported: the API rejects the value and never
            returns it. Required.
          type: string
          format: enum
          enum:
            - STREAM_KIND_LOGS
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus:
      type: object
      properties:
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        state:
          description: >-
            Current state of the stream. `ACTIVE` when data is being collected,
            `INACTIVE` when collection is paused, `ERROR` if collection has
            failed, `UNSPECIFIED` when the state has not been set.
          type: string
          format: enum
          enum:
            - TELEMETRY_STREAM_STATE_UNSPECIFIED
            - TELEMETRY_STREAM_STATE_ACTIVE
            - TELEMETRY_STREAM_STATE_ERROR
            - TELEMETRY_STREAM_STATE_INACTIVE
          readOnly: true
        stateMessage:
          type: string
        zonesActive:
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ZoneClusterStatus
    coreweave.telemetryrelay.types.v1beta1.LabelSelector:
      type: object
      properties:
        include:
          type: object
          additionalProperties:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.StringList
        exclude:
          type: object
          additionalProperties:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.StringList
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ZoneClusterStatus:
      type: object
      properties:
        zoneSlug:
          type: string
        clusters:
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ClusterStatus
    coreweave.telemetryrelay.types.v1beta1.StringList:
      type: object
      properties:
        values:
          type: array
          items:
            type: string
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ClusterStatus:
      type: object
      properties:
        id:
          type: string
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [CW-API-TOKEN]

````
