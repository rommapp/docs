---
title: Reverse Proxy
description: Caddy, nginx, Traefik, and Nginx Proxy Manager
---

# Reverse Proxy

The container listens on plain HTTP on port `8080`. For anything beyond `localhost` (e.g., a LAN or the internet) you should put it behind a reverse proxy that terminates TLS and forwards to the container. The examples here assume your container is reachable at `romm:8080` (by container name on a Docker network) or `192.168.1.100:8080` (by IP on the LAN).

## Caddy

Dead-simple, auto-HTTPS via Let's Encrypt:

```caddyfile
romm.mysite.com {
  encode zstd gzip

  header {
    Strict-Transport-Security "max-age=31536000;"
    X-XSS-Protection "1; mode=block"
    X-Frame-Options "SAMEORIGIN"
    X-Robots-Tag "noindex, nofollow"
    -Server
    -X-Powered-By
  }

  reverse_proxy romm:8080
}
```

If you just want HTTP on the LAN:

```caddyfile
http://romm.mysite.com {
  reverse_proxy romm:8080
}
```

## Nginx

### HTTP only

```nginx
server {
  listen 80 default_server;
  server_name romm.mysite.com;
  client_max_body_size 0;

  location / {
    proxy_pass http://romm:8080;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}
```

### HTTPS with HSTS

```nginx
server {
  listen 80 default_server;
  server_name _;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  server_name romm.mysite.com;
  ssl_certificate     /etc/ssl/romm/fullchain.pem;
  ssl_certificate_key /etc/ssl/romm/privkey.pem;
  client_max_body_size 0;

  location / {
    proxy_pass http://romm:8080;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    server_tokens off;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
  }
}
```

<!-- prettier-ignore -->
!!! note "`client_max_body_size 0`"
    Required so large ROM uploads aren't rejected by nginx before they reach RomM.

## Traefik

### Dynamic configuration file

```yaml
http:
    routers:
        romm:
            entryPoints:
                - websecure
            rule: "Host(`romm.mysite.com`)"
            middlewares:
                - default-headers
                - https-redirectscheme
            tls:
                certResolver: letsencrypt
            service: romm

    services:
        romm:
            loadBalancer:
                servers:
                    - url: "http://192.168.1.100:8080"
                passHostHeader: true
```

### Docker Compose labels

Add these to the `romm` service in your `docker-compose.yml`:

```yaml
labels:
    - "traefik.enable=true"
    - "traefik.http.services.romm.loadbalancer.server.port=8080"
    - "traefik.http.routers.romm.rule=Host(`romm.mysite.com`)"
    - "traefik.http.routers.romm.entrypoints=websecure"
    - "traefik.http.routers.romm.tls=true"
    - "traefik.http.routers.romm.tls.certresolver=letsencrypt"
```

## Nginx Proxy Manager

Items marked ❗ are important. RomM won't work right without them.

### Details

- **Domain Names**: `romm.mysite.com`
- **Scheme**: `http`
- **Forward Hostname/IP**: container hostname or LAN IP (e.g. `192.168.1.100`)
- **Forward Port**: `8080`
- **Cache Assets**: `off` ❗
- **Block Common Exploits**: `on`
- **Websockets Support**: `on` ❗
- **Access List**: as needed

<!-- prettier-ignore -->
!!! warning "Leave `Websockets Support` on"
    With it off, NPM strips the `Upgrade` and `Connection` headers, so RomM never sees an upgrade request and the Socket.IO handshake is rejected. Scan progress, notifications, and log streaming then fall back to HTTP long polling.

<!-- prettier-ignore -->
!!! warning "Leave `Cache Assets` off"
    It sends every `.js`, `.css`, `.svg`, and image request through NPM's shared cache, which discards RomM's `Cache-Control`, `Last-Modified`, and `Vary` headers and replaces them with a flat `Expires` pinned to a clock time (NPM's `expires @30m`), which can leave a browser holding a stale copy for hours. Content-hashed bundles lose their one year `immutable` caching, covers and screenshots lose the revalidation that keeps them fresh after a rescan, and dropping `Vary: Accept-Encoding` allows a compressed response to be handed to a client that never asked for one. It also pins a 45s read timeout and a 5s connect timeout on those requests, overriding anything you set below.

### SSL

- **SSL Certificate**: Request a new SSL Certificate
- **Force SSL**: `on`
- **HTTP/2 Support**: `on`
- **HSTS Enabled**: `on` (after you've confirmed TLS works)
- **Trust Upstream Forwarded Proto Headers**: `off` (NPM 2.14 and newer)
- **Email Address for Let's Encrypt**: your address
- **I Agree to the TOS**: `on`

<!-- prettier-ignore -->
!!! warning "`Trust Upstream Forwarded Proto Headers`"
    Turn this on only when NPM itself sits behind another proxy that terminates TLS, such as a Cloudflare Tunnel or an upstream load balancer. When NPM is the edge, it lets any client skip the Force SSL redirect just by adding `X-Forwarded-Proto: https` to a plain HTTP request, so the cleartext request reaches RomM and RomM treats it as secure. The toggle only gates that redirect, because NPM passes the client's `X-Forwarded-Proto` value upstream either way.

| Details                                                                                                        | SSL                                                                                                        |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| ![NPM proxy host Details tab](https://github.com/user-attachments/assets/40b7b009-63e3-4fe9-94c6-7c0e3429261e) | ![NPM proxy host SSL tab](https://github.com/user-attachments/assets/3ebdb711-a8be-487e-8237-d384d49ce60e) |

### Advanced ❗

Paste this into the proxy host's **Advanced** tab. NPM's defaults are tuned for small web apps and get in the way of multi-GB ROM transfers.

```nginx
# Uploads. NPM caps request bodies at 2000m, which rejects a larger ROM with
# a 413 before it reaches RomM. Streaming the body also keeps NPM from
# spooling the whole upload to disk inside its own container first.
client_max_body_size      0;
proxy_request_buffering   off;

# Downloads. Buffer responses in RAM with 1 MB of read-ahead so a single
# download keeps its connection saturated, and never spool to disk.
# nginx requires busy (128k) >= buffer_size (64k), and busy <= the total
# of all buffers (1 MB) minus one buffer.
proxy_buffering           on;
proxy_buffer_size         64k;
proxy_buffers             16 64k;
proxy_busy_buffers_size   128k;
proxy_max_temp_file_size  0;

# Timeouts. NPM's proxy defaults are 90s and nginx's send_timeout is 60s, both
# short for large transfers and slow metadata calls. Socket.IO pings every 25s,
# so it stays well inside these.
proxy_connect_timeout     10s;
proxy_read_timeout        300s;
proxy_send_timeout        300s;
send_timeout              300s;

# Compression. RomM already gzips HTML, JSON, JS, and CSS itself. This adds
# the types it doesn't: platform icons (SVG) and the emulator cores (wasm).
# Binary assets and ROM downloads are intentionally left uncompressed.
gzip                      on;
gzip_vary                 on;
gzip_proxied              any;
gzip_comp_level           5;
gzip_min_length           1024;
gzip_types                text/plain text/css application/json
                          application/javascript application/xml
                          image/svg+xml application/wasm;
```

What each block buys you:

| Block           | Without it                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Uploads**     | Uploads over 2 GB are rejected with `413 Request Entity Too Large`, and smaller ones are written to disk inside the NPM container before RomM sees a byte.         |
| **Downloads**   | nginx spools each in-flight download to a temp file, up to 1 GB per connection, on the NPM container's filesystem.                                                 |
| **Timeouts**    | Long downloads and slow metadata calls are cut off after 60 to 90s of inactivity.                                                                                  |
| **Compression** | Platform icons and emulator cores cross the wire uncompressed. RomM ships about 4 MB of SVG, plus 25 MB of wasm on the full image, and both compress by 60 to 75%. |

<!-- prettier-ignore -->
!!! note "Don't set `proxy_buffering off`"
    It is a common suggestion for large downloads, but it does the opposite here: nginx falls back to relaying through a single small buffer and a single download runs at roughly half the speed. `proxy_buffering on` paired with `proxy_max_temp_file_size 0` gives you the read-ahead without the disk writes.

<!-- prettier-ignore -->
!!! note "Memory use"
    `proxy_buffers 16 64k` reserves up to 1 MB per in-flight proxied response. On a small box serving many simultaneous downloads, drop to `8 32k` (256 KB each) if memory is tight.

## Set `ROMM_BASE_URL` behind HTTPS

Once you're proxying through HTTPS, set `ROMM_BASE_URL` in the container's environment so generated links (QR codes, invite links, OIDC redirects) use the public URL:

```yaml
environment:
    - ROMM_BASE_URL=https://romm.mysite.com
```

If you're also using OIDC, update `OIDC_REDIRECT_URI` to match (see [OIDC Setup](../administration/oidc/index.md)).

## Harden cookies and CORS behind HTTPS

Two optional env vars tighten browser security once you're on HTTPS:

```yaml
environment:
    - ROMM_SESSION_SECURE_COOKIE=true
    - ROMM_CORS_ALLOWED_ORIGINS=https://romm.mysite.com
```

- `ROMM_SESSION_SECURE_COOKIE` marks the session and CSRF cookies `Secure` so browsers only send them over HTTPS. Leave it `false` if you still reach the instance over plain HTTP, or logins will silently fail.
- `ROMM_CORS_ALLOWED_ORIGINS` is a comma-separated allowlist of origins permitted to call the API from a browser. An empty value (the default) allows any origin, so set it to your public URL (plus any companion-app origins) when you want to lock cross-origin requests down.
