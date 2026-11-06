# Configure SSO with OIDC

Source: https://docs.coreweave.com/products/wandb/platform/hosting/iam/sso

# Configure SSO with OIDC

> Configure Weights & Biases SSO with OpenID Connect providers such as Okta, Azure AD, and AWS Cognito.

This guide is for administrators of W\&B Dedicated Cloud or Self-Managed instances who want to enable single sign-on (SSO) using an OpenID Connect (OIDC) compatible identity provider. By the end, you've configured your identity provider, connected it to Weights & Biases so that users can sign in through your organization's existing identity system, and you can manage user identities and group memberships through providers like Okta, Keycloak, Auth0, Google, and Entra.

## OpenID Connect

Weights & Biases supports the following OIDC authentication flows for integrating with external Identity Providers (IdPs):

* Implicit flow with form post.
* Authorization code flow with Proof Key for Code Exchange (PKCE).

These flows authenticate users and provide Weights & Biases with the identity information (in the form of ID tokens) needed to manage access control.

The ID token is a JWT that contains the user's identity information, such as their name, username, email, and group memberships. Weights & Biases uses this token to authenticate the user and map them to appropriate roles or groups in the system.

In the context of Weights & Biases, access tokens authorize requests to APIs on behalf of the user, but because Weights & Biases's primary concern is user authentication and identity, it only requires the ID token.

You can use environment variables to [configure IAM options](https://docs.coreweave.com/products/wandb/platform/hosting/iam/advanced_env_vars.md) for your [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) instance.

To assist with configuring Identity Providers for [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) deployments, follow these guidelines. If you're using W\&B Multi-tenant Cloud, reach out to [forge-support@coreweave.com](mailto:forge-support@coreweave.com) for assistance.

## Configure your IdP

The following sections describe how to configure your identity provider (IdP) for OIDC. Complete the configuration steps for your IdP first. You use the resulting **Client ID**, **Issuer URL**, and (optionally) **Client Secret** when you set up SSO in Weights & Biases in the next section. Select the tab for your IdP for details.

> [tab] Cognito
>
> Follow this procedure to set up AWS Cognito as your IdP. At the end, you have a **Client ID** and **OIDC issuer URL** to use when you configure Weights & Biases.
>
> 1. Sign in to your AWS account and navigate to the [AWS Cognito](https://aws.amazon.com/cognito/) App.
>
>    ![AWS Cognito setup](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/setup_aws_cognito.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=97d69ef033862f40319dc004ef2439b7)
>
> 2. Provide an allowed callback URL to configure the application in your IdP. Add `http(s)://[YOUR-W-AND-B-HOST]/oidc/callback` as the callback URL. Replace `[YOUR-W-AND-B-HOST]` with your Weights & Biases host path.
>
> 3. If your IdP supports universal logout, set the Logout URL to `http(s)://[YOUR-W-AND-B-HOST]`. Replace `[YOUR-W-AND-B-HOST]` with your Weights & Biases host path.
>
>    For example, if your application runs at `https://wandb.mycompany.com`, replace `[YOUR-W-AND-B-HOST]` with `wandb.mycompany.com`.
>
>    The following image demonstrates how to provide allowed callback and sign-out URLs in AWS Cognito.
>
>    ![Host configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/setup_aws_cognito_ui_settings.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=0d936108334e39bf4de873f979bdbb21)
>
>    `wandb/local` uses the [`implicit` grant with the `form_post` response type](https://auth0.com/docs/get-started/authentication-and-authorization-flow/implicit-flow-with-form-post) by default.
>
>    You can also configure `wandb/local` to perform an `authorization_code` grant that uses the [PKCE Code Exchange](https://www.oauth.com/oauth2-servers/pkce/) flow.
>
> 4. Select one or more OAuth grant types to configure how AWS Cognito delivers tokens to your app.
>
> 5. Weights & Biases requires specific OpenID Connect (OIDC) scopes. Select the following from AWS Cognito App:
>
>    * `openid`
>    * `profile`
>    * `email`
>
>    For example, your AWS Cognito App UI should look similar to the following image:
>
>    ![Required fields](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/setup_aws_required_fields.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=02020eb604d0b7f8c42c4a49baf60ab4)
>
>    Select the **Auth Method** in the settings page or set the `OIDC_AUTH_METHOD` environment variable to specify which grant `wandb/local` uses.
>
>    You must set the **Auth Method** to `pkce`.
>
> 6. You need a **Client ID** and the URL of your OIDC issuer. The OpenID discovery document must be available at `$OIDC_ISSUER/.well-known/openid-configuration`.
>
>    For example, you can generate your issuer URL by appending your User Pool ID to the Cognito IdP URL from the **App Integration** tab within the **User Pools** section:
>
>    ![AWS Cognito issuer URL](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/setup_aws_cognito_issuer_url.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=302b9baea3e7d017f46a16ff31260ae5)
>
>    Don't use the Cognito domain for the IdP URL. Cognito provides its discovery document at `https://cognito-idp.$REGION.amazonaws.com/$USER_POOL_ID`.
>
> Next, [Set up SSO in Weights & Biases](#set-up-sso-in-w%26b).

> [tab] Okta
>
> Follow this procedure to set up Okta as your IdP. At the end, you have a **Client ID** and **OIDC issuer URL** to use when you configure Weights & Biases.
>
> 1. Sign in to the [Okta Portal](https://login.okta.com/).
>
> 2. On the left side, select **Applications** and then **Applications** again.
>
>    ![Okta Applications menu](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_select_applications.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=e643af5b8e0d40fc7380f3c9f86ce080)
>
> 3. Click **Create App integration**.
>
>    ![Create App integration button](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_create_new_app_integration.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=23f1a2ba321bdd292f79972ba0fd6830)
>
> 4. On the screen named **Create a new app integration**, select **OIDC - OpenID Connect** and **Single-Page Application**. Then click **Next**.
>
>    ![OIDC Single-Page Application selection](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_create_a_new_app_integration.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=05aa74721f03a1db34739cf63066b8fe)
>
> 5. On the screen named **New Single-Page App Integration**, complete the values as follows and click **Save**:
>    * **App integration name**, for example `W&B`.
>    * **Grant type**: Select both **Authorization Code** and **Implicit (hybrid)**.
>    * **Sign-in redirect URIs**: `https://[YOUR-W-AND-B-URL]/oidc/callback`.
>    * **Sign-out redirect URIs**: `https://[YOUR-W-AND-B-URL]/logout`.
>    * **Assignments**: Select **Skip group assignment for now**.
>      ![Single-Page App configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_new_single_page_app_integration.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=fd2da4993fa4410ef871937a7ff87a97)
>
> 6. On the overview screen of the Okta application you created, make note of the **Client ID** under **Client Credentials** under the **General** tab:
>
>    ![Okta Client ID location](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_make_note_of_client_id.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=86b93e5e0f6d1c9adb13ed4ad6a4ca19)
>
> 7. To identify the Okta **OIDC Issuer URL**, select **Settings** and then **Account** on the left side.
>    The Okta UI shows the company name under **Organization Contact**.
>
>    ![Okta organization settings](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/okta_identify_oidc_issuer_url.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cc7acb003dc09c40eaf402529db90600)
>
> The OIDC issuer URL has the following format: `https://[COMPANY].okta.com`. Replace `[COMPANY]` with the corresponding value. Make note of it.
>
> Next, [Set up SSO in Weights & Biases](#set-up-sso-in-w%26b).

> [tab] Entra
>
> Azure AD (Entra ID) supports two OIDC configuration modes for Weights & Biases. Choose the configuration that matches your security requirements:
>
> * [Public client](#public-client): Uses PKCE without a client secret. Simpler to configure, suitable for most deployments.
>
> * [Confidential client](#confidential-client): Uses PKCE with a client secret. Required if you need to set the `GORILLA_OIDC_SECRET` environment variable.
>
> > [!WARNING]
> >
> > Don't mix configurations. If you select **Single-page application** in Azure AD, don't provide a client secret. If you need a client secret, you must select **Web** as the platform type.
>
> > [accordion] Public client
> >
> > Use this configuration if you don't need to specify a client secret. It's suitable for deployments without advanced security requirements.
> >
> > 1. Sign in to the [Azure Portal](https://portal.azure.com/).
> > 2. Navigate to **Microsoft Entra ID** service and select **App registrations** from the left sidebar.
> > 3. Click **New registration** at the top of the page.
> > 4. On the **Register an application** screen, configure the following:
> >    * **Name**: Enter a descriptive name.
> >    * **Supported account types**: Keep the default **Single tenant** or modify as needed.
> >    * **Redirect URI**: Select platform type **Single-page application** and enter `https://[YOUR-W-AND-B-URL]/oidc/callback`.
> >    * Click **Register**.
> > 5. After registration, note the following values from the Overview page:
> >    * **Application (client) ID**: Your OIDC Client ID.
> >    * **Directory (tenant) ID**: Your OIDC Issuer URL.
> >      ![Application and Directory IDs](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/entra_app_overview_make_note.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6f612679b9f58a10263a9652e1ec6ca9)
> > 6. Configure authentication settings:
> >    * Select **Authentication** from the left sidebar.
> >    * Under **Front-channel logout URL**, enter `https://[YOUR-W-AND-B-URL]/logout`.
> >    * Click **Save**.
> >
> > Make a note of the following details:
> >
> > * **OIDC Client ID**: The Application (client) ID from step 5.
> > * **OIDC Issuer URL**: `https://login.microsoftonline.com/[TENANT-ID]/v2.0` (replace `[TENANT-ID]` with your Directory ID from step 5).
> >
> > When configuring Weights & Biases, use:
> >
> > * **Auth Method**: `pkce`.
> > * **OIDC Client Secret**: Leave empty (don't set `GORILLA_OIDC_SECRET`).
> >
> > Next, [Set up SSO in Weights & Biases](#set-up-sso-in-w%26b).
>
> > [accordion] Confidential client
> >
> > Use this configuration if you need to authenticate using a client secret.
> >
> > 1. Sign in to the [Azure Portal](https://portal.azure.com/).
> > 2. Navigate to **Microsoft Entra ID** service and select **App registrations** from the left sidebar.
> > 3. Click **New registration** at the top of the page.
> > 4. On the **Register an application** screen, configure the following:
> >    * **Name**: Enter a descriptive name.
> >    * **Supported account types**: Keep the default **Single tenant** or modify as needed.
> >    * **Redirect URI**: Select platform type **Web** and enter `https://[YOUR-W-AND-B-URL]/oidc/callback`.
> >    * Click **Register**.
> > 5. After registration, note the following values from the Overview page:
> >    * **Application (client) ID**: Your OIDC Client ID.
> >    * **Directory (tenant) ID**: Your OIDC Issuer URL.
> >      ![Application and Directory IDs](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/entra_app_overview_make_note.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6f612679b9f58a10263a9652e1ec6ca9)
> > 6. Configure authentication settings:
> >    * Select **Authentication** from the left sidebar.
> >    * Under **Front-channel logout URL**, enter `https://[YOUR-W-AND-B-URL]/logout`.
> >    * Click **Save**.
> > 7. Create a client secret:
> >    * Select **Certificates & secrets** from the left sidebar.
> >    * Click **New client secret**.
> >    * Add a description for the secret.
> >    * Choose an expiration period.
> >    * Click **Add**. \[!WARNING] Copy and save the secret **Value** immediately (not the Secret ID).
> >      ![Client secret value](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/entra_make_note_of_secret_value.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5698006cc84c519eca6382ed1a0baa36)
> >
> > Make a note of the following details:
> >
> > * **OIDC Client ID**: The Application (client) ID from step 5.
> > * **OIDC Client Secret**: The secret value from step 7.
> > * **OIDC Issuer URL**: `https://login.microsoftonline.com/[TENANT-ID]/v2.0` (replace `[TENANT-ID]` with your Directory ID from step 5).
> >
> > When configuring Weights & Biases, use:
> >
> > * **Auth Method**: `pkce`.
> >
> > * **OIDC Client Secret**: Set the `GORILLA_OIDC_SECRET` environment variable to the secret value from step 7.
> >
> > > [!NOTE]
> > >
> > > The v2.0 endpoint supports both personal Microsoft accounts and work/school accounts. If your organization requires the v1.0 endpoint, use `https://login.microsoftonline.com/[TENANT-ID]` instead.
> >
> > Next, [Set up SSO in Weights & Biases](#set-up-sso-in-w%26b).

## Set up SSO in Weights & Biases

After you finish configuring your IdP, complete the following steps in Weights & Biases to connect the IdP and enable SSO for your instance.

To set up SSO, you must have administrator privileges and the following information:

* **OIDC Client ID**.
* **OIDC Auth method** (`implicit` or `pkce`).
* **OIDC Issuer URL**.
* **OIDC Client Secret** (optional, depends on how you've set up your IdP).

If your IdP requires an OIDC Client Secret, specify it by passing the [environment variables](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md) `GORILLA_OIDC_SECRET`:

* In the W\&B App, go to **System Console** > **Settings** > **Advanced** > **User Spec** and add `GORILLA_OIDC_SECRET` to the `extraENV` section as shown in the following example.
* In Helm, configure `values.global.extraEnv` as shown in the following example.
  ```yaml theme={"system"}
  values:
  global:
      extraEnv:
      GORILLA_OIDC_SECRET="[YOUR-SECRET]"
  ```

> [!NOTE]
>
> If you can't sign in to your instance after configuring SSO, you can restart the instance with the `LOCAL_RESTORE=true` environment variable set. This outputs a temporary password to the container's logs and disables SSO. After you resolve any issues with SSO, you must remove that environment variable to enable SSO again.

> [tab] System Console
>
> Use this tab if you deploy Weights & Biases with the W\&B Kubernetes Operator. The System Console is the successor to the System Settings page. It's available with the [W\&B Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) based deployment.
>
> 1. Refer to [Access the W\&B Management Console](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#access-the-weights-&-biases-management-console).
>
> 2. Navigate to **Settings**, then **Authentication**. Select **OIDC** in the **Type** dropdown.
>
>    ![System Console OIDC configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/sso_configure_via_console.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=70a695ab0b5688022a624ee4c7bfced8)
>
> 3. Enter the values.
>
> 4. Click **Save**.
>
> 5. Sign out and then sign back in, this time using the IdP sign-in screen.
>
> ## Find your customer namespace
>
> Before you can configure team-level BYOB with CoreWeave storage on W\&B Dedicated Cloud or Self-Managed, you must obtain your organization's **Customer Namespace**. You can view and copy it from the bottom of the **Authentication** tab.
>
> For detailed instructions on configuring CoreWeave storage with your Customer Namespace, see [CoreWeave requirements for Dedicated Cloud or Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md#provision-your-bucket).

> [tab] System settings
>
> 1. Sign in to your Weights & Biases instance.
>
> 2. Navigate to the W\&B App.
>
> 3. Click your user profile icon. In the dropdown, select **System Settings**:
>
>    ![System Settings dropdown](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/system_settings_select_settings.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=e7de9673604b0cc11f00272ad7003444)
>
> 4. Enter your **Issuer**, **Client ID**, and **Authentication Method**.
>
> 5. Select **Update settings**.
>
> ![Update settings button](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/system_settings_select_update.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5f6a620ecc4fe0c1e1ffa1252b832336)

> [!NOTE]
>
> If you can't sign in to your instance after configuring SSO, you can restart the instance with the `LOCAL_RESTORE=true` environment variable set. This outputs a temporary password to the container's logs and disables SSO. After you resolve any issues with SSO, you must remove that environment variable to enable SSO again.

## Security Assertion Markup Language (SAML)

Weights & Biases doesn't support SAML.
