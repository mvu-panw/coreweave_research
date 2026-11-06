# Test destination

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/test-destination

# Test destination

> Send a test notification to a CoreWeave Alerts destination.

Requires the **Alerts Admin** role.

The test notification has the subject `Test Notification`. A test of a `queue`
destination adds a message to the queue, and a test of the `in_app` destination adds an
entry to the Cloud Console Alert history page. The response returns
`delivered: true` on success, or `delivered: false` with the delivery error in `error`.
If the destination's credential is revoked, the request fails with `FAILED_PRECONDITION`.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/notifications/destinations/[DESTINATION-ID]/test \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml post /v1/notifications/destinations/{destId}/test
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
  /v1/notifications/destinations/{destId}/test:
    post:
      tags:
        - NotificationsService
      summary: Test destination
      description: >-
        Sends a test notification to a destination and reports whether delivery
        succeeded.
      operationId: NotificationsService_TestDestination
      parameters:
        - name: destId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TestDestinationRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TestDestinationResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    TestDestinationRequest:
      type: object
      properties:
        destId:
          type: string
      required:
        - destId
    TestDestinationResponse:
      type: object
      properties:
        eventId:
          description: The ID of the test notification.
          type: string
        delivered:
          description: Whether the test notification was delivered.
          type: boolean
        error:
          description: The delivery error when `delivered` is `false`.
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
