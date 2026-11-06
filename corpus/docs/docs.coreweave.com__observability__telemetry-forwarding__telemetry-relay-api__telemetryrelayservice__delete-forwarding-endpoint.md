# Delete forwarding endpoint

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/delete-forwarding-endpoint

# Delete forwarding endpoint

> Deletes a forwarding endpoint identified by `ref.slug`. Delete any pipelines that target the endpoint first: if the endpoint is still referenced, the request is rejected with `412` (reason `TELEMETRYRELAY_ENDPOINT_IN_USE`) and the response lists the pipelines that must be deleted first. Returns `404` (reason `TELEMETRYRELAY_ENDPOINT_NOT_FOUND`) if no endpoint with that slug exists.



## OpenAPI

````yaml /openapi/o11y/openapi.yaml delete /v1beta1/telemetryrelay/endpoints/{ref.slug}
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
  /v1beta1/telemetryrelay/endpoints/{ref.slug}:
    delete:
      tags:
        - TelemetryRelayService
      summary: Delete forwarding endpoint
      description: >-
        Deletes a forwarding endpoint identified by `ref.slug`. Delete any
        pipelines that target the endpoint first: if the endpoint is still
        referenced, the request is rejected with `412` (reason
        `TELEMETRYRELAY_ENDPOINT_IN_USE`) and the response lists the pipelines
        that must be deleted first. Returns `404` (reason
        `TELEMETRYRELAY_ENDPOINT_NOT_FOUND`) if no endpoint with that slug
        exists.
      operationId: TelemetryRelayService_DeleteEndpoint
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
                  #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.DeleteEndpointResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.DeleteEndpointResponse:
      type: object
      properties: {}
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [CW-API-TOKEN]

````
