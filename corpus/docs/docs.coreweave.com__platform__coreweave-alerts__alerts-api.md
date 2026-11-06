# CoreWeave Alerts API

Source: https://docs.coreweave.com/platform/coreweave-alerts/alerts-api

# CoreWeave Alerts API

> REST API for managing CoreWeave Alerts destinations and subscriptions, and reading delivery history

The CoreWeave Alerts API manages where CoreWeave Alerts are delivered and which alerts each destination receives. With the API, you can create destinations, subscribe alerts to them, review delivery history, and pull alerts from a queue destination. Use it to manage alert delivery from scripts and automation. It covers the same configuration as the Cloud Console [Integrations](https://console.coreweave.com/organization/integrations) and [Alert configuration](https://console.coreweave.com/account/alerts/configuration) pages. For an introduction to destinations and alert configuration, see [CoreWeave Alerts](https://docs.coreweave.com/platform/coreweave-alerts.md).

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `[API-ACCESS-TOKEN]` in the following examples with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

## Authentication and permissions

Send your API access token in the `Authorization` header of every request:

```bash title="Example request" theme={"system"}
curl https://api.coreweave.com/v1/notifications/destinations \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]"
```

The CoreWeave Alerts API checks one of two Identity and Access Management (IAM) roles on each request. Grant them through an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies/manage.md).

| Role | Grants |
| :- | :- |
| **Alerts Viewer** (`READ_NOTIFICATIONS`) | Every `GET` endpoint. |
| **Alerts Admin** (`WRITE_NOTIFICATIONS`) | Every endpoint, including those that create, change, test, delete, or acknowledge. |

Each endpoint page lists the role it requires. Every request applies to the organization that owns the API access token.

> [!NOTE]
>
> The Cloud Console [Integrations](https://console.coreweave.com/organization/integrations) page uses the separate **Integrations Viewer** and **Integrations Admin** roles. The CoreWeave Alerts API checks only the Alerts roles, including for destination and Slack channel endpoints.

## Endpoints

The following tables list the API endpoints, grouped by resource. Each operation links to its reference page.

### Destinations

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List destinations](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-destinations.md) | `GET` | `/v1/notifications/destinations` |
| [Create destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-destination.md) | `POST` | `/v1/notifications/destinations` |
| [Update destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/update-destination.md) | `PUT` | `/v1/notifications/destinations/{id}` |
| [Delete destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/delete-destination.md) | `DELETE` | `/v1/notifications/destinations/{id}` |
| [Test destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/test-destination.md) | `POST` | `/v1/notifications/destinations/{destId}/test` |

### Credentials

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List credentials](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-credentials.md) | `GET` | `/v1/notifications/credentials` |
| [Create credential](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-credential.md) | `POST` | `/v1/notifications/credentials` |
| [Update credential status](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/update-credential-status.md) | `PUT` | `/v1/notifications/credentials/{id}/status` |
| [Delete credential](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/delete-credential.md) | `DELETE` | `/v1/notifications/credentials/{id}` |

### Alert subscriptions

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List alert subscriptions](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-alert-subscriptions.md) | `GET` | `/v1/notifications/subscriptions/alerts` |
| [Set alert subscription](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/set-alert-subscription.md) | `PUT` | `/v1/notifications/subscriptions/alerts/{alertName}` |
| [Subscribe to category](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/subscribe-to-category.md) | `POST` | `/v1/notifications/subscriptions/alerts/categories/{category}/subscribe` |
| [Unsubscribe from category](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/unsubscribe-from-category.md) | `POST` | `/v1/notifications/subscriptions/alerts/categories/{category}/unsubscribe` |

### Delivery history

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List alerts](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-alerts.md) | `GET` | `/v1/notifications/alerts` |
| [List delivery statuses](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-delivery-statuses.md) | `GET` | `/v1/notifications/statuses` |

### Queue delivery

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-queue-messages.md) | `GET` | `/v1/notifications/queues/{destinationId}/messages` |
| [Acknowledge queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/acknowledge-queue-messages.md) | `POST` | `/v1/notifications/queues/{destinationId}/messages/ack` |

### Slack channels

| Operation | Method | Endpoint |
| :- | :- | :- |
| [List Slack channels](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/list-slack-channels.md) | `GET` | `/v1/notifications/integrations/slack-channels` |
| [Join Slack channel](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/join-slack-channel.md) | `POST` | `/v1/notifications/integrations/slack-channels/invite` |

## Destination channels and credentials

Every destination has a `channel` that determines how CoreWeave Alerts delivers to it. You can create `webhook`, `slack_webhook`, `google_chat`, and `queue` destinations with [Create destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-destination.md), and `slack` destinations with [Join Slack channel](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/join-slack-channel.md). Channels that deliver to a secret URL keep that URL in a credential. Create the credential with [Create credential](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-credential.md), then pass its `id` as `credentialId` when you create the destination. CoreWeave encrypts credential secrets and never returns them.

The following table lists every channel the API supports and what each one needs:

| Channel | Credential type | Credential `secret` | Destination `config` |
| :- | :- | :- | :- |
| `webhook` | `webhook` | A JSON-encoded string: `{"url": "https://...", "signing_secret": "..."}`. `signing_secret` is optional. | None |
| `slack_webhook` | `slack_webhook` | A Slack incoming webhook URL that starts with `https://hooks.slack.com/services/`. | None |
| `google_chat` | `google_chat` | A Google Chat webhook URL that starts with `https://chat.googleapis.com/v1/spaces/`. | None |
| `slack` | `slack_oauth` | Created by the Cloud Console [Slack OAuth](https://docs.coreweave.com/platform/coreweave-alerts/slack-oauth.md) flow. | `{"channelId": "..."}` |
| `queue` | None | None | None |

The following rules apply to destinations and credentials:

* **Webhook URLs:** A `webhook` URL must use HTTPS and a hostname. CoreWeave rejects bare IP addresses and reserved addresses.
* **Webhook signatures:** When a `webhook` credential has a `signing_secret`, each request carries an `X-CoreWeave-Signature` header set to `sha256=` followed by the hex-encoded HMAC-SHA256 of the request body. For the payload format, see [Webhook integrations](https://docs.coreweave.com/platform/coreweave-alerts/webhooks.md#webhook-payload-format).
* **Slack OAuth:** In the Cloud Console, connect Slack OAuth first. Then use [List Slack channels](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/list-slack-channels.md) and [Join Slack channel](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/integrationsservice/join-slack-channel.md) to get a destination for each channel.
* **Revoked credentials:** Setting a credential to `revoked` with [Update credential status](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/update-credential-status.md) stops delivery to every destination that uses it until you set it back to `active`.
* **In-app delivery:** Every organization has one `in_app` destination, which delivers to the Cloud Console [Alert history](https://console.coreweave.com/account/alerts) page. CoreWeave creates it, and you can't create other `in_app` destinations. Subscribe alerts to it like any other destination.
* **Test notifications:** [Test destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/test-destination.md) works on every channel. A test of a `queue` destination adds a message to the queue, and a test of the `in_app` destination adds an entry to the Alert history page.
* **Uniqueness:** A `webhook`, `slack_webhook`, or `google_chat` credential can back only one destination. `slack` and `queue` destinations are unique by channel and config, so several `slack` destinations, one per Slack channel, share the same `slack_oauth` credential. A duplicate fails with `ALREADY_EXISTS`.
* **Deletion order:** Delete a destination before its credential, and unsubscribe every alert from a destination before you delete the destination. Deleting a resource that's still referenced fails with `FAILED_PRECONDITION`.

## Queue delivery

A `queue` destination stores alerts for you to pull instead of pushing them to an endpoint. Use it when your system can't receive inbound webhooks.

To receive alerts through a queue destination, complete the following steps:

1. Call [Create destination](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/create-destination.md) with `"channel": "queue"`. Save the destination `id` from the response for the following steps.
2. Subscribe alerts to the destination. For the endpoints, see [Alert subscriptions](#alert-subscriptions).
3. Poll [List queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-queue-messages.md). It returns up to `limit` messages, oldest first. The default is 100 and the maximum is 500.
4. After you process the messages, send their IDs to [Acknowledge queue messages](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/acknowledge-queue-messages.md). Listing doesn't remove messages, so unacknowledged messages appear again on the next poll.

Each message `payload` carries the same `subject` and `body` fields as a webhook delivery. Its `requestId` matches the `requestId` in [List alerts](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-alerts.md) and [List delivery statuses](https://docs.coreweave.com/platform/coreweave-alerts/alerts-api/notificationsservice/list-delivery-statuses.md).

The following limits apply:

* **Polling rate:** Poll each queue destination at most once every 10 seconds. A faster poll fails with `RESOURCE_EXHAUSTED` and a `Retry-After` header that gives the number of seconds to wait.
* **Retention:** CoreWeave Alerts deletes messages that aren't acknowledged within 7 days.

> [!WARNING]
>
> Deleting a queue destination permanently deletes every message in its queue, including messages you haven't acknowledged. Pull and acknowledge the remaining messages before you delete the destination.

## Pagination

List alerts and List delivery statuses return results in pages, newest first. Pass `page`, starting at `1`, and `pageSize`. `pageSize` defaults to 100, which is also the maximum. Continue while the response returns `hasNextPage: true`. To limit results to recent alerts, pass `fromDate` as an RFC 3339 timestamp, such as `2026-10-01T00:00:00Z`.

## Errors

A failed request returns a JSON error body with a numeric `code` and a `message`:

```json title="Example error response" theme={"system"}
{
  "code": 9,
  "message": "destination cannot be deleted while it is referenced by a subscription"
}
```

The CoreWeave Alerts API returns these errors:

| Error | HTTP status | Cause |
| :- | :- | :- |
| `INVALID_ARGUMENT` | `400` | A field is missing or invalid, such as an ID that isn't a UUID or an unsupported channel. |
| `FAILED_PRECONDITION` | `400` | The resource is still referenced, or the destination's credential is revoked. |
| `NOT_FOUND` | `404` | The destination or alert doesn't exist, or Slack OAuth isn't connected. |
| `ALREADY_EXISTS` | `409` | A destination with the same credential, or the same channel and config, already exists. |
| `RESOURCE_EXHAUSTED` | `429` | A queue destination was polled too often. Wait for the number of seconds in the `Retry-After` header. |
| `PERMISSION_DENIED` | `403` | The token's principal doesn't have the required role. |

A request with a missing or invalid API access token fails with HTTP `401` before it reaches the CoreWeave Alerts API.

## OpenAPI specification

The complete OpenAPI 3.0 specification for the CoreWeave Alerts API is embedded in the following code block. To expand the code block, click **See all** at the bottom. To download or copy the specification, use the buttons in the title bar.

```yaml expandable title="CoreWeave Alerts OpenAPI" theme={"system"}
openapi: 3.0.3
info:
  title: CoreWeave Alerts API
  version: 0.0.1
  description: Manage where CoreWeave Alerts are delivered, which alerts each destination receives, and
    review delivery history.
servers:
- url: https://api.coreweave.com
  description: CoreWeave API gateway.
paths:
  /v1/notifications/alerts:
    get:
      operationId: NotificationsService_ListAlerts
      summary: List alerts
      description: Returns alerts delivered to the caller's organization through the `in_app` destination,
        newest first, one entry per alert.
      parameters:
      - name: fromDate
        in: query
        description: Return only alerts created at or after this RFC 3339 timestamp, such as `2026-10-01T00:00:00Z`.
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
        description: The number of alerts per page. Defaults to `100`, which is also the maximum.
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
      tags:
      - NotificationsService
  /v1/notifications/credentials:
    get:
      operationId: NotificationsService_ListCredentials
      summary: List credentials
      description: Returns every credential in the caller's organization. The response never includes
        secrets.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListCredentialsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
    post:
      operationId: NotificationsService_CreateCredential
      summary: Create credential
      description: Stores an encrypted secret, such as a webhook URL, for destinations to use.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateCredentialRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateCredentialResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/credentials/{id}:
    delete:
      operationId: NotificationsService_DeleteCredential
      summary: Delete credential
      description: Deletes a credential. Fails with `FAILED_PRECONDITION` while a destination references
        the credential.
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
      tags:
      - NotificationsService
  /v1/notifications/credentials/{id}/status:
    put:
      operationId: NotificationsService_UpdateCredentialStatus
      summary: Update credential status
      description: Sets a credential to `active` or `revoked`.
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
              $ref: '#/components/schemas/UpdateCredentialStatusRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateCredentialStatusResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/destinations:
    get:
      operationId: NotificationsService_ListDestinations
      summary: List destinations
      description: Returns every destination in the caller's organization, including the default in-app
        destination.
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
      tags:
      - NotificationsService
    post:
      operationId: NotificationsService_CreateDestination
      summary: Create destination
      description: Creates a destination that CoreWeave Alerts can deliver to.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateDestinationRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateDestinationResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/destinations/{destId}/test:
    post:
      operationId: NotificationsService_TestDestination
      summary: Test destination
      description: Sends a test notification to a destination and reports whether delivery succeeded.
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
      tags:
      - NotificationsService
  /v1/notifications/destinations/{id}:
    put:
      operationId: NotificationsService_UpdateDestination
      summary: Update destination
      description: Updates the display name, credential, or config of a destination. Omitted fields keep
        their current value. An empty `displayName` or `config` also keeps the current value.
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
      tags:
      - NotificationsService
    delete:
      operationId: NotificationsService_DeleteDestination
      summary: Delete destination
      description: Deletes a destination. Fails with `FAILED_PRECONDITION` while a subscription references
        the destination.
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
                $ref: '#/components/schemas/DeleteDestinationResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/integrations/slack-channels:
    get:
      operationId: IntegrationsService_ListSlackChannels
      summary: List Slack channels
      description: Returns the Slack channels visible to your organization's Slack OAuth integration.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListSlackChannelsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - IntegrationsService
  /v1/notifications/integrations/slack-channels/invite:
    post:
      operationId: IntegrationsService_InviteToSlackChannel
      summary: Join Slack channel
      description: Adds the CoreWeave Mission Control app to a Slack channel and returns the Slack destination
        for that channel.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InviteToSlackChannelRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InviteToSlackChannelResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - IntegrationsService
  /v1/notifications/queues/{destinationId}/messages:
    get:
      operationId: NotificationsService_ListQueueMessages
      summary: List queue messages
      description: Returns unacknowledged messages from a queue destination, oldest first.
      parameters:
      - name: destinationId
        in: path
        required: true
        schema:
          type: string
      - name: limit
        in: query
        description: The maximum number of messages to return, from `1` to `500`. Defaults to `100`.
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
      tags:
      - NotificationsService
  /v1/notifications/queues/{destinationId}/messages/ack:
    post:
      operationId: NotificationsService_AckQueueMessages
      summary: Acknowledge queue messages
      description: Removes processed messages from a queue destination and returns how many were removed.
      parameters:
      - name: destinationId
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AckQueueMessagesRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckQueueMessagesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/statuses:
    get:
      operationId: NotificationsService_ListStatuses
      summary: List delivery statuses
      description: Returns per-destination delivery records. Pass `requestId` to get every delivery of
        one alert.
      parameters:
      - name: requestId
        in: query
        description: Return every delivery of this alert. When set, the response ignores `fromDate`, `page`,
          and `pageSize`.
        schema:
          type: string
      - name: fromDate
        in: query
        description: Return only deliveries created at or after this RFC 3339 timestamp, such as `2026-10-01T00:00:00Z`.
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
        description: The number of delivery records per page. Defaults to `100`, which is also the maximum.
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
      tags:
      - NotificationsService
  /v1/notifications/subscriptions/alerts:
    get:
      operationId: NotificationsService_ListAlertSubscriptions
      summary: List alert subscriptions
      description: Returns the alert subscriptions in the caller's organization, one entry per alert and
        destination pair.
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
      tags:
      - NotificationsService
  /v1/notifications/subscriptions/alerts/categories/{category}/subscribe:
    post:
      operationId: NotificationsService_SubscribeToCategory
      summary: Subscribe to category
      description: Enables every alert in a category for one destination.
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
              $ref: '#/components/schemas/SubscribeToCategoryRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubscribeToCategoryResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - NotificationsService
  /v1/notifications/subscriptions/alerts/categories/{category}/unsubscribe:
    post:
      operationId: NotificationsService_UnsubscribeFromCategory
      summary: Unsubscribe from category
      description: Disables every alert in a category for one destination.
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
      tags:
      - NotificationsService
  /v1/notifications/subscriptions/alerts/{alertName}:
    put:
      operationId: NotificationsService_UpsertAlertSubscription
      summary: Set alert subscription
      description: Turns delivery of one alert to one destination on or off, creating the subscription
        if it doesn't exist.
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
      tags:
      - NotificationsService
components:
  schemas:
    AckQueueMessagesRequest:
      type: object
      properties:
        destinationId:
          description: The queue destination the messages belong to.
          type: string
        messageIds:
          description: Between 1 and 500 message IDs to acknowledge.
          type: array
          items:
            type: string
      required:
      - destinationId
      - messageIds
    AckQueueMessagesResponse:
      type: object
      properties:
        acked:
          description: The number of messages removed from the queue.
          type: integer
          format: int32
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
          description: The alert's category, for example `gpu`, `sunk`, `node`, `kubernetes`, `storage`,
            or `caios`.
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
    AlertSummary:
      description: One alert delivered to the `in_app` destination, with every channel it was delivered
        to.
      type: object
      properties:
        requestId:
          description: The unique identifier for the alert. Pass it to List delivery statuses for per-destination
            detail.
          type: string
        orgUid:
          description: The organization that received the alert.
          type: string
        templateId:
          description: The notification template used to render the message, `vm-alert` for alerts or
            `custom` for test notifications.
          type: string
        channels:
          description: Every channel the alert was delivered to.
          type: array
          items:
            type: string
        status:
          description: The status of the alert's `in_app` delivery. For other channels, use List delivery
            statuses. `DELIVERY_STATUS_STATE_UNSPECIFIED` means the status was never set.
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
    CreateCredentialRequest:
      type: object
      properties:
        displayName:
          description: A human-readable name for the credential, 1 to 255 characters.
          type: string
        credentialType:
          description: The kind of secret. Use `webhook` for generic webhooks, `slack_webhook` for Slack
            incoming webhooks, and `google_chat` for Google Chat webhooks. The Cloud Console creates `slack_oauth`
            credentials through the Slack OAuth flow.
          type: string
        secret:
          description: The secret value. For `webhook`, a JSON-encoded string with a required HTTPS `url`
            and an optional `signing_secret`. For `slack_webhook`, a URL that starts with `https://hooks.slack.com/services/`.
            For `google_chat`, a URL that starts with `https://chat.googleapis.com/v1/spaces/`.
          type: string
      required:
      - displayName
      - credentialType
      - secret
    CreateCredentialResponse:
      type: object
      properties:
        credential:
          $ref: '#/components/schemas/Credential'
    CreateDestinationRequest:
      type: object
      properties:
        channel:
          description: The delivery channel, `webhook`, `slack_webhook`, `google_chat`, or `queue`. `webhook`,
            `slack_webhook`, and `google_chat` require `credentialId`. Create `slack` destinations with
            Join Slack channel.
          type: string
        displayName:
          description: A human-readable name for the destination, 1 to 255 characters.
          type: string
        credentialId:
          description: The ID of a credential from Create credential. Required for `webhook`, `slack_webhook`,
            and `google_chat`.
          type: string
        config:
          description: Channel-specific configuration as a JSON-encoded string.
          type: string
      required:
      - channel
      - displayName
    CreateDestinationResponse:
      type: object
      properties:
        destination:
          $ref: '#/components/schemas/Destination'
    Credential:
      description: An encrypted secret that a destination uses to deliver alerts. The API never returns
        the secret value.
      type: object
      properties:
        id:
          description: The unique identifier for the credential.
          type: string
        orgUid:
          description: The organization that owns the credential.
          type: string
        displayName:
          description: A human-readable name for the credential.
          type: string
        credentialType:
          description: The kind of secret, such as `webhook`, `slack_webhook`, `google_chat`, or `slack_oauth`.
          type: string
        status:
          description: '`active` or `revoked`.'
          type: string
        createdAt:
          description: The time the credential was created.
          type: string
          format: date-time
    DeleteCredentialResponse:
      type: object
      properties: {}
    DeleteDestinationResponse:
      type: object
      properties: {}
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
          description: The notification template used to render the message, `vm-alert` for alerts or
            `custom` for test notifications.
          type: string
        channel:
          description: The channel the alert was delivered on.
          type: string
        status:
          description: The delivery state. `DELIVERY_STATUS_STATE_UNSPECIFIED` means the status was never
            set.
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
          description: The delivery channel, such as `webhook`, `slack`, `slack_webhook`, `google_chat`,
            `queue`, or `in_app`.
          type: string
        displayName:
          description: A human-readable name for the destination.
          type: string
        credentialId:
          description: The credential that holds the destination's secret URL or token, if the channel
            uses one.
          type: string
        config:
          description: Channel-specific configuration as a JSON-encoded string. Slack destinations use
            `{"channelId":"..."}`. Empty for channels that need no configuration.
          type: string
        credentialType:
          description: The type of the referenced credential, if any.
          type: string
        credentialStatus:
          description: The status of the referenced credential, `active` or `revoked`, if any.
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
      description: Contains an arbitrary serialized message along with a @type that describes the type
        of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    InviteToSlackChannelRequest:
      type: object
      properties:
        channelId:
          description: The Slack channel ID from List Slack channels.
          type: string
        displayName:
          description: A display name for the Slack destination.
          type: string
    InviteToSlackChannelResponse:
      type: object
      properties:
        destinationId:
          description: The ID of the Slack destination for the channel.
          type: string
    ListAlertSubscriptionsResponse:
      type: object
      properties:
        subscriptions:
          type: array
          items:
            $ref: '#/components/schemas/AlertSubscription'
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
    ListCredentialsResponse:
      type: object
      properties:
        credentials:
          type: array
          items:
            $ref: '#/components/schemas/Credential'
    ListDestinationsResponse:
      type: object
      properties:
        destinations:
          type: array
          items:
            $ref: '#/components/schemas/Destination'
    ListQueueMessagesResponse:
      type: object
      properties:
        messages:
          type: array
          items:
            $ref: '#/components/schemas/QueueMessage'
    ListSlackChannelsResponse:
      type: object
      properties:
        channels:
          type: array
          items:
            $ref: '#/components/schemas/SlackChannel'
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
          description: The page size used, at most 100. Zero when the request filtered by `requestId`.
          type: integer
          format: int32
        hasNextPage:
          description: Whether another page of results exists.
          type: boolean
    QueueMessage:
      description: An alert waiting in a queue destination.
      type: object
      properties:
        id:
          description: The unique identifier for the message. Pass it to Acknowledge queue messages.
          type: string
        createdAt:
          description: When the message was queued.
          type: string
          format: date-time
        payload:
          description: The alert, with the same `subject` and `body` fields, and optional `data` field,
            as a webhook delivery.
          type: object
        requestId:
          description: The alert this message belongs to. Matches `requestId` in delivery statuses and
            alerts.
          type: string
    SlackChannel:
      type: object
      properties:
        id:
          description: The Slack channel ID.
          type: string
        name:
          description: The Slack channel name.
          type: string
        isArchived:
          description: Whether the channel is archived.
          type: boolean
        isMember:
          description: Whether the CoreWeave Mission Control app is already in the channel.
          type: boolean
        numMembers:
          description: The number of members in the channel.
          type: integer
          format: int32
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
    SubscribeToCategoryRequest:
      type: object
      properties:
        category:
          description: The alert category, for example `gpu`.
          type: string
        destinationId:
          description: The destination to enable every alert in the category for.
          type: string
      required:
      - category
      - destinationId
    SubscribeToCategoryResponse:
      type: object
      properties: {}
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
    UpdateCredentialStatusRequest:
      type: object
      properties:
        id:
          description: The ID of the credential to update.
          type: string
        status:
          description: '`active` or `revoked`.'
          type: string
      required:
      - id
      - status
    UpdateCredentialStatusResponse:
      type: object
      properties:
        credential:
          $ref: '#/components/schemas/Credential'
    UpdateDestinationRequest:
      type: object
      properties:
        id:
          description: The ID of the destination to update.
          type: string
        displayName:
          description: A new display name, up to 255 characters. Empty keeps the current name.
          type: string
        credentialId:
          description: The ID of a replacement credential. Omit it to keep the current credential.
          type: string
        config:
          description: Replacement channel configuration as a JSON-encoded string. Empty keeps the current
            config.
          type: string
      required:
      - id
    UpdateDestinationResponse:
      type: object
      properties:
        destination:
          $ref: '#/components/schemas/Destination'
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer [API-ACCESS-TOKEN]
tags:
- name: IntegrationsService
  description: List and join Slack channels through your organization's Slack OAuth integration.
  x-group: IntegrationsService
- name: NotificationsService
  description: Manage destinations, credentials, and alert subscriptions, read delivery history, and pull
    alerts from queue destinations.
  x-group: NotificationsService
security:
- bearerAuth: []
```
