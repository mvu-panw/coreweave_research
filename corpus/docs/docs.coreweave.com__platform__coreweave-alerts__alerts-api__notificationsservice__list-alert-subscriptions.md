# List alert subscriptions

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-alert-subscriptions

# List alert subscriptions

> List which CoreWeave Alerts each destination receives.

Requires the **Alerts Viewer** role.

Each entry pairs one alert with one destination and includes the alert's `category`,
`severity`, and `description`. Use the `alertName` and `category` values from this
response in the other alert subscription endpoints.

```bash title="Example request" theme={"system"}
curl https://api.coreweave.com/v1/notifications/subscriptions/alerts \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/subscriptions/alerts
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
  /v1/notifications/subscriptions/alerts:
    get:
      tags:
        - NotificationsService
      summary: List alert subscriptions
      description: >-
        Returns the alert subscriptions in the caller's organization, one entry
        per alert and destination pair.
      operationId: NotificationsService_ListAlertSubscriptions
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListAlertSubscriptionsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListAlertSubscriptionsResponse:
      type: object
      properties:
        subscriptions:
          type: array
          items:
            $ref: '#/components/schemas/AlertSubscription'
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
    AlertSubscription:
      description: Whether one alert is delivered to one destination.
      type: object
      properties:
        id:
          description: The unique identifier for the subscription.
          type: string
        alertName:
          description: The alert's name in the alert catalog, for example `GPUWantsReset`.
          type: string
        category:
          description: >-
            The alert's category, for example `gpu`, `sunk`, `node`,
            `kubernetes`, `storage`, or `caios`.
          type: string
        displayName:
          description: The alert's human-readable name.
          type: string
        description:
          description: What the alert means.
          type: string
        severity:
          description: The alert's severity.
          type: string
        enabled:
          description: Whether the alert is delivered to the destination.
          type: boolean
        destinationId:
          description: The destination the subscription applies to.
          type: string
        channel:
          description: The destination's delivery channel.
          type: string
        destinationDisplayName:
          description: The destination's display name.
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
