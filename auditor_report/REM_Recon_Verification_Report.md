# REM-Recon Verification Report (Auditor-Readable)

## 1. Scope
This report verifies that the REM-Recon deterministic reduction process preserves reconciliation correctness and completeness for a reproducible, synthetic two-ledger dataset.

## 2. What Was Tested
- Synthetic ledgers A and B generated with realistic transaction fields.
- Known anomalies injected (duplicates, missing counterpart, amount mismatch, timing drift).
- Reconciliation performed on:
  (a) full datasets
  (b) reduced candidate datasets produced deterministically
- Results compared for equivalence.

## 3. Verification Criteria (Pass/Fail)
A test run PASSES if all criteria hold:

1) Mismatch Preservation
- All mismatches detected on full data are present in reduced-data results.
- No mismatch type is hidden by reduction.

2) Aggregate Invariance
- Aggregate totals and net flows computed by the reconciliation logic match exactly.

3) Cryptographic Verifiability
- SHA-256 hashes are produced for key inputs and outputs.

## 4. Independent Reproducibility
Any third party can reproduce the results by running:

- scripts/generate_synthetic_data.py
- scripts/run_proof.py
- scripts/verify_proof.py

No external data or credentials are required.

## 5. Audit Conclusion
If `outputs/equivalence_report.txt` indicates PASS and hashes are present in `outputs/sha256_manifest.txt`,
then the reduced dataset is reconciliation-equivalent to the full dataset for the included test definitions.
