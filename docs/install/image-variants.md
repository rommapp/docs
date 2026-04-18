---
title: Image Variants
description: Choose between the slim and full RomM container images.
---

# Image Variants

RomM publishes two production image variants. They're interchangeable at the config level — pick based on whether you want in-browser emulation.

| Variant | Tag | Includes | Approx size | When to pick |
| --- | --- | --- | --- | --- |
| **Full** (default) | `rommapp/romm:latest`, `rommapp/romm:5.0.0` | Backend + frontend + **EmulatorJS** + **Ruffle** + embedded Redis + nginx with `mod_zip` | ~1.2 GB | You want in-browser play. 95% of users pick this. |
| **Slim** | `rommapp/romm:slim`, `rommapp/romm:5.0.0-slim` | Backend + frontend + embedded Redis + nginx with `mod_zip` | ~400 MB | Headless use (API + native-app clients only), bandwidth-constrained hosts, or when you're running emulators elsewhere. |

Both variants are published on Docker Hub (`rommapp/romm`) and GitHub Container Registry (`ghcr.io/rommapp/romm`). The GHCR images track the same tags and are a good choice if you rely on Docker Hub rate limits.

## Switching variants

Change the `image:` line in `docker-compose.yml` and recreate the container:

```yaml
services:
  romm:
    image: rommapp/romm:5.0.0-slim  # was :5.0.0
```

```sh
docker compose up -d
```

No data migration is required — saves, states, metadata, and `config.yml` are the same across variants.

## Dev images

`rommapp/romm:dev-slim` and `rommapp/romm:dev-full` track the `master` branch with hot-reload-friendly entrypoints. Useful for testing changes against a real library — not recommended for anything you care about. See [Development Setup](../developers/development-setup.md).

## What's actually different

The two images share the same backend code, frontend bundle, nginx config, and entrypoint. The slim image omits:

- **EmulatorJS** (~700 MB uncompressed) — the in-browser retro emulator bundle.
- **Ruffle** (~20 MB) — the Flash/Shockwave emulator.

If you set `ENABLE_EMULATORJS=false` and `ENABLE_RUFFLE=false` on the full image, behaviour matches slim — only the image is larger. Setting them to `true` on the slim image will cause players to 404 at runtime.
