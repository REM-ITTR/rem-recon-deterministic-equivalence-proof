from __future__ import annotations
import argparse
import os

from rem_recon.io import read_csv, write_csv
from rem_recon.reducer import reduce_candidates
from rem_recon.recon import reconcile, write_json
from rem_recon.hashing import write_manifest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    pathA = os.path.join(args.data_dir, "ledger_A.csv")
    pathB = os.path.join(args.data_dir, "ledger_B.csv")

    A = read_csv(pathA)
    B = read_csv(pathB)

    full = reconcile(A, B)
    full_path = os.path.join(args.out_dir, "full_recon_result.json")
    write_json(full_path, full)

    rr = reduce_candidates(A, B)

    reducedA_path = os.path.join(args.out_dir, "reduced_A.csv")
    reducedB_path = os.path.join(args.out_dir, "reduced_B.csv")

    # Preserve original columns
    fieldnames = list(A[0].keys()) if A else []
    write_csv(reducedA_path, rr.reduced_A, fieldnames=fieldnames)
    write_csv(reducedB_path, rr.reduced_B, fieldnames=fieldnames)

    reduced = reconcile(rr.reduced_A, rr.reduced_B)
    reduced_path = os.path.join(args.out_dir, "reduced_recon_result.json")
    write_json(reduced_path, reduced)

    # Write manifest for audit
    manifest_path = os.path.join(args.out_dir, "sha256_manifest.txt")
    write_manifest(manifest_path, [pathA, pathB, full_path, reducedA_path, reducedB_path, reduced_path])

    # Quick summary
    print("=== SUMMARY ===")
    print(f"Full rows A+B: {full['meta']['rows_A'] + full['meta']['rows_B']}")
    print(f"Reduced rows A+B: {reduced['meta']['rows_A'] + reduced['meta']['rows_B']}")
    print(f"Mismatch count (full): {full['meta']['mismatch_count']}")
    print(f"Mismatch count (reduced): {reduced['meta']['mismatch_count']}")
    print(f"Wrote manifest: {manifest_path}")

if __name__ == "__main__":
    main()
