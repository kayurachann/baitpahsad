#!/usr/bin/env bash
# Rebuild the submission: figures, Paper_HoanChinh_2.docm (edited from the group's Paper_HoanChinh_1),
# supplementary material; run the checker and export PDFs when LibreOffice is available.
set -euo pipefail
cd "$(dirname "$0")/scripts"
python3 results_data.py > /dev/null          # arithmetic / sign checks on the reported numbers
python3 make_figures.py
python3 sua_hoanchinh.py ../manuscript/Paper_HoanChinh_1_goc.docm ../manuscript/Paper_HoanChinh_2.docm
python3 kiem_tra_hoanchinh.py ../manuscript/Paper_HoanChinh_2.docm
python3 build_supplementary.py
if command -v soffice > /dev/null; then
  soffice --headless --convert-to pdf --outdir ../manuscript ../manuscript/Paper_HoanChinh_2.docm > /dev/null
  soffice --headless --convert-to pdf --outdir ../supplementary ../supplementary/StegaGuard_supplementary.docx > /dev/null
  command -v pdfinfo > /dev/null && pdfinfo ../manuscript/Paper_HoanChinh_2.pdf | grep Pages
fi
