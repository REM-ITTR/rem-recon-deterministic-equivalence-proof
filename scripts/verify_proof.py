from __future__ import annotations
import argparse
import json
import os

from rem_recon.verify import equivalent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    full_path = os.path.join(args.out_dir, "full_recon_result.json")
    reduced_path = os.path.join(args.out_dir, "reduced_recon_result.json")
    report_path = os.path.join(args.out_dir, "equivalence_report.txt")

    with open(full_path, "r", encoding="utf-8") as f:
        full = json.load(f)

    with open(reduced_path, "r", encoding="utf-8") as f:
        reduced = json.load(f)

    ok, msg = equivalent(full, reduced)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(msg + "\n")

    print(msg)
    print(f"Wrote: {report_path}")

if __name__ == "__main__":
    main()
