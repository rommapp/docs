"""Shared helpers for source-of-truth generators."""

from __future__ import annotations

import urllib.request
import tomllib
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
DOCS_DIR = REPO_ROOT / "docs"
SNIPPETS_DIR = DOCS_DIR / "resources" / "snippets"
SOURCES_FILE = SCRIPTS_DIR / "sources.toml"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"
SITE_DIR = REPO_ROOT / "site"
ENV_FILE = REPO_ROOT / ".env"


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
