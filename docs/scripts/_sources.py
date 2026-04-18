"""Shared helpers for source-of-truth generators."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

SCRIPTS_DIR = Path(__file__).resolve().parent
SOURCES_FILE = SCRIPTS_DIR / "sources.toml"
SNIPPETS_DIR = SCRIPTS_DIR.parent / "resources" / "snippets"


def load_sources() -> dict:
    with SOURCES_FILE.open("rb") as f:
        return tomllib.load(f)


def romm_raw_url(path: str) -> str:
    sources = load_sources()
    repo = sources["romm"]["repo"]
    ref = sources["romm"]["ref"]
    return f"https://raw.githubusercontent.com/{repo}/{ref}/{path.lstrip('/')}"


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def write_snippet(name: str, content: str) -> Path:
    SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
    out = SNIPPETS_DIR / name
    out.write_text(content, encoding="utf-8")
    return out
