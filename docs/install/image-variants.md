---
title: Image Variants
description: Choose between the slim and full container images
---

# Image Variants

RomM publishes two production image variants. They're interchangeable at the config level, so pick based on whether you want the browser emulator runtimes baked into the image or fetched from a CDN at runtime.

| Variant            | Tag                                           | Approx size | When to pick                                                                         |
| ------------------ | --------------------------------------------- | ----------- | ------------------------------------------------------------------------------------ |
| **Full** (default) | `rommapp/romm:latest` `rommapp/romm:5.0.0`    | ~400MB      | You want in-browser play with every runtime baked in (most users pick this).         |
| **Slim**           | `rommapp/romm:slim` `rommapp/romm:5.0.0-slim` | ~100MB      | Headless use, or you're fine fetching EmulatorJS and `js-dos` from a CDN at runtime. |

Both variants are published on Docker Hub (`docker.io/rommapp/romm`) and GitHub Container Registry (`ghcr.io/rommapp/romm`). The GHCR images track the same tags and are a good choice if you run into Docker Hub's rate limits.

## Switching variants

Change the `image:` line in `docker-compose.yml` and recreate the container:

```yaml
services:
    romm:
        image: rommapp/romm:5.0.0-slim # was :5.0.0
```

```sh
docker compose up -d
```

No data migration is required. Saves, states, metadata, and `config.yml` are the same across variants.
