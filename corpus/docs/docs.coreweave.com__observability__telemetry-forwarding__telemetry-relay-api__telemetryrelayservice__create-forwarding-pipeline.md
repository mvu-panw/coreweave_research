# Create forwarding pipeline

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/create-forwarding-pipeline

# Create forwarding pipeline

> Creates a forwarding pipeline. The request body must include `ref.slug` and a `spec` with the source stream's `slug`, the destination endpoint's `slug`, and `enabled` (true to start forwarding immediately).



## OpenAPI

````yaml /openapi/o11y/openapi.yaml post /v1beta1/telemetryrelay/pipelines
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
  /v1beta1/telemetryrelay/pipelines:
    post:
      tags:
        - TelemetryRelayService
      summary: Create forwarding pipeline
      description: >-
        Creates a forwarding pipeline. The request body must include `ref.slug`
        and a `spec` with the source stream's `slug`, the destination endpoint's
        `slug`, and `enabled` (true to start forwarding immediately).
      operationId: TelemetryRelayService_CreatePipeline
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineRequest
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineRequest:
      type: object
      properties:
        ref:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef
        spec:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec
      required:
        - ref
        - spec
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineResponse:
      type: object
      properties:
        pipeline:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline
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
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef:
      type: object
      properties:
        slug:
          description: >-
            slug is a unique identifier for the pipeline within the
            organization. Must be 3-65 characters, start with alphanumeric, and
            contain only alphanumeric and hyphens.
          type: string
          maxLength: 65
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec:
      description: >-
        Configuration for a forwarding pipeline. `source` references a
        `TelemetryStream` by slug; `destination` references a
        `ForwardingEndpoint` by slug. Set `enabled: false` to pause forwarding
        without deleting the pipeline.
      type: object
      properties:
        source:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef
        destination:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef
        enabled:
          type: boolean
        zoneSlugs:
          description: >-
            zone_slugs restricts which zones this pipeline provisions connectors
            in.
             Empty means all zones with an active cluster registration for the
             organization. Set at creation and immutable thereafter — UpdatePipeline
             rejects any request whose zone_slugs differs from the stored value.
             To change zone placement, delete and recreate the pipeline.
          type: array
          items:
            type: string
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline:
      type: object
      properties:
        ref:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef
        spec:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec
        status:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus
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
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef:
      description: >-
        ForwardingEndpointRef uniquely identifies a forwarding endpoint within
        an organization.

         Endpoints are referenced by a human-readable slug that must be unique per organization.
      type: object
      properties:
        slug:
          description: >-
            slug is a unique identifier for the endpoint within the
            organization.
             Must be 3-32 characters, start with alphanumeric, and contain only alphanumeric and hyphens.
          type: string
          maxLength: 32
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
      required:
        - slug
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus:
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
            Current operational state of the pipeline. `PENDING` while
            provisioning, `ACTIVE` once data is flowing, `ERROR` if forwarding
            has failed, `STOPPED` if `spec.enabled` is false or the pipeline has
            been deactivated, `UNSPECIFIED` when the state has not been set.
          type: string
          format: enum
          enum:
            - FORWARDING_PIPELINE_STATE_UNSPECIFIED
            - FORWARDING_PIPELINE_STATE_PENDING
            - FORWARDING_PIPELINE_STATE_ACTIVE
            - FORWARDING_PIPELINE_STATE_ERROR
            - FORWARDING_PIPELINE_STATE_STOPPED
          readOnly: true
        stateMessage:
          type: string
        zonesActive:
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ZoneClusterStatus
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ZoneClusterStatus:
      type: object
      properties:
        zoneSlug:
          type: string
        clusters:
          type: array
          items:
            $ref: >-
              #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ClusterStatus
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ClusterStatus:
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
