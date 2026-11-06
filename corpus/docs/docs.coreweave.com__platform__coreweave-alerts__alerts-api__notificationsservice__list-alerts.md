# List alerts

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-alerts

# List alerts

> List the CoreWeave Alerts your organization received.

Requires the **Alerts Viewer** role.

This endpoint returns the data behind the Cloud Console
[Alert history](https://console.coreweave.com/account/alerts) page. Each entry is
one alert, identified by `requestId`. Only alerts delivered to the `in_app` destination
appear. An alert that went only to other destinations isn't listed. To see per-destination delivery for an alert, pass
its `requestId` to [List delivery statuses](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-delivery-statuses.md).

Pass `fromDate` as an RFC 3339 timestamp. Results are paginated. For details, see
[Pagination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md#pagination).

```bash title="Example request" theme={"system"}
curl "https://api.coreweave.com/v1/notifications/alerts?fromDate=2026-10-01T00:00:00Z&pageSize=50" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/alerts
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
  /v1/notifications/alerts:
    get:
      tags:
        - NotificationsService
      summary: List alerts
      description: >-
        Returns alerts delivered to the caller's organization through the
        `in_app` destination, newest first, one entry per alert.
      operationId: NotificationsService_ListAlerts
      parameters:
        - name: fromDate
          in: query
          description: >-
            Return only alerts created at or after this RFC 3339 timestamp, such
            as `2026-10-01T00:00:00Z`.
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
            The number of alerts per page. Defaults to `100`, which is also the
            maximum.
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListAlertsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListAlertsResponse:
      type: object
      properties:
        alerts:
          type: array
          items:
            $ref: '#/components/schemas/AlertSummary'
        page:
          description: The page returned.
          type: integer
          format: int32
        pageSize:
          description: The page size used, at most 100.
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
    AlertSummary:
      description: >-
        One alert delivered to the `in_app` destination, with every channel it
        was delivered to.
      type: object
      properties:
        requestId:
          description: >-
            The unique identifier for the alert. Pass it to List delivery
            statuses for per-destination detail.
          type: string
        orgUid:
          description: The organization that received the alert.
          type: string
        templateId:
          description: >-
            The notification template used to render the message, `vm-alert` for
            alerts or `custom` for test notifications.
          type: string
        channels:
          description: Every channel the alert was delivered to.
          type: array
          items:
            type: string
        status:
          description: >-
            The status of the alert's `in_app` delivery. For other channels, use
            List delivery statuses. `DELIVERY_STATUS_STATE_UNSPECIFIED` means
            the status was never set.
          type: string
          format: enum
          enum:
            - DELIVERY_STATUS_STATE_UNSPECIFIED
            - DELIVERY_STATUS_STATE_PENDING
            - DELIVERY_STATUS_STATE_SENT
            - DELIVERY_STATUS_STATE_FAILED
            - DELIVERY_STATUS_STATE_RESOLVED
        severity:
          description: The alert's severity.
          type: string
        subject:
          description: The alert's subject line.
          type: string
        content:
          description: The rendered alert message.
          type: string
        createdAt:
          description: When the alert was first delivered, as an RFC 3339 timestamp.
          type: string
        updatedAt:
          description: When the alert was last updated, as an RFC 3339 timestamp.
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
