# About buckets

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/about

# About buckets

> Learn about AI Object Storage buckets as primary organizational containers, including prerequisites

Buckets are the primary organizational containers for your data in CoreWeave AI Object Storage. Think of them as top-level folders that contain your objects (files). Each bucket has a globally unique name and its own access policies.

> [accordion] Bucket naming rules
>
> Bucket names must be globally unique and adhere to the following rules:
>
> * **Length:** 3 to 63 characters.
> * **Characters:** Only lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`). No dots, uppercase letters, underscores, spaces, or other special characters.
> * **Start and end:** Must begin and end with a letter or number. Cannot start or end with a hyphen (`-`).
> * **Prohibited patterns:** Cannot start with `xn--`.
> * **Reserved:** Must not begin with `cw-`, `vip-`, or `log-stitcher-ch-`. Must not be the exact name `int`. CoreWeave reserves these for internal use.

## Prerequisites

After you've set up authentication and access control (access tokens, access keys, and organization policies), you can create and use buckets in Object Storage.

Before you create your first bucket, [set up your endpoint configuration once](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md) to use the required virtual-hosted addressing style and the correct endpoints for AI Object Storage. This helps reduce errors.

## Typical workflow

To start using Object Storage buckets, follow these steps:

1. Configure [authentication and access control](https://docs.coreweave.com/products/storage/object-storage/auth-access/about.md), making sure to set an [organization access policy](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md).
2. [Attach your endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md) (one-time setup).
3. Optional: Set a bucket access policy to control a specific resource.
4. Create buckets for different projects or purposes.
5. Upload objects using your preferred tools.

To manage buckets and objects, you can use the [Object Storage S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md), as well as command-line tools and libraries such as the AWS CLI, `s3cmd`, and Boto3. You can also use Cyberduck or Cloud Console.

## Bucket security

Two levels of policies control access to buckets:

* **Organization policies**: Authorize principals in your organization.
* **Bucket policies**: Control a specific resource, including access from other organizations.

For more information, see [Policy evaluation](https://docs.coreweave.com/products/storage/object-storage/auth-access/policies.md#policy-evaluation) and [Bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md).
