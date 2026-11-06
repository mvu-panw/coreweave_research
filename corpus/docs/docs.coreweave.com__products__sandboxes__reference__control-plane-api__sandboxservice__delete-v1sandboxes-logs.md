# Delete v1sandboxes logs

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/delete-v1sandboxes-logs

# Delete v1sandboxes logs

> DeleteSandboxLogs deletes a sandbox's stored logs: the stored stdout and
 stderr history that ListSandboxLogs serves. Only an ended sandbox's logs
 can be deleted. The creating user, or a caller with the sandbox_admin
 action in the sandbox's organization, can delete them; a caller who
 cannot see the sandbox gets the same error as GetSandbox.

 From the moment the call returns, ListSandboxLogs refuses the sandbox
 with CWSANDBOX_LOGS_DELETED; a page already being served may still
 complete. Under normal load, while the service is healthy, the lines are
 removed from log storage within 24 hours of the request; the storage's
 object store and backups follow on the managed storage service's own
 schedule. The delete covers the stored history this API serves, not
 copies in node-local files or in CoreWeave's internal operational
 logging. DeleteSandbox stops a sandbox and leaves its stored logs
 readable; it does not delete them.

 The call is idempotent: repeating it returns the first call's
 deleted_at. It also succeeds for an ended sandbox whose logs were never
 stored or have expired.

 Errors:
   - FAILED_PRECONDITION (CWSANDBOX_SANDBOX_NOT_TERMINAL): the sandbox has
     not ended. Stop it, then retry.
   - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED): stored logs are not
     enabled for the organization.
   - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED) with
     RetryInfo: the organization made more than 10 deletes in the current
     second, or too many stored-log calls are in flight. Retry after the
     delay.
   - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE) with RetryInfo: the
     stored-log backend is unavailable. Retry after the delay.
   - UNAVAILABLE (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs
     are enabled could not be determined. Retry later.
   - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the
     sandbox's stored-log state could not be read. Retry after the delay.
   - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED): the deployment does not
     serve stored logs.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml delete /v1/sandboxes/{sandboxId}/logs
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
    delete:
      tags:
        - SandboxService
      description: |-
        DeleteSandboxLogs deletes a sandbox's stored logs: the stored stdout and
         stderr history that ListSandboxLogs serves. Only an ended sandbox's logs
         can be deleted. The creating user, or a caller with the sandbox_admin
         action in the sandbox's organization, can delete them; a caller who
         cannot see the sandbox gets the same error as GetSandbox.

         From the moment the call returns, ListSandboxLogs refuses the sandbox
         with CWSANDBOX_LOGS_DELETED; a page already being served may still
         complete. Under normal load, while the service is healthy, the lines are
         removed from log storage within 24 hours of the request; the storage's
         object store and backups follow on the managed storage service's own
         schedule. The delete covers the stored history this API serves, not
         copies in node-local files or in CoreWeave's internal operational
         logging. DeleteSandbox stops a sandbox and leaves its stored logs
         readable; it does not delete them.

         The call is idempotent: repeating it returns the first call's
         deleted_at. It also succeeds for an ended sandbox whose logs were never
         stored or have expired.

         Errors:
           - FAILED_PRECONDITION (CWSANDBOX_SANDBOX_NOT_TERMINAL): the sandbox has
             not ended. Stop it, then retry.
           - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED): stored logs are not
             enabled for the organization.
           - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED) with
             RetryInfo: the organization made more than 10 deletes in the current
             second, or too many stored-log calls are in flight. Retry after the
             delay.
           - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE) with RetryInfo: the
             stored-log backend is unavailable. Retry after the delay.
           - UNAVAILABLE (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs
             are enabled could not be determined. Retry later.
           - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the
             sandbox's stored-log state could not be read. Retry after the delay.
           - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED): the deployment does not
             serve stored logs.
      operationId: SandboxService_DeleteSandboxLogs
      parameters:
        - name: sandboxId
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
                  #/components/schemas/coreweave.sandbox.v1.DeleteSandboxLogsResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
components:
  schemas:
    coreweave.sandbox.v1.DeleteSandboxLogsResponse:
      type: object
      properties:
        deletedAt:
          description: >-
            When the deletion was recorded. A repeated call returns the first
            call's
             value.
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
