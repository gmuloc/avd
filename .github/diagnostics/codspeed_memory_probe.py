# Copyright (c) 2026 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
# ruff: noqa: INP001
"""Observe CodSpeed Python profiling outside benchmark measurement windows."""

from __future__ import annotations

import json
import os
import shutil
import sys
import sysconfig
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

OUTPUT = Path(os.environ.get("MEMORY_DIAGNOSTIC_OUTPUT", "/tmp/avd-memory-diagnostic"))  # noqa: S108


def record_state(stage: str, nodeid: str | None = None) -> None:
    """Record profiler state without enabling or altering profiling."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    pid = os.getpid()
    perf_map = Path(f"/tmp/perf-{pid}.map")  # noqa: S108
    lines = perf_map.read_text().splitlines() if perf_map.exists() else []
    checker = getattr(sys, "is_stack_trampoline_active", None)
    state = {
        "stage": stage,
        "nodeid": nodeid,
        "pid": pid,
        "python": sys.version,
        "pytest_codspeed": version("pytest-codspeed"),
        "supports_perf_trampoline": sysconfig.get_config_var("PY_HAVE_PERF_TRAMPOLINE"),
        "stack_trampoline_active": checker() if checker else None,  # pylint: disable=using-constant-test
        "perf_map": str(perf_map),
        "perf_map_exists": perf_map.exists(),
        "perf_map_lines": len(lines),
        "perf_map_benchmark_examples": [line for line in lines if "benchmarks/test_" in line][:5],
        "children": Path(f"/proc/{pid}/task/{pid}/children").read_text().strip(),
        "thread_count": len(list(Path(f"/proc/{pid}/task").iterdir())),
        "environment": {
            key: os.environ.get(key)
            for key in (
                "CODSPEED_ENV",
                "CODSPEED_RUNNER_MODE",
                "CODSPEED_PROFILE_FOLDER",
                "PYTHONPERFSUPPORT",
                "PYTHON_PERF_JIT_SUPPORT",
                "PYTHONMALLOC",
            )
        },
    }
    with (OUTPUT / "states.jsonl").open("a") as stream:
        stream.write(json.dumps(state) + "\n")
    print("MEMORY_DIAGNOSTIC " + json.dumps(state), flush=True)  # noqa: T201
    profile_folder = os.environ.get("CODSPEED_PROFILE_FOLDER")
    if profile_folder:
        (OUTPUT / "profile-folder.txt").write_text(profile_folder)
    if perf_map.exists():
        shutil.copy2(perf_map, OUTPUT / perf_map.name)


@pytest.hookimpl(trylast=True)
def pytest_sessionstart() -> None:
    """Observe the state after pytest-codspeed configures its instrument."""
    record_state("session_start")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item: pytest.Item) -> Iterator[None]:
    """Observe each case after the measured callback and fixture teardown."""
    try:
        yield
    finally:
        record_state("after_test", item.nodeid)


def pytest_sessionfinish() -> None:
    """Preserve the Python symbol map before the process exits."""
    record_state("session_finish")


def collect_artifacts() -> None:
    """Retain the runner's completed profile after its action returns."""
    profile_file = OUTPUT / "profile-folder.txt"
    if not profile_file.exists():
        print("No profile directory was recorded", flush=True)  # noqa: T201
        return
    source = Path(profile_file.read_text().strip())
    if not source.is_dir():
        print(f"Recorded profile directory is missing: {source}", flush=True)  # noqa: T201
        return
    shutil.copytree(source, OUTPUT / "runner-profile", dirs_exist_ok=True)
    inventory = [{"path": str(path.relative_to(source)), "bytes": path.stat().st_size} for path in sorted(source.rglob("*")) if path.is_file()]
    (OUTPUT / "profile-inventory.json").write_text(json.dumps(inventory, indent=2))
    print(json.dumps(inventory, indent=2), flush=True)  # noqa: T201


if __name__ == "__main__":
    collect_artifacts()
