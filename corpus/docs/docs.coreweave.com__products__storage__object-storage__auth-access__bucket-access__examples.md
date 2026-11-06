# Bucket access policy examples

Source: https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/examples

# Bucket access policy examples

> Example bucket access policies for AI Object Storage

The following examples show common bucket access policy patterns. For details on how to apply a policy to a bucket, see [Manage bucket policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md).

## Allow read access for a user and group

The following policy allows read access to the specified bucket for one console user and one SAML group.

Fill in the following parameters in the policy:

* `[ORG-ID]` with your organization's ID.
* `[USER-ID]` with the console user's ID.
* `[SAML-GROUP-ID]` with the SAML group ID.
* `[BUCKET-NAME]` with the name of the bucket you want to grant read access to.

```json title="Allow read access for a user and group" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetObject",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Effect": "Allow",
      "Action": [
          "s3:GetObject",
          "s3:ListBucket"
          ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
        ],
      "Condition": {
          "StringEquals": {
              "cw:PrincipalOrgID": ["[ORG-ID]"]
          }
      }
    }
  ]
}
```

## Allow access from another organization

You can also use bucket access policies to grant users from other organizations access to your bucket. The following example grants read access to one console user and one SAML group, and scopes access to principals from your organization and one other organization:

Fill in the following parameters in the policy:

* `[ORG-ID]` with your organization's ID.
* `[OTHER-ORG-ID]` with the other organization's ID.
* `[USER-ID]` with the console user's ID.
* `[SAML-GROUP-ID]` with the SAML group ID.
* `[BUCKET-NAME]` with the name of the bucket you want to grant read access to.

```json title="Allow users from other organizations to access your bucket" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetObject",
      "Principal": {
        "CW": ["arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"],
        "AWS": ["arn:aws:iam::[ORG-ID]:saml/[SAML-GROUP-ID]"]
      },
      "Effect": "Allow",
      "Action": [
          "s3:GetObject",
          "s3:ListBucket"
          ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
        ],
      "Condition": {
          "StringEquals": {
              "cw:PrincipalOrgID": ["[ORG-ID]", "[OTHER-ORG-ID]"]
          }
      }
    }
  ]
}
```

## Prevent a specific user from deleting objects

This policy prevents a specific user from deleting objects. Replace `[ORG-ID]` with your organization's ID and `[USER-ID]` with the user's ID.

```json title="Prevent a specific user from deleting objects" theme={"system"}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "statement",
      "Effect": "Deny",
      "Principal": {
        "CW": "arn:aws:iam::[ORG-ID]:coreweave/[USER-ID]"
      },
      "Action": [
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:PutLifecycleConfiguration"
      ],
      "Resource": [
        "arn:aws:s3:::[BUCKET-NAME]",
        "arn:aws:s3:::[BUCKET-NAME]/*"
      ]
    }
  ]
}
```

## Additional resources

* [Manage bucket policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/manage-bucket-policies.md)
* [Bucket access policies](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md)
* [Access control for AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/auth-access/about.md)
