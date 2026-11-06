# List delivery statuses

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-delivery-statuses

# List delivery statuses

> Get per-destination delivery status for CoreWeave Alerts.

Requires the **Alerts Viewer** role.

Each record is one delivery of one alert to one destination. When you pass `requestId`,
the response returns every delivery of that alert and ignores the pagination parameters.
Otherwise, the response is paginated and filtered by `fromDate`, an RFC 3339 timestamp.

```bash title="Example request" theme={"system"}
curl "https://api.coreweave.com/v1/notifications/statuses?requestId=[REQUEST-ID]" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/statuses
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
  /v1/notifications/statuses:
    get:
      tags:
        - NotificationsService
      summary: List delivery statuses
      description: >-
        Returns per-destination delivery records. Pass `requestId` to get every
        delivery of one alert.
      operationId: NotificationsService_ListStatuses
      parameters:
        - name: requestId
          in: query
          description: >-
            Return every delivery of this alert. When set, the response ignores
            `fromDate`, `page`, and `pageSize`.
          schema:
            type: string
        - name: fromDate
          in: query
          description: >-
            Return only deliveries created at or after this RFC 3339 timestamp,
            such as `2026-10-01T00:00:00Z`.
          schema:
            type: string
        - name: page
          in: query
          description: The page to return, starting at `1`. Defaults to `1`.
          schema:
            type: integer
            format: int32
        - name: pageSize
          in: query
          description: >-
            The number of delivery records per page. Defaults to `100`, which is
            also the maximum.
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListStatusesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListStatusesResponse:
      type: object
      properties:
        statuses:
          type: array
          items:
            $ref: '#/components/schemas/DeliveryStatus'
        page:
          description: The page returned. Zero when the request filtered by `requestId`.
          type: integer
          format: int32
        pageSize:
          description: >-
            The page size used, at most 100. Zero when the request filtered by
            `requestId`.
          type: integer
          format: int32
        hasNextPage:
          description: Whether another page of results exists.
          type: boolean
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
    DeliveryStatus:
      description: One delivery of one alert to one destination.
      type: object
      properties:
        id:
          description: The unique identifier for the delivery record.
          type: string
        requestId:
          description: The alert this delivery belongs to.
          type: string
        orgUid:
          description: The organization that received the alert.
          type: string
        templateId:
          description: >-
            The notification template used to render the message, `vm-alert` for
            alerts or `custom` for test notifications.
          type: string
        channel:
          description: The channel the alert was delivered on.
          type: string
        status:
          description: >-
            The delivery state. `DELIVERY_STATUS_STATE_UNSPECIFIED` means the
            status was never set.
          type: string
          format: enum
          enum:
            - DELIVERY_STATUS_STATE_UNSPECIFIED
            - DELIVERY_STATUS_STATE_PENDING
            - DELIVERY_STATUS_STATE_SENT
            - DELIVERY_STATUS_STATE_FAILED
            - DELIVERY_STATUS_STATE_RESOLVED
        createdAt:
          description: When the delivery was created, as an RFC 3339 timestamp.
          type: string
        updatedAt:
          description: When the delivery was last updated, as an RFC 3339 timestamp.
          type: string
        severity:
          description: The alert's severity.
          type: string
        subject:
          description: The alert's subject line.
          type: string
        content:
          description: The rendered alert message.
          type: string
        destinationId:
          description: The destination the alert was delivered to.
          type: string
        messageHash:
          type: string
        externalId:
          type: string
        parentId:
          type: string
        destinationDisplayName:
          description: The destination's display name at the time of delivery.
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
