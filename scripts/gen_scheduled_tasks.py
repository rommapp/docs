"""Generate the scheduled-tasks reference table from the upstream task registry.

Output: docs/resources/snippets/scheduled-tasks.md (a Markdown table).

Included by administration/scheduled-tasks.md via:
    --8<-- "scheduled-tasks.md"

Run manually:
    uv run python -m scripts.gen_scheduled_tasks

Sources, all fetched at the ref pinned in sources.toml:

    backend/tasks/registry.py   the SCHEDULED_TASKS and MANUAL_TASKS registries
    backend/tasks/**.py         each task's title, enabled flag and cron default
    env.template                resolves env constants to documented defaults

Every env var name in the output is resolved through env.template. A task
referencing a constant env.template doesn't define fails the build instead of
printing an invented name, which is how this table drifted for several releases
(see the `*_INTERVAL_CRON` names that never existed upstream).

Watchers aren't Task subclasses, so they can't be discovered the same way. They
stay declared in WATCHERS below, but their env vars go through the same
env.template check as everything else.
"""

from __future__ import annotations

import ast
import sys
from typing import Iterable

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

TASK_BASES = {"Task", "PeriodicTask", "RemoteFilePullTask"}
ABSENT = object()  # Distinguishes "resolved to None" from "keyword not passed".


class UpstreamDrift(RuntimeError):
    """Upstream no longer matches what this generator knows how to read."""


def import_map(tree: ast.Module) -> dict[str, str]:
    """Map imported task singletons to the module path they came from.

    `from tasks.scheduled.scan_library import scan_library_task`
        -> {"scan_library_task": "backend/tasks/scheduled/scan_library.py"}
    """
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        # `tasks.tasks` holds the base classes and TaskType, not task singletons.
        if not node.module.startswith("tasks.") or node.module == "tasks.tasks":
            continue
        path = "backend/" + node.module.replace(".", "/") + ".py"
        for alias in node.names:
            out[alias.asname or alias.name] = path
    return out


def assigned_dict(tree: ast.Module, name: str) -> ast.Dict:
    """The dict literal assigned to a module-level `name`.

    Both registries are module-level, so `tree.body` is enough and nothing is
    gained by walking into function bodies.
    """
    for node in tree.body:
        if isinstance(node, ast.AnnAssign):
            targets: list[ast.expr] = [node.target]
        elif isinstance(node, ast.Assign):
            targets = list(node.targets)
        else:
            continue
        if not any(isinstance(t, ast.Name) and t.id == name for t in targets):
            continue
        if not isinstance(node.value, ast.Dict):
            raise UpstreamDrift(
                f"`{name}` in backend/tasks/registry.py is a "
                f"{type(node.value).__name__}, not a dict literal, so this "
                "parser can no longer read the registry."
            )
        return node.value

    raise UpstreamDrift(
        f"no `{name}` dict found in backend/tasks/registry.py. The registry moved "
        "or changed shape, so this parser needs updating."
    )


def registry_module_paths(
    tree: ast.Module, imports: dict[str, str], name: str
) -> list[str]:
    """Module paths for the task singletons a registry dict maps to.

    `SCHEDULED_TASKS = {"scan_library": scan_library_task, ...}`
        -> ["backend/tasks/scheduled/scan_library.py", ...]

    Registry order is the table's order, so the dict is read in source order.
    """
    paths: list[str] = []
    for value in assigned_dict(tree, name).values:
        if not isinstance(value, ast.Name):
            raise UpstreamDrift(
                f"{name} in backend/tasks/registry.py maps a key to a "
                f"{type(value).__name__} rather than an imported task "
                "singleton, which this parser cannot resolve."
            )
        path = imports.get(value.id)
        if path is None:
            raise UpstreamDrift(
                f"{name} references {value.id}, which is not imported from a "
                "tasks.* module in backend/tasks/registry.py."
            )
        if path in paths:
            # Registry keys are unique, so two of them resolving to one module
            # means two task singletons share a file. `task_kwargs` reads only
            # the first task class it finds there, so the second would vanish
            # from the table without a word.
            raise UpstreamDrift(
                f"{name} maps two tasks to {path}. task_kwargs() reads only the "
                "first task class in a module, so one would be dropped silently."
            )
        paths.append(path)
    return paths


def task_kwargs(module_src: str, path: str) -> dict[str, ast.expr]:
    """Keyword args of the `super().__init__(...)` call in a task class."""
    tree = ast.parse(module_src)

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {b.id for b in node.bases if isinstance(b, ast.Name)}
        if not base_names & TASK_BASES:
            continue
        for call in ast.walk(node):
            if not isinstance(call, ast.Call):
                continue
            func = call.func
            if not isinstance(func, ast.Attribute) or func.attr != "__init__":
                continue
            return {kw.arg: kw.value for kw in call.keywords if kw.arg}

    raise UpstreamDrift(f"no task class with a `super().__init__(...)` call in {path}")


def resolve(node: ast.expr | None, env: dict[str, dict], path: str, field: str):
    """Resolve a constructor argument to (env_var_name, value).

    A literal resolves to itself with no env var. A `Name` is an env constant, so
    it is looked up in env.template and fails loudly if absent.
    """
    if node is None:
        return None, ABSENT

    if isinstance(node, ast.Constant):
        return None, node.value

    if isinstance(node, ast.Name):
        var = node.id
        if var not in env:
            raise UpstreamDrift(
                f"{path} passes {field}={var}, but env.template does not define "
                f"{var}. Either the variable was renamed upstream or it is "
                f"undocumented, and printing it here would be a guess."
            )
        return var, env[var]["default"]

    # Anything else (a call, an f-string, a conditional) is beyond what this
    # parser claims to understand, so say so rather than print something wrong.
    raise UpstreamDrift(
        f"{path} passes a {type(node).__name__} for {field}, which this parser "
        f"cannot resolve. Extend resolve() to handle it."
    )


def build_row(path: str, kind: str, env: dict[str, dict]) -> dict:
    kwargs = task_kwargs(fetch_text(romm_raw_url(path)), path)

    _, title = resolve(kwargs.get("title"), env, path, "title")
    _, description = resolve(kwargs.get("description"), env, path, "description")
    enable_var, _ = resolve(kwargs.get("enabled"), env, path, "enabled")
    cron_var, cron = resolve(kwargs.get("cron_string"), env, path, "cron_string")

    if title in (ABSENT, None, ""):
        raise UpstreamDrift(f"{path} has no title= in its constructor")

    if description in (ABSENT, None, ""):
        purpose = "-"
    else:
        purpose = str(description).rstrip(".") + "."
    if kind == "Scheduled" and not enable_var:
        purpose += " Always on, not configurable."

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
    imports = import_map(registry)
    scheduled = registry_module_paths(registry, imports, "SCHEDULED_TASKS")
    manual = registry_module_paths(registry, imports, "MANUAL_TASKS")

    rows = [build_row(p, "Scheduled", env) for p in scheduled]
    # A task in both registries is scheduled and also runnable by hand, so it is
    # already listed above.
    rows += [build_row(p, "Manual", env) for p in manual if p not in scheduled]

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
