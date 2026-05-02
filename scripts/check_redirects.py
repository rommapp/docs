"""Validate the redirect_maps in mkdocs.yml against the built site.

Fails CI if any redirect target file does not exist after `mkdocs build`.

Run manually:
    uv run mkdocs build
    uv run python -m scripts.check_redirects
"""

from __future__ import annotations

import sys

import yaml

from scripts._sources import MKDOCS_YML, SITE_DIR


class _LooseLoader(yaml.SafeLoader):
    pass


def _ignore_python_tags(loader, tag_suffix, node):  # noqa: ARG001
    return None


_LooseLoader.add_multi_constructor("tag:yaml.org,2002:python/", _ignore_python_tags)


def load_redirect_map() -> dict[str, str]:
    with MKDOCS_YML.open("r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=_LooseLoader)
    for plugin in cfg.get("plugins", []):
        if isinstance(plugin, dict) and "redirects" in plugin:
            return plugin["redirects"].get("redirect_maps", {})
    return {}


def main() -> int:
    if not SITE_DIR.exists():
        print(
            f"ERROR: {SITE_DIR} does not exist. Run `mkdocs build` first.",
            file=sys.stderr,
        )
        return 2

    redirects = load_redirect_map()
    missing: list[tuple[str, str]] = []
    for src, dst in redirects.items():
        # mkdocs-redirects rewrites the source page to redirect to the target.
        # Targets are .md paths relative to docs_dir; resolve to built HTML.
        # Strip any anchor fragment before checking the file exists.
        target = dst.split("#", 1)[0]
        if not target.endswith(".md"):
            continue
        stem = target[: -len(".md")]
        # Under use_directory_urls=true (mkdocs default):
        #   foo/index.md -> site/foo/index.html
        #   foo/bar.md   -> site/foo/bar/index.html
        if stem == "index" or stem.endswith("/index"):
            html_path = SITE_DIR / f"{stem}.html"
        else:
            html_path = SITE_DIR / f"{stem}/index.html"
        if not html_path.exists():
            missing.append((src, dst))

    if missing:
        print(f"ERROR: {len(missing)} redirect target(s) do not exist in built site:")
        for src, dst in missing:
            print(f"  {src} -> {dst}")
        return 1

    print(f"OK: all {len(redirects)} redirect targets exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
