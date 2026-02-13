# OIDC Setup With Keycloak

## A quick rundown of the technologies

### What is Keycloak?

Keycloak is an open-source Identity and Access Management solution that provides single sign-on (SSO), OpenID Connect (OIDC), OAuth2, amongst other protocols.

## Setting up a Provider and Application in Keycloak

### Step 1: Install or access Keycloak

Before setting up the OIDC client, ensure that Keycloak is installed and running by following the [setup guide](https://www.keycloak.org/getting-started).

Log into the Admin Console and either create a new realm for RomM or reuse an existing one.

### Step 2: Add a client

1. In the Admin Console select your realm → **Clients** → **Create client**.
2. Leave `Client type` as `OpenID Connect` and enter a `Client ID` (for example `romm`). Click **Next**.
3. On the next page:
   - Enable **Client authentication**.
   - Leave only the **Standard flow** option enabled.
   - Click **Next**.
4. Set the following URLs:
   - **Root URL**: `http://romm.host.local` (replace with your RomM URL)
   - **Valid Redirect URIs**: `http://romm.host.local/api/oauth/openid` (replace with your RomM URL)
   - **Web origins**: `http://romm.host.local` (replace with your RomM URL)
5. Go to the **Credentials** tab and copy the **Client Secret** — you'll need this for the RomM configuration.

### Step 3: Configure RomM Environment Variables

To enable OIDC authentication in RomM, you need to set the following environment variables:

- `OIDC_ENABLED`: Set to `true` to enable OIDC authentication.
- `OIDC_PROVIDER`: The lowercase name of the provider (`keycloak`).
- `OIDC_CLIENT_ID`: The client ID copied from the Keycloak application.
- `OIDC_CLIENT_SECRET`: The generated output from `Random Password`.
- `OIDC_REDIRECT_URI`: The redirect URI configured in the Keycloak provider, in the format `http://romm.host.local/api/oauth/openid`.
- `OIDC_SERVER_APPLICATION_URL`: The base URL for you Keycloak instance including the realm name, e.g. `http://keycloak.host.local/realms/<realm-name>`.

### Step 5: Set your Email in RomM

In RomM, open your user profile and set your email address. This email **has to match** your user email in Keycloak.

Open the Keycloak Admin Console → Users and mark each RomM user's email as verified. Users without verified emails will not be able to log in.

### Step 6: Test the Integration

After configuring the environment variables, restart (or stop and remove) your RomM instance and navigate to the login page. You should see the option "LOGIN WITH KEYCLOAK". Click on it and you'll be redirected to Keycloak for authentication. Once authenticated, you'll be redirected back to RomM.

Note that if the user already exists in RomM, they will be logged in with their existing account and permissions. If it's a new user, an account will be created for them with viewer permissions by default. To change the permissions for new users, see Step 8 below.

### Step 7: (Optional) Disable password logins

If you want to enforce OIDC logins and disable password-based logins, set the environment variable `PASSWORD_AUTH_ENABLED` to `false`. This will hide the password login option on the login page, ensuring that all users must authenticate via Keycloak.

### Step 8: (Optional) Configure permissions for new users

By default, new users logging in via OIDC will be created with viewer permissions. If you want to change this default behavior, you can set the environment variables:

- `OIDC_CLAIM_ROLES`: Set to the name of the claim that contains the user's role
- `OIDC_ROLE_VIEWER`: The value of the role claim that maps to viewer permissions
- `OIDC_ROLE_EDITOR`: The value of the role claim that maps to editor permissions
- `OIDC_ROLE_ADMIN`: The value of the role claim that maps to admin permissions

Configure Keycloak to include the appropriate role claim in the token
