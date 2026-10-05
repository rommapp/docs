---
title: Email
description: Send notification emails and password reset links over SMTP
---

# Email

RomM can send email through an SMTP server you provide, once both `SMTP_HOST` and `SMTP_FROM` are set. It's used for:

- Password reset links (see [Password reset](authentication.md#password-reset))
- Email [notification channels](../using/notifications.md#email)
- Confirmation codes that prove an address belongs to the user who added it as a channel

## Configuration

| Variable        | Default    | Description                                                |
| --------------- | ---------- | ---------------------------------------------------------- |
| `SMTP_HOST`     |            | SMTP server host                                           |
| `SMTP_PORT`     | `587`      | SMTP server port                                           |
| `SMTP_USERNAME` |            | Login for the SMTP server, left empty when it needs none   |
| `SMTP_PASSWORD` |            | Password for the SMTP server                               |
| `SMTP_FROM`     |            | Sender address, such as `romm@example.com`                 |
| `SMTP_SECURITY` | `starttls` | How the connection is secured: `starttls`, `tls` or `none` |

`SMTP_SECURITY` takes one of three modes:

- `starttls` connects in plain text and upgrades with STARTTLS before logging in, which is what port `587` expects.
- `tls` uses implicit TLS from the first byte, usually on port `465`.
- `none` sends everything, including the SMTP password, unencrypted, so keep it for a relay on the same host or a trusted network.

Any other value leaves email off rather than falling back to plain text. Certificates are checked against the system CAs.

```yaml
environment:
    - SMTP_HOST=smtp.example.com
    - SMTP_PORT=587
    - SMTP_SECURITY=starttls
    - SMTP_USERNAME=romm@example.com
    - SMTP_PASSWORD=app-password-here
    - SMTP_FROM=romm@example.com
```

For a provider that only offers implicit TLS, set `SMTP_PORT=465` and `SMTP_SECURITY=tls`. Many mail providers refuse an account's normal password over SMTP and want an app password or an SMTP-specific credential instead.

Set [`ROMM_BASE_URL`](../reference/environment-variables.md) to your instance's public URL, such as `https://romm.example.com`. Reset links are only emailed when it points at a real host, not `localhost`, a loopback address or the default `0.0.0.0`, and notification emails use it to link back into RomM.

## Testing it

`GET /api/heartbeat` reports the email status under `NOTIFICATIONS`:

- `EMAIL_ENABLED` is `true` once the `SMTP_*` settings are complete.
- `EMAILS_RESET_LINKS` is `true` when reset links will be emailed, which also needs `ROMM_BASE_URL`.

To check that mail actually goes out, add an email [notification channel](../using/notifications.md#email) for your own address. The confirmation code is the first message sent there, and if the SMTP server refuses that message, the request returns the server's error right away. A confirmed channel can send a test notification on demand too.

If a reset link can't be emailed, it's written to the container log instead, so check `docker logs romm` for `Could not email the reset link` along with the SMTP server's error.
