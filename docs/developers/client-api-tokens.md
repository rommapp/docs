---
title: Client API Tokens
description: Long-lived bearer tokens for companion apps
---

# Client API Tokens

A **Client API Token** is a long-lived credential that a companion app (or script, or CI job) uses to authenticate against RomM on behalf of a specific user. Think "personal access token" on GitHub. Tokens are **per-user** and **per-scope-subset**: a token can hold any subset of the owning user's scopes, scoped narrower than the user's role. You get up to **25 active tokens per user**.

## Why not just store a password?

- Passwords grant full access to the account but tokens can be scope-narrowed.
- Tokens are one-click revocable without changing your password.
- Tokens are safer to type (or paste) into a companion app's config file than a password.

## Token format

64 hex characters prefixed with `rmm_`:

```text
rmm_abcdef0123456789abcdef0123456789abcdef01
```

Send as a bearer token on any authenticated API call:

```http
Authorization: Bearer rmm_abcdef...
```

## Creating a token

From the RomM UI: **Profile → Client API Tokens → + Create**.

- **Token name**: descriptive (e.g. "Grout on RG35XX")
- **Expiration**: optional, blank = never expires until revoked
- **Permissions**: default: read-only, and don't give every token `users.write`.

The token is shown **exactly once**. Copy it now, cause if you lose it, you'll need to revoke and regenerate it, because you can't get it back.

## Device pairing

Typing a 68-character token into a handheld thumbstick isn't realistic. Instead:

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

- Pairing codes are valid for **60 seconds** after creation
- Once a device exchanges the code, it's invalid for anyone else (single-use)
- Re-create it if the user doesn't complete the flow within the time window

### Who generates the code

The user who owns the token from a device already signed into RomM (web UI, usually). The handheld/companion device then enters or scans the code.

### What "pairing" gives you

The companion app stores the token and uses it on every subsequent API call. From RomM's side, it looks like any other token, and there's no special treatment beyond the fact that pairing is how the token got there.

## Scoping tokens properly

A token can only hold scopes the owning user _also_ holds. If the user is an Editor, their token can hold any Editor scope but not `users.write` (which is Admin-only). The UI's scope-selection step defaults to read-only, only tick write scopes you actually need.

## What happens on user role change

If the owning user's role drops below what the token needs, the token continues to exist but fails at request time with **403 Forbidden**. It's the user's decision to revoke it. However if the user is deleted, all their tokens are revoked immediately.

## Anti-patterns

- **Sharing a token between users.** If two people need access, give them each an account and each creates their own token.
- **Embedding a token in public source.** Obvious but worth saying, if you accidentally commit one, revoke immediately from the RomM UI.
- **A single token for every app.** Name and scope per-app, so revoking one doesn't kill the others.
- **Infinite-expiry tokens in untrusted locations.** If a device might be lost / handed off, set an expiry.

## See also

- [Device Sync Protocol](device-sync-protocol.md): how the synced content flows after pairing
- [API Authentication](api-authentication.md): all RomM auth modes side-by-side
- [Users & Roles → scope matrix](../administration/users-and-roles.md#scope-matrix): the 19-scope taxonomy
