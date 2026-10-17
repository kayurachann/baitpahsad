"""Build the supplementary material (full result tables moved out of the 12-page manuscript).

Usage: python3 build_supplementary.py [LNCS template dir] [output .docx]   (defaults: templates/lncs, supplementary/StegaGuard_supplementary.docx)
"""
import shutil
import sys
from pathlib import Path

from docx_builder import Doc, prepare_template
from build_manuscript import SECT_PR, f3, ci
from results_data import MATRIX, RQ3, DETECTORS, PROTOCOLS, ALGORITHMS, FP_PER_SEED, low_fpr_summary

# tên bài theo bản nộp của nhóm (Paper_HoanChinh)
TITLE = ("StegaGuard: A Controlled Robustness Study of Lightweight Image Steganalysis under Algorithm "
         "and Payload Shift")


def build(template_src: Path, out: Path):
    work = out.parent / "_lncs_template_supp"
    prepare_template(template_src, work)
    d = Doc(work)
    d.counters["Table"] = 0
    d.para(d.runs("Supplementary Material"), "papertitle", '<w:spacing w:after="120"/>')
    d.para(d.runs(TITLE), "address", '<w:spacing w:after="240"/>')
    d.p("This supplement lists the full results that the manuscript summarizes. Unless stated otherwise, "
        "values are means over seeds 42, 43 and 44 on the same 120 test source covers; they are repeated "
        "measurements on one partition, not independent samples.")

    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            for a in ALGORITHMS:
                for b in (0.4, 0.1):
                    auc, sd, f1, ber, rec, fpr = MATRIX[(det, p, a, b)]
                    rows.append([det if (p, a, b) == ("P1", "WOW", 0.4) else "",
                                 p if (a, b) == ("WOW", 0.4) else "", a if b == 0.4 else "", f"{b:.1f}",
                                 f"{auc:.3f} ± {sd:.3f}", f"{f1:.3f}", f"{ber:.3f}", f"{rec:.3f}", f"{fpr:.3f}"])
    d.labels["tab:s1"] = ("Table", "S1")
    d.para(d.runs("**Table S1.** Detector × protocol × algorithm × payload results on the 120 test covers. "
                  "ROC-AUC is mean ± sample SD over three seeds; F1 and BER use the validation-selected "
                  "τ_{BER}; recall and FPR use the validation-selected τ_{low} (validation FPR ≤ 1%)."),
           "tablecaption", '<w:jc w:val="both"/>')
    _table(d, [1250, 330, 1000, 400, 1100, 600, 600, 760, 878],
           [["Detector", "P", "Algorithm", "bpp", "ROC-AUC", "F1", "BER", "Recall@τ_{low}", "FPR@τ_{low}"]],
           rows, group_rules=(18,), sub_rules=tuple(k for k in range(6, 36, 6) if k != 18))
    d.p("Residual-LR shows a seed SD of 0.000 under P1, consistent with P1 involving no variant sampling and a "
        "deterministic fit. The FPR column is constant within each detector and protocol because the 120 test "
        "covers are scored identically in all six stego conditions. Table S3 lists the false positives behind "
        "each rate per run.", style="p1a")

    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            for a in ALGORITHMS:
                delta, lo, hi = RQ3[(det, p, a)]
                a4, a1 = MATRIX[(det, p, a, 0.4)][0], MATRIX[(det, p, a, 0.1)][0]
                rows.append([det if (p, a) == ("P1", "WOW") else "", p if a == "WOW" else "", a, f3(a4), f3(a1),
                             f3(delta, True), ci(lo, hi)])
    d.para(d.runs("**Table S2.** Payload-shift comparisons (RQ3). ΔAUC = AUC(0.1 bpp) − AUC(0.4 bpp), paired "
                  "on the 120 test covers, with 95% paired bootstrap intervals (resampling unit: source cover; one draw shared "
                  "by the three seeds; B = 10,000; see Sect. 3.5 of the manuscript). ΔAUC is "
                  "computed from unrounded AUCs and may differ by 0.001 from the rounded columns."),
           "tablecaption", '<w:jc w:val="both"/>')
    _table(d, [1400, 400, 1200, 900, 900, 900, 1218],
           [["Detector", "P", "Algorithm", "AUC 0.4", "AUC 0.1", "ΔAUC", "95% CI"]], rows, group_rules=(9,),
           sub_rules=(3, 6, 12, 15))

    rows = []
    for r in low_fpr_summary():
        fp = FP_PER_SEED[(r["detector"], r["protocol"])]
        assert sum(fp) == r["fp_total"], (r["detector"], r["protocol"])
        rows.append([r["detector"] if r["protocol"] == "P1" else "", r["protocol"], *map(str, fp),
                     f"{sum(fp)}/360", f"{r['fpr']:.3f}"])
    d.para(d.runs("**Table S3.** Test false positives at τ_{low} per run (out of 120 test covers), counted from the "
                  "per-image test scores of each run. The observed test FPR is the total over 3 × 120 cover "
                  "evaluations."), "tablecaption", '<w:jc w:val="both"/>')
    _table(d, [1400, 400, 900, 900, 900, 1200, 1218],
           [["Detector", "P", "Seed 42", "Seed 43", "Seed 44", "Total", "Test FPR"]], rows, group_rules=(3,))
    d.para(d.runs("**Software.** All values in Tables S1-S3 and in the manuscript were reproduced from the 600 "
                  "source images with Python 3.13, NumPy 2.5.3 (OpenBLAS, Haswell kernel), SciPy 1.18.1, "
                  "scikit-learn 1.9.1, conseal 2025.11 and sealwatch 2025.9."), "p1a")
    d.save(out, SECT_PR)
    shutil.rmtree(work)
    return d


def _table(d, widths, header, rows, group_rules=(), sub_rules=()):
    """Small wrapper: booktabs table without a numbered caption (captions above are written manually)."""
    saved = d.caption
    d.caption = lambda *a, **k: None
    d.table("_", "", widths, header, rows, size=16, aligns=["left"] + ["center"] * (len(widths) - 1),
            group_rules=tuple(group_rules) + tuple(sub_rules))
    d.caption = saved


if __name__ == "__main__":
    from build_manuscript import ROOT
    tpl = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "templates" / "lncs"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "supplementary/StegaGuard_supplementary.docx"
    build(tpl, out)
    print("written", out)
