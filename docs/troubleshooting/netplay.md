---
title: Netplay Troubleshooting
description: Fix EmulatorJS Netplay issues: rooms not appearing, failed to start, desync, lag.
---

# Netplay Troubleshooting

Netplay uses WebRTC + ICE servers for peer-to-peer connections. Most issues are ICE-related.

## `Failed to start game`

The most common error. Almost always the operator-side config:

1. **Is Netplay enabled?** `emulatorjs.netplay.enabled: true` in `config.yml`.
2. **Are ICE servers configured?** The operator needs at least one STUN server in `emulatorjs.netplay.ice_servers`. Without any, NAT traversal can't begin.
3. **ICE server URLs reachable?** RomM can't talk to `stun.l.google.com:19302` if your server has no outbound internet. Sounds silly but happens in air-gapped labs.

Operator: check `docker logs romm | grep -i netplay`. Errors usually point at ICE config or network access.

Full config: [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay-new-in-50).

## Can't see the room

You created a room as host but other players don't see it.

- **They need RomM accounts on your instance.** Netplay doesn't federate. A user with no account or on a different RomM can't see or join.
- **WebSocket connection is broken.** Open devtools → Network → WS tab. If socket.io is disconnecting, see [Authentication Troubleshooting → WebSockets](authentication.md#400-bad-request-on-the-websocket-endpoint).
- **Other player didn't open the Netplay panel.** They need to click the 🌐 icon on the emulator toolbar to see the room list.

## Joined but video never appears

- **Host's browser stopped streaming.** Check host's tab is still foregrounded, because browsers throttle background tabs.
- **NAT traversal failed.** STUN couldn't hole-punch, and you have no TURN configured. Add a TURN server. See [Netplay → ICE servers](../using/netplay.md#ice-servers-the-nat-stuff).
- **Symmetric NAT on one end.** Corporate networks and some carrier-grade NAT can't be STUN-traversed. Only TURN (relay) will work.

## High lag / input delay

Normal Netplay delay is 50–150 ms. More than that:

- **You're routing through TURN.** TURN relays add latency proportional to your distance from the TURN server. Pick a TURN server geographically close to both players, or set up your own [coturn](https://github.com/coturn/coturn).
- **Host has slow uplink.** The host is streaming video to everyone, so if upload bandwidth is tight, lag spikes. Test host's upload with `speedtest-cli`.
- **Weak host CPU.** The host runs the emulator AND encodes the video stream. A Raspberry Pi hosting N64 Netplay is going to struggle.

## Desync (players see different game state)

Different players' screens diverge over time: you do a move, they don't see it.

- **Browser tab backgrounded.** Browsers throttle. Keep both tabs foregrounded.
- **Bandwidth starvation.** Video stream is dropping frames, inputs are queueing. Reduce resolution or lower the emulator frame rate.
- **Core-specific bug.** Not all cores handle Netplay cleanly. `snes9x` and `genesis_plus_gx` are most reliable but some 64-bit era cores have known desync bugs.

## Audio crackle / cuts out on the client side

WebRTC audio is known to be fragile. Workarounds:

- **Use Chrome.** Its WebRTC implementation is the most mature.
- **Lower audio quality** in the in-game Menu → Audio.
- **Restart the session**. Audio sometimes recovers only after a full room teardown.

## Room disappears after the host leaves

Expected. Rooms are ephemeral: when the host disconnects, the room is cleaned up (either immediately or by the next [Netplay Cleanup scheduled task](../administration/scheduled-tasks.md) sweep).

If you want your session back, the host recreates the room and other players rejoin.

## `nightly CDN 404` or `localization file not found`

Netplay switches EmulatorJS to nightly-CDN assets. Sometimes the nightly is temporarily broken.

- **Temporary**: usually self-heals within a day
- **Workaround**: operator can disable Netplay (`emulatorjs.netplay.enabled: false`) to go back to stable local assets.

See [In-Browser Play → Netplay](../using/netplay.md#known-caveat-nightly-cdn).

## Still stuck?

- `docker logs romm | grep -i netplay`: server-side log
- Browser devtools Console: client-side log
- `chrome://webrtc-internals`: live ICE / WebRTC stats on Chrome. Shows exactly where ICE is failing.
- [Discord](https://discord.gg/romm) `#help` with both sides' error text

## See also

- [Using → Netplay](../using/netplay.md): how Netplay works and how to configure it
- [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay-new-in-50): full config schema
