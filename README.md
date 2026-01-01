# REM-Recon — Deterministic Reconciliation Equivalence Proof (Neutral / No Customer Data)

This repository provides a public, reproducible demonstration that a deterministic reduction step can shrink the reconciliation comparison universe while preserving reconciliation outcomes.

## What this proves (non-negotiable invariants)

Given two ledgers A and B containing transactions, including injected anomalies:

1) Mismatch preservation
- Every mismatch detected on the full dataset is also detected on the reduced dataset.
- Equivalence is verified using deterministic mismatch signatures (join_key, counts, sums).

2) Aggregate invariance (correct definition)
- The aggregate mismatch delta total is identical before vs after reduction:
  mismatch_delta_total_cents = Σ(sumA_cents - sumB_cents) across all mismatch groups

3) Cryptographic verifiability
- The pipeline produces SHA-256 manifests for key inputs and outputs to support independent verification.

If any invariant fails, the proof fails.

## What this is NOT
- Not a claim about any specific bank’s data.
- Not a production integration.
- Not a probabilistic/ML approach.

## Quickstart

python scripts/generate_synthetic_data.py --out-dir data --n 100000
python scripts/run_proof.py --data-dir data --out-dir outputs
python scripts/verify_proof.py --out-dir outputs

Expected:
- outputs/equivalence_report.txt => PASS/FAIL
- outputs/sha256_manifest.txt => cryptographic manifest

## Outputs (key audit artifacts)
- outputs/full_recon_result.json
- outputs/reduced_recon_result.json
- outputs/equivalence_report.txt
- outputs/sha256_manifest.txt
- auditor_report/REM_Recon_Verification_Report.md

## 1-page “No-Data Proof” PDF (shareable)
- outputs/REM_Recon_No_Data_Proof_1pager.pdf

## License
MIT (see LICENSE)
