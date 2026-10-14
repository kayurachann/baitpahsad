"""Build the supplementary material (full result tables moved out of the 12-page manuscript).

Usage: python3 build_supplementary.py [LNCS template dir] [output .docx]   (defaults: templates/lncs, supplementary/StegaGuard_supplementary.docx)
"""
import shutil
import sys
from pathlib import Path

from docx_builder import Doc, prepare_template
from build_manuscript import SECT_PR, TITLE, f3, ci
from results_data import MATRIX, RQ3, DETECTORS, PROTOCOLS, ALGORITHMS, low_fpr_summary


def build(template_src: Path, out: Path):
    work = out.parent / "_lncs_template_supp"
    prepare_template(template_src, work)
    d = Doc(work)
    d.counters["Table"] = 0
    d.para(d.runs("Supplementary Material"), "papertitle", '<w:spacing w:after="120"/>')
    d.para(d.runs(TITLE), "address", '<w:spacing w:after="240"/>')
    d.p("This supplement lists the full results that the manuscript summarizes. All values are means over "
        "seeds 42, 43 and 44 on the same 120 test source covers; they are repeated measurements on one "
        "partition, not independent samples.")

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
    _table(d, [1250, 330, 1100, 400, 1150, 600, 600, 760, 728],
           [["Detector", "P", "Algorithm", "bpp", "ROC-AUC", "F1", "BER", "Recall@τ_{low}", "FPR@τ_{low}"]],
           rows, group_rules=(18,), sub_rules=tuple(k for k in range(6, 36, 6) if k != 18))
    d.p("Residual-LR shows a seed SD of 0.000 under P1 because P1 involves no variant sampling and the "
        "logistic regression fit is deterministic. The FPR column is constant within each detector and "
        "protocol because the 120 test covers are scored identically in all six stego conditions. Multiplying "
        "the FPR by 3 × 120 gives the false-positive totals of the manuscript (e.g. 0.042 → 15/360); the "
        "per-seed counts must be read from the stored score files.", style="p1a")

    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            for a in ALGORITHMS:
                delta, lo, hi = RQ3[(det, p, a)]
                a4, a1 = MATRIX[(det, p, a, 0.4)][0], MATRIX[(det, p, a, 0.1)][0]
                rows.append([det if (p, a) == ("P1", "WOW") else "", p if a == "WOW" else "", a, f3(a4), f3(a1),
                             f3(delta, True), ci(lo, hi)])
    d.para(d.runs("**Table S2.** Payload-shift comparisons (RQ3). ΔAUC = AUC(0.1 bpp) − AUC(0.4 bpp), paired "
                  "on the 120 test covers, with 95% paired bootstrap intervals (resampling unit: source cover)."),
           "tablecaption", '<w:jc w:val="both"/>')
    _table(d, [1400, 400, 1200, 900, 900, 900, 1218],
           [["Detector", "P", "Algorithm", "AUC 0.4", "AUC 0.1", "ΔAUC", "95% CI"]], rows, group_rules=(9,),
           sub_rules=(3, 6, 12, 15))

    rows = [[r["detector"] if r["protocol"] == "P1" else "", r["protocol"], f"{r['fpr']:.3f}",
             f"{r['fp_total']}/360", f"{r['fp_total'] / 3:.2f}"] for r in low_fpr_summary()]
    d.para(d.runs("**Table S3.** False-positive counts implied by the reported mean test FPR at τ_{low}. Each "
                  "count is the unique integer k with k/360 rounding to the reported FPR; per-seed values "
                  "must be confirmed from the score files."), "tablecaption", '<w:jc w:val="both"/>')
    _table(d, [1700, 500, 1500, 1500, 1700],
           [["Detector", "P", "Mean test FPR", "False positives (3 seeds)", "Mean per run (of 120)"]], rows,
           group_rules=(3,))
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
