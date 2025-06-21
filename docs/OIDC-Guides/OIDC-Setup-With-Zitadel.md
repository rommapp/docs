# OIDC Setup With Zitadel

## A quick rundown of the technologies

### What is Zitadel

Zitadel is an enterprise-grade, open-source identity and access management (IAM) platform that supports OAuth2, OpenID Connect, SAML, and passwordless authentication. It's used to manage users, roles, and secure login for web and cloud applications.

### What is OAuth2?

OAuth2 (Open Authorization 2.0) is an industry-standard protocol for authorization. It allows applications (clients) to gain limited access to user accounts on an HTTP service without sharing the user’s credentials. Instead, it uses access tokens to facilitate secure interactions. OAuth2 is commonly used in scenarios where users need to authenticate via a third-party service.

### What is OpenID Connect (OIDC)?

OIDC (OpenID Connect) is an identity layer built on top of OAuth2. While OAuth2 primarily handles authorization, OIDC adds authentication, enabling applications to verify a user’s identity and obtain profile information. This makes OIDC suitable for SSO solutions, where user identity is central to access management.

## Setting up a client in Zitadel

### Step 1: Install and Configure Zitadel

Before setting up the OIDC client, ensure that Zitadel is installed and running by following the [setup guide](https://zitadel.com/docs/self-hosting/deploy/overview).

### Step 2: Create a Project

Once you have logged in and changed the default password for your Zitadel organization, create a new Project (i.e Romm). This will be the basic settings for roles and authorization.

In the "General" tab, there are options to allow the following:

- Assert Roles on Authentication

Unnecessary: Romm (at this time) does not allow granting permissions based on role, everyone gets viewer and will have to be changed manually using an admin account if desired.

- Check authorization on Authentication

Recommended: If you allow registration to your platform, then anyone who registers can instantly access Romm (although only as a viewer, which may not be a problem for some)

- Check for Project on Authentication

Optional: It could be used if you plan on separating users by organizations for other applications, but creating separate organizations is not typically useful for general self-hosting purposes

### Step 2.5 (Optional: If you enabled "Check authorization on Authentication"): Grant user(s) access to the Project

Click on the Authorization tab and click New.

Enter the user(s) and click Continue

It should say "No role has been created yet.", but this is fine, you can just click Save and it should bring you back to the Authorization page with your user(s) listed with no roles

### Step 3: Create the application

On the General tab, click the New button under Applications.

(Check "I'm a pro. Skip this wizard." to enter the information quicker)

- `Name`: RomM (or whatever you want)
- `Application Type`: Web
- `Grant Types`: Authorization Code
- `Response Types`: Code
- `Authentication Method`: Basic
- `Redirect URIs`:
  https://romm.domain.com/api/oauth/openid
- `Post Logout URIs`:
  https://romm.domain.com/

Click Create.

- Stay on this page or copy these down elsewhere, the secret will only show **this one time**

### Step 3: Configure RomM Environment Variables

To enable OIDC authentication in RomM, you need to set the following environment variables:

- `OIDC_ENABLED`: Set to `true` to enable OIDC authentication.
- `OIDC_PROVIDER`: The name of the provider `Zitadel`.
- `OIDC_CLIENT_ID`: The client ID copied from the Zitadel application
- `OIDC_CLIENT_SECRET`: The client secret generated from the Zitadel application
- `OIDC_REDIRECT_URI`: The redirect URI configured in Zitadel `https://rom.domain.com/api/oauth/openid`.
- `OIDC_SERVER_APPLICATION_URL`: The domain for your Zitadel instance `https://zitadel.domain.com`. (The discovery URL for Zitadel is on the basedomain under /.well-known/openid-configuration)

### Step 4: Enable claims from ID Token (this resolves the "Email is missing from token" error)

Click close to finish creating the application and then go to the Token Settings tab.

Check "User Info inside ID Token" and click Save

### Step 5: Set your Email in RomM

For your existing RomM admin account, open your user profile on Zitadel and set your email address. This email **has to match** your user email in Zitadel.

### Step 6: Test the Integration

After configuring the environment variables, restart (or stop and remove) your RomM instance and navigate to the login page. You should see the option "LOGIN WITH ZITADEL". Click on it and you'll be redirected to Zitadel for authentication. Once authenticated, you'll be redirected back to RomM.
