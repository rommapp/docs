---
title: Emulator Streaming Troubleshooting
description: Fix emulator streaming setup, GPU and network issues
---

# Emulator Streaming Troubleshooting

## Test the container on its own first

Get the [webstation](../using/emulator-streaming.md#run-the-webstation-container) container working by itself before you add it to `config.yml`. Open its Selkies web UI from the machine you'll play on, launch a game from inside the emulator, and check that it runs at full speed. If it doesn't, nothing in RomM's config will fix it.

To confirm the GPU is in use, open a terminal inside the container and run `vkcube`. It should name your graphics card, and `llvmpipe` means the container fell back to software rendering. When a desktop container can't get the GPU at all, smoke-test a plain Selkies container such as [webtop](https://docs.linuxserver.io/images/docker-webtop/) with the [LinuxServer GPU guide](https://docs.linuxserver.io/selkies/user-guide/gpu/) before you go back to the emulator.

## The GPU isn't used, or the emulator fails to initialize

On NVIDIA, these are the only GPU settings a Selkies container needs:

```yaml
shm_size: 1gb
devices:
    - /dev/nvidia-modeset:/dev/nvidia-modeset
deploy:
    resources:
        reservations:
            devices:
                - driver: nvidia
                  count: 1
                  capabilities: [compute, video, graphics, utility]
```

On a standard Linux host, Compose only picks this up once NVIDIA is Docker's default runtime:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Start from a minimal compose file with only the image, the broker variables, ports, volumes and the block above. Extra settings such as `security_opt`, `QT_QPA_PLATFORM` or `PIXELFLUX_WAYLAND` can stop the emulator from starting, so add them back one at a time once it works.

## The container crashes without an error

Check the host's kernel log right after the crash. The first command shows NVIDIA driver (Xid) errors, and the second shows processes the kernel killed for running out of memory:

```bash
dmesg -T | grep -i xid
dmesg -T | grep -i "killed process"
```

If both are empty, look for session and connection errors in the container's own log:

```bash
docker logs <container> --since 10m | grep -i -E "timeout|idle|heartbeat|disconnect|session"
```

## No stream action on a platform

Either `streaming.enabled` is off, nothing is configured for that platform slug, or the config hasn't reloaded. The streaming config is read when the app loads, so refresh the page after editing `config.yml`.

A YAML mapping can't hold the same key twice, so a second `containers:` under `streaming:` replaces the first and only the containers in the last one show up. Put every entry under a single `containers:` list.

## The stream never loads, or fails outside your home network

The stream is an iframe the browser loads straight from `host`, so `host` has to be HTTPS and reachable from wherever the browser is. A LAN address works at home but gives a 502 or a blank player outside it. Open the `host` URL directly from the client machine to see what it does.

For remote play, put the container behind your [reverse proxy](../install/reverse-proxy.md) and set `host` to its public HTTPS address. Selkies serves a self-signed certificate on its HTTPS port, so either proxy to that port with certificate checks turned off (`tls_insecure_skip_verify` in Caddy) or proxy to the container's plain HTTP port.

The broker is served under the container's `SUBFOLDER` on the same origin as the stream, so a single proxy host covers both. `broker_host` is only called by the RomM server, so if you set it, it can stay on an internal address.

## Launch or save errors out

Either the server can't reach `broker_host` or the secret is wrong. Check that `STREAMING_BROKER_SECRET` matches the container's `BROKER_SECRET`, and that `broker_host` resolves from the RomM server. A `broker_secret` in `config.yml` is ignored whenever `STREAMING_BROKER_SECRET` is set (see [Set the shared secret](../using/emulator-streaming.md#set-the-shared-secret)).

## The emulator can't find the game

The path sent to the container is `library_path` (default `/romm/library`) followed by the ROM's path inside the RomM library, such as `roms/ps2/game.iso`. The container's mount has to mirror the RomM library layout under that prefix. If your library uses `roms/ps2/` and you mount the PS2 folder at `/romm/library/ps2/roms`, the emulator gets a path that doesn't exist. Either fix the mount or set `library_path` to wherever the container sees the library.

## Controllers or the virtual gamepad don't respond

Try another browser before anything else, because some don't pass gamepad input through to Selkies. Zen has failed on both Linux and macOS, while Firefox and Vivaldi work.

## A container shows as unconfigured

Its `host` is missing a scheme, or there's no reachable broker for it, and it can't be claimed until that's fixed.

## A platform is stuck as in use

Someone disconnected without releasing it. Wait for the heartbeat to go stale or force-release it from the fleet (see [Emulator Streaming](../using/emulator-streaming.md)).

## "The previous session is still saving"

An exit is still pulling state off the container, so give it a moment and try again. If saves on a slow container time out, raise `STREAMING_SAVE_TIMEOUT` (see [Environment Variables → Emulator Streaming](../reference/environment-variables.md#emulator-streaming)).
