---
name: humanize-docs
description: Run the vendored humanizer and the docs-style house rules over the documentation pages a change adds or edits, as the last step before opening a PR. Rewrites prose only, leaving headings, front matter, snippet partials and MkDocs syntax untouched.
argument-hint: "[page paths | nothing for the pages changed since main]"
disable-model-invocation: true
---

# Humanize changed docs pages

Apply `.claude/skills/humanizer/SKILL.md` and then `.claude/skills/docs-style/SKILL.md`
to the prose a change adds, then prove the site still builds. Read both files and
follow them rather than invoking the skills, since a personal install of the same
name would load instead. Where the two disagree, `docs-style` wins, because it
holds the house rules (such as the passive voice that replaces "RomM" as a filler
subject).

## Target

`$ARGUMENTS` is a list of page paths, or nothing. With nothing, the target is
every page under `docs/` that differs from `main`, committed or not:

```bash
set -eu
git fetch origin main
BASE="$(git merge-base origin/main HEAD)"
git diff --name-only --diff-filter=AM "$BASE" -- 'docs/*.md' \
  ':(exclude)docs/resources/snippets/**' ':(exclude)docs/Navigation.md'
```

Snippet partials are included into several pages, so a rewrite there changes
pages the diff never shows; leave them out even when passed by name.
`Navigation.md` is the nav tree, not prose.

## Scope

In file mode, rewrite only the paragraphs `git diff "$BASE"` adds or changes on
each page. Untouched paragraphs stay as they are, even when they carry a tell.

Leave these exactly as written:

- Front matter (`title`, `description`, `search`), which feeds the nav and
  search index.
- Heading text. Pages link to `#anchors` derived from it, and the docs use
  Title Case, so skip the "Decorative headings" pattern.
- MkDocs syntax: `!!!` and `???` admonition lines and their quoted titles,
  `===` tab labels, `--8<--` includes, `{ ... }` attribute lists, `/// caption`
  blocks, footnote markers and table structure. Prose inside them is in scope.
- UI labels, setting names, env vars, paths and version numbers. They have to
  match the app, so a "more natural" wording is wrong.
- Bold on UI labels and on lead-in sentences in lists; "Bold as decoration"
  applies only to bold a new paragraph adds for emphasis.

## Finish

1. Run `trunk fmt && trunk check` on the pages you touched.
2. Run `uv run mkdocs build --strict`, which CI runs on every PR; a broken
   anchor or include fails it.
3. Commit the rewrite on its own, so it is one `git revert` away.

Report which pages changed and any tell you left in place because it sat in a
protected span.
