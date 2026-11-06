# Update destination

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/update-destination

# Update destination

> Change the display name, credential, or config of a CoreWeave Alerts destination.

Requires the **Alerts Admin** role.

Send only the fields you want to change. An empty `displayName` or `config` keeps the
current value. Omit `credentialId` to keep the current credential. An empty `credentialId`
fails with `INVALID_ARGUMENT`. The channel of a destination can't change. To switch channels, create a
new destination and delete the old one.

```bash title="Example request" theme={"system"}
curl -X PUT https://api.coreweave.com/v1/notifications/destinations/[DESTINATION-ID] \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"displayName": "Ops webhook (primary)"}'
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml put /v1/notifications/destinations/{id}
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
  /v1/notifications/destinations/{id}:
    put:
      tags:
        - NotificationsService
      summary: Update destination
      description: >-
        Updates the display name, credential, or config of a destination.
        Omitted fields keep their current value. An empty `displayName` or
        `config` also keeps the current value.
      operationId: NotificationsService_UpdateDestination
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateDestinationRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateDestinationResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UpdateDestinationRequest:
      type: object
      properties:
        id:
          description: The ID of the destination to update.
          type: string
        displayName:
          description: >-
            A new display name, up to 255 characters. Empty keeps the current
            name.
          type: string
        credentialId:
          description: >-
            The ID of a replacement credential. Omit it to keep the current
            credential.
          type: string
        config:
          description: >-
            Replacement channel configuration as a JSON-encoded string. Empty
            keeps the current config.
          type: string
      required:
        - id
    UpdateDestinationResponse:
      type: object
      properties:
        destination:
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
