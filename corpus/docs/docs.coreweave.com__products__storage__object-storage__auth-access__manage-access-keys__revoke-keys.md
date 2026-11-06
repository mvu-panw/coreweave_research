# Revoke access keys

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/revoke-keys

# Revoke access keys

> Revoke Object Storage access keys using the Cloud Console or the Object Storage API

Revoking an Object Storage access key invalidates it so it can no longer authenticate requests. Revoke keys when credentials are compromised, when a user leaves your organization, or as part of routine credential rotation. You can revoke access keys two ways: through the Cloud Console for individual keys, and through the Object Storage API for individual keys or all keys associated with a principal.

## Prerequisites

* You must be signed in as a user who has the **Object Storage Admin** IAM role or an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/about.md) that grants `cwobject:RevokeAccessKeyByAccessKey` for individual keys and `cwobject:RevokeAccessKeysByPrincipal` for principal-wide revocation. See the [Console permissions reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/console-permissions.md).
* You must have an [AI Object Storage access key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) to revoke.

## Revoke keys in Cloud Console

Use the Cloud Console to revoke a single access key through the web UI. This is the quickest option when you know which key to revoke and only need to revoke one at a time.

1. Navigate to the [Access Keys](https://console.coreweave.com/object-storage/access-keys) page in the Cloud Console.

2. Use the **Search** function to find keys by name or principal.

   ![Access Keys page in the Cloud Console showing a list of Object Storage keys](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/storage/_media/cloud-console-object-storage-keys.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=94cd5bcaa714cfe30927e90e7bb21c4b)

3. Click the **More** menu on the right of the key you want to revoke.

4. Click **Revoke**.

5. In the **Revoke Key** modal, type the ID of the key you want to revoke and click **Revoke**. Typing the ID confirms that you intend to revoke this specific key.

After you complete these steps, the key is revoked and no longer appears as active on the Access Keys page. Any requests made with the revoked key fail to authenticate.

## Revoke keys with the Object Storage API

Use the Object Storage API to script revocations, integrate revocation into automated workflows, or revoke many keys at once. The [Object Storage API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref.md) provides endpoints to revoke individual access keys, or all keys associated with a principal.

### Revoke an individual access key

Use this approach when you need to invalidate one specific key, such as when a single credential is compromised or no longer needed.

To revoke an access key, first create a JSON object that specifies the key ID. Replace `[ACCESS-KEY-ID]` with the ID of the key to revoke.

```json title="data.json" theme={"system"}
{
  "accessKey": "[ACCESS-KEY-ID]"
}
```

Then, submit the request to the `/revoke-access-key/access-key` endpoint with the JSON object in the body. Replace `[API-ACCESS-TOKEN]` with your API access token.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/revoke-access-key/access-key \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
       -d @data.json
```

A successful response returns an empty object and the key is revoked. Subsequent requests made with the revoked key fail to authenticate.

```json title="Response status code 200" theme={"system"}
{}
```

### Revoke all access keys for a principal

Use this approach to revoke every key associated with a single principal at once, such as when a user leaves your organization or when you need to fully rotate credentials for a service account.

To revoke all access keys for a principal, create a JSON object that specifies the principal name. Replace `[PRINCIPAL-NAME]` with the principal whose keys you want to revoke (for example, `coreweave/user-uid` or `saml/user@example.com`).

```json title="data.json" theme={"system"}
{
  "principalName": "[PRINCIPAL-NAME]"
}
```

Then, submit the request to the `/revoke-access-key/principal` endpoint with the JSON object in the body. Replace `[API-ACCESS-TOKEN]` with your API access token.

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/revoke-access-key/principal \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
       -d @data.json
```

A successful response returns an empty object and all keys for the principal are revoked. The principal can't authenticate any Object Storage request until new keys are issued.

```json title="Response status code 200" theme={"system"}
{}
```
