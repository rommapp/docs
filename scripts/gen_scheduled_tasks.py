"""Generate the scheduled-tasks reference table from the upstream task registry.

Output: docs/resources/snippets/scheduled-tasks.md (a Markdown table).

Included by administration/scheduled-tasks.md via:
    --8<-- "scheduled-tasks.md"

Run manually:
    uv run python -m scripts.gen_scheduled_tasks

Sources, all fetched at the ref pinned in sources.toml:

    backend/tasks/registry.py   the SCHEDULED_TASKS and MANUAL_TASKS registries,
                                and the TaskSpec each entry maps to (title,
                                enabled flag and cron default)
    env.template                resolves env constants to documented defaults

Every env var name in the output is resolved through env.template. A task
referencing a constant env.template doesn't define fails the build instead of
printing an invented name, which is how this table drifted for several releases
(see the `*_INTERVAL_CRON` names that never existed upstream).

Watchers aren't registered tasks, so they can't be discovered the same way. They
stay declared in WATCHERS below, but their env vars go through the same
env.template check as everything else.
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Iterable, Iterator

from scripts._sources import fetch_text, romm_raw_url, write_snippet
from scripts.gen_env_vars import parse as parse_env_template

# Watchers live outside backend/tasks/, so they're declared rather than
# discovered. The env var names are still validated against env.template.
WATCHERS = [
    {
        "name": "Filesystem watcher",
        "enable_var": "ENABLE_RESCAN_ON_FILESYSTEM_CHANGE",
        "env_var": "RESCAN_ON_FILESYSTEM_CHANGE_DELAY",
        "purpose": "Watch the library folder and trigger a rescan on changes.",
    },
    {
        "name": "Sync folder watcher",
        "enable_var": "ENABLE_SYNC_FOLDER_WATCHER",
        "env_var": "SYNC_FOLDER_SCAN_DELAY",
        "purpose": "Watch the sync folder and trigger a scan on changes.",
    },
]

ABSENT = object()  # Distinguishes "resolved to None" from "keyword not passed".

# Tasks whose `enabled=` is a function call rather than an env constant. The
# call can't be resolved statically, so its meaning is declared here instead.
ENABLED_CALLS = {
    "streaming_enabled": "Runs only while emulator streaming is enabled.",
}


class UpstreamDrift(RuntimeError):
    """Upstream no longer matches what this generator knows how to read."""


def module_assignments(tree: ast.Module) -> Iterator[tuple[str, ast.expr | None]]:
    """(name, value) for every module-level `name = value` or `name: T = value`.

    The registries and their TaskSpecs are module-level, so `tree.body` is
    enough and nothing is gained by walking into function bodies.
    """
    for node in tree.body:
        if isinstance(node, ast.AnnAssign):
            targets: list[ast.expr] = [node.target]
        elif isinstance(node, ast.Assign):
            targets = list(node.targets)
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                yield target.id, node.value


def assigned_dict(tree: ast.Module, name: str) -> ast.Dict:
    """The dict literal assigned to a module-level `name`."""
    for target, value in module_assignments(tree):
        if target != name:
            continue
        if not isinstance(value, ast.Dict):
            raise UpstreamDrift(
                f"`{name}` in backend/tasks/registry.py is a "
                f"{type(value).__name__}, not a dict literal, so this "
                "parser can no longer read the registry."
            )
        return value

    raise UpstreamDrift(
        f"no `{name}` dict found in backend/tasks/registry.py. The registry moved "
        "or changed shape, so this parser needs updating."
    )


def task_specs(tree: ast.Module) -> dict[str, dict[str, ast.expr]]:
    """Keyword args of every module-level `X_SPEC = TaskSpec(...)` assignment.

    `SCAN_LIBRARY_SPEC: Final = TaskSpec(title="Scheduled rescan", ...)`
        -> {"SCAN_LIBRARY_SPEC": {"title": <Constant>, ...}}
    """
    specs: dict[str, dict[str, ast.expr]] = {}
    for name, value in module_assignments(tree):
        if not (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "TaskSpec"
        ):
            continue
        # Positional or `**` arguments would hide a title, flag or cron from
        # this parser, which would then print a default instead of failing.
        if value.args or any(kw.arg is None for kw in value.keywords):
            raise UpstreamDrift(
                f"{name} passes positional or ** arguments to TaskSpec, which "
                "this parser cannot resolve."
            )
        specs[name] = {kw.arg: kw.value for kw in value.keywords if kw.arg}
    return specs


def registry_specs(
    tree: ast.Module, specs: dict[str, dict[str, ast.expr]], name: str
) -> list[tuple[str, dict[str, ast.expr]]]:
    """The (spec name, kwargs) pairs a registry dict maps to, in source order.

    `SCHEDULED_TASKS = {"scan_library": SCAN_LIBRARY_SPEC, ...}`
        -> [("SCAN_LIBRARY_SPEC", {...}), ...]
    """
    out: list[tuple[str, dict[str, ast.expr]]] = []
    for value in assigned_dict(tree, name).values:
        if not isinstance(value, ast.Name):
            raise UpstreamDrift(
                f"{name} in backend/tasks/registry.py maps a key to a "
                f"{type(value).__name__} rather than a TaskSpec constant, which "
                "this parser cannot resolve."
            )
        if value.id not in specs:
            raise UpstreamDrift(
                f"{name} references {value.id}, which is not a module-level "
                "TaskSpec(...) in backend/tasks/registry.py."
            )
        if any(spec_name == value.id for spec_name, _ in out):
            raise UpstreamDrift(
                f"{name} maps two keys to {value.id}, which would list the same "
                "task twice."
            )
        out.append((value.id, specs[value.id]))
    return out


def env_name(var: str, env: dict[str, dict], where: str, field: str) -> str:
    if var not in env:
        raise UpstreamDrift(
            f"{where} passes {field}={var}, but env.template does not define "
            f"{var}. Either the variable was renamed upstream or it is "
            f"undocumented, and printing it here would be a guess."
        )
    return var


def resolve(node: ast.expr | None, env: dict[str, dict], where: str, field: str):
    """Resolve a TaskSpec argument to (env_var_name, value).

    A literal resolves to itself with no env var. A `Name` is an env constant, so
    it is looked up in env.template and fails loudly if absent.
    """
    if node is None:
        return None, ABSENT

    if isinstance(node, ast.Constant):
        return None, node.value

    if isinstance(node, ast.Name):
        var = env_name(node.id, env, where, field)
        return var, env[var]["default"]

    # `f"... {ENV_VAR} ..."`: print the env var's name where its value goes.
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            elif isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Name):
                parts.append(f"`{env_name(v.value.id, env, where, field)}`")
            else:
                break
        else:
            return None, "".join(parts)

    # `enabled=ENV_VAR > 0`: the env var is still what turns the task on.
    if isinstance(node, ast.Compare) and isinstance(node.left, ast.Name):
        var = env_name(node.left.id, env, where, field)
        return var, env[var]["default"]

    # Anything else (a call, a conditional) is beyond what this parser claims
    # to understand, so say so rather than print something wrong.
    raise UpstreamDrift(
        f"{where} passes a {type(node).__name__} for {field}, which this parser "
        f"cannot resolve. Extend resolve() to handle it."
    )


def build_row(
    where: str, kwargs: dict[str, ast.expr], kind: str, env: dict[str, dict]
) -> dict:
    _, title = resolve(kwargs.get("title"), env, where, "title")
    _, description = resolve(kwargs.get("description"), env, where, "description")
    cron_var, cron = resolve(kwargs.get("cron_string"), env, where, "cron_string")

    enabled = kwargs.get("enabled")
    note = ""
    enabled_value: object = True
    if (
        isinstance(enabled, ast.Call)
        and isinstance(enabled.func, ast.Name)
        and enabled.func.id in ENABLED_CALLS
    ):
        enable_var, note = None, ENABLED_CALLS[enabled.func.id]
    else:
        enable_var, enabled_value = resolve(enabled, env, where, "enabled")
        if isinstance(enabled, ast.Compare):
            # The env var isn't a plain on/off switch, so spell out the test.
            note = f"Runs while `{ast.unparse(enabled)}`."

    if title in (ABSENT, None, ""):
        raise UpstreamDrift(f"{where} has no title=")

    if description in (ABSENT, None, ""):
        purpose = "-"
    else:
        purpose = str(description).rstrip(".") + "."
    if note:
        purpose += " " + note
    elif kind == "Scheduled" and not enable_var:
        # TaskSpec defaults `enabled` to False, so a missing flag means off too.
        if enabled_value is True:
            purpose += " Always on, not configurable."
        else:
            purpose += " Off, not configurable."

    return {
        "name": str(title),
        "type": kind,
        "default_cron": str(cron) if cron not in (ABSENT, None, "") else "-",
        "enable_var": enable_var or "-",
        "env_var": cron_var or "-",
        "purpose": purpose,
    }


def collect(env: dict[str, dict]) -> list[dict]:
    registry = ast.parse(fetch_text(romm_raw_url("backend/tasks/registry.py")))
    specs = task_specs(registry)
    scheduled = registry_specs(registry, specs, "SCHEDULED_TASKS")
    manual = registry_specs(registry, specs, "MANUAL_TASKS")
    scheduled_names = {name for name, _ in scheduled}

    rows = [build_row(n, kw, "Scheduled", env) for n, kw in scheduled]
    # A task in both registries is scheduled and also runnable by hand, so it is
    # already listed above.
    rows += [
        build_row(n, kw, "Manual", env) for n, kw in manual if n not in scheduled_names
    ]

    for w in WATCHERS:
        for field in ("enable_var", "env_var"):
            if w[field] not in env:
                raise UpstreamDrift(
                    f"watcher {w['name']} references {w[field]}, which env.template "
                    f"does not define. Update WATCHERS in this script."
                )
        rows.append({**w, "type": "Watcher", "default_cron": "-"})

    return rows


def render(rows: Iterable[dict]) -> str:
    out = [
        "<!-- AUTOGENERATED by scripts/gen_scheduled_tasks.py: do not edit. -->",
        "",
        "| Task | Type | Default schedule | Enable var | Schedule/delay var | Purpose |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for t in rows:
        out.append(
            f"| {t['name']} | {t['type']} | `{t['default_cron']}` "
            f"| `{t['enable_var']}` | `{t['env_var']}` | {t['purpose']} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> int:
    env_rows = parse_env_template(fetch_text(romm_raw_url("env.template")))
    env = {r["name"]: r for r in env_rows}
    if not env:
        print("WARN: no env vars parsed from env.template", file=sys.stderr)
        return 1

    try:
        rows = collect(env)
    except UpstreamDrift as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out = write_snippet("scheduled-tasks.md", render(rows))
    counts = {
        kind: sum(1 for r in rows if r["type"] == kind)
        for kind in ("Scheduled", "Manual", "Watcher")
    }
    print(
        f"Wrote {len(rows)} tasks to {out} ({counts['Scheduled']} scheduled, "
        f"{counts['Manual']} manual, {counts['Watcher']} watchers)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
