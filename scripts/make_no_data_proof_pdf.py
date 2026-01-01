from __future__ import annotations
import argparse
import os
from datetime import datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/REM_Recon_No_Data_Proof_1pager.pdf")
    ap.add_argument("--repo", default="rem-recon-deterministic-equivalence-proof")
    args = ap.parse_args()

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
    except Exception as e:
        raise SystemExit(
            "reportlab is required. Install with: pip install reportlab\n"
            f"Original error: {e}"
        )

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter

    margin = 0.75 * inch
    x = margin
    y = height - margin

    def line(text, size=11, gap=14, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, text)
        y -= gap

    # Header
    line("REM-Recon™ — Deterministic Reconciliation Cost Reduction", size=16, gap=20, bold=True)
    line("Public, reproducible proof — no customer data required", size=12, gap=18)

    y -= 6
    c.line(x, y, width - margin, y)
    y -= 18

    # Problem
    line("Problem", size=12, gap=16, bold=True)
    line("Banks and processors reconcile by comparing enormous transaction universes to avoid audit risk.", size=11, gap=14)
    line("This brute-force approach drives recurring OPEX, long cycle times, and exception backlogs.", size=11, gap=18)

    # Claim
    line("Claim", size=12, gap=16, bold=True)
    line("REM-Recon reduces reconciliation workload by shrinking the comparison universe", size=11, gap=14)
    line("without excluding any recon-relevant mismatches — proven deterministically.", size=11, gap=18)

    # Proof
    line("Proof (independent verification)", size=12, gap=16, bold=True)
    line("We publish an end-to-end reproducible proof using synthetic, financially realistic ledgers:", size=11, gap=14)
    line("• Reconciliation on full dataset vs reduced candidate dataset", size=11, gap=14)
    line("• Identical mismatch signatures (join_key, counts, sums)", size=11, gap=14)
    line("• Identical aggregate mismatch delta total", size=11, gap=14)
    line("• SHA-256 manifests for cryptographic verification", size=11, gap=18)

    # Safety
    line("Safety / Risk Controls", size=12, gap=16, bold=True)
    line("• No production access required", size=11, gap=14)
    line("• Tokenized historical files acceptable (no PII required)", size=11, gap=14)
    line("• Read-only processing; no system replacement", size=11, gap=18)

    # What you get
    line("What you receive in a pilot", size=12, gap=16, bold=True)
    line("• Before/after metrics: candidate breaks, cycle time, workload estimate", size=11, gap=14)
    line("• Reconciliation equivalence report (PASS/FAIL)", size=11, gap=14)
    line("• SHA-256 verification manifest for audit", size=11, gap=18)

    # Ask
    line("What we ask (minimal)", size=12, gap=16, bold=True)
    line("One historical reconciliation batch export (CSV/Parquet/fixed-width), tokenized if preferred.", size=11, gap=14)
    line("If equivalence fails, we stop.", size=11, gap=18)

    # Footer
    y = margin
    c.setFont("Helvetica", 9)
    c.drawString(x, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Repo: {args.repo}")
    c.drawRightString(width - margin, y, "© 2026 REM — Confidential until published")

    c.showPage()
    c.save()
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
