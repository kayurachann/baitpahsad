#!/usr/bin/env bash
# Rebuild figures, manuscript and supplementary material; export PDFs when LibreOffice is available.
set -euo pipefail
cd "$(dirname "$0")/scripts"
python3 results_data.py > /dev/null          # arithmetic / sign checks on the reported numbers
python3 make_figures.py
python3 build_manuscript.py
python3 build_supplementary.py
if command -v soffice > /dev/null; then
  soffice --headless --convert-to pdf --outdir ../manuscript ../manuscript/StegaGuard_revised.docx > /dev/null
  soffice --headless --convert-to pdf --outdir ../supplementary ../supplementary/StegaGuard_supplementary.docx > /dev/null
  command -v pdfinfo > /dev/null && pdfinfo ../manuscript/StegaGuard_revised.pdf | grep Pages
fi
