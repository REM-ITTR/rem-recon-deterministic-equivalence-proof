from __future__ import annotations
from typing import Dict, List, Tuple
from datetime import datetime
import hashlib
import json

Row = Dict[str, str]

def _tx_id(row: Row) -> str:
    s = f'{row["ledger"]}|{row["trace_id"]}|{row["timestamp_iso"]}|{row["amount_cents"]}|{row["currency"]}|{row["direction"]}'
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def _minute_bucket(ts: str) -> str:
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%dT%H:%M")

def _join_key(row: Row) -> Tuple[str, str, str, str]:
    return (row["trace_id"], row["currency"], row["direction"], _minute_bucket(row["timestamp_iso"]))

def reconcile(ledger_A: List[Row], ledger_B: List[Row]) -> Dict:
    def group(rows: List[Row]) -> Dict[Tuple[str, str, str, str], List[Row]]:
        g: Dict[Tuple[str, str, str, str], List[Row]] = {}
        for r in rows:
            g.setdefault(_join_key(r), []).append(r)
        return g

    gA = group(ledger_A)
    gB = group(ledger_B)

    mismatches = []
    keys = sorted(set(gA.keys()) | set(gB.keys()))

    # Totals of the provided dataset (full or reduced). Useful for context, but not an equivalence invariant.
    totalA = sum(int(r["amount_cents"]) for r in ledger_A)
    totalB = sum(int(r["amount_cents"]) for r in ledger_B)

    mismatch_delta_total = 0

    for k in keys:
        a_rows = gA.get(k, [])
        b_rows = gB.get(k, [])
        sumA = sum(int(r["amount_cents"]) for r in a_rows)
        sumB = sum(int(r["amount_cents"]) for r in b_rows)

        if len(a_rows) != len(b_rows) or sumA != sumB:
            mismatch_delta_total += (sumA - sumB)
            mismatches.append({
                "join_key": k,
                "count_A": len(a_rows),
                "count_B": len(b_rows),
                "sumA_cents": sumA,
                "sumB_cents": sumB,
                "sample_tx_A": [_tx_id(r) for r in a_rows[:3]],
                "sample_tx_B": [_tx_id(r) for r in b_rows[:3]],
            })

    result = {
        "meta": {
            "rows_A": len(ledger_A),
            "rows_B": len(ledger_B),
            "totalA_cents": totalA,
            "totalB_cents": totalB,
            "mismatch_count": len(mismatches),
            "mismatch_delta_total_cents": mismatch_delta_total,
        },
        "mismatches": mismatches,
    }
    return result

def write_json(path: str, obj: Dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
