---
title: API Authentication
description: How to authenticate to the API
---

# API Authentication

The API accepts multiple authentication modes:

| Mode                 | Who it's for                                             | How the credential is carried                         |
| -------------------- | -------------------------------------------------------- | ----------------------------------------------------- |
| **Session cookie**   | Browser UI                                               | `Cookie: session=…` after `POST /api/auth/login`      |
| **HTTP Basic**       | Quick scripts, curl one-liners                           | `Authorization: Basic <base64(user:pass)>`            |
| **OAuth2 Bearer**    | Automation, CI, third-party apps                         | `Authorization: Bearer <jwt>`                         |
| **Client API Token** | Companion apps (Argosy, Grout, Playnite, custom scripts) | `Authorization: Bearer rmm_<token>`                   |

All of them resolve to the same scope model. See the [scope matrix in Users & Roles](../administration/users-and-roles.md#scope-matrix). A request is allowed if the active identity holds all scopes the endpoint requires.

## Base URL

```text
https://<your-instance>/api
```

When the app is behind a reverse proxy (as it should be when hosted in public), that's your public URL. When running locally without a proxy, the container listens on port `80`.

## Session login (browsers)

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=alice&password=s3cret
```

Response sets a `romm_session` cookie, and subsequent requests from the same browser are authenticated automatically.

Log out:

```http
POST /api/auth/logout
```

For OIDC logins, hitting `/api/auth/logout` also triggers RP-Initiated Logout if your OIDC provider supports it (configured via `OIDC_END_SESSION_ENDPOINT`).

## HTTP Basic

```bash
curl -u alice:s3cret https://demo.romm.app/api/roms
```

```python
import requests
from requests.auth import HTTPBasicAuth
r = requests.get("https://demo.romm.app/api/roms",
                 auth=HTTPBasicAuth("alice", "s3cret"))
```

## OAuth2 Bearer token

The RomM backend implements the OAuth2 password grant, where you exchange credentials for a short-lived access token and a refresh token. Access and refresh token expiry times are configurable via `OAUTH_ACCESS_TOKEN_EXPIRE_SECONDS` and `OAUTH_REFRESH_TOKEN_EXPIRE_SECONDS`.

```http
POST /api/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=alice&password=s3cret&scope=roms.read%20roms.write
```

```json
{
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires": 1800,
    "refresh_expires": 604800,
}
```

Access tokens are HS256-signed JWTs valid for `OAUTH_ACCESS_TOKEN_EXPIRE_SECONDS` seconds. Send them as:

```http
Authorization: Bearer eyJhbGciOi...
```

Refresh before expiry:

```http
POST /api/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=eyJhbGciOi...
```

Request only the scopes you need and RomM will issue a token with the intersection of what you asked for and what the user has.

## Client API tokens (for companion apps)

For anything long-lived (a running companion app, a cron job, a CI integration), use **Client API Tokens** instead of OAuth2. They're issued per-user from **Administration → Client API Tokens**, carry a subset of the user's scopes, and don't expire unless you set an expiry.

Token format: `rmm_` + 64 hex chars. Use it as a bearer:

```bash
curl -H "Authorization: Bearer rmm_abcdef0123456789..." \
     https://demo.romm.app/api/roms
```

Each user gets up to 25 active tokens. Tokens can be paired with a device via the [pairing flow](client-api-tokens.md), useful when you don't want to type a long token on a handheld.

## OIDC

Users signing in through an OIDC provider get a regular RomM session, same as username/password login. For the API side this means you can't use an OIDC access token directly. Authenticate the user through the browser first (they'll be redirected to the OIDC provider, then back to RomM), then use the resulting session cookie, **or** mint a Client API Token for programmatic use.

OIDC provider setup lives in [Administration → OIDC](../administration/oidc/index.md).

## Which scopes do I need?

Every endpoint in the [API Reference](api-reference.md) lists its required scopes. The short version:

- **Read**-ish endpoints want the matching `*.read` scope.
- **Write**-ish endpoints want `*.write`.
- **Admin**-ish endpoints want `users.read`, `users.write`, or `tasks.run`.

## Errors

| HTTP               | Meaning                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| `401 Unauthorized` | No credential, expired credential, bad credential.                      |
| `403 Forbidden`    | Authenticated but the identity lacks a required scope.                  |
| `404 Not Found`    | The resource doesn't exist, or, for privacy, the identity can't see it. |

When debugging a 403, check:

1. The **user's role** in Administration → Users.
2. The **token's scopes** (for OAuth2/Client API Tokens). Scopes are narrower than the user's role by default.
3. The endpoint's scope requirements in the [API Reference](api-reference.md).

## OpenAPI

The full machine-readable schema is served at `/openapi.json`. It's the source of truth for generated clients, Postman collections, and the in-docs [API Reference](api-reference.md).

```bash
curl https://demo.romm.app/openapi.json > romm-openapi.json
```

See [Consuming OpenAPI](openapi.md) for codegen tips.
