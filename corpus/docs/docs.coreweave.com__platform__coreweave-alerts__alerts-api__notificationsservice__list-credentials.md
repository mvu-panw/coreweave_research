# List credentials

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-credentials

# List credentials

> List the credentials that CoreWeave Alerts destinations use.

Requires the **Alerts Viewer** role.

The response never includes the secret value of a credential.

```bash title="Example request" theme={"system"}
curl https://api.coreweave.com/v1/notifications/credentials \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/credentials
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
  /v1/notifications/credentials:
    get:
      tags:
        - NotificationsService
      summary: List credentials
      description: >-
        Returns every credential in the caller's organization. The response
        never includes secrets.
      operationId: NotificationsService_ListCredentials
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListCredentialsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListCredentialsResponse:
      type: object
      properties:
        credentials:
          type: array
          items:
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
