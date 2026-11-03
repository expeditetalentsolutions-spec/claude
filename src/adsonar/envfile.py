"""Minimal .env loader (no extra dependency)."""

from __future__ import annotations

import os
from pathlib import Path


def load_env_file(path: str | os.PathLike = ".env", override: bool = False) -> bool:
    """Load KEY=VALUE lines into os.environ. Returns True if the file existed."""
    p = Path(path)
    if not p.is_file():
        return False
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if override or key not in os.environ:
            os.environ[key] = value
    return True
