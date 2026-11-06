# Create access keys

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys

# Create access keys

> Create access keys for Object Storage using Cloud Console or API calls

This page shows you how to create the access keys you use to authenticate against CoreWeave AI Object Storage. You need access keys to call the [Object Storage S3 endpoint](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) and the [Object Storage API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md).

Access keys created with an API access token can be permanent or temporary. Permanent keys don't expire, while temporary keys are valid for a specified duration. You can create access keys in the CoreWeave Cloud Console or with the CoreWeave API. Choose the Cloud Console method for an interactive workflow, or the API method when you need to automate key creation.

> [!TIP]
>
> Most users no longer need to create a static Access Key. If you already authenticate with a [CoreWeave API access token](https://docs.coreweave.com/products/storage/object-storage/auth-access/create-access-tokens.md), exchange it directly for temporary credentials instead. See [Direct access token exchange](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md). Create a static key only when you specifically need a long-lived or manually managed key.

> [!NOTE]
>
> Production workloads should use [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) instead of static keys. Workload Identity Federation provides a more secure, controlled way to generate time-limited access keys by exchanging tokens from your compute platform or identity provider.

## Create access keys in the Cloud Console

> [!NOTE]
>
> Creating access keys in the Cloud Console requires the `Object Storage Admin` role or an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) that grants `cwobject:CreateAccessKey`.

1. In the Cloud Console, navigate to the [Access Keys](https://console.coreweave.com/object-storage/access-keys) page.
2. Click the **Create Key** button at the top right corner of the page.
3. In the dialog:
   * For a temporary key, enter the desired duration in seconds and click **Create**.
   * For a permanent key, select **Enable Permanent Key** and click **Create**.

![Create access key](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/create-access-key-cloud-console.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=d7b1175d25107de73754d311b3e522c8)

## Create access keys with the API

Use this method to create keys programmatically, for example, from a script or automated workflow. To create access keys with the API, you must first create a JSON object that defines the key's properties. The JSON object must include the `durationSeconds` property, which specifies how long the key is valid.

The following sections show how to create permanent and temporary keys.

### Permanent keys

Permanent keys don't expire and can be used indefinitely. To create a permanent access key, set `durationSeconds` to `0` in a JSON object. The value of `0` in the example `data.json` indicates that the key doesn't expire.

```json title="data.json" theme={"system"}
{
  "durationSeconds": 0
}
```

Then, submit the request to the `/access-key` endpoint with the JSON object in the body. Replace `[API-ACCESS-TOKEN]` with your API access token.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/access-key \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
     -d @data.json
```

A successful response returns the key with the `expiry` field set to `1970-01-01T00:00:00Z`, which indicates that the key doesn't expire.

```json title="Response status code 200" theme={"system"}
{
    "accessKeyID": "CWABCDEFGHIJKLMN",
    "expiry": "1970-01-01T00:00:00Z",
    "principalName": "coreweave/my-user@test.com",
    "secretKey": "cwo1234567890abcdefghijklmnopqrstuvwxyz1234"
}
```

### Temporary keys

To create temporary access keys, set `durationSeconds` to the desired duration in seconds. Temporary keys expire after the specified duration.

To begin, create a JSON object that defines `durationSeconds`. The following example creates a key with a 300-second (5-minute) duration.

```json title="data.json" theme={"system"}
{
  "durationSeconds": 300
}
```

Submit the request to the `/access-key` endpoint with the JSON object in the body. Replace `[API-ACCESS-TOKEN]` with your API access token.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/access-key \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
     -d @data.json
```

A successful response returns the key. The `expiry` field is set to the time the key expires.

```json title="Response status code 200" theme={"system"}
{
    "accessKeyID": "CWABCDEFGHIJKLMN",
    "expiry": "2024-01-01T09:15:01Z",
    "principalName": "coreweave/my-user@test.com",
    "secretKey": "cwo1234567890abcdefghijklmnopqrstuvwxyz1234"
}
```
