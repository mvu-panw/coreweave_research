# Usage information and limits

Source: https://docs.coreweave.com/products/inference/serverless/usage-limits

# Usage information and limits

> Understand pricing, usage limits, and account restrictions for Serverless Inference


This page describes the pricing, usage limits, and account restrictions that apply to Serverless Inference. Use this information to plan your usage and avoid unexpected charges or interruptions. Review it before you send production traffic, especially if you manage billing or operate at higher concurrency.

> [!NOTE]
>
> If you have questions about pricing, limits, or your account that this page doesn't answer, contact [Support](mailto:forge-support@coreweave.com) to discuss your requirements.

## View billing and usage information

Organization admins can track credit balance and usage history from the Forge console:

1. In the top right corner, click your **user profile icon**.
2. Select **Billing**.
3. Select the **Usage & Alerts** tab.
4. Choose **Inference** from the sidebar menu.
5. From here you can:
   * See your usage over time.
   * Configure spend alerts.

## Pricing

For detailed model pricing information, visit [Serverless Inference pricing](https://coreweave.com/forge-pricing/inference-agents).

## Purchase more credits

Serverless Inference credits come with Free, Pro, and Academic plans for a limited time. Enterprise availability may vary. When credits run out:

* **Free accounts** must activate pay-as-you-go inference on the **Billing** tab, or upgrade to a paid plan to continue using Serverless Inference. [Activate pay-as-you-go or upgrade](https://forge.coreweave.com/subscriptions).
* CoreWeave bills **Pro plan users** for overages monthly, based on [model-specific pricing](https://coreweave.com/forge-pricing/inference-agents).
* **Enterprise accounts** should contact their account executive.

## Account tiers and default usage caps

Each account tier has a default spending cap to help manage costs and prevent unexpected charges. CoreWeave requires prepayment for paid Serverless Inference access.

The following table shows the default cap for each tier and how to request a change. If you need to change your cap, contact your account executive or [Support](mailto:forge-support@coreweave.com) to adjust your limit.

| Account tier | Default cap | How to change limit |
| - | - | - |
| Free | \$100/month | Upgrade to Pro or Enterprise |
| Pro | \$6,000/month | Contact your account executive or support for manual review |
| Enterprise | \$700,000/year | Contact your account executive or support for manual review |

## Concurrency limits

Concurrency limits protect service quality by capping how many requests a project or user can have in flight at once. If you exceed the concurrency limit, the API returns a `429 Concurrency limit reached for requests` response. To fix this error, reduce the number of concurrent requests.

CoreWeave applies concurrency limits per Weights & Biases project and per user. For example, if you have three projects in a team, each project has its own concurrency limit quota.

If your use case requires increased limits, contact [Support](mailto:forge-support@coreweave.com) to discuss your requirements.

## Geographic restrictions

Serverless Inference is available only from supported geographic locations, due to compliance and regulatory requirements, including U.S. trade controls. Serverless Inference determines your location from your IP address at the time of each request, and returns a `403` error for requests from other locations.

CoreWeave doesn't publish the full list of locations that Serverless Inference blocks, because the list changes as regulatory requirements change. To confirm whether your location is supported, email [Forge Support](mailto:forge-support@coreweave.com). For the trade sanctions terms that apply, see the [CoreWeave Terms of Service](https://docs.coreweave.com/policies/terms-of-service.md). For help with the error, see [API error code 403 - Country, region, or territory not supported](https://docs.coreweave.com/support/inference/articles/api-error-code-403-country-region-or-ter).

## Next steps

See [available models](https://docs.coreweave.com/products/inference/serverless/models.md) and their specific pricing.
