# Get v1sandboxes logs

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/get-v1sandboxes-logs

# Get v1sandboxes logs

> ListSandboxLogs returns one page of a sandbox's stored stdout and stderr
 lines, ordered by (timestamp, event_id). Stored logs stay readable while
 the sandbox runs and after it ends, until retention_expires_at; unlike
 StreamLogs, a terminal sandbox is served. The creating user, or a caller
 with the sandbox_admin action in the sandbox's organization, can read
 them. A caller who cannot see the sandbox gets the same error as
 GetSandbox, whether or not logs exist.

 Collection is best effort: lines can be missing, for example when a
 sandbox ends within about a minute of writing them or when output
 arrives faster than it can be collected. Lines longer than the
 collection line limit are not stored whole. A line that is a JSON
 object is stored as normalized JSON: duplicate keys keep their first
 value, and whitespace, number formatting, and escapes are normalized.
 Bodies are stored as written, without redaction, so do not write
 secrets to stdout or stderr. Stored logs are not subject to legal hold.

 Each line is stored for a fixed time after it was written, and reads end
 30 days after the sandbox ends. A sandbox that ran up to 16 days keeps
 its full history for those 30 days; a longer sandbox keeps its full
 history while it runs, and afterwards its oldest lines expire first.

 Pagination is keyset and weakly consistent: a line that arrives late,
 behind the page cursor, appears only in a new first-page request. A
 sandbox whose images are still being built returns an empty page.

 Errors:
   - INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST): a field is out of
     range, the container names a platform sidecar, or page_token is
     malformed, expired, or does not match the request.
   - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED): the sandbox has no
     stored logs to serve. Stored logs were not enabled for it when it was
     created, or are not enabled for the organization.
   - FAILED_PRECONDITION (CWSANDBOX_LOGS_DELETED): the sandbox's stored
     logs were deleted.
   - FAILED_PRECONDITION (CWSANDBOX_LOG_RETENTION_EXPIRED): the stored
     logs are past their retention deadline.
   - FAILED_PRECONDITION (CWSANDBOX_LOG_QUERY_TOO_EXPENSIVE): the query
     exceeds a cost limit and fails the same way on retry. Narrow the time
     range, or remove text_contains.
   - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED) with
     RetryInfo: too many stored-log calls are in flight, or the query met
     transient pressure. Retry after the delay.
   - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE) with RetryInfo: the
     stored-log backend is unavailable. Retry after the delay.
   - UNAVAILABLE (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs
     are enabled could not be determined. Retry later.
   - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the
     sandbox's stored-log state could not be read. Retry after the delay.
   - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED): the deployment does not
     serve stored logs.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/sandboxes/{sandboxId}/logs
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
  /v1/sandboxes/{sandboxId}/logs:
    get:
      tags:
        - SandboxService
      description: |-
        ListSandboxLogs returns one page of a sandbox's stored stdout and stderr
         lines, ordered by (timestamp, event_id). Stored logs stay readable while
         the sandbox runs and after it ends, until retention_expires_at; unlike
         StreamLogs, a terminal sandbox is served. The creating user, or a caller
         with the sandbox_admin action in the sandbox's organization, can read
         them. A caller who cannot see the sandbox gets the same error as
         GetSandbox, whether or not logs exist.

         Collection is best effort: lines can be missing, for example when a
         sandbox ends within about a minute of writing them or when output
         arrives faster than it can be collected. Lines longer than the
         collection line limit are not stored whole. A line that is a JSON
         object is stored as normalized JSON: duplicate keys keep their first
         value, and whitespace, number formatting, and escapes are normalized.
         Bodies are stored as written, without redaction, so do not write
         secrets to stdout or stderr. Stored logs are not subject to legal hold.

         Each line is stored for a fixed time after it was written, and reads end
         30 days after the sandbox ends. A sandbox that ran up to 16 days keeps
         its full history for those 30 days; a longer sandbox keeps its full
         history while it runs, and afterwards its oldest lines expire first.

         Pagination is keyset and weakly consistent: a line that arrives late,
         behind the page cursor, appears only in a new first-page request. A
         sandbox whose images are still being built returns an empty page.

         Errors:
           - INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST): a field is out of
             range, the container names a platform sidecar, or page_token is
             malformed, expired, or does not match the request.
           - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED): the sandbox has no
             stored logs to serve. Stored logs were not enabled for it when it was
             created, or are not enabled for the organization.
           - FAILED_PRECONDITION (CWSANDBOX_LOGS_DELETED): the sandbox's stored
             logs were deleted.
           - FAILED_PRECONDITION (CWSANDBOX_LOG_RETENTION_EXPIRED): the stored
             logs are past their retention deadline.
           - FAILED_PRECONDITION (CWSANDBOX_LOG_QUERY_TOO_EXPENSIVE): the query
             exceeds a cost limit and fails the same way on retry. Narrow the time
             range, or remove text_contains.
           - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED) with
             RetryInfo: too many stored-log calls are in flight, or the query met
             transient pressure. Retry after the delay.
           - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE) with RetryInfo: the
             stored-log backend is unavailable. Retry after the delay.
           - UNAVAILABLE (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs
             are enabled could not be determined. Retry later.
           - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the
             sandbox's stored-log state could not be read. Retry after the delay.
           - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED): the deployment does not
             serve stored logs.
      operationId: SandboxService_ListSandboxLogs
      parameters:
        - name: sandboxId
          in: path
          required: true
          schema:
            type: string
        - name: startTime
          in: query
          description: >-
            Inclusive start of the time range. Defaults to one hour before the
            earlier of endTime and the effective read window's end. A request
            covers at most 24 hours and is narrowed to the read window. That
            window starts five minutes before log collection began and ends five
            minutes after the sandbox's terminal time (or the request time for a
            running sandbox). A range outside that window returns no lines.
          schema:
            type: string
            format: date-time
        - name: endTime
          in: query
          description: >-
            Exclusive end of the time range. Defaults to just after the
            effective read window ends, five minutes after the sandbox
            terminates, or five minutes after the request time while it runs.
          schema:
            type: string
            format: date-time
        - name: container
          in: query
          description: >-
            Container name. Empty selects every workload container. Platform
            sidecar
             names are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).
          schema:
            type: string
        - name: stream
          in: query
          description: Output stream. Unspecified selects both.
          schema:
            type: string
            format: enum
            enum:
              - SANDBOX_LOG_STREAM_UNSPECIFIED
              - SANDBOX_LOG_STREAM_STDOUT
              - SANDBOX_LOG_STREAM_STDERR
        - name: textContains
          in: query
          description: >-
            Return only lines whose body contains this literal byte sequence
            (case
             sensitive, no wildcards). 3 to 256 bytes. Requires explicit start_time
             and end_time at most one hour apart.
          schema:
            type: string
        - name: pageSize
          in: query
          description: >-
            Maximum entries per page. 0 means 100; values above 1000 are treated
            as
             1000; negative values are INVALID_ARGUMENT. A page may hold fewer
             entries, so continue while next_page_token is set.
          schema:
            type: integer
            format: int32
        - name: pageToken
          in: query
          description: >-
            nextPageToken from the previous page. Keep the time fields,
            container, stream, textContains, and order unchanged from the
            request that returned it. pageSize can change between pages. A token
            expires 60 minutes after it is issued.
          schema:
            type: string
        - name: order
          in: query
          description: Page order. Unspecified is ascending.
          schema:
            type: string
            format: enum
            enum:
              - LIST_SANDBOX_LOGS_ORDER_UNSPECIFIED
              - LIST_SANDBOX_LOGS_ORDER_ASC
              - LIST_SANDBOX_LOGS_ORDER_DESC
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListSandboxLogsResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.sandbox.v1.ListSandboxLogsResponse:
      type: object
      properties:
        entries:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.StoredSandboxLogEntry'
          readOnly: true
        nextPageToken:
          description: Token for the next page; empty on the last page.
          type: string
          readOnly: true
        retentionExpiresAt:
          description: >-
            When the stored logs stop being readable. Absent while the sandbox
            has
             not ended.
          type: string
          format: date-time
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
    coreweave.sandbox.v1.StoredSandboxLogEntry:
      description: StoredSandboxLogEntry is one stored log line.
      type: object
      properties:
        eventId:
          description: |-
            Stable identity of the line. A line collected more than once is
             returned once.
          type: string
          readOnly: true
        data:
          description: The stored body.
          type: string
          format: bytes
          readOnly: true
        timestamp:
          description: When the container wrote the line.
          type: string
          format: date-time
          readOnly: true
        container:
          description: The container that wrote the line.
          type: string
          readOnly: true
        stream:
          type: string
          format: enum
          enum:
            - SANDBOX_LOG_STREAM_UNSPECIFIED
            - SANDBOX_LOG_STREAM_STDOUT
            - SANDBOX_LOG_STREAM_STDERR
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
