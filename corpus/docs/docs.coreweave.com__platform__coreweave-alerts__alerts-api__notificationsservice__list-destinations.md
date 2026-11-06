# List destinations

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-destinations

# List destinations

> List every CoreWeave Alerts destination in your organization.

Requires the **Alerts Viewer** role. For details, see the
[CoreWeave Alerts API overview](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api.md).

Use the `id` of a destination in the response when you subscribe alerts to it.

```bash title="Example request" theme={"system"}
curl https://api.coreweave.com/v1/notifications/destinations \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml get /v1/notifications/destinations
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
  /v1/notifications/destinations:
    get:
      tags:
        - NotificationsService
      summary: List destinations
      description: >-
        Returns every destination in the caller's organization, including the
        default in-app destination.
      operationId: NotificationsService_ListDestinations
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListDestinationsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListDestinationsResponse:
      type: object
      properties:
        destinations:
          type: array
          items:
            $ref: '#/components/schemas/Destination'
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
    Destination:
      description: A place CoreWeave Alerts delivers to.
      type: object
      properties:
        id:
          description: The unique identifier for the destination.
          type: string
        orgUid:
          description: The organization that owns the destination.
          type: string
        channel:
          description: >-
            The delivery channel, such as `webhook`, `slack`, `slack_webhook`,
            `google_chat`, `queue`, or `in_app`.
          type: string
        displayName:
          description: A human-readable name for the destination.
          type: string
        credentialId:
          description: >-
            The credential that holds the destination's secret URL or token, if
            the channel uses one.
          type: string
        config:
          description: >-
            Channel-specific configuration as a JSON-encoded string. Slack
            destinations use `{"channelId":"..."}`. Empty for channels that need
            no configuration.
          type: string
        credentialType:
          description: The type of the referenced credential, if any.
          type: string
        credentialStatus:
          description: >-
            The status of the referenced credential, `active` or `revoked`, if
            any.
          type: string
        createdAt:
          description: The time the destination was created.
          type: string
          format: date-time
        updatedAt:
          description: The time the destination was last updated.
          type: string
          format: date-time
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
