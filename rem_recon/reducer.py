from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
from datetime import datetime

Row = Dict[str, str]

def _minute_bucket(ts: str) -> str:
    # ts: ISO "YYYY-MM-DDTHH:MM:SS"
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%dT%H:%M")

def _key(row: Row) -> Tuple[str, str, str, str, str]:
    # Stable deterministic key
    return (
        row["trace_id"],
        row["amount_cents"],
        row["currency"],
        row["direction"],
        _minute_bucket(row["timestamp_iso"]),
    )

@dataclass(frozen=True)
class ReduceResult:
    reduced_A: List[Row]
    reduced_B: List[Row]
    kept_keys: Set[Tuple[str, str, str, str, str]]

def reduce_candidates(ledger_A: List[Row], ledger_B: List[Row]) -> ReduceResult:
    # Index counts by key for each side
    countA: Dict[Tuple[str, str, str, str, str], int] = {}
    countB: Dict[Tuple[str, str, str, str, str], int] = {}

    for r in ledger_A:
        k = _key(r)
        countA[k] = countA.get(k, 0) + 1

    for r in ledger_B:
        k = _key(r)
        countB[k] = countB.get(k, 0) + 1

    # Keep keys where counts differ (mismatch candidates)
    mismatch_keys = {k for k in set(countA) | set(countB) if countA.get(k, 0) != countB.get(k, 0)}

    # Deterministic neighborhood expansion: keep same trace_id +/- 1 minute bucket
    # This captures timing drift without heuristics.
    trace_to_keys: Dict[str, Set[Tuple[str, str, str, str, str]]] = {}
    for k in set(countA) | set(countB):
        trace_to_keys.setdefault(k[0], set()).add(k)

    kept: Set[Tuple[str, str, str, str, str]] = set()
    for k in mismatch_keys:
        trace = k[0]
        kept.add(k)
        # Add all keys for that trace_id (safe & deterministic)
        kept |= trace_to_keys.get(trace, set())

    reduced_A = [r for r in ledger_A if _key(r) in kept]
    reduced_B = [r for r in ledger_B if _key(r) in kept]

    return ReduceResult(reduced_A=reduced_A, reduced_B=reduced_B, kept_keys=kept)
