# OIDC Setup

OpenID Connect (OIDC) allows you to authenticate to RomM using external identity providers, enabling Single Sign-On (SSO) and centralized user management. This setup eliminates the need to manage separate credentials for RomM.

## What is OIDC?

OIDC is an identity layer built on top of OAuth2. While OAuth2 primarily handles authorization, OIDC adds authentication, enabling applications to verify a user's identity and obtain profile information. This makes OIDC suitable for SSO solutions, where user identity is central to access management.

## How It Works

1. Click the OIDC login button on RomM's login page
2. You're redirected to your identity provider
3. Authenticate with your credentials
4. You're redirected back to RomM and logged in automatically

## Supported Identity Providers

RomM supports OIDC authentication with the following identity providers:

### [Authelia](OIDC-Setup-With-Authelia.md)
An open-source authentication and authorization server providing two-factor authentication and SSO. Ideal for self-hosters looking for a lightweight solution.

### [Authentik](OIDC-Setup-With-Authentik.md)
An open-source identity provider with support for modern authentication protocols, MFA, and comprehensive user management.

### [PocketID](OIDC-Setup-With-PocketID.md)
A simple OIDC provider that exclusively supports passkey authentication - no passwords required.

### [Zitadel](OIDC-Setup-With-Zitadel.md)
An enterprise-grade, open-source identity and access management platform supporting OAuth2, OIDC, SAML, and passwordless authentication.

## General Setup Requirements

Regardless of which provider you choose, you'll need to configure these environment variables in RomM:

```env
OIDC_ENABLED=true
OIDC_PROVIDER=<provider_name>
OIDC_CLIENT_ID=<your_client_id>
OIDC_CLIENT_SECRET=<your_client_secret>
OIDC_REDIRECT_URI=<your_romm_url>/api/oauth/openid
OIDC_SERVER_APPLICATION_URL=<your_provider_url>
```

## Important Notes

- **Email matching**: Your email address in RomM must match the email in your identity provider
- **First-time users**: Users logging in via OIDC for the first time will be created automatically with viewer permissions
- **Existing users**: Users who already have an account in RomM need to ensure their email addresses match between RomM and the identity provider

## Troubleshooting

If you encounter issues with OIDC authentication:

- Verify all environment variables are set correctly
- Check that the redirect URI matches exactly between RomM and your identity provider
- Ensure your email address in RomM matches your email in the identity provider
- Review the [Authentication Issues](../Troubleshooting/Authentication-Issues.md) documentation
- Check your identity provider's logs for any authentication errors

## Next Steps

Choose a provider from the list above and follow its specific setup guide. Each guide provides detailed step-by-step instructions for configuring both the identity provider and RomM.
