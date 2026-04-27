---
title: Reverse Proxy
description: Put RomM behind Caddy, nginx, Traefik, or Nginx Proxy Manager with TLS.
---

# Reverse Proxy

The RomM container listens on plain HTTP on port `8080`. For anything beyond `localhost` you should put it behind a reverse proxy that terminates TLS and forwards to the container.

<!-- prettier-ignore -->
!!! tip "WebSockets are required"
    RomM uses socket.io (both the general `/ws/socket.io` endpoint and the `/netplay/socket.io` endpoint) for live updates, scan progress, and Netplay. Every reverse-proxy recipe below keeps WebSocket support on, so don't strip it out.

The examples here assume your RomM container is reachable at `romm:8080` (by container name on a Docker network) or `192.168.1.100:8080` (by IP on the LAN). Swap to whatever's right for your setup.

## Caddy

Dead-simple, auto-HTTPS via Let's Encrypt.

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
- **Cache Assets**: `off`
- **Block Common Exploits**: `on`
- **Websockets Support**: `on` ❗
- **Access List**: as needed

### SSL

- **SSL Certificate**: Request a new SSL Certificate
- **Force SSL**: `on`
- **HTTP/2 Support**: `on`
- **HSTS Enabled**: `on` (after you've confirmed TLS works)
- **Email Address for Let's Encrypt**: your address
- **I Agree to the TOS**: `on`

### Advanced: custom nginx configuration ❗

```nginx
proxy_max_temp_file_size 0;
```

Without that line, large downloads (bulk ROM zips, multi-disc games) will fail on NPM because nginx tries to buffer them to disk.

| Details                                                                                   | SSL                                                                                        | Advanced                                                                                   |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| ![image](https://github.com/user-attachments/assets/e106a8e9-8b27-41ef-8ba2-d43c3b68b269) | ![image2](https://github.com/user-attachments/assets/6c82c785-792a-410a-80f2-d95839cba47b) | ![image3](https://github.com/user-attachments/assets/566ae834-99b5-42f3-b46b-306b8f73b5b4) |

## Set `ROMM_BASE_URL` behind HTTPS

Once you're proxying through HTTPS, set `ROMM_BASE_URL` in the RomM container's environment so generated links (QR codes, invite links, OIDC redirects) use the public URL:

```yaml
environment:
    - ROMM_BASE_URL=https://romm.mysite.com
```

If you're also using OIDC, update `OIDC_REDIRECT_URI` to match. See [OIDC Setup](../administration/oidc/index.md).
