# Enterprise licenses

Source: https://docs.coreweave.com/products/wandb/platform/hosting/enterprise-licenses

# Enterprise licenses

> Learn about Weights & Biases Enterprise licenses, what features they include, and how to obtain and configure them.

An Enterprise license unlocks Weights & Biases features designed for organizations that need enhanced capabilities in areas of security, compliance, or administration. See the list of [Enterprise features](#enterprise-features).

An Enterprise license includes the following:

* **Security**: Enhanced authentication, encryption, and access controls.
* **Compliance**: Audit logging, HIPAA compliance options, and data governance controls.
* **Administration**: User management features like SCIM provisioning, custom roles, and automation capabilities.

This page is for administrators responsible for Weights & Biases deployments. It explains what Enterprise features are available, how to obtain a license, and how to configure and verify it for your deployment.

## Deployment options

Enterprise licenses are available for W\&B Dedicated Cloud and Self-Managed deployments. The configuration steps differ depending on which deployment you use.

* [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) provides dedicated, isolated infrastructure managed by Weights & Biases, deployed in Google Cloud. Dedicated Cloud deployments automatically include an Enterprise license. You don't need to configure anything, and all Enterprise features become available as soon as Weights & Biases provisions your deployment.
* [W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) deploys on your own infrastructure, providing full control over your deployment and data. W\&B Self-Managed supports air-gapped deployments. Without an Enterprise license, [Enterprise features](#enterprise-features) are unavailable.

## Obtain an Enterprise license

How you obtain an Enterprise license depends on your deployment type. Select the tab that matches your use case to continue.

> [tab] Dedicated Cloud
>
> W\&B Dedicated Cloud includes an Enterprise license, and no action is required. [Start an Enterprise trial](https://wandb.ai/site/for-enterprise/dedicated-saas-trial/) or contact [Sales](https://www.coreweave.com/contact-us) to discuss your requirements.

> [tab] Self-Managed
>
> Request an Enterprise license:
>
> * **Evaluation**: Submit the [Request a trial license](https://wandb.ai/site/for-enterprise/self-hosted-trial) form or contact [Sales](https://www.coreweave.com/contact-us) to discuss your requirements.
>
> * **Production**: Contact [Sales](https://www.coreweave.com/contact-us) to discuss your deployment requirements and sizing, and to receive your license details.
>
> > [!WARNING]
> >
> > Store license keys securely and treat them as sensitive credentials.

## Configure an Enterprise license

> [!NOTE]
>
> This section is relevant only for W\&B Self-Managed. Dedicated Cloud deployments don't require manual configuration.

After you [obtain an Enterprise license](#obtain-an-enterprise-license), you can configure it programmatically as part of your deployment or in the W\&B App after deployment. Select the tab that matches your deployment method.

> [tab] Kubernetes Operator
>
> 1. Update your `operator.yaml` (the `WeightsAndBiases` custom resource) to set the license. Replace `[YOUR-LICENSE-KEY]` with the license key you received from Weights & Biases:
>
>    ```yaml theme={"system"}
>    spec:
>      values:
>        global:
>          license: "[YOUR-LICENSE-KEY]"
>    ```
>
> 2. Apply the updated configuration:
>    ```bash theme={"system"}
>    kubectl apply -f operator.yaml
>    ```

> [tab] Terraform
>
> 1. Update your Terraform variables. Replace `[YOUR-LICENSE-KEY]` with the license key you received from Weights & Biases:
>
>    ```hcl theme={"system"}
>    variable "license" {
>      default = "[YOUR-LICENSE-KEY]"
>    }
>    ```
>
> 2. Apply the Terraform configuration:
>    ```bash theme={"system"}
>    terraform apply -var="license=$LICENSE_KEY"
>    ```

> [tab] W\&B App
>
> For existing deployments without environment variable configuration:
>
> 1. Log in as an admin user.
> 2. Navigate to **System Settings**.
> 3. Find the **License** section.
> 4. Enter your new license key.
> 5. Save the changes.

> [tab] Docker
>
> \[!WARNING] Deploying Weights & Biases on Docker is deprecated. Weights & Biases strongly encourages migrating to a [Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) deployment managed by Helm or Terraform. Refer to [Reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md) or contact [Support](mailto:forge-support@coreweave.com) for guidance.
> Set the `LICENSE` environment variable. Replace `[YOUR-LICENSE-KEY]` with the license key you received from Weights & Biases:
>
> ```bash theme={"system"}
> docker run -d \
>   -e LICENSE="[YOUR-LICENSE-KEY]" \
>   -e OTHER_ENV_VARS \
>   wandb/local
> ```

Next, [verify your Enterprise license](#verify-and-manage-an-enterprise-license).

## Verify and manage an Enterprise license

After you configure a license, verify that it's active and review its entitlements. As an instance or organization admin, follow these steps:

1. In the W\&B App, click your user profile icon in the top right, then click **System Console**.
2. Go to the **License** tab. A dashboard summarizes the license entitlements, expiration, and usage over time. If you see an error, see [Common issues](#common-issues).
3. For detailed information about the license and its entitlements, click **View license online**.

   From this page, you can also order a new trial or production license. At the top of the page, click **New license order** and submit the form.
4. To renew an expired license or to update the license key, click **Update License**.

> [!TIP]
>
> To ensure uninterrupted service, Weights & Biases contacts you:
>
> * 30 days before the license expires.
> * When the license has expired.

## Enterprise features

For a full, categorized list of available Enterprise features, see the [Pricing](https://coreweave.com/forge-pricing) page, then click **Cloud-hosted** or **Privately-hosted**.

## Common issues

If you encounter problems configuring or using your Enterprise license, review the following common issues before contacting support.

### License not recognized

If your license isn't recognized, check the following:

* Verify that the license key is correctly formatted (no extra spaces).
* Ensure that the license hasn't expired.
* Check that the license is set in the correct configuration location.

### Features not available after setting license

If features aren't available after you set the license, try the following:

* Restart your Weights & Biases services after setting the license.
* Verify that the license includes the specific features you're trying to access.
* Check the system logs for any license validation errors.

### License expiration warnings

To stay ahead of license expiration:

* Monitor the **System Settings** page for expiration notifications.
* Set up alerts for license expiration in your monitoring system.
* Keep your account team contact information up to date.

### Get support

For assistance with Enterprise licenses, contact your account team, [Sales](https://www.coreweave.com/contact-us), or [Support](mailto:forge-support@coreweave.com).

## Additional resources

* [Pricing](https://coreweave.com/forge-pricing)
* [W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md)
* [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md)
* [Security and compliance](https://wandb.ai/site/security/)
