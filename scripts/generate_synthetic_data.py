from __future__ import annotations
import argparse
import csv
import json
import os
import random
from datetime import datetime, timedelta

FIELDS = ["ledger","trace_id","timestamp_iso","amount_cents","currency","direction","merchant","channel"]

def make_row(ledger: str, trace_id: str, ts: datetime, amount_cents: int, currency: str, direction: str, merchant: str, channel: str):
    return {
        "ledger": ledger,
        "trace_id": trace_id,
        "timestamp_iso": ts.strftime("%Y-%m-%dT%H:%M:%S"),
        "amount_cents": str(amount_cents),
        "currency": currency,
        "direction": direction,
        "merchant": merchant,
        "channel": channel,
    }

def write_csv(path: str, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--n", type=int, default=100000)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    random.seed(args.seed)

    start = datetime(2026, 1, 1, 9, 0, 0)
    currencies = ["USD"]
    directions = ["DEBIT","CREDIT"]
    merchants = ["M1","M2","M3","M4","M5"]
    channels = ["POS","ECOM","MOTO"]

    A = []
    B = []
    injected = {
        "missing_in_B": [],
        "missing_in_A": [],
        "amount_mismatch": [],
        "timing_drift": [],
        "duplicate_in_B": []
    }

    # Generate base matching transactions
    for i in range(args.n):
        trace_id = f"T{i:09d}"
        ts = start + timedelta(seconds=i % 3600)  # repeat within hour
        amount = random.randint(100, 25000)       # $1 to $250
        currency = currencies[0]
        direction = random.choice(directions)
        merchant = random.choice(merchants)
        channel = random.choice(channels)

        rowA = make_row("A", trace_id, ts, amount, currency, direction, merchant, channel)
        rowB = make_row("B", trace_id, ts, amount, currency, direction, merchant, channel)
        A.append(rowA)
        B.append(rowB)

    # Inject anomalies deterministically by index slices
    # 1) Missing in B
    for i in range(100, 150):
        injected["missing_in_B"].append(A[i]["trace_id"])
        B[i] = None

    # 2) Missing in A
    for i in range(200, 240):
        injected["missing_in_A"].append(B[i]["trace_id"])
        A[i] = None

    # 3) Amount mismatch in B
    for i in range(400, 460):
        injected["amount_mismatch"].append(A[i]["trace_id"])
        B[i]["amount_cents"] = str(int(B[i]["amount_cents"]) + 37)

    # 4) Timing drift (+65 seconds) in B (same minute bucket may change)
    for i in range(700, 760):
        injected["timing_drift"].append(A[i]["trace_id"])
        ts = datetime.fromisoformat(B[i]["timestamp_iso"]) + timedelta(seconds=65)
        B[i]["timestamp_iso"] = ts.strftime("%Y-%m-%dT%H:%M:%S")

    # 5) Duplicate in B
    for i in range(900, 930):
        injected["duplicate_in_B"].append(A[i]["trace_id"])
        B.append(dict(B[i]))  # duplicate row

    # Remove Nones
    A = [r for r in A if r is not None]
    B = [r for r in B if r is not None]

    write_csv(os.path.join(args.out_dir, "ledger_A.csv"), A)
    write_csv(os.path.join(args.out_dir, "ledger_B.csv"), B)

    with open(os.path.join(args.out_dir, "injected_breaks.json"), "w", encoding="utf-8") as f:
        json.dump(injected, f, indent=2, sort_keys=True)

    print(f"Wrote {len(A)} rows to ledger_A.csv")
    print(f"Wrote {len(B)} rows to ledger_B.csv")
    print("Wrote injected_breaks.json")

if __name__ == "__main__":
    main()
