# Audit logging for AI Object Storage

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/audit-logging

# Audit logging for AI Object Storage

> Granular records of actions performed on your CoreWeave AI Object Storage resources

Audit logging for CoreWeave AI Object Storage provides granular records of actions performed on your object storage resources. This page explains the types of events captured, how logs are formatted and delivered, and how to enable audit logging for your organization or for specific buckets. Logs are written to a reserved bucket named `cw-[ORG-ID]-audit-logs` in your organization.

Audit logging supports the following use cases:

* Security and compliance teams: trace data access and administrative actions.
* Platform and storage admins: understand access patterns and debug incidents.
* Application engineers: correlate storage audit logs with application logs to investigate behavior during incidents.

> [!WARNING]
>
> **Limited availability**
>
> Audit logging is in limited availability. To request access, [contact the CoreWeave Support team](https://docs.coreweave.com/support.md).

## Log types

Audit logging captures two types of events: control plane events and data plane events.

### Control plane logs

Control plane logs capture administrative and configuration-level events, including:

* Key creation
* Key revocation
* Audit logging enabled for a bucket or for the organization
* Audit logging disabled

Each control plane log entry includes the following fields (not exhaustive):

| Field | Description |
| - | - |
| `action` | The action performed |
| `principal` | The identity that performed the action |
| `principalRole` | The role associated with the principal |
| `timestamp` | When the action occurred |
| `identifier` | The access key ID or bucket name, depending on the event |
| `duration_seconds` | Duration of the action in seconds |

Control plane logs are stored under a `cw-control-plane/` prefix in your organization's audit logging bucket, partitioned by date and time.

### Data plane logs

Data plane logs capture authenticated access to data, including:

* Object operations such as puts, gets, and deletes
* Bucket operations such as bucket creation and listings

Each data plane log entry includes the following fields (not exhaustive):

| Field | Description |
| - | - |
| `action` | The operation performed |
| `aws:arn` | The resource ARN; for object operations, includes the object key path |
| `principal` | The identity ARN of the principal that performed the operation |
| `timestamp` | When the operation occurred |
| `sourceIp` | The source IP address of the request |
| `host` | The HTTP Host header of the request |
| `bucketName` | The name of the bucket |
| `accessKeyId` | The access key ID used |
| `requestId` | A correlation handle for logs and request traces |

Data plane logs are stored under a `cw-data-plane/` prefix in your organization's audit logging bucket, partitioned by date and time.

## Log format and delivery

CoreWeave batches and compresses audit log events before writing them to the audit logging bucket. Events are written to a durable message queue and bundled at least every 15 minutes before persistence.

The on-disk format is line-delimited JSON, where each line is a JSON object, stored in compressed files (`.json` or `.json.gz`). Object keys follow this format:

| Log type | Object key format |
| - | - |
| Control plane | `cw-control-plane/YYYY/MM/DD/HHMM+[ID].[FILE-FORMAT]` |
| Data plane | `cw-data-plane/YYYY/MM/DD/HHMM+[ID].[FILE-FORMAT]` |

Keep the following in mind when processing audit logs:

* The order of events inside a bundle doesn't necessarily match the order in which CoreWeave generated them.
* The order of bundles written to the audit logging bucket doesn't reflect the precise generation order.
* A single request (for example, a multi-object delete) can generate multiple log entries.

### Audit logging bucket

Each organization has one audit logging bucket, named `cw-[ORG-ID]-audit-logs`, where `[ORG-ID]` is your organization ID. The bucket is isolated per organization and governed by your organization access policies and bucket access policies. You are responsible for managing the data in the bucket and pay storage fees for that data. For billing details, see [Usage-based billing](https://docs.coreweave.com/products/storage/object-storage/about.md#usage-based-billing) and [pricing](https://www.coreweave.com/pricing).

## Configuration

Audit logging can be configured at the organization level or at the individual bucket level, so you can choose the right scope for your use case.

| Scope | What it controls | API endpoint |
| - | - | - |
| Organization | Control plane events; data plane events for buckets created after the setting is enabled | [SetOrganizationSettings](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-organization-settings.md) |
| Bucket | Data plane events for a specific bucket | [SetBucketSettings](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-bucket-settings.md) |

Control plane logging can only be enabled at the organization level. It cannot be scoped to individual buckets.

When you enable data plane logging at the organization level, it applies only to new buckets created after the setting is enabled. Buckets that already exist keep their prior data plane logging state until you enable data plane logging for each bucket. Because high-traffic buckets can produce large volumes of log data, per-bucket logging is more targeted and can help avoid unexpected storage fees.

## Enable audit logging

Enabling audit logging requires steps from both CoreWeave and your team. CoreWeave provisions your destination bucket and enables the feature on the backend. You configure the bucket access policy and logging settings.

### Prerequisites

Enabling audit logging requires two separate permissions:

* **To set the bucket access policy**: An [AI Object Storage Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) and an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md) that allows `s3:PutBucketPolicy` on the `cw-[ORG-ID]-audit-logs` bucket (or `s3:*` on all buckets).
* **To call the Object Storage API**: A [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) for a principal with the [Object Storage Admin role](https://docs.coreweave.com/security/iam/access-policies/roles.md#object-storage) or the applicable granular `cwobject:` permissions in an organization access policy.

### Steps

1. [Contact CoreWeave support](https://coreweave.freshdesk.com/support/login) to request enablement, and include your organization name and Org ID.

   Your **Org ID** is a short hexadecimal string (for example, `ab1cd2`). Find it on the [Settings page](https://console.coreweave.com/account/settings) of your Cloud Console account.

   CoreWeave creates your `cw-[ORG-ID]-audit-logs` destination bucket as part of the enablement process.

2. After CoreWeave creates the destination bucket, apply a bucket access policy granting the CoreWeave audit logging service account permission to write logs. The policy must grant at minimum `s3:ListBucket` and `s3:PutObject`. Replace `[ORG-ID]` with your organization ID.

   ```json title="audit-logging-bucket-access-policy.json" theme={"system"}
   {
     "Statement": [
       {
         "Sid": "AllowAuditLoggingServiceAccount",
         "Action": [
           "s3:ListBucket",
           "s3:PutObject"
         ],
         "Effect": "Allow",
         "Principal": {
           "CW": [
             "arn:aws:iam::coreweave:static/audit-logs"
           ]
         },
         "Resource": [
           "arn:aws:s3:::cw-[ORG-ID]-audit-logs",
           "arn:aws:s3:::cw-[ORG-ID]-audit-logs/*"
         ]
       }
     ],
     "Version": "2012-10-17"
   }
   ```

   For instructions on applying this policy using S3 clients or Terraform, see [Manage bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md).

3. Notify CoreWeave that you've applied the bucket access policy, either by replying to your CoreWeave support ticket or by notifying CoreWeave through your support Slack channel. The CoreWeave admin then finishes enabling audit logging for your organization.

   After CoreWeave confirms that audit logging is enabled for your organization, you can choose which event types to capture.

4. Call the Object Storage API to enable the types of logs you want. In each request, replace `[API-ACCESS-TOKEN]` with the [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) for the `Object Storage Admin` role:

   * Use organization-level settings to enable control plane logging, data plane logging for all buckets created after the setting is enabled, or both.
   * Use bucket-level settings to enable data plane logging for a specific bucket only.

   > [tab] Organization-level
   >
   > Organization-level settings let you enable control plane logging, data plane logging for all buckets created after the setting is enabled, or both.
   >
   > Set the flags to `true` or `false` based on which event types you want to log:
   >
   > * `controlPlaneAuditLoggingEnabled`: Control plane logging
   > * `bucketAuditLoggingEnabled`: Data plane logging for buckets created after the setting is enabled
   >
   > Save the following as `organization-settings.json`:
   >
   > ```json title="organization-settings.json" theme={"system"}
   > {
   >   "settings": {
   >     "controlPlaneAuditLoggingEnabled": true,
   >     "bucketAuditLoggingEnabled": true
   >   }
   > }
   > ```
   >
   > Submit the request:
   >
   > ```bash title="Example request" theme={"system"}
   > curl -X PUT https://api.coreweave.com/v1/cwobject/organization/settings \
   >   -H "Content-Type: application/json" \
   >   -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
   >   -d @organization-settings.json
   > ```
   >
   > A successful response returns the updated organization settings:
   >
   > ```json title="Response status code 200" theme={"system"}
   > {
   >   "settings": {
   >     "controlPlaneAuditLoggingEnabled": true,
   >     "bucketAuditLoggingEnabled": true
   >   }
   > }
   > ```

   > [tab] Bucket-level
   >
   > Bucket-level settings enable data plane logging for a specific bucket. Control plane logging is not available at the bucket level.
   >
   > Save the following as `bucket-settings.json`, replacing `[BUCKET-NAME]` with the name of the bucket to monitor. Set the `auditLoggingEnabled` flag to `true` to enable data plane logging for the bucket.
   >
   > ```json title="bucket-settings.json" theme={"system"}
   > {
   >   "bucketName": "[BUCKET-NAME]",
   >   "settings": {
   >     "auditLoggingEnabled": true
   >   }
   > }
   > ```
   >
   > Submit the request:
   >
   > ```bash title="Example request" theme={"system"}
   > curl -X PUT https://api.coreweave.com/v1/cwobject/bucket/settings \
   >   -H "Content-Type: application/json" \
   >   -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
   >   -d @bucket-settings.json
   > ```
   >
   > A successful response returns the updated bucket settings:
   >
   > ```json title="Response status code 200" theme={"system"}
   > {
   >   "settings": {
   >     "auditLoggingEnabled": true
   >   }
   > }
   > ```
   >
   > You can also modify bucket settings in Terraform using the [coreweave\_object\_storage\_bucket\_settings](https://docs.coreweave.com/platform/terraform/resources/object_storage_bucket_settings.md) resource.
