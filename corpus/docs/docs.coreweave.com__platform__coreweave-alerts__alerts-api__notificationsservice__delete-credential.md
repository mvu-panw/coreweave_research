# Delete credential

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/delete-credential

# Delete credential

> Delete a CoreWeave Alerts credential.

Requires the **Alerts Admin** role.

Delete every destination that uses the credential first. While a destination references
the credential, the request fails with `FAILED_PRECONDITION`.

```bash title="Example request" theme={"system"}
curl -X DELETE https://api.coreweave.com/v1/notifications/credentials/[CREDENTIAL-ID] \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```


## OpenAPI

````yaml /openapi/notifications/openapi.yaml delete /v1/notifications/credentials/{id}
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
  /v1/notifications/credentials/{id}:
    delete:
      tags:
        - NotificationsService
      summary: Delete credential
      description: >-
        Deletes a credential. Fails with `FAILED_PRECONDITION` while a
        destination references the credential.
      operationId: NotificationsService_DeleteCredential
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteCredentialResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    DeleteCredentialResponse:
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
