# Enable web browser access with CORS

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/configure-cors

# Enable web browser access with CORS

> Configure CORS policies to allow web browsers to access your Object Storage buckets from different domains.

To enable cross-origin resource sharing (CORS) for your CoreWeave AI Object Storage bucket, set an XML CORS configuration using the `s3:PutBucketCORS` action. This configuration defines which origins, HTTP methods, and headers are permitted. For more information about CORS, see [CORS for Web Browser Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html).

The following sections show two example CORS configurations.

## Prerequisites

* Have the `Object Storage Admin` IAM role (assigned through CoreWeave [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md)), or equivalent permissions to configure AI Object Storage access policies.
* Ensure that your AI Object Storage organization or bucket access policies grant your principal the `s3:PutBucketCORS` action (or `s3:*`) on the target bucket.
* Have the `aws s3api` CLI tool installed and configured for your AI Object Storage environment.

## All origins GET request

This policy allows cross-origin resource sharing for a specific bucket. The policy has one statement that allows all origins to perform `GET` requests on the bucket:

```xml title="All origins GET request" theme={"system"}
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
    </CORSRule>
</CORSConfiguration>
```

In this example, the CORS configuration allows any origin (`*`) to perform `GET` requests on the bucket. You can customize the `AllowedOrigin`, `AllowedMethod`, and `AllowedHeader` elements as needed.

To apply this CORS configuration, replace `[BUCKET-NAME]` with the name of your bucket, then run the following `aws s3api` command:

```bash theme={"system"}
aws s3api put-bucket-cors --bucket [BUCKET-NAME] --cors-configuration file://cors.xml
```

The `cors.xml` file contains the CORS configuration in XML format, like the preceding example.

## Specific origin with multiple methods

The following example restricts CORS to a specific origin and allows multiple HTTP methods and specific headers. The configuration also sets a `MaxAgeSeconds` value to cache the preflight response for 30 minutes and exposes a custom `x-amz-request-id` header to the client.

```xml title="Restrict to a specific origin and multiple methods" theme={"system"}
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>https://www.example.com</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedHeader>Authorization</AllowedHeader>
        <AllowedHeader>Content-Type</AllowedHeader>
        <MaxAgeSeconds>1800</MaxAgeSeconds>
        <ExposeHeader>x-amz-request-id</ExposeHeader>
    </CORSRule>
</CORSConfiguration>
```
