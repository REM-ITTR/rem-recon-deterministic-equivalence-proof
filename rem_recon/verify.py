from __future__ import annotations
from typing import Dict, Tuple, List

def _mismatch_signatures(result: Dict) -> List[Tuple]:
    sigs = []
    for m in result["mismatches"]:
        sigs.append((tuple(m["join_key"]), m["count_A"], m["count_B"], m["sumA_cents"], m["sumB_cents"]))
    sigs.sort()
    return sigs

def equivalent(full_result: Dict, reduced_result: Dict) -> Tuple[bool, str]:
    fmeta = full_result["meta"]
    rmeta = reduced_result["meta"]

    # Core invariant: same mismatch set (same signatures)
    fsigs = _mismatch_signatures(full_result)
    rsigs = _mismatch_signatures(reduced_result)

    if fmeta["mismatch_count"] != rmeta["mismatch_count"]:
        return (False, f"FAIL: mismatch_count differs (full={fmeta['mismatch_count']} reduced={rmeta['mismatch_count']}).")

    if fsigs != rsigs:
        return (False, "FAIL: mismatch signatures differ (join_key/count/sums).")

    # Aggregate invariance (correct definition): mismatch delta totals match
    if fmeta.get("mismatch_delta_total_cents") != rmeta.get("mismatch_delta_total_cents"):
        return (False, "FAIL: mismatch delta total differs (sumA-sumB across mismatches).")

    return (True, "PASS: reduced reconciliation is equivalent to full reconciliation (mismatches + mismatch-delta totals).")
