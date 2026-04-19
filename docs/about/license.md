---
title: License
description: How RomM is licensed, and what that means for you.
---

# License

## Core app: AGPL-3.0

The main [RomM application](https://github.com/rommapp/romm) is licensed under the [GNU Affero General Public License v3.0](https://choosealicense.com/licenses/agpl-3.0/).

In short, AGPL says:

- **You can** use RomM privately, commercially, or at any scale.
- **You can** modify the source code however you want.
- **You must** make your modifications available under AGPL-3.0 if you distribute them *or* run them as a network-accessible service for others.
- **You must** preserve copyright and license notices.

The "network service" clause is the key AGPL twist: if you host a modified RomM and other people use it over the network, you owe them the source. This prevents the "hosted SaaS fork without upstream contributions" failure mode that's common with plain GPL.

For most self-hosters this has zero practical effect: you're running an unmodified version for yourself, the license doesn't constrain you. For companies thinking about shipping a modified RomM commercially, understand the AGPL obligations first.

Full license text: [rommapp/romm/blob/master/LICENSE](https://github.com/rommapp/romm/blob/master/LICENSE).

## Companion apps: varies

The RomM umbrella hosts several projects under different licenses:

| Project | License |
| --- | --- |
| [rommapp/romm](https://github.com/rommapp/romm) | AGPL-3.0 |
| [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher) | GPL-3.0 |
| [rommapp/grout](https://github.com/rommapp/grout) | MIT |
| [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin) | GPL-3.0 |
| [rommapp/muos-app](https://github.com/rommapp/muos-app) | check repo |
| [rommapp/docs](https://github.com/rommapp/docs) (what you're reading) | CC0 |

Companion repos use more permissive licenses (GPL-3.0 or MIT) because they're smaller, more-replaceable, and don't host the library. The AGPL network-service clause doesn't offer the same protection benefits there.

Docs (this site) are CC0: do whatever you want with the content. Attribution appreciated but not required.

## Third-party components

RomM ships several third-party components with their own licenses: [EmulatorJS](https://emulatorjs.org/), [Ruffle](https://ruffle.rs/), Vue, FastAPI, and a long list of smaller dependencies. Their licenses apply to their respective code, and none of them override AGPL-3.0 on the RomM code itself.

Full list via `uv tree` in the backend and `npm ls` in the frontend. Redistribution respects each upstream's terms.

## FAQ

### Can I use RomM at work / for my company's gaming night?

Yes. AGPL doesn't restrict private or commercial use.

### Can I fork RomM and relicense my fork?

No: AGPL is a strong copyleft, so forks remain AGPL, and while you can add your own changes under AGPL you can't relicense the original code.

### Can I charge money for RomM-as-a-service?

Yes, but you owe your users the source, so you can't run a modified closed-source hosted RomM for paying customers.

### Can I sell ROMs through RomM?

RomM doesn't care: legality of doing so is governed by copyright law, not AGPL.

### Is there a commercial / dual-license option?

No, AGPL-only, and if that's a blocker then RomM isn't the right choice.

## Contributions

By contributing code to RomM, you agree your contribution is licensed under the same AGPL-3.0 (or, for companion repos, the repo's license).

Full contributor terms: [Contributing → Licensing](../developers/contributing.md#licensing).

## See also

- [Credits](credits.md): the humans and projects behind RomM.
- [AGPL-3.0 overview](https://choosealicense.com/licenses/agpl-3.0/): plain-language explainer.
- Full license text: [LICENSE](https://github.com/rommapp/romm/blob/master/LICENSE).
