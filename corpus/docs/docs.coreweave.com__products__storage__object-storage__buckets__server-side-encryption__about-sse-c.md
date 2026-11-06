# About SSE-C

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c

# About SSE-C

> Understand server-side encryption with customer keys for AI Object Storage

Server-side encryption with customer keys (SSE-C) lets you encrypt your data in CoreWeave AI Object Storage using encryption keys that you provide and manage. This approach gives you complete control over your encryption keys, while CoreWeave handles the encryption and decryption process on your behalf.

SSE-C is ideal for scenarios where you need:

* **Regulatory compliance**: Meet requirements for customer-managed encryption keys.
* **Enhanced security**: Maintain complete control over your encryption keys.
* **Multi-tenant environments**: Use different keys for different customers or projects.
* **Key rotation**: Implement your own key rotation policies.
* **Audit requirements**: Demonstrate control over encryption key management.

## How SSE-C works

This section explains the upload and retrieval flow so you can understand what CoreWeave does with your key at each step.

SSE-C provides encryption at rest for your objects stored in AI Object Storage. When you upload an object with SSE-C enabled, you provide an encryption key with your request. CoreWeave uses this key to encrypt your data before storing it. The encryption key is never stored with your data. Only a hash of the key is retained for verification.

When you retrieve an object, you must provide the same encryption key that was used during upload. CoreWeave uses this key to decrypt your data before returning it to you.

## Key verification

CoreWeave AI Object Storage uses your provided key to encrypt or decrypt your data as required, but doesn't permanently store that key itself. Instead, CoreWeave stores only a base64-encoded MD5 digest of your encryption key.

This hash is stored solely for verification. When you later access the object, you must supply the same key and hash you used originally. CoreWeave checks the hash of the supplied key against the stored hash to verify that the correct key is provided before attempting decryption.

> [!NOTE]
>
> **Why only the hash?**
>
> The hash of the key serves as a checksum: it can verify that the key is correct, but it can't be used to reconstruct the actual key. By storing only the hash and not the key itself, CoreWeave ensures that only someone who possesses the original encryption key can access the corresponding encrypted data. If you lose your key, neither you nor CoreWeave can recover your data. The hash makes it computationally infeasible to recover the original key due to the one-way nature of cryptographic hashes.

## Key characteristics

| Characteristic | Description |
| - | - |
| **Customer-managed keys** | You generate, store, and manage your encryption keys outside of CoreWeave |
| **Key verification** | CoreWeave stores only a hash of your encryption key for verification |
| **S3 compatibility** | SSE-C works with standard S3-compatible tools and libraries |
| **Per-request encryption** | You can use different keys for different objects or requests |
| **Automatic encryption and decryption** | CoreWeave handles the encryption and decryption process transparently |

## Supported encryption algorithms

CoreWeave AI Object Storage supports the following encryption algorithms for SSE-C:

* **AES-256**: Advanced Encryption Standard with 256-bit keys.
* **SHA-256**: Secure Hash Algorithm 256 for key verification.

## Security considerations and responsibilities

Because you control the encryption keys, you take on responsibilities that CoreWeave handles for other encryption modes. When using SSE-C, you're responsible for:

| Responsibility | Description |
| - | - |
| **Key generation** | Creating cryptographically strong encryption keys |
| **Key storage** | Securely storing your encryption keys outside of CoreWeave |
| **Key distribution** | Safely distributing keys to authorized applications |
| **Key rotation** | Implementing key rotation policies according to your security requirements |
| **Key backup** | Ensuring your keys are backed up securely |

> [!CAUTION]
>
> **You must store your encryption key**
>
> If you lose your encryption key, you can't recover your encrypted data. CoreWeave doesn't store your encryption keys, and can't decrypt your data without them. See the [Key management](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/use-sse-c.md#key-management) section for best practices on storing and managing your encryption keys securely.

## Integration with LOTA

SSE-C is compatible with [CoreWeave's Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). When you retrieve objects using SSE-C, the data remains encrypted in the cache, maintaining the same security as your original encrypted objects.

## API compatibility

SSE-C is implemented using standard S3-compatible headers and follows the S3 SSE-C specification. This means you can use any S3-compatible tool or library that supports SSE-C with CoreWeave AI Object Storage.

> [!NOTE]
>
> For detailed API information, see the [S3 compatibility reference](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#server-side-encryption-with-customer-provided-keys-sse-c).

## Additional resources

* Learn how to [use SSE-C with your applications](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/use-sse-c.md).
* Review the [S3-compatible API reference](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) for SSE-C headers and parameters.
