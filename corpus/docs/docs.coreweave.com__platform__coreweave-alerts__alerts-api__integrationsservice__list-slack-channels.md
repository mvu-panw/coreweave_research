# List Slack channels

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/list-slack-channels

# List Slack channels

> List the Slack channels CoreWeave Alerts can deliver to.

Requires the **Alerts Viewer** role and an active Slack OAuth integration. In the
Cloud Console, set up the integration first. For details, see
[Slack OAuth integration](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md). Without an active
integration, the request fails with `NOT_FOUND`.

```bash title="Example request" theme={"system"}
curl https://api.coreweave.com/v1/notifications/integrations/slack-channels \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/integrations/slack-channels
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
  /v1/notifications/integrations/slack-channels:
    get:
      tags:
        - IntegrationsService
      summary: List Slack channels
      description: >-
        Returns the Slack channels visible to your organization's Slack OAuth
        integration.
      operationId: IntegrationsService_ListSlackChannels
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListSlackChannelsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListSlackChannelsResponse:
      type: object
      properties:
        channels:
          type: array
          items:
            $ref: '#/components/schemas/SlackChannel'
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
    SlackChannel:
      type: object
      properties:
        id:
          description: The Slack channel ID.
          type: string
        name:
          description: The Slack channel name.
          type: string
        isArchived:
          description: Whether the channel is archived.
          type: boolean
        isMember:
          description: Whether the CoreWeave Mission Control app is already in the channel.
          type: boolean
        numMembers:
          description: The number of members in the channel.
          type: integer
          format: int32
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
