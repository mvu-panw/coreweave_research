# Acknowledge queue messages

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/acknowledge-queue-messages

# Acknowledge queue messages

> Remove processed CoreWeave Alerts from a queue destination.

Requires the **Alerts Admin** role.

Send between 1 and 500 message IDs from
[List queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-queue-messages.md).
The request skips IDs that were already acknowledged or that expired, so `acked` can be
lower than the number of IDs you sent.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/queues/[DESTINATION-ID]/messages/ack \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"messageIds": ["[MESSAGE-ID]"]}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/queues/{destinationId}/messages/ack
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
  /v1/notifications/queues/{destinationId}/messages/ack:
    post:
      tags:
        - NotificationsService
      summary: Acknowledge queue messages
      description: >-
        Removes processed messages from a queue destination and returns how many
        were removed.
      operationId: NotificationsService_AckQueueMessages
      parameters:
        - name: destinationId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AckQueueMessagesRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckQueueMessagesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    AckQueueMessagesRequest:
      type: object
      properties:
        destinationId:
          description: The queue destination the messages belong to.
          type: string
        messageIds:
          description: Between 1 and 500 message IDs to acknowledge.
          type: array
          items:
            type: string
      required:
        - destinationId
        - messageIds
    AckQueueMessagesResponse:
      type: object
      properties:
        acked:
          description: The number of messages removed from the queue.
          type: integer
          format: int32
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
