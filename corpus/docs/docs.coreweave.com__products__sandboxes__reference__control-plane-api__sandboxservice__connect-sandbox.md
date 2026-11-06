# Connect sandbox

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/connect-sandbox

# Connect sandbox

> Issue short-lived client credentials and return the direct data-plane endpoint of a running sandbox.

The credentials and endpoint this method returns are for a direct
connection to the runner that owns the sandbox. The runner does not
serve this REST API: it accepts Connect RPC over HTTP/2 and requires
the client certificate issued here.

The client generates and keeps the private key, and sends only a
signed certificate signing request (CSR). For the full flow, see
[Direct sandbox connections](https://docs.coreweave.com/products/sandboxes/client/guides/direct-connections.md),
which the `cwsandbox` Python SDK implements for you.


## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml post /v1/sandboxes/{sandboxId}:connect
openapi: 3.0.3
info:
  title: CoreWeave Sandboxes API
  version: 0.0.1
  description: >-
    The Sandboxes API lets you manage runners, templates, volumes, network
    configurations, organization settings, and the lifecycle of individual
    sandboxes on CoreWeave.
servers:
  - url: https://api.cwsandbox.com
    description: >-
      CoreWeave sandbox data plane. Hosts the sandbox lifecycle, volumes,
      snapshots, runner discovery, and organization settings.
  - url: https://api.coreweave.com
    description: >-
      CoreWeave control plane. Hosts managed runner and sandbox template
      administration.
security:
  - bearerAuth: []
tags:
  - name: NetworkConfigService
    description: >-
      Create, get, list, update, and delete desired network configurations.
      Updating a configuration bound to a running sandbox changes its network
      rules without a restart. Requires API enablement and a runner with live
      network update support.
  - name: SandboxService
    description: >-
      Endpoints for the sandbox lifecycle: create (directly, from a template, or
      from a Compose file), get, list, exec, read and write files, snapshot,
      connect, purge, and delete.
  - name: DiscoveryService
    description: >-
      Read-only endpoints for discovering the runners visible to the caller's
      organization, with view, capability, and service-visibility filters.
      Runner IDs are unique only within an organization.
  - name: SettingsService
    description: >-
      Organization-level sandbox settings: the object-storage Workload Identity
      Federation (WIF) configuration, the file-system snapshot bucket
      configuration, Compose build storage, and secret stores.
  - name: VolumeService
    description: >-
      CRUD operations for organization-registered volumes that sandboxes can
      mount, plus the validation call that confirms a volume's backing source is
      usable.
  - name: RunnerManagementService
    description: >-
      CRUD operations for managed runners and the runner policy each one
      carries. Policy is a field on the runner, mutated through
      `CreateManagedRunner` and `UpdateManagedRunner`.
  - name: SandboxTemplateService
    description: >-
      CRUD operations for organization-scoped sandbox templates, the partial
      specs that `CreateSandboxFromTemplate` merges with per-request overrides.
paths:
  /v1/sandboxes/{sandboxId}:connect:
    post:
      tags:
        - SandboxService
      summary: Connect sandbox
      description: |-
        ConnectSandbox issues short-lived client credentials and returns
         the direct data-plane endpoint for a running sandbox. The client generates
         and retains the private key; this method accepts only its signed CSR.
      operationId: SandboxService_ConnectSandbox
      parameters:
        - name: sandboxId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ConnectSandboxRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxConnection'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
        - url: https://api.cwsandbox.com
          description: CoreWeave sandbox data plane.
components:
  schemas:
    coreweave.sandbox.v1.ConnectSandboxRequest:
      description: |-
        ConnectSandboxRequest requests sandbox-scoped direct-connection
         credentials. The sandbox must be running and its Runner must advertise a
         compatible direct data-plane endpoint.
      type: object
      properties:
        sandboxId:
          type: string
        csrDer:
          description: >-
            DER-encoded PKCS #10 certificate signing request. The issuer
            validates the
             proof-of-possession signature and copies only the public key; requested
             identity, extensions, and lifetime are ignored.
          type: string
          format: bytes
        requestedPermissions:
          description: >-
            Operations to authorize on the issued certificate. At least one
            concrete permission is required. SANDBOX_DATA_PERMISSION_UNSPECIFIED
            and unknown values are invalid. The server returns only permissions
            allowed for the caller.
          type: array
          items:
            enum:
              - SANDBOX_DATA_PERMISSION_UNSPECIFIED
              - SANDBOX_DATA_PERMISSION_EXEC
              - SANDBOX_DATA_PERMISSION_STREAM_EXEC
              - SANDBOX_DATA_PERMISSION_STREAM_LOGS
              - SANDBOX_DATA_PERMISSION_WRITE_FILE
              - SANDBOX_DATA_PERMISSION_READ_FILE
            type: string
            format: enum
      required:
        - sandboxId
        - csrDer
        - requestedPermissions
    coreweave.sandbox.v1.SandboxConnection:
      description: >-
        SandboxConnection contains everything except the client private key
        needed
         to establish a sandbox-scoped direct connection.
      type: object
      properties:
        endpointUri:
          description: Stable absolute URI for the logical Runner data-plane endpoint.
          type: string
          readOnly: true
        clientCertificateChainPem:
          description: >-
            PEM certificate chain for the public key in the request CSR. The
            leaf
             certificate is first.
          type: string
          format: bytes
          readOnly: true
        serverCaBundlePem:
          description: >-
            PEM trust bundle for authenticating the endpoint. Empty means the
            endpoint
             chains to roots available from the client's system trust store.
          type: string
          format: bytes
          readOnly: true
        expiresAt:
          description: >-
            Time at which the client certificate and established connection
            expire.
          type: string
          format: date-time
          readOnly: true
        endpointId:
          description: Opaque stable identity of the logical Runner endpoint.
          type: string
          readOnly: true
        transport:
          description: >-
            Transport for the issued connection. Successful responses use
            SANDBOX_DATA_TRANSPORT_DIRECT_MTLS.
            SANDBOX_DATA_TRANSPORT_UNSPECIFIED means no transport is specified
            and is not emitted for a successful connection.
          type: string
          format: enum
          enum:
            - SANDBOX_DATA_TRANSPORT_UNSPECIFIED
            - SANDBOX_DATA_TRANSPORT_DIRECT_MTLS
          readOnly: true
        protocol:
          description: >-
            Protocol for the issued connection. Successful responses use
            SANDBOX_DATA_PROTOCOL_CONNECT_H2_V1.
            SANDBOX_DATA_PROTOCOL_UNSPECIFIED means no protocol is specified and
            is not emitted for a successful connection.
          type: string
          format: enum
          enum:
            - SANDBOX_DATA_PROTOCOL_UNSPECIFIED
            - SANDBOX_DATA_PROTOCOL_CONNECT_H2_V1
          readOnly: true
        grantedPermissions:
          description: >-
            Effective permissions encoded in the issued certificate. Successful
            responses contain at least one permission from the intersection of
            requested and allowed permissions and do not contain
            SANDBOX_DATA_PERMISSION_UNSPECIFIED.
          type: array
          items:
            enum:
              - SANDBOX_DATA_PERMISSION_UNSPECIFIED
              - SANDBOX_DATA_PERMISSION_EXEC
              - SANDBOX_DATA_PERMISSION_STREAM_EXEC
              - SANDBOX_DATA_PERMISSION_STREAM_LOGS
              - SANDBOX_DATA_PERMISSION_WRITE_FILE
              - SANDBOX_DATA_PERMISSION_READ_FILE
            type: string
            format: enum
          readOnly: true
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
      x-default: Bearer {API_ACCESS_TOKEN}

````
