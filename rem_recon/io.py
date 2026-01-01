from __future__ import annotations
import csv
from typing import Dict, Iterable, List

Row = Dict[str, str]

def read_csv(path: str) -> List[Row]:
    with open(path, "r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return [dict(row) for row in r]

def write_csv(path: str, rows: Iterable[Row], fieldnames: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)
