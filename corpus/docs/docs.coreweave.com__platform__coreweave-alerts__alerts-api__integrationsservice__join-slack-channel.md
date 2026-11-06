# Join Slack channel

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/join-slack-channel

# Join Slack channel

> Add the CoreWeave Mission Control app to a Slack channel and get its destination ID.

Requires the **Alerts Admin** role and an active Slack OAuth integration.

Pass a channel `id` from
[List Slack channels](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/list-slack-channels.md).
The response returns the `destinationId` of the Slack destination for that channel,
creating it if needed. To start delivery, subscribe alerts to that destination.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/integrations/slack-channels/invite \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"channelId": "C0123456789", "displayName": "#gpu-alerts"}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/integrations/slack-channels/invite
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
  /v1/notifications/integrations/slack-channels/invite:
    post:
      tags:
        - IntegrationsService
      summary: Join Slack channel
      description: >-
        Adds the CoreWeave Mission Control app to a Slack channel and returns
        the Slack destination for that channel.
      operationId: IntegrationsService_InviteToSlackChannel
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InviteToSlackChannelRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InviteToSlackChannelResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    InviteToSlackChannelRequest:
      type: object
      properties:
        channelId:
          description: The Slack channel ID from List Slack channels.
          type: string
        displayName:
          description: A display name for the Slack destination.
          type: string
    InviteToSlackChannelResponse:
      type: object
      properties:
        destinationId:
          description: The ID of the Slack destination for the channel.
          type: string
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
