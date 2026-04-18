"""One-shot scaffolder: create placeholder pages for the v5.0 IA.

Idempotent: pages that already exist are left alone. Used during the
initial overhaul setup; can be deleted once the IA is stable.

Run:
    uv run python docs/scripts/scaffold_ia.py
"""

from __future__ import annotations

from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]

# (relative_path, page_title, wave) -- wave is informational, surfaced in the stub.
PAGES: list[tuple[str, str, int]] = [
    # Getting Started
    ("getting-started/quick-start.md", "Quick Start", 1),
    ("getting-started/folder-structure.md", "Folder Structure", 1),
    ("getting-started/first-scan.md", "Your First Scan", 1),
    ("getting-started/concepts.md", "Core Concepts", 1),
    ("getting-started/what-is-new-in-5.md", "What's New in 5.0", 1),
    # Install & Deploy
    ("install/index.md", "Install & Deploy", 1),
    ("install/docker-compose.md", "Docker Compose", 1),
    ("install/image-variants.md", "Image Variants", 1),
    ("install/databases.md", "Databases", 1),
    ("install/redis-or-valkey.md", "Redis or Valkey", 1),
    ("install/reverse-proxy.md", "Reverse Proxy", 1),
    ("install/unraid.md", "Unraid", 1),
    ("install/synology.md", "Synology", 1),
    ("install/truenas.md", "TrueNAS", 1),
    ("install/kubernetes.md", "Kubernetes", 1),
    ("install/backup-and-restore.md", "Backup & Restore", 1),
    # Administration
    ("administration/index.md", "Administration", 1),
    ("administration/users-and-roles.md", "Users & Roles", 1),
    ("administration/invitations-and-registration.md", "Invitations & Registration", 1),
    ("administration/authentication.md", "Authentication", 1),
    ("administration/metadata-providers.md", "Metadata Providers", 1),
    ("administration/scanning-and-watcher.md", "Scanning & Watcher", 1),
    ("administration/scheduled-tasks.md", "Scheduled Tasks", 1),
    ("administration/server-stats.md", "Server Stats", 1),
    ("administration/observability.md", "Observability", 1),
    ("administration/firmware-management.md", "Firmware Management", 1),
    ("administration/ssh-sync.md", "SSH Sync", 1),
    ("administration/administration-page.md", "Administration Page", 1),
    # Administration / OIDC
    ("administration/oidc/index.md", "OIDC Setup", 1),
    ("administration/oidc/authelia.md", "OIDC with Authelia", 1),
    ("administration/oidc/authentik.md", "OIDC with Authentik", 1),
    ("administration/oidc/keycloak.md", "OIDC with Keycloak", 1),
    ("administration/oidc/pocketid.md", "OIDC with PocketID", 1),
    ("administration/oidc/zitadel.md", "OIDC with Zitadel", 1),
    # Using RomM
    ("using/index.md", "Using RomM", 2),
    ("using/library.md", "Library", 2),
    ("using/collections.md", "Collections", 2),
    ("using/smart-collections.md", "Smart Collections", 2),
    ("using/virtual-collections.md", "Virtual Collections", 2),
    ("using/downloads.md", "Downloads", 2),
    ("using/uploads.md", "Uploads", 2),
    ("using/in-browser-play.md", "In-Browser Play", 2),
    ("using/saves-and-states.md", "Saves & States", 2),
    ("using/retroachievements.md", "RetroAchievements", 2),
    ("using/rom-patcher.md", "ROM Patcher", 2),
    ("using/netplay.md", "Netplay", 2),
    ("using/console-mode.md", "Console Mode", 2),
    ("using/pwa.md", "Install as PWA", 2),
    ("using/mobile-and-tv.md", "Mobile & TV", 2),
    ("using/account-and-profile.md", "Account & Profile", 2),
    ("using/languages.md", "Languages", 2),
    # Platforms & Players
    ("platforms/index.md", "Platforms & Players", 2),
    ("platforms/supported-platforms.md", "Supported Platforms", 2),
    ("platforms/custom-platforms.md", "Custom Platforms", 2),
    ("platforms/ms-dos.md", "MS-DOS", 2),
    ("platforms/emulatorjs-config.md", "EmulatorJS Configuration", 2),
    ("platforms/ruffle-config.md", "Ruffle Configuration", 2),
    ("platforms/firmware-by-platform.md", "Firmware by Platform", 2),
    # Ecosystem
    ("ecosystem/index.md", "Integrations & Ecosystem", 3),
    ("ecosystem/argosy.md", "Argosy Launcher", 3),
    ("ecosystem/grout.md", "Grout", 3),
    ("ecosystem/playnite-plugin.md", "Playnite Plugin", 3),
    ("ecosystem/muos-app.md", "muOS App", 3),
    ("ecosystem/tinfoil.md", "Tinfoil", 3),
    ("ecosystem/pkgj.md", "pkgj", 3),
    ("ecosystem/fpkgi.md", "fpkgi", 3),
    ("ecosystem/kekatsu.md", "Kekatsu", 3),
    ("ecosystem/webrcade.md", "WebRcade", 3),
    ("ecosystem/community-apps.md", "Community Apps", 3),
    ("ecosystem/device-sync-protocol.md", "Device Sync Protocol", 3),
    ("ecosystem/client-api-tokens.md", "Client API Tokens", 3),
    ("ecosystem/igir.md", "Igir Collection Manager", 3),
    # Developers
    ("developers/index.md", "API & Development", 1),
    ("developers/api-reference.md", "API Reference", 1),
    ("developers/api-authentication.md", "API Authentication", 1),
    ("developers/websockets.md", "WebSockets", 3),
    ("developers/openapi.md", "Consuming OpenAPI", 3),
    ("developers/development-setup.md", "Development Setup", 1),
    ("developers/architecture.md", "Architecture", 3),
    ("developers/contributing.md", "Contributing", 1),
    ("developers/i18n.md", "Translations (i18n)", 3),
    ("developers/releasing.md", "Releasing", 3),
    # Reference
    ("reference/environment-variables.md", "Environment Variables", 1),
    ("reference/configuration-file.md", "Configuration File", 1),
    ("reference/scheduled-tasks.md", "Scheduled Tasks Reference", 1),
    ("reference/exports.md", "Exports", 3),
    ("reference/feeds.md", "Feeds", 3),
    ("reference/ports-and-endpoints.md", "Ports & Endpoints", 3),
    ("reference/glossary.md", "Glossary", 3),
    # Troubleshooting
    ("troubleshooting/index.md", "Troubleshooting", 1),
    ("troubleshooting/scanning.md", "Scanning", 1),
    ("troubleshooting/authentication.md", "Authentication", 1),
    ("troubleshooting/synology.md", "Synology", 1),
    ("troubleshooting/kubernetes.md", "Kubernetes", 1),
    ("troubleshooting/in-browser-play.md", "In-Browser Play", 2),
    ("troubleshooting/netplay.md", "Netplay", 2),
    ("troubleshooting/sync.md", "Device Sync", 2),
    ("troubleshooting/miscellaneous.md", "Miscellaneous", 1),
    # Releases
    ("releases/index.md", "Release Notes & Migration", 1),
    ("releases/upgrading-to-5.0.md", "Upgrading to 5.0", 1),
    ("releases/upgrading-to-3.0.md", "Upgrading to 3.0", 1),
    ("releases/changelog.md", "Changelog", 1),
    # About
    ("about/faqs.md", "FAQs", 3),
    ("about/brand-guidelines.md", "Brand Guidelines", 3),
    ("about/license.md", "License", 3),
    ("about/credits.md", "Credits", 3),
]


STUB = """\
---
status: placeholder
wave: {wave}
---

# {title}

!!! warning "Placeholder — RomM 5.0 docs overhaul"
    This page is part of the RomM 5.0 documentation overhaul (Wave {wave}) and
    has not been written yet. See the overhaul plan for status and ownership.
"""


def main() -> int:
    created = 0
    for rel, title, wave in PAGES:
        path = DOCS / rel
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(title=title, wave=wave), encoding="utf-8")
        created += 1
    print(f"Created {created} placeholder pages ({len(PAGES) - created} already existed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
