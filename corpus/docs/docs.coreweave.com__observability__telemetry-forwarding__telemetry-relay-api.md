# Telemetry Relay API

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api

# Telemetry Relay API

> REST API for managing forwarding endpoints, pipelines, and telemetry streams for CoreWeave Telemetry Relay.

With an access token, you can interact with the Telemetry Relay API using `curl` or any other HTTP client. The API lets you manage forwarding endpoints and pipelines and list telemetry streams. These resources forward CoreWeave audit logs from the managed observability platform to destinations of your choice.

For a conceptual walkthrough of Telemetry Relay (what an endpoint, pipeline, and stream are, and how they wire together), see the [CoreWeave Telemetry Relay overview](https://docs.coreweave.com/observability/telemetry-forwarding/relay.md). For Cloud Console procedures, see [Configure Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/configure.md).

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `[API-ACCESS-TOKEN]` in the examples on each operation page with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * With self-service, you can forward only supported audit logs to HTTPS endpoints or AWS S3 destinations. [Contact Support](https://docs.coreweave.com/support.md) if you want to forward other telemetry or use a different destination type.
> * Write operations (`POST`, `PATCH`, `DELETE`) require the Telemetry Relay Admin role. Read operations (`GET`) require the Telemetry Relay Reader role.
> * For information on required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

## Endpoints

The API exposes three resource families: **forwarding endpoints**, **forwarding pipelines**, and **telemetry streams**. Per-resource operations take the resource's `ref.slug` (a project-scoped human-readable name) as a path parameter, shown as `{ref.slug}` in the path templates below.

### Forwarding endpoints

The following operations manage forwarding endpoints:

| Operation | Method | Endpoint | Description |
| - | - | - | - |
| [List forwarding endpoints](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/list-forwarding-endpoints.md) | `GET` | `/v1beta1/telemetryrelay/endpoints` | List all forwarding endpoints. |
| [Create forwarding endpoint](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/create-forwarding-endpoint.md) | `POST` | `/v1beta1/telemetryrelay/endpoints` | Create a forwarding endpoint. |
| [Get forwarding endpoint](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-forwarding-endpoint.md) | `GET` | `/v1beta1/telemetryrelay/endpoints/{ref.slug}` | Get a forwarding endpoint. |
| [Update forwarding endpoint](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/update-forwarding-endpoint.md) | `PATCH` | `/v1beta1/telemetryrelay/endpoints/{ref.slug}` | Update a forwarding endpoint. |
| [Delete forwarding endpoint](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/delete-forwarding-endpoint.md) | `DELETE` | `/v1beta1/telemetryrelay/endpoints/{ref.slug}` | Delete a forwarding endpoint. |
| [Get forwarding endpoint status](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-forwarding-endpoint-status.md) | `GET` | `/v1beta1/telemetryrelay/endpoints/{ref.slug}:check` | Read the last-known status of a forwarding endpoint. |

### Forwarding pipelines

The following operations manage forwarding pipelines:

| Operation | Method | Endpoint | Description |
| - | - | - | - |
| [List forwarding pipelines](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/list-forwarding-pipelines.md) | `GET` | `/v1beta1/telemetryrelay/pipelines` | List all forwarding pipelines. |
| [Create forwarding pipeline](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/create-forwarding-pipeline.md) | `POST` | `/v1beta1/telemetryrelay/pipelines` | Create a forwarding pipeline. |
| [Get forwarding pipeline](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-forwarding-pipeline.md) | `GET` | `/v1beta1/telemetryrelay/pipelines/{ref.slug}` | Get a forwarding pipeline. |
| [Update forwarding pipeline](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/update-forwarding-pipeline.md) | `PATCH` | `/v1beta1/telemetryrelay/pipelines/{ref.slug}` | Update a forwarding pipeline. |
| [Delete forwarding pipeline](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/delete-forwarding-pipeline.md) | `DELETE` | `/v1beta1/telemetryrelay/pipelines/{ref.slug}` | Delete a forwarding pipeline. |

### Telemetry streams

The following operations list and read telemetry streams:

| Operation | Method | Endpoint | Description |
| - | - | - | - |
| [List telemetry streams](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/list-telemetry-streams.md) | `GET` | `/v1beta1/telemetryrelay/streams` | List all telemetry streams. |
| [Get telemetry stream](https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/get-telemetry-stream.md) | `GET` | `/v1beta1/telemetryrelay/streams/{ref.slug}` | Get a telemetry stream. |

## OpenAPI specification

The complete OpenAPI 3.0 specification for the Telemetry Relay API is embedded below. Expand the code block by clicking "See all" at the bottom, or use the download and copy buttons in the title bar.

```yaml expandable title="Telemetry Relay OpenAPI" theme={"system"}
openapi: 3.0.3
info:
  title: CoreWeave Telemetry Relay API
  version: 0.0.1
  description: The CoreWeave Telemetry Relay API provides programmatic control over Telemetry Relay, CoreWeave's
    managed solution for forwarding telemetry to destinations outside the CoreWeave observability platform.
servers:
- url: https://api.coreweave.com
paths:
  /v1beta1/telemetryrelay/endpoints:
    get:
      operationId: TelemetryRelayService_ListEndpoints
      summary: List forwarding endpoints
      description: Returns every forwarding endpoint in the caller's organization. Each endpoint is a
        destination that pipelines can target. Credentials are never returned in responses.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.ListEndpointsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    post:
      operationId: TelemetryRelayService_CreateEndpoint
      summary: Create forwarding endpoint
      description: Creates a forwarding endpoint. The request body must include `ref.slug` (the unique
        per-organization identifier), `spec` (display name plus exactly one protocol-specific config),
        and the matching credentials block in the same oneof. Credentials are stored encrypted and never
        returned in responses.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreateEndpointRequest'
            examples:
              bearerAuthGzip:
                summary: HTTPS destination with bearer authentication and gzip
                value:
                  ref:
                    slug: audit-https
                  spec:
                    displayName: HTTPS audit logs
                    https:
                      endpoint: https://receiver.example.com/logs
                      compression: COMPRESSION_TYPE_GZIP
                  https:
                    authHeaders:
                      headers:
                        Authorization: Bearer [DESTINATION-TOKEN]
              apiKeyGzip:
                summary: HTTPS destination with an API key and gzip
                value:
                  ref:
                    slug: audit-https
                  spec:
                    displayName: HTTPS audit logs
                    https:
                      endpoint: https://receiver.example.com/logs
                      compression: COMPRESSION_TYPE_GZIP
                  https:
                    authHeaders:
                      headers:
                        X-API-Key: '[DESTINATION-API-KEY]'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreateEndpointResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/endpoints/{ref.slug}:
    get:
      operationId: TelemetryRelayService_GetEndpoint
      summary: Get forwarding endpoint
      description: Returns a single forwarding endpoint by its `ref.slug`, including the protocol-specific
        `spec` and current `status`. Credentials are never returned.
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.GetEndpointResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    delete:
      operationId: TelemetryRelayService_DeleteEndpoint
      summary: Delete forwarding endpoint
      description: 'Deletes a forwarding endpoint identified by `ref.slug`. Delete any pipelines that
        target the endpoint first: if the endpoint is still referenced, the request is rejected with `412`
        (reason `TELEMETRYRELAY_ENDPOINT_IN_USE`) and the response lists the pipelines that must be deleted
        first. Returns `404` (reason `TELEMETRYRELAY_ENDPOINT_NOT_FOUND`) if no endpoint with that slug
        exists.'
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.DeleteEndpointResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    patch:
      operationId: TelemetryRelayService_UpdateEndpoint
      summary: Update forwarding endpoint
      description: Updates a forwarding endpoint identified by `ref.slug`. The request body must include
        the full `spec`. The endpoint's protocol type cannot change after creation. Use `credentialAction`
        to preserve, replace, or clear stored credentials. You can't clear credentials for AWS S3 destinations.
      parameters:
      - name: ref.slug
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointRequest'
            examples:
              disableGzip:
                summary: Disable gzip and preserve stored credentials
                value:
                  ref:
                    slug: audit-https
                  spec:
                    displayName: HTTPS audit logs
                    https:
                      endpoint: https://receiver.example.com/logs
                      compression: COMPRESSION_TYPE_NONE
                  credentialAction: CREDENTIAL_ACTION_PRESERVE
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/endpoints/{ref.slug}:check:
    get:
      operationId: TelemetryRelayService_CheckEndpoint
      summary: Get forwarding endpoint status
      description: Returns the last-known `ForwardingEndpointStatus` for a forwarding endpoint identified
        by `ref.slug`. This reads persisted state. It is not a live connectivity probe and does not verify
        TLS, authentication, or reachability against the destination. Live liveness checking is planned
        for a future release. The `zones_active` field in the response may be empty regardless of actual
        endpoint usage.
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CheckEndpointResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/pipelines:
    get:
      operationId: TelemetryRelayService_ListPipelines
      summary: List forwarding pipelines
      description: Returns every forwarding pipeline in the caller's organization. A pipeline binds a
        `source` stream to a `destination` endpoint and can be enabled or disabled independently.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.ListPipelinesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    post:
      operationId: TelemetryRelayService_CreatePipeline
      summary: Create forwarding pipeline
      description: Creates a forwarding pipeline. The request body must include `ref.slug` and a `spec`
        with the source stream's `slug`, the destination endpoint's `slug`, and `enabled` (true to start
        forwarding immediately).
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/pipelines/{ref.slug}:
    get:
      operationId: TelemetryRelayService_GetPipeline
      summary: Get forwarding pipeline
      description: Returns a single forwarding pipeline by its `ref.slug`, including the source/destination
        references and the current state.
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.GetPipelineResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    delete:
      operationId: TelemetryRelayService_DeletePipeline
      summary: Delete forwarding pipeline
      description: Permanently deletes a forwarding pipeline identified by `ref.slug`. Forwarding stops
        immediately. Underlying endpoints and streams are not affected. Returns `404` (reason `TELEMETRYRELAY_PIPELINE_NOT_FOUND`)
        if no pipeline with that slug exists.
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.DeletePipelineResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
    patch:
      operationId: TelemetryRelayService_UpdatePipeline
      summary: Update forwarding pipeline
      description: Updates a forwarding pipeline identified by `ref.slug`. The request body must include
        the full `spec` (source, destination, enabled). Use this to retarget a pipeline, enable or disable
        forwarding, or temporarily pause delivery.
      parameters:
      - name: ref.slug
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.UpdatePipelineResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/streams:
    get:
      operationId: TelemetryRelayService_ListStreams
      summary: List telemetry streams
      description: Returns every telemetry stream available to the caller's organization. Streams are
        pre-defined categories of platform telemetry (for example, audit logs) that can be forwarded by
        binding them to an endpoint via a pipeline.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.ListStreamsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
  /v1beta1/telemetryrelay/streams/{ref.slug}:
    get:
      operationId: TelemetryRelayService_GetStream
      summary: Get telemetry stream
      description: Returns a single telemetry stream by its `ref.slug`. Includes the stream's `spec` (display
        name, kind, label-selector filter) and `status` (current state and active zones).
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
                $ref: '#/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.GetStreamResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - TelemetryRelayService
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.CheckEndpointResponse:
      type: object
      properties:
        status:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus'
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreateEndpointRequest:
      type: object
      properties:
        ref:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef'
        spec:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec'
        s3:
          description: '`s3` credentials for AWS S3 destinations.'
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.S3Credentials'
        https:
          description: https credentials for HTTPS endpoints, using basic auth or request headers.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.HTTPSCredentials'
      oneOf:
      - required:
        - s3
        properties:
          spec:
            required:
            - s3
        not:
          required:
          - https
      - properties:
          spec:
            required:
            - https
        not:
          required:
          - s3
      required:
      - ref
      - spec
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreateEndpointResponse:
      type: object
      properties:
        endpoint:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint'
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineRequest:
      type: object
      properties:
        ref:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef'
        spec:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec'
      required:
      - ref
      - spec
    coreweave.telemetryrelay.svc.cluster.v1beta1.CreatePipelineResponse:
      type: object
      properties:
        pipeline:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline'
    coreweave.telemetryrelay.svc.cluster.v1beta1.DeleteEndpointResponse:
      type: object
      properties: {}
    coreweave.telemetryrelay.svc.cluster.v1beta1.DeletePipelineResponse:
      type: object
      properties: {}
    coreweave.telemetryrelay.svc.cluster.v1beta1.GetEndpointResponse:
      type: object
      properties:
        endpoint:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint'
    coreweave.telemetryrelay.svc.cluster.v1beta1.GetPipelineResponse:
      type: object
      properties:
        pipeline:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline'
    coreweave.telemetryrelay.svc.cluster.v1beta1.GetStreamResponse:
      type: object
      properties:
        stream:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStream'
    coreweave.telemetryrelay.svc.cluster.v1beta1.ListEndpointsResponse:
      type: object
      properties:
        endpoints:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint'
    coreweave.telemetryrelay.svc.cluster.v1beta1.ListPipelinesResponse:
      type: object
      properties:
        pipelines:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline'
    coreweave.telemetryrelay.svc.cluster.v1beta1.ListStreamsResponse:
      type: object
      properties:
        streams:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStream'
    coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointRequest:
      type: object
      properties:
        ref:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef'
        spec:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec'
        credentialAction:
          description: Controls how the endpoint's stored credentials are handled during the update. `CREDENTIAL_ACTION_PRESERVE`
            keeps the existing credentials unchanged. `CREDENTIAL_ACTION_REPLACE` replaces them with the
            credentials supplied in this request. Credentials must be provided when this action is used.
            `CREDENTIAL_ACTION_CLEAR` removes the stored credentials, but it isn't supported for AWS S3
            destinations. The underlying enum also declares `CREDENTIAL_ACTION_UNSPECIFIED` (its zero
            value); omit the field rather than sending it.
          type: string
          format: enum
          enum:
          - CREDENTIAL_ACTION_PRESERVE
          - CREDENTIAL_ACTION_REPLACE
          - CREDENTIAL_ACTION_CLEAR
        s3:
          description: '`s3` credentials for AWS S3 destinations.'
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.S3Credentials'
        https:
          description: https credentials for HTTPS endpoints, using basic auth or request headers.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.HTTPSCredentials'
      not:
        required:
        - s3
        - https
      required:
      - ref
      - spec
    coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointResponse:
      type: object
      properties:
        endpoint:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint'
    coreweave.telemetryrelay.svc.cluster.v1beta1.UpdatePipelineResponse:
      type: object
      properties:
        pipeline:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline'
    coreweave.telemetryrelay.types.v1beta1.AuthHeadersCredentials:
      description: "AuthHeadersCredentials contains custom HTTP headers for authentication.\n\n Used for\
        \ APIs that require authentication via custom headers (e.g., X-API-Key, X-Auth-Token).\n All header\
        \ values are encrypted at rest and in transit.\n Header names are case-insensitive per HTTP specification."
      type: object
      properties:
        headers:
          description: 'Map of 1 to 20 HTTP header names to authentication values. Values are write-only
            and never returned in responses.


            Names must contain 1 to 255 characters, match ``^[A-Za-z0-9!#$%&''*+.^_`|~-]+$``, and be unique
            ignoring case.

            Values must contain 1 to 2048 characters and match `^[\x21-\x2B\x2D-\x7E]([\x09\x20\x21-\x2B\x2D-\x7E]*[\x21-\x2B\x2D-\x7E])?$`:
            visible ASCII except commas, with spaces and tabs allowed only internally.

            Neither names nor values may contain `${`. The connector sets `Host`, `Content-Length`, `Content-Type`,
            `Connection`, and `Transfer-Encoding`; these names cannot be overridden, regardless of case.'
          type: object
          additionalProperties:
            type: string
      required:
      - headers
    coreweave.telemetryrelay.types.v1beta1.BasicAuthCredentials:
      description: BasicAuthCredentials contains username and password for HTTP Basic authentication.
        This is a reusable credential type for any endpoint that uses HTTP Basic authentication, including
        generic HTTPS endpoints. Credentials are encrypted at rest and in transit.
      type: object
      properties:
        username:
          description: username for HTTP Basic authentication. Must be non-empty.
          type: string
          writeOnly: true
        password:
          description: "password for HTTP Basic authentication.\n This field is write-only and never returned\
            \ in responses."
          type: string
          writeOnly: true
      required:
      - username
      - password
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint:
      description: ForwardingEndpoint represents a destination where telemetry data can be forwarded.
        Endpoints are organization-scoped and identified by a unique slug. Endpoints forward to HTTPS
        endpoints or AWS S3 destinations.
      type: object
      properties:
        ref:
          description: ref uniquely identifies this endpoint within the organization.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef'
        spec:
          description: spec contains the desired configuration for this endpoint.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec'
        status:
          description: "status reflects the current state of the endpoint.\n This field is output-only\
            \ and managed by the system."
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus'
          readOnly: true
      required:
      - ref
      - spec
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef:
      description: "ForwardingEndpointRef uniquely identifies a forwarding endpoint within an organization.\n\
        \n Endpoints are referenced by a human-readable slug that must be unique per organization."
      type: object
      properties:
        slug:
          description: "slug is a unique identifier for the endpoint within the organization.\n Must be\
            \ 3-32 characters, start with alphanumeric, and contain only alphanumeric and hyphens."
          type: string
          maxLength: 32
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
      required:
      - slug
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec:
      description: Configuration for a forwarding endpoint. Includes a human-readable `displayName` and
        exactly one protocol-specific config. The protocol type is fixed at creation time and cannot be
        changed afterward.
      type: object
      properties:
        displayName:
          description: "display_name is a human-readable name for this endpoint.\n Used for display purposes\
            \ in UIs and logs."
          type: string
        s3:
          description: '`s3` configures an AWS S3 destination for archiving telemetry data.'
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.S3Config'
        https:
          description: https configures a generic HTTPS endpoint for custom integrations.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.HTTPSConfig'
      oneOf:
      - required:
        - s3
      - required:
        - https
      required:
      - displayName
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus:
      description: "ForwardingEndpointStatus reflects the current operational state of an endpoint.\n\n\
        \ Status is managed by the system and includes connection state, timestamps,\n and information\
        \ about which zones/clusters are actively using the endpoint."
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
          description: Current operational state of the endpoint. `PENDING` while the endpoint is being
            provisioned, `CONNECTED` once the endpoint is operational and receiving data, `ERROR` when
            the endpoint encountered an error and is not operational, `UNSPECIFIED` when the state has
            not been set.
          type: string
          format: enum
          enum:
          - FORWARDING_ENDPOINT_STATE_UNSPECIFIED
          - FORWARDING_ENDPOINT_STATE_PENDING
          - FORWARDING_ENDPOINT_STATE_CONNECTED
          - FORWARDING_ENDPOINT_STATE_ERROR
          readOnly: true
        stateMessage:
          description: "state_message provides additional context about the current state.\n Especially\
            \ useful when state is ERROR to describe what went wrong."
          type: string
          readOnly: true
        zonesActive:
          description: "zones_active lists which zones and clusters are actively forwarding\n data to\
            \ this endpoint."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ZoneClusterStatus'
          readOnly: true
        credentialsConfigured:
          description: "credentials_configured indicates whether credentials have been set for this endpoint.\n\
            \ Does not indicate if the credentials are valid, only that they exist."
          type: boolean
          readOnly: true
        credentialsUpdatedAt:
          description: "credentials_updated_at is when credentials were last set or updated.\n Unset if\
            \ credentials have never been configured."
          type: string
          format: date-time
          readOnly: true
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ClusterStatus:
      description: ClusterStatus identifies a single cluster using this endpoint.
      type: object
      properties:
        id:
          description: id is the cluster's unique identifier.
          type: string
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
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus_ClusterStatus'
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipeline:
      type: object
      properties:
        ref:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef'
        spec:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec'
        status:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus'
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineRef:
      type: object
      properties:
        slug:
          description: slug is a unique identifier for the pipeline within the organization. Must be 3-65
            characters, start with alphanumeric, and contain only alphanumeric and hyphens.
          type: string
          maxLength: 65
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineSpec:
      description: 'Configuration for a forwarding pipeline. `source` references a `TelemetryStream` by
        slug; `destination` references a `ForwardingEndpoint` by slug. Set `enabled: false` to pause forwarding
        without deleting the pipeline.'
      type: object
      properties:
        source:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef'
        destination:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef'
        enabled:
          type: boolean
        zoneSlugs:
          description: "zone_slugs restricts which zones this pipeline provisions connectors in.\n Empty\
            \ means all zones with an active cluster registration for the\n organization. Set at creation\
            \ and immutable thereafter — UpdatePipeline\n rejects any request whose zone_slugs differs\
            \ from the stored value.\n To change zone placement, delete and recreate the pipeline."
          type: array
          items:
            type: string
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
          description: Current operational state of the pipeline. `PENDING` while provisioning, `ACTIVE`
            once data is flowing, `ERROR` if forwarding has failed, `STOPPED` if `spec.enabled` is false
            or the pipeline has been deactivated, `UNSPECIFIED` when the state has not been set.
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
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ZoneClusterStatus'
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ClusterStatus:
      type: object
      properties:
        id:
          type: string
    coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ZoneClusterStatus:
      type: object
      properties:
        zoneSlug:
          type: string
        clusters:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingPipelineStatus_ClusterStatus'
    coreweave.telemetryrelay.types.v1beta1.HTTPSConfig:
      description: Configures an HTTPS destination for forwarding telemetry. To authenticate to the destination,
        provide `HTTPSCredentials` with either `basicAuth` or `authHeaders` when creating or updating
        the endpoint. If no credentials are stored for the endpoint, requests are sent without authentication.
      type: object
      properties:
        endpoint:
          description: "endpoint is the URL of the HTTPS endpoint.\n Must be a valid HTTPS URL; plain\
            \ HTTP is rejected.\n Targets that resolve to loopback, private, or link-local addresses are\n\
            \ rejected by the service at submission time to prevent SSRF (see O11Y-2851)."
          type: string
        tls:
          description: "tls configures TLS settings for connecting to the endpoint.\n Optional - omit\
            \ when using system default trust."
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TLSConfig'
        compression:
          description: 'Optional compression setting for HTTPS delivery. Omit the field or use `COMPRESSION_TYPE_UNSPECIFIED`
            for uncompressed delivery. `COMPRESSION_TYPE_NONE` explicitly disables compression. Both send
            no Content-Encoding header, but UNSPECIFIED is omitted from responses and NONE is returned
            explicitly. `COMPRESSION_TYPE_GZIP` compresses the complete NDJSON body and sets `Content-Encoding:
            gzip`; the destination must accept gzip-compressed request bodies. Batching and Content-Type
            are unchanged. Compression level is service-managed. Endpoint updates replace the full spec:
            omitting this field resets compression to uncompressed delivery.'
          type: string
          format: enum
          enum:
          - COMPRESSION_TYPE_UNSPECIFIED
          - COMPRESSION_TYPE_NONE
          - COMPRESSION_TYPE_GZIP
      required:
      - endpoint
    coreweave.telemetryrelay.types.v1beta1.HTTPSCredentials:
      description: Credentials for authenticating delivery to an HTTPS destination. Provide either `basicAuth`
        or `authHeaders`. For bearer authentication, use `authHeaders.headers` with an `Authorization`
        header whose value is `Bearer` followed by the destination token. For a custom API key, use the
        header name required by the destination, such as `X-API-Key`. Header authentication is supported
        only for HTTPS destinations. These credentials are separate from the CoreWeave API access token
        used to call the Telemetry Relay API.
      type: object
      properties:
        basicAuth:
          description: basic_auth provides HTTP Basic authentication credentials.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.BasicAuthCredentials'
        authHeaders:
          description: auth_headers provides custom HTTP header authentication.
          allOf:
          - $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.AuthHeadersCredentials'
    coreweave.telemetryrelay.types.v1beta1.LabelSelector:
      type: object
      properties:
        include:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.StringList'
        exclude:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.StringList'
    coreweave.telemetryrelay.types.v1beta1.S3Config:
      description: '`S3Config` configures an AWS S3 destination for archiving telemetry data. Data is
        written to the specified bucket and optional prefix. `S3Credentials` must be provided when creating
        the destination and cannot be cleared afterward.'
      type: object
      properties:
        uri:
          description: '`uri` is the S3 URI where data is written. Use the format `s3://[BUCKET-NAME]/[PREFIX]/`.
            Replace `[BUCKET-NAME]` with the bucket name and `[PREFIX]` with the optional prefix.'
          type: string
          maxLength: 2048
          minLength: 1
          pattern: ^s3://[a-z0-9][a-z0-9.-]*[a-z0-9](/.*)?$
        region:
          description: '`region` is the AWS region where the bucket is located. Required.'
          type: string
          maxLength: 64
          minLength: 1
      required:
      - uri
      - region
    coreweave.telemetryrelay.types.v1beta1.S3Credentials:
      description: '`S3Credentials` contains AWS credentials for accessing an AWS S3 bucket. Credentials
        are encrypted and never returned in API responses.'
      type: object
      properties:
        accessKeyId:
          description: '`accessKeyId` is the AWS access key ID. Long-term credentials typically begin
            with `AKIA`. Required.'
          type: string
          maxLength: 128
          minLength: 16
          pattern: ^[A-Z0-9]+$
          writeOnly: true
        secretAccessKey:
          description: '`secretAccessKey` is the AWS secret access key. This field is write-only and never
            returned in responses. Required.'
          type: string
          maxLength: 1024
          minLength: 1
          writeOnly: true
        sessionToken:
          description: '`sessionToken` is an AWS session token for temporary credentials. Provide it when
            using temporary credentials from AWS STS or IAM roles. Omit it for long-term IAM user credentials.'
          type: string
          maxLength: 2048
          writeOnly: true
      required:
      - accessKeyId
      - secretAccessKey
    coreweave.telemetryrelay.types.v1beta1.StringList:
      type: object
      properties:
        values:
          type: array
          items:
            type: string
    coreweave.telemetryrelay.types.v1beta1.TLSConfig:
      description: "TLSConfig configures TLS settings for secure connections.\n\n Used when connecting\
        \ to endpoints that require custom CA certificates\n or specific TLS configuration."
      type: object
      properties:
        certificateAuthorityData:
          description: "certificate_authority_data contains the PEM-encoded CA certificate bundle.\n Must\
            \ be base64-encoded when transmitted.\n If not provided, the system's default trust store\
            \ is used."
          type: string
    coreweave.telemetryrelay.types.v1beta1.TelemetryStream:
      type: object
      properties:
        ref:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef'
        spec:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamSpec'
        status:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus'
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamRef:
      type: object
      properties:
        slug:
          type: string
          maxLength: 32
          minLength: 3
          pattern: ^[a-zA-Z0-9][a-zA-Z0-9-]+$
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamSpec:
      description: Configuration for a telemetry stream. `displayName` is a human-readable label; `filter`
        narrows the stream by label selectors; `kind` declares the category of telemetry the stream carries.
      type: object
      properties:
        displayName:
          type: string
        filter:
          $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.LabelSelector'
        kind:
          description: 'Category of telemetry carried by the stream. The API forwards audit logs, so `STREAM_KIND_LOGS`
            is the only available kind. The underlying enum also defines `STREAM_KIND_METRICS`, but metrics
            streams are not supported: the API rejects the value and never returns it. Required.'
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
          description: Current state of the stream. `ACTIVE` when data is being collected, `INACTIVE`
            when collection is paused, `ERROR` if collection has failed, `UNSPECIFIED` when the state
            has not been set.
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
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ZoneClusterStatus'
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ClusterStatus:
      type: object
      properties:
        id:
          type: string
    coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ZoneClusterStatus:
      type: object
      properties:
        zoneSlug:
          type: string
        clusters:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.telemetryrelay.types.v1beta1.TelemetryStreamStatus_ClusterStatus'
    google.protobuf.Any:
      description: Contains an arbitrary serialized message along with a @type that describes the type
        of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    google.rpc.Status:
      description: 'The `Status` type defines a logical error model that is suitable for different programming
        environments, including REST APIs and RPC APIs. It is used by [gRPC](https://github.com/grpc).
        Each `Status` message contains three pieces of data: error code, error message, and error details.
        You can find out more about this error model and how to work with it in the [API Design Guide](https://cloud.google.com/apis/design/errors).'
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
            $ref: '#/components/schemas/google.protobuf.Any'
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [CW-API-TOKEN]
tags:
- name: TelemetryRelayService
  description: 'Endpoints for managing forwarding endpoints, forwarding pipelines, and reading available
    telemetry streams. Use these endpoints to configure how CoreWeave platform telemetry is forwarded
    to destinations outside the CoreWeave observability platform. For Cloud Console procedures, see the
    [Telemetry Relay configure guide](/observability/telemetry-forwarding/configure).


    With self-service, you can forward only supported audit logs to HTTPS endpoints or AWS S3 destinations.
    To forward other telemetry or use a different destination type, [contact Support](/support).


    Write operations (`POST`, `PATCH`, `DELETE`) require the `Telemetry Relay Admin` role; read operations
    (`GET`) require the `Telemetry Relay Reader` role.'
security:
- bearerAuth: []
```
