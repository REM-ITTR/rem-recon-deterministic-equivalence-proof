from __future__ import annotations
import hashlib
from typing import Iterable, Tuple

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def write_manifest(manifest_path: str, files: Iterable[str]) -> None:
    lines = []
    for p in files:
        lines.append(f"{sha256_file(p)}  {p}")
    lines.sort()
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
