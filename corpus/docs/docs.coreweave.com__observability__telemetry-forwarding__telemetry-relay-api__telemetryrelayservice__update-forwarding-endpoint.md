# Update forwarding endpoint

Source: https://docs.coreweave.com/observability/telemetry-forwarding/telemetry-relay-api/telemetryrelayservice/update-forwarding-endpoint

# Update forwarding endpoint

> Updates a forwarding endpoint identified by `ref.slug`. The request body must include the full `spec`. The endpoint's protocol type cannot change after creation. Use `credentialAction` to preserve, replace, or clear stored credentials. You can't clear credentials for AWS S3 destinations.



## OpenAPI

````yaml /openapi/o11y/openapi.yaml patch /v1beta1/telemetryrelay/endpoints/{ref.slug}
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
    patch:
      tags:
        - TelemetryRelayService
      summary: Update forwarding endpoint
      description: >-
        Updates a forwarding endpoint identified by `ref.slug`. The request body
        must include the full `spec`. The endpoint's protocol type cannot change
        after creation. Use `credentialAction` to preserve, replace, or clear
        stored credentials. You can't clear credentials for AWS S3 destinations.
      operationId: TelemetryRelayService_UpdateEndpoint
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
              $ref: >-
                #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointRequest
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
                $ref: >-
                  #/components/schemas/coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.telemetryrelay.svc.cluster.v1beta1.UpdateEndpointRequest:
      type: object
      properties:
        ref:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef
        spec:
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec
        credentialAction:
          description: >-
            Controls how the endpoint's stored credentials are handled during
            the update. `CREDENTIAL_ACTION_PRESERVE` keeps the existing
            credentials unchanged. `CREDENTIAL_ACTION_REPLACE` replaces them
            with the credentials supplied in this request. Credentials must be
            provided when this action is used. `CREDENTIAL_ACTION_CLEAR` removes
            the stored credentials, but it isn't supported for AWS S3
            destinations. The underlying enum also declares
            `CREDENTIAL_ACTION_UNSPECIFIED` (its zero value); omit the field
            rather than sending it.
          type: string
          format: enum
          enum:
            - CREDENTIAL_ACTION_PRESERVE
            - CREDENTIAL_ACTION_REPLACE
            - CREDENTIAL_ACTION_CLEAR
        s3:
          description: '`s3` credentials for AWS S3 destinations.'
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.S3Credentials
        https:
          description: >-
            https credentials for HTTPS endpoints, using basic auth or request
            headers.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.HTTPSCredentials
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
          $ref: >-
            #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint
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
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec:
      description: >-
        Configuration for a forwarding endpoint. Includes a human-readable
        `displayName` and exactly one protocol-specific config. The protocol
        type is fixed at creation time and cannot be changed afterward.
      type: object
      properties:
        displayName:
          description: |-
            display_name is a human-readable name for this endpoint.
             Used for display purposes in UIs and logs.
          type: string
        s3:
          description: '`s3` configures an AWS S3 destination for archiving telemetry data.'
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.S3Config
        https:
          description: https configures a generic HTTPS endpoint for custom integrations.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.HTTPSConfig
      oneOf:
        - required:
            - s3
        - required:
            - https
      required:
        - displayName
    coreweave.telemetryrelay.types.v1beta1.S3Credentials:
      description: >-
        `S3Credentials` contains AWS credentials for accessing an AWS S3 bucket.
        Credentials are encrypted and never returned in API responses.
      type: object
      properties:
        accessKeyId:
          description: >-
            `accessKeyId` is the AWS access key ID. Long-term credentials
            typically begin with `AKIA`. Required.
          type: string
          maxLength: 128
          minLength: 16
          pattern: ^[A-Z0-9]+$
          writeOnly: true
        secretAccessKey:
          description: >-
            `secretAccessKey` is the AWS secret access key. This field is
            write-only and never returned in responses. Required.
          type: string
          maxLength: 1024
          minLength: 1
          writeOnly: true
        sessionToken:
          description: >-
            `sessionToken` is an AWS session token for temporary credentials.
            Provide it when using temporary credentials from AWS STS or IAM
            roles. Omit it for long-term IAM user credentials.
          type: string
          maxLength: 2048
          writeOnly: true
      required:
        - accessKeyId
        - secretAccessKey
    coreweave.telemetryrelay.types.v1beta1.HTTPSCredentials:
      description: >-
        Credentials for authenticating delivery to an HTTPS destination. Provide
        either `basicAuth` or `authHeaders`. For bearer authentication, use
        `authHeaders.headers` with an `Authorization` header whose value is
        `Bearer` followed by the destination token. For a custom API key, use
        the header name required by the destination, such as `X-API-Key`. Header
        authentication is supported only for HTTPS destinations. These
        credentials are separate from the CoreWeave API access token used to
        call the Telemetry Relay API.
      type: object
      properties:
        basicAuth:
          description: basic_auth provides HTTP Basic authentication credentials.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.BasicAuthCredentials
        authHeaders:
          description: auth_headers provides custom HTTP header authentication.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.AuthHeadersCredentials
    coreweave.telemetryrelay.types.v1beta1.ForwardingEndpoint:
      description: >-
        ForwardingEndpoint represents a destination where telemetry data can be
        forwarded. Endpoints are organization-scoped and identified by a unique
        slug. Endpoints forward to HTTPS endpoints or AWS S3 destinations.
      type: object
      properties:
        ref:
          description: ref uniquely identifies this endpoint within the organization.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointRef
        spec:
          description: spec contains the desired configuration for this endpoint.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointSpec
        status:
          description: |-
            status reflects the current state of the endpoint.
             This field is output-only and managed by the system.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.ForwardingEndpointStatus
          readOnly: true
      required:
        - ref
        - spec
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
    coreweave.telemetryrelay.types.v1beta1.S3Config:
      description: >-
        `S3Config` configures an AWS S3 destination for archiving telemetry
        data. Data is written to the specified bucket and optional prefix.
        `S3Credentials` must be provided when creating the destination and
        cannot be cleared afterward.
      type: object
      properties:
        uri:
          description: >-
            `uri` is the S3 URI where data is written. Use the format
            `s3://[BUCKET-NAME]/[PREFIX]/`. Replace `[BUCKET-NAME]` with the
            bucket name and `[PREFIX]` with the optional prefix.
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
    coreweave.telemetryrelay.types.v1beta1.HTTPSConfig:
      description: >-
        Configures an HTTPS destination for forwarding telemetry. To
        authenticate to the destination, provide `HTTPSCredentials` with either
        `basicAuth` or `authHeaders` when creating or updating the endpoint. If
        no credentials are stored for the endpoint, requests are sent without
        authentication.
      type: object
      properties:
        endpoint:
          description: |-
            endpoint is the URL of the HTTPS endpoint.
             Must be a valid HTTPS URL; plain HTTP is rejected.
             Targets that resolve to loopback, private, or link-local addresses are
             rejected by the service at submission time to prevent SSRF (see O11Y-2851).
          type: string
        tls:
          description: |-
            tls configures TLS settings for connecting to the endpoint.
             Optional - omit when using system default trust.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.telemetryrelay.types.v1beta1.TLSConfig
        compression:
          description: >-
            Optional compression setting for HTTPS delivery. Omit the field or
            use `COMPRESSION_TYPE_UNSPECIFIED` for uncompressed delivery.
            `COMPRESSION_TYPE_NONE` explicitly disables compression. Both send
            no Content-Encoding header, but UNSPECIFIED is omitted from
            responses and NONE is returned explicitly. `COMPRESSION_TYPE_GZIP`
            compresses the complete NDJSON body and sets `Content-Encoding:
            gzip`; the destination must accept gzip-compressed request bodies.
            Batching and Content-Type are unchanged. Compression level is
            service-managed. Endpoint updates replace the full spec: omitting
            this field resets compression to uncompressed delivery.
          type: string
          format: enum
          enum:
            - COMPRESSION_TYPE_UNSPECIFIED
            - COMPRESSION_TYPE_NONE
            - COMPRESSION_TYPE_GZIP
      required:
        - endpoint
    coreweave.telemetryrelay.types.v1beta1.BasicAuthCredentials:
      description: >-
        BasicAuthCredentials contains username and password for HTTP Basic
        authentication. This is a reusable credential type for any endpoint that
        uses HTTP Basic authentication, including generic HTTPS endpoints.
        Credentials are encrypted at rest and in transit.
      type: object
      properties:
        username:
          description: username for HTTP Basic authentication. Must be non-empty.
          type: string
          writeOnly: true
        password:
          description: |-
            password for HTTP Basic authentication.
             This field is write-only and never returned in responses.
          type: string
          writeOnly: true
      required:
        - username
        - password
    coreweave.telemetryrelay.types.v1beta1.AuthHeadersCredentials:
      description: |-
        AuthHeadersCredentials contains custom HTTP headers for authentication.

         Used for APIs that require authentication via custom headers (e.g., X-API-Key, X-Auth-Token).
         All header values are encrypted at rest and in transit.
         Header names are case-insensitive per HTTP specification.
      type: object
      properties:
        headers:
          description: >-
            Map of 1 to 20 HTTP header names to authentication values. Values
            are write-only and never returned in responses.


            Names must contain 1 to 255 characters, match
            ``^[A-Za-z0-9!#$%&'*+.^_`|~-]+$``, and be unique ignoring case.

            Values must contain 1 to 2048 characters and match
            `^[\x21-\x2B\x2D-\x7E]([\x09\x20\x21-\x2B\x2D-\x7E]*[\x21-\x2B\x2D-\x7E])?$`:
            visible ASCII except commas, with spaces and tabs allowed only
            internally.

            Neither names nor values may contain `${`. The connector sets
            `Host`, `Content-Length`, `Content-Type`, `Connection`, and
            `Transfer-Encoding`; these names cannot be overridden, regardless of
            case.
          type: object
          additionalProperties:
            type: string
      required:
        - headers
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
    coreweave.telemetryrelay.types.v1beta1.TLSConfig:
      description: |-
        TLSConfig configures TLS settings for secure connections.

         Used when connecting to endpoints that require custom CA certificates
         or specific TLS configuration.
      type: object
      properties:
        certificateAuthorityData:
          description: >-
            certificate_authority_data contains the PEM-encoded CA certificate
            bundle.
             Must be base64-encoded when transmitted.
             If not provided, the system's default trust store is used.
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
