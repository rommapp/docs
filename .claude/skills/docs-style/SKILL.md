---
name: docs-style
description: RomM's house style for docs pages, covering what the general humanizer doesn't. Use whenever you write, edit or review prose under docs/ in this repo, including new pages, release-notes passes and PR review. Covers restated context, "RomM" as a filler subject, crammed clauses, choppy sentence runs, cross-reference form, punctuation, describing current behavior, UI walkthroughs and facts that belong on another page.
---

# RomM docs style

These rules come from edits maintainers kept making by hand on docs PRs. Apply them while drafting, not only as a cleanup pass. They sit on top of `.claude/skills/humanizer/SKILL.md`, and when the two disagree this file wins (see rule 2 on passive voice).

Every rule has the same limit: never drop or add a fact, and never change code, inline code, paths, env vars, link targets, anchors or table values. Each edit should read better _and_ say the same thing.

## 1. Don't restate context the reader already has

Cut phrases that repeat the page title, the heading, a list's lead-in, a table header or the sentence just before.

- On the Email page, under "It's used for:": "Email notification channels, which users add to get their [notifications](...) by email" → "Email [notification channels](...)"
- Same list: "Password reset links, emailed to the account's address (see ...)" → "Password reset links (see ...)"
- On the RetroArch Cloud Sync page: "Point RetroArch's Cloud Sync at ..." → "Point Cloud Sync at ..."
- Bullets under "A bound token can:": "A bound token can read its own device's play sessions" → "It can read its own device's play sessions"
- A troubleshooting section that opens by repeating its heading: cut the opener and start with the cause.

When trimming around a link, keep the link and make its text the noun that's left. Keep a repeat when cutting it would make the sentence ambiguous, such as "the device" vs a bare "it" when a game is also in the sentence.

## 2. Don't use "RomM" as a filler subject

Every page is about RomM, so `RomM <verbs> X` usually just names the obvious actor. Lead with the thing acted on, and use the passive if that's what it takes.

- "RomM seeds two groups" → "Two groups are seeded"
- "RomM keeps a notification inbox for each user" → "Each user has a notification inbox"
- "RomM can convert disc and cartridge images" → "Disc and cartridge images can be converted"
- "RomM upgrades in place" → "Upgrades happen in place"

Keep "RomM" when it tells RomM apart from another actor in the same passage, such as RetroArch, a metadata provider, the OIDC provider, a reverse proxy, the browser or a device app. On integration pages that's most occurrences, so leave those.

Don't turn a gerund into the actor: "Turning sync off refuses that device's requests" is wrong, and "Turning sync off means that device's requests are refused" is right.

## 3. Don't cram clauses

Put the subject before its verb, and don't leave a long subject stranded inside a "which" clause.

- "which an upgrade from a release before permission groups also uses" → "which are also used by an upgrade from a release before permission groups"
- "appends the address it received each request from to `X-Forwarded-For`" → "appends the address each request came from to `X-Forwarded-For`"
- "when a task that only runs one at a time, such as Convert library, is already queued" → "when a single-instance task such as Convert library is already queued"

## 4. Merge choppy runs, but not separate points

When a sentence is followed by one to three short ones that only qualify it, merge them into one sentence with a comma, "with", "and", "so" or "which".

- "members only see games rated for this age or younger. The UI offers 3, 6, 7 ... 18, and the API accepts any whole number from `0` to `21`. No limit is the default." → "members only see games rated for this age or younger, from `0` to `21`, with no limit as the default."
- "...play, pause, skip and seek. This doesn't work while a console sound file plays." → "...play, pause, skip and seek, except while a console sound file plays."
- "Kept for 90 days by default. A scheduled cleanup runs daily..." → "Kept for 90 days by default, and a scheduled cleanup deletes older ones daily..."

Stranded fragments get the same treatment: ". Useful for X.", ". Best for X.", ". Same X.", ". Requires X." all fold into the sentence before them.

Don't merge sentences that make separate points, and keep sentences under about 40 words. Fragments are fine in table cells, glossary entries (`**Term**: noun phrase.` is that page's voice), colon-introduced lists and tight numbered steps.

## 5. Cross-references are parentheticals

Fold a "more info" link into the sentence it supports: "... in `config.yml`. See [Configuration File](...)." → "... in `config.yml` (see [Configuration File](...))." A standalone "See also" list stays a list.

## 6. No em dashes and no semicolons in prose

Use a period, a comma, a colon, parentheses or a linking word ("and", "but", "so", "because"). This doesn't apply to code, URLs or hyphenated compounds like "read-only".

## 7. Describe how it works now

Pages describe current behavior. "Now", "no longer", "used to", "before 5.4" and "was renamed from" belong only in `install/upgrading.md` and other migration guides. Elsewhere, state the current fact and link to the upgrade page if the change matters.

- "An invalid bearer token no longer returns a `500`" → "An invalid bearer token leaves the request unauthenticated"

## 8. No UI walkthroughs

UI labels, menus and layouts change faster than the docs do.

- Under `docs/using/`, keep concepts, paths, URLs, config keys, scopes and API endpoints. Cut click sequences, menu paths ("Settings › Logs › Events"), dialog, drawer and tab names, button labels and icon descriptions. Ask whether the sentence would survive a UI redesign.
- Leave out UI-only detail, such as which values a dropdown offers. Give the range the API accepts instead.
- Under `docs/install/`, provider pages carry URLs, paths, env vars and specs. Screenshots cover the provider's ordering flow and control panel, so don't narrate them.

## 9. Keep facts on the page that owns them

Don't repeat a rule, a default or a caveat that a reference page or another feature page already owns. Link to it instead, or leave it out.

- Defaults belong to the env var and config tables, so "Both are off by default" in a feature intro is redundant.
- Image contents belong to Image Variants, so cut "The CLI ships in both the slim and full images" from a feature page.
- Password rules belong in one place, not on every page that mentions a password.
- Cut asides with no action attached, such as "Messages are plain text and in English."

## 10. Short front matter, short warnings

- A front-matter `description` is one clause about the page's subject: "Age limits on permission groups and users", not "..., and how RomM works out a game's age".
- A warning is the instruction alone, without its justification: "**Back up your library before the first run!**"

## 11. Terms and facts

- The embedded store is **Valkey**, not Redis.
- The slim image fetches EmulatorJS and `js-dos` from a CDN at runtime, so it doesn't disable them. Ruffle, PICO-8 and EasyRPG ship only in the full image.
- Check behavior against the `rommapp/romm` source at the ref in `scripts/sources.toml`, not against changelogs or older pages, because both drift.

## Before you finish

Read each changed paragraph against rules 1 to 4 one more time. Those are the patterns that survive a first draft. Then run:

```bash
BASE="$(git merge-base origin/main HEAD)"
# Dashes and semicolons in added prose (inspect each hit, since code is exempt)
git diff "$BASE" -- docs ':!docs/resources/snippets' | grep '^+[^+]' | grep -nE '—|[a-z]; [a-z]'
# "RomM" as a sentence subject in added lines (keep the ones that tell RomM apart from another actor)
git diff "$BASE" -- docs ':!docs/resources/snippets' | grep '^+[^+]' | grep -noE '(^\+|\. )RomM [a-z]+s\b'
# History words outside the upgrade guide (some hits are fine, like "no longer matches a DAT")
git diff "$BASE" -- docs ':!docs/install/upgrading.md' | grep '^+[^+]' | grep -nE '\b([Nn]o longer|used to (be|have|allow|return|send)|now [a-z]+s|[Bb]efore [0-9]\.[0-9])\b'
```

Finish with `trunk fmt && trunk check` and `uv run mkdocs build --strict`.
