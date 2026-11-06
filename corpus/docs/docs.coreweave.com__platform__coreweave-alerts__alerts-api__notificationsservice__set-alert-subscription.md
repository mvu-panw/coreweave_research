# Set alert subscription

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/set-alert-subscription

# Set alert subscription

> Turn delivery of one CoreWeave alert to one destination on or off.

Requires the **Alerts Admin** role.

To stop delivery without removing the subscription, set `enabled` to `false`. If
`alertName` isn't in the alert catalog, the request fails with `NOT_FOUND`.

```bash title="Example request" theme={"system"}
curl -X PUT https://api.coreweave.com/v1/notifications/subscriptions/alerts/GPUWantsReset \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"destinationId": "[DESTINATION-ID]", "enabled": true}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml put /v1/notifications/subscriptions/alerts/{alertName}
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
  /v1/notifications/subscriptions/alerts/{alertName}:
    put:
      tags:
        - NotificationsService
      summary: Set alert subscription
      description: >-
        Turns delivery of one alert to one destination on or off, creating the
        subscription if it doesn't exist.
      operationId: NotificationsService_UpsertAlertSubscription
      parameters:
        - name: alertName
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpsertAlertSubscriptionRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpsertAlertSubscriptionResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UpsertAlertSubscriptionRequest:
      type: object
      properties:
        alertName:
          description: The alert's name in the alert catalog.
          type: string
        destinationId:
          description: The destination to turn delivery on or off for.
          type: string
        enabled:
          description: '`true` to deliver the alert to the destination, `false` to stop.'
          type: boolean
      required:
        - alertName
        - destinationId
        - enabled
    UpsertAlertSubscriptionResponse:
      type: object
      properties: {}
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
