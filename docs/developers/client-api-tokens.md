---
title: Client API Tokens
description: Long-lived bearer tokens for companion apps
---

# Client API Tokens

A **Client API Token** is a long-lived credential that a companion app (or script, or CI job) uses to authenticate against RomM on behalf of a specific user, similar to a personal access token on GitHub. Each token belongs to one user and can hold any subset of that user's scopes, so it can be narrower than the user's role. Each user can have up to 25 active tokens.

## Why not just store a password?

- Passwords grant full access to the account but tokens can be scope-narrowed.
- Tokens are one-click revocable without changing your password.
- Tokens are safer to type (or paste) into a companion app's config file than a password.

## Token format

64 hex characters prefixed with `rmm_`:

```text
rmm_abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789
```

Send as a bearer token on any authenticated API call:

```http
Authorization: Bearer rmm_abcdef...
```

## Creating a token

A token is created with three params:

- **Token name**: descriptive (e.g. "Grout on RG35XX")
- **Expiration**: optional, blank = never expires until revoked
- **Permissions**: default to read-only, and don't grant every token `users.write`.

The token is shown exactly once, at creation time. Copy it then, because if you lose it you'll need to revoke and regenerate.

## Device pairing

Typing a 68-character token with a handheld's thumbstick isn't realistic, so devices pair with a short code instead.

### Flow

```ascii
┌───────────┐                                 ┌───────────┐
│  Device   │                                 │   RomM    │
└─────┬─────┘                                 └─────┬─────┘
      │                                             │
      │ 1. POST /api/client-tokens/{id}/pair        │
      │ (from the web UI, by the token's owner)     │
      │<── generates short code (8 digits) ─────────│
      │                                             │
      │ 2. Device user types the 8-digit code       │
      │    into the companion app                   │
      │                                             │
      │ 3. Device: POST /api/client-tokens/exchange │
      │     body: { "code": "12345678" }            │
      │──────────────────────────────────────────→  │
      │                                             │
      │<── full token (rmm_...) ────────────────────│
      │                                             │
      │ 4. Device stores the token, uses it from    │
      │    now on.                                  │
      │                                             │
```

### Timing

- Pairing codes are valid for 5 minutes after creation
- Once a device exchanges the code, it's invalid for anyone else (single-use)
- Re-create it if the user doesn't complete the flow within the time window

### Who generates the code

The token's owner generates the code from a device already signed into RomM (usually the web UI). The handheld or companion device then enters or scans the code.

### What "pairing" gives you

The companion app stores the token and uses it on every subsequent API call. RomM treats it like any other token, and pairing only affects how the token reached the device.

## Device-bound tokens

A token issued through the device authorization flow under `/api/auth/device/` (where the device starts the flow and the user approves its code) is bound to the [device](device-sync-protocol.md#registering-a-device) it registers. A bound token identifies its device on every call, so sync endpoints can leave out `device_id`, and some calls accept nothing else:

- Claiming and reporting [installs on devices](device-sync-protocol.md#installs-on-devices) only works with a token bound to that device.
- The [`/devices` socket](device-sync-protocol.md#the-devices-socket) only admits bound tokens that hold `devices.read`.
- A bound token can read its own device's play sessions without `devices.read`.

A bound token can't manage installs for another of the same user's devices, and deleting the device closes the sockets its tokens opened.

## Scoping tokens properly

A token can only hold scopes the owning user _also_ holds, and a user's scopes come from their [permission group](../administration/users-and-roles.md#permission-groups) plus any overrides (Admins hold everything). For example, a token can't carry `users.write` unless its owner is an Admin. Default to read-only, and only grant write scopes the app actually needs.

## What happens on permission change

If the owning user's permissions are narrowed so they no longer hold what a token needs, the token continues to exist but fails at request time with 403 Forbidden, and revoking it is up to the user. Deleting the user revokes all their tokens immediately.

## Anti-patterns

- **Sharing a token between users.** If two people need access, give them each an account and each creates their own token.
- **Embedding a token in public source.** If you accidentally commit one, revoke it immediately.
- **A single token for every app.** Name and scope per-app, so revoking one doesn't kill the others.
- **Infinite-expiry tokens in untrusted locations.** If a device might be lost/handed off, set an expiry.

## See also

- [Device Sync Protocol](device-sync-protocol.md): how the synced content flows after pairing
- [API Authentication](api-authentication.md): all RomM auth modes side-by-side
- [Users & Roles → OAuth scopes](../administration/users-and-roles.md#oauth-scopes): the full scope taxonomy
