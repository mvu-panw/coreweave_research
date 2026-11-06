# Unsubscribe from category

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/unsubscribe-from-category

# Unsubscribe from category

> Stop sending every CoreWeave alert in a category to a destination.

Requires the **Alerts Admin** role.

This endpoint matches clearing a destination in **Configure all** on the Cloud Console
[Alert configuration](https://console.coreweave.com/account/alerts/configuration)
page. Category values are lowercase, for example `gpu`, `sunk`, or `storage`.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/subscriptions/alerts/categories/gpu/unsubscribe \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"destinationId": "[DESTINATION-ID]"}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/subscriptions/alerts/categories/{category}/unsubscribe
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
  /v1/notifications/subscriptions/alerts/categories/{category}/unsubscribe:
    post:
      tags:
        - NotificationsService
      summary: Unsubscribe from category
      description: Disables every alert in a category for one destination.
      operationId: NotificationsService_UnsubscribeFromCategory
      parameters:
        - name: category
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UnsubscribeFromCategoryRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UnsubscribeFromCategoryResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UnsubscribeFromCategoryRequest:
      type: object
      properties:
        category:
          description: The alert category, for example `gpu`.
          type: string
        destinationId:
          description: The destination to disable every alert in the category for.
          type: string
      required:
        - category
        - destinationId
    UnsubscribeFromCategoryResponse:
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
