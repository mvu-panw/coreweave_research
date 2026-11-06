# Update credential status

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/update-credential-status

# Update credential status

> Revoke or reactivate a CoreWeave Alerts credential.

Requires the **Alerts Admin** role.

Revoking a credential stops delivery to every destination that uses it until you set
the credential back to `active`.

```bash title="Example request" theme={"system"}
curl -X PUT https://api.coreweave.com/v1/notifications/credentials/[CREDENTIAL-ID]/status \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"status": "revoked"}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml put /v1/notifications/credentials/{id}/status
openapi: 3.0.3
info:
  title: CoreWeave Alerts API
  version: 0.0.1
  description: >-
    Manage where CoreWeave Alerts are delivered, which alerts each destination
    receives, and review delivery history.
servers:
  - url: https://api.coreweave.com
    description: CoreWeave API gateway.
security:
  - bearerAuth: []
tags:
  - name: IntegrationsService
    description: >-
      List and join Slack channels through your organization's Slack OAuth
      integration.
    x-group: IntegrationsService
  - name: NotificationsService
    description: >-
      Manage destinations, credentials, and alert subscriptions, read delivery
      history, and pull alerts from queue destinations.
    x-group: NotificationsService
paths:
  /v1/notifications/credentials/{id}/status:
    put:
      tags:
        - NotificationsService
      summary: Update credential status
      description: Sets a credential to `active` or `revoked`.
      operationId: NotificationsService_UpdateCredentialStatus
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateCredentialStatusRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateCredentialStatusResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UpdateCredentialStatusRequest:
      type: object
      properties:
        id:
          description: The ID of the credential to update.
          type: string
        status:
          description: '`active` or `revoked`.'
          type: string
      required:
        - id
        - status
    UpdateCredentialStatusResponse:
      type: object
      properties:
        credential:
          $ref: '#/components/schemas/Credential'
    Status:
      description: The error returned when a request fails.
      type: object
      properties:
        code:
          description: The numeric gRPC status code.
          type: integer
          format: int32
        message:
          description: A developer-facing error message.
          type: string
        details:
          description: Additional error details.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    Credential:
      description: >-
        An encrypted secret that a destination uses to deliver alerts. The API
        never returns the secret value.
      type: object
      properties:
        id:
          description: The unique identifier for the credential.
          type: string
        orgUid:
          description: The organization that owns the credential.
          type: string
        displayName:
          description: A human-readable name for the credential.
          type: string
        credentialType:
          description: >-
            The kind of secret, such as `webhook`, `slack_webhook`,
            `google_chat`, or `slack_oauth`.
          type: string
        status:
          description: '`active` or `revoked`.'
          type: string
        createdAt:
          description: The time the credential was created.
          type: string
          format: date-time
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
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [API-ACCESS-TOKEN]

````
