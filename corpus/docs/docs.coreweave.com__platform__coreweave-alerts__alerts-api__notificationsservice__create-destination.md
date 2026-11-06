# Create destination

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-destination

# Create destination

> Create a CoreWeave Alerts destination.

Requires the **Alerts Admin** role.

The `webhook`, `slack_webhook`, and `google_chat` channels deliver to a URL held in a
credential, so create the credential first with
[Create credential](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-credential.md)
and pass its `id` as `credentialId`. A `queue` destination needs no credential or config.
For the format each channel expects, see
[Destination channels and credentials](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md#destination-channels-and-credentials).

A new destination receives no alerts until you subscribe alerts to it.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/destinations \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "webhook",
    "displayName": "Ops webhook",
    "credentialId": "[CREDENTIAL-ID]"
  }'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/destinations
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
  /v1/notifications/destinations:
    post:
      tags:
        - NotificationsService
      summary: Create destination
      description: Creates a destination that CoreWeave Alerts can deliver to.
      operationId: NotificationsService_CreateDestination
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateDestinationRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateDestinationResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    CreateDestinationRequest:
      type: object
      properties:
        channel:
          description: >-
            The delivery channel, `webhook`, `slack_webhook`, `google_chat`, or
            `queue`. `webhook`, `slack_webhook`, and `google_chat` require
            `credentialId`. Create `slack` destinations with Join Slack channel.
          type: string
        displayName:
          description: A human-readable name for the destination, 1 to 255 characters.
          type: string
        credentialId:
          description: >-
            The ID of a credential from Create credential. Required for
            `webhook`, `slack_webhook`, and `google_chat`.
          type: string
        config:
          description: Channel-specific configuration as a JSON-encoded string.
          type: string
      required:
        - channel
        - displayName
    CreateDestinationResponse:
      type: object
      properties:
        destination:
          $ref: '#/components/schemas/Destination'
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
    Destination:
      description: A place CoreWeave Alerts delivers to.
      type: object
      properties:
        id:
          description: The unique identifier for the destination.
          type: string
        orgUid:
          description: The organization that owns the destination.
          type: string
        channel:
          description: >-
            The delivery channel, such as `webhook`, `slack`, `slack_webhook`,
            `google_chat`, `queue`, or `in_app`.
          type: string
        displayName:
          description: A human-readable name for the destination.
          type: string
        credentialId:
          description: >-
            The credential that holds the destination's secret URL or token, if
            the channel uses one.
          type: string
        config:
          description: >-
            Channel-specific configuration as a JSON-encoded string. Slack
            destinations use `{"channelId":"..."}`. Empty for channels that need
            no configuration.
          type: string
        credentialType:
          description: The type of the referenced credential, if any.
          type: string
        credentialStatus:
          description: >-
            The status of the referenced credential, `active` or `revoked`, if
            any.
          type: string
        createdAt:
          description: The time the destination was created.
          type: string
          format: date-time
        updatedAt:
          description: The time the destination was last updated.
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
