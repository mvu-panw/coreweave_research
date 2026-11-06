# Create credential

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-credential

# Create credential

> Store an encrypted secret for a CoreWeave Alerts destination.

Requires the **Alerts Admin** role.

CoreWeave encrypts the `secret` and never returns it. The format of `secret` depends on
`credentialType`. For the formats, see
[Destination channels and credentials](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md#destination-channels-and-credentials).

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/credentials \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Ops webhook",
    "credentialType": "webhook",
    "secret": "{\"url\": \"https://alerts.example.com/coreweave\", \"signing_secret\": \"[SIGNING-SECRET]\"}"
  }'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/credentials
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
    post:
      tags:
        - NotificationsService
      summary: Create credential
      description: >-
        Stores an encrypted secret, such as a webhook URL, for destinations to
        use.
      operationId: NotificationsService_CreateCredential
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateCredentialRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateCredentialResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    CreateCredentialRequest:
      type: object
      properties:
        displayName:
          description: A human-readable name for the credential, 1 to 255 characters.
          type: string
        credentialType:
          description: >-
            The kind of secret. Use `webhook` for generic webhooks,
            `slack_webhook` for Slack incoming webhooks, and `google_chat` for
            Google Chat webhooks. The Cloud Console creates `slack_oauth`
            credentials through the Slack OAuth flow.
          type: string
        secret:
          description: >-
            The secret value. For `webhook`, a JSON-encoded string with a
            required HTTPS `url` and an optional `signing_secret`. For
            `slack_webhook`, a URL that starts with
            `https://hooks.slack.com/services/`. For `google_chat`, a URL that
            starts with `https://chat.googleapis.com/v1/spaces/`.
          type: string
      required:
        - displayName
        - credentialType
        - secret
    CreateCredentialResponse:
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
