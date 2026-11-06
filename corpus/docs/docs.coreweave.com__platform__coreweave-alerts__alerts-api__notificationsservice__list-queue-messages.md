# List queue messages

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-queue-messages

# List queue messages

> Pull CoreWeave Alerts from a queue destination.

Requires the **Alerts Viewer** role.

A queue destination holds alerts until you acknowledge them. Listing doesn't remove
messages, so call [Acknowledge queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/acknowledge-queue-messages.md)
after you process them. For polling limits and retention, see
[Queue delivery](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md#queue-delivery).

```bash title="Example request" theme={"system"}
curl "https://api.coreweave.com/v1/notifications/queues/[DESTINATION-ID]/messages?limit=100" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/queues/{destinationId}/messages
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
  /v1/notifications/queues/{destinationId}/messages:
    get:
      tags:
        - NotificationsService
      summary: List queue messages
      description: Returns unacknowledged messages from a queue destination, oldest first.
      operationId: NotificationsService_ListQueueMessages
      parameters:
        - name: destinationId
          in: path
          required: true
          schema:
            type: string
        - name: limit
          in: query
          description: >-
            The maximum number of messages to return, from `1` to `500`.
            Defaults to `100`.
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListQueueMessagesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListQueueMessagesResponse:
      type: object
      properties:
        messages:
          type: array
          items:
            $ref: '#/components/schemas/QueueMessage'
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
    QueueMessage:
      description: An alert waiting in a queue destination.
      type: object
      properties:
        id:
          description: >-
            The unique identifier for the message. Pass it to Acknowledge queue
            messages.
          type: string
        createdAt:
          description: When the message was queued.
          type: string
          format: date-time
        payload:
          description: >-
            The alert, with the same `subject` and `body` fields, and optional
            `data` field, as a webhook delivery.
          type: object
        requestId:
          description: >-
            The alert this message belongs to. Matches `requestId` in delivery
            statuses and alerts.
          type: string
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
