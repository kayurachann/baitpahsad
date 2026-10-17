"""Build the revised StegaGuard manuscript (Springer LNCS layout of PaperID 581).

Usage: python3 build_manuscript.py [LNCS template dir] [output .docx]   (defaults: templates/lncs, manuscript/StegaGuard_revised.docx)
"""
import sys
from pathlib import Path

from docx_builder import Doc, prepare_template, mr, mfrac, msub, mparen
from results_data import MATRIX, RQ1, RQ2, RQ3, DETECTORS, PROTOCOLS, ALGORITHMS, low_fpr_summary
from references import REFERENCES
from related_work import write_related_work, write_discussion

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
SECT_PR = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838" w:code="9"/>'
           '<w:pgMar w:top="2948" w:right="2494" w:bottom="2948" w:left="2494" w:header="2381" '
           'w:footer="2324" w:gutter="0"/><w:cols w:space="227"/><w:titlePg/><w:docGrid w:linePitch="240"/>'
           '</w:sectPr>')

TITLE = ("StegaGuard: A Controlled Robustness Study of Feature-Based Image Steganalysis under Algorithm "
         "and Payload Shift")
AUTHORS = [("Quoc Hung NGUYEN", "*[0000-0002-6363-0160]"), ("Minh Tri HUYNH", "[0009-0004-4214-6355]"),
           ("Phu NGUYEN", "[0009-0004-7291-9072]"), ("Huu Minh Tri NGUYEN", "[0009-0002-8275-4326]"),
           ("Duong Gia Bao NGUYEN", "[0009-0009-3717-2424]"), ("Huu Loc TRAN", "[0009-0004-0634-0310]")]

ABSTRACT = (
    "**Abstract.** Steganalysis detectors are trained on known embedding algorithms and payloads, but an "
    "adversary can change both. StegaGuard is a controlled robustness study of two existing feature-based "
    "detectors: Residual-LR (76 residual statistics, logistic regression) and SRM+Ensemble (34,671 Spatial "
    "Rich Model features, Fisher linear discriminant ensemble). We split 600 BOSSbase 1.01 covers, resized "
    "to 256 × 256, into 360 training, 120 validation and 120 test covers before embedding them with WOW, "
    "S-UNIWARD and HILL at 0.1 and 0.4 bpp, so every stego variant stays in the partition of its source "
    "cover. Three training protocols of 360 cover–stego pairs were run with three seeds, and paired "
    "differences were assessed by a bootstrap over test covers. Trained on WOW at 0.4 bpp, SRM+Ensemble "
    "reached an AUC of 0.714 on matched WOW and 0.645 on unseen HILL (ΔAUC = −0.070, 95% CI [−0.093, "
    "−0.046]). Adding 0.1 bpp variants to a WOW/S-UNIWARD training pool gave SRM+Ensemble no reliable "
    "change on unseen HILL (ΔAUC = −0.022, 95% CI [−0.050, +0.005]). AUC at 0.1 bpp was lower than at "
    "0.4 bpp in all 18 comparisons (ΔAUC −0.022 to −0.183). At thresholds set for a validation "
    "false-positive rate (FPR) of at most 1%, mean recall was 0.062 for Residual-LR and 0.080 for "
    "SRM+Ensemble at mean test FPRs of 0.045 and 0.034, so neither detector operated reliably at a 1% "
    "false-alarm budget on this resized BOSSbase subset.")

KEYWORDS = ("**Keywords:** Image Steganalysis, Robustness Evaluation, Algorithm Mismatch, Payload Mismatch, "
            "Spatial Rich Model, Low False-Positive Rate.")


def f3(x, sign=False):
    if round(x, 3) == 0:
        return "0.000"   # không viết +0.000 / −0.000
    s = f"{x:+.3f}" if sign else f"{x:.3f}"
    return s.replace("-", "−")


def ci(lo, hi):
    return f"[{f3(lo, True)}, {f3(hi, True)}]"


# ====================================================================== front matter + Sect. 1
def front_matter(d):
    d.para(d.runs(TITLE), "papertitle", '<w:spacing w:after="240"/>')
    xml = []
    for k, (name, orcid) in enumerate(AUTHORS):
        xml.append(d.runs(name + " "))
        xml.append(f'<w:r><w:rPr><w:rStyle w:val="ORCID"/></w:rPr>{d.t(orcid)}</w:r>')
        if k < len(AUTHORS) - 1:
            xml.append(d.runs(", "))
    d.para("".join(xml), "author", '<w:spacing w:after="120"/>')
    d.para(d.runs("University of Economics Ho Chi Minh City (UEH), Ho Chi Minh City, Vietnam"), "address",
           '<w:spacing w:after="60"/>')
    d.para(d.runs("Corresponding author: hungngq@ueh.edu.vn", font="Courier New"), "address")
    d.para(d.runs(ABSTRACT), "abstract", '<w:spacing w:before="360" w:after="120"/><w:ind w:firstLine="0"/>')
    d.para(d.runs(KEYWORDS), "keywords", '<w:spacing w:before="120" w:after="0"/>')


FIG1_POS = "intro_mid"


def fig1(d):
    d.figure("fig:pipeline", FIG / "fig1_pipeline.png", 4.8,
             "StegaGuard evaluation pipeline. Both detectors are trained on the same splits, protocols and "
             "seeds, and every model is scored on the same 120 test covers.")


def introduction(d):
    d.h1("Introduction")
    d.p("Image steganography hides a message by making small changes to a cover image. Current spatial-domain "
        "schemes such as WOW, S-UNIWARD and HILL assign a distortion cost to every pixel and use "
        "syndrome-trellis coding, or a simulation of it, to place most changes in textured regions that are "
        "hard to model \\cite{stc,wow,uniward,hill}. Steganalysis detectors either train a classifier on "
        "statistics of noise residuals, such as SPAM or the Spatial Rich Model (SRM) \\cite{spam,srm,ens}, or "
        "train a convolutional neural network (CNN) such as Yedroudj-Net or SRNet \\cite{yedroudj,srnet}.")
    d.p("In a security setting the detector does not choose its test data: a defender trains on a few "
        "algorithms at known payloads, while an adversary may use an unseen algorithm or a shorter message. "
        "The operating point matters as well: a "
        "screening system inspects many innocent images, so what counts is the share of stego images caught "
        "when the false-positive rate (FPR) is held near 1%, not only the area under the ROC curve (AUC).")
    d.p("Both issues are known, but they are usually studied one at a time. Work on cover-source mismatch "
        "changes where the images come from \\cite{csm,giboulot,mallet}, work on stego-source mismatch "
        "changes the embedding method \\cite{butora19,wang25}, and papers that introduce detectors mostly "
        "train and test on the same algorithm and payload \\cite{srm,yedroudj,srnet}. Two design choices can "
        "also bias robustness claims: splitting after embedding lets variants of one cover fall on both sides "
        "and inflate test scores, and a detector that is weak in the matched condition says little about the "
        "shift itself.")
    d.p("The gap has two parts. For the detector, it is unclear how much a standard SRM+Ensemble loses on a "
        "small, resized BOSSbase subset when the algorithm or payload changes, and whether mixing algorithms "
        "and payloads in training reduces the loss. For the evaluation, few shift studies combine a source-cover split fixed before embedding, a matched-condition reference, "
        "paired intervals on identical test covers and an explicit low-FPR operating point. StegaGuard "
        "({fig:pipeline}) addresses the second part to answer the first; it evaluates two existing detectors "
        "and proposes no new detection algorithm. Three questions guide the study:")
    if FIG1_POS == "intro_mid":
        fig1(d)
    d.bullets([
        "**RQ1 (unseen algorithm).** Under protocol P1, which trains on WOW at 0.4 bits per pixel (bpp), how does "
        "detection of "
        "unseen HILL at 0.4 bpp compare with detection of matched WOW at 0.4 bpp on the same test covers?",
        "**RQ2 (mixed training).** With training size fixed at 360 cover–stego pairs, does adding 0.1 bpp "
        "variants to a WOW/S-UNIWARD training pool (P3 versus P2) improve detection of unseen HILL at 0.4 bpp?",
        "**RQ3 (payload shift).** For each detector, protocol and algorithm, how much does detection change "
        "when the payload falls from 0.4 to 0.1 bpp?",
    ])
    d.runin("Contributions.", "(i) A controlled evaluation in which both detectors share covers, training "
            "size, seeds and test images, so that differences between protocols P1–P3 trace back to the "
            "training pool. (ii) Source-cover leakage prevention: the split is fixed before embedding and "
            "audited against a hashed manifest. (iii) A robustness assessment of algorithm and payload shift and "
            "of mixed training with paired ΔAUC and bootstrap intervals over test covers. (iv) A security "
            "operating-point analysis that separates the validation-selected threshold from the FPR observed "
            "on test covers.")
    if FIG1_POS == "intro":
        fig1(d)


# ====================================================================== Sect. 3
def methodology(d):
    d.h1("Methodology")
    d.p("{fig:pipeline} summarizes the pipeline. Stages 1–3 build a leakage-controlled dataset, stages 4–5 "
        "train the two detectors in parallel under protocols P1–P3, and stages 6–7 evaluate every trained "
        "model on one fixed set of test covers.")
    if FIG1_POS == "method":
        fig1(d)

    d.h2("Dataset Preparation and Leakage Prevention")
    d.p("BOSSbase 1.01 contains 10,000 grayscale images of 512 × 512 pixels \\cite{boss}. We drew 600 of them "
        "(6%) with the fixed seed 20260918 and downsampled each to 256 × 256 before embedding, as several CNN "
        "studies do \\cite{yedroudj,srnet}. Resizing alters cover noise "
        "statistics, so our numbers are not comparable with results at 512 × 512.")
    d.p("Leakage is prevented by the order of operations. The 600 source covers were first assigned to "
        "training (360), validation (120) and test (120). Only then was each cover embedded with WOW "
        "\\cite{wow}, S-UNIWARD \\cite{uniward} and HILL \\cite{hill} at 0.1 and 0.4 bpp, giving six variants "
        "per cover: 600 stego images per algorithm–payload condition, 3,600 in total and 4,200 PNG files with "
        "the covers. Training, validation and test hold 2,160, 720 and 720 stego images (360, 120 and 120 per "
        "condition). Each stego file inherits the cover_id and split of its source, so a cover and its six "
        "variants always share a partition. The manifest records cover_id, split, algorithm, payload, "
        "embedding seed and SHA-256 hash; a manifest audit confirmed that every stego variant stays in the "
        "partition of its source cover (manifest SHA-256 13c01ca9…2799e8c).")

    d.h2("Feature Extraction and Detectors")
    d.p("Both detectors output a score, higher for stego, that is used for every metric; "
        "{tab:detectors} summarizes their configuration. Residual-LR, the lightweight baseline, describes each "
        "image by 76 statistics of its noise residuals and classifies them with scikit-learn logistic "
        "regression \\cite{sklearn}. SRM+Ensemble, the established reference, extracts the 106 SRM submodels "
        "(34,671 features) \\cite{srm} with the sealwatch library \\cite{sealwatch} and trains the FLD "
        "ensemble of \\cite{ens} with L = 50 base learners and random feature subspaces of dimension "
        "d_{sub} = 500. Both detectors keep the same settings in every protocol and seed, so the configuration "
        "cannot explain differences between protocols.")
    d.table("tab:detectors", "Detector configuration.",
            [1650, 2634, 2634],
            [["Setting", "Residual-LR", "SRM+Ensemble"]],
            [["Features", "76 residual statistics", "SRM: 106 submodels, 34,671 dimensions"],
             ["Classifier", "logistic regression (scikit-learn)", "FLD ensemble, L = 50, d_{sub} = 500"],
             ["Training data per run", "360 cover–stego pairs", "360 cover–stego pairs"],
             ["Seed-dependent parts", "variant sampling (P2, P3); random parts of model fitting",
              "variant sampling (P2, P3); random parts of model fitting"]],
            aligns=["left", "left", "left"])

    d.h2("Experimental Protocols")
    d.p("The protocols in {tab:protocols} differ only in the stego variant attached to each of the 360 "
        "training covers. For every training cover and seed, one variant is sampled from the protocol's pool, "
        "so each run sees 360 cover–stego pairs built from the same 360 covers; P1 involves no sampling. "
        "Validation images serve only to set thresholds. HILL is never used for model fitting or threshold "
        "selection, and S-UNIWARD is unseen under P1. Seeds 42, 43 and 44 "
        "control the variant draws and the random parts of model fitting.")
    d.table("tab:protocols", "Training protocols. All share the same 360 training, 120 validation and 120 "
            "test covers; every model is tested on all six conditions (3 algorithms × 2 payloads).",
            [600, 2500, 1050, 2768],
            [["P", "Training stego pool", "Variants in pool", "Role"]],
            [["P1", "WOW 0.4 bpp", "1", "RQ1 (WOW 0.4 matched, HILL 0.4 unseen); RQ3"],
             ["P2", "WOW and S-UNIWARD at 0.4 bpp", "2", "RQ2 reference; RQ3"],
             ["P3", "WOW and S-UNIWARD at 0.1 and 0.4 bpp", "4", "RQ2 (P3 − P2 on HILL 0.4); RQ3"]],
            aligns=["center", "left", "left", "left"])
    d.p("RQ1 uses P1 because it trains on WOW 0.4 alone, so WOW 0.4 is matched and HILL 0.4 unseen for the "
        "same model. P2 and P3 differ only in the 0.1 bpp variants, which RQ2 isolates. "
        "In every comparison both conditions are scored on the same 120 test covers.")

    d.h2("Evaluation Metrics")
    d.p("For each run and test condition a detector produces 240 scores (120 test covers and their 120 stego "
        "variants), from which ROC-AUC is computed. Two thresholds are fixed from validation scores alone, "
        "never from test labels. The first, τ_{BER}, is the balanced-error point on the validation scores, with "
        "BER = (FPR + P_{MD})/2 and P_{MD} the missed-detection rate; F1 = 2·Prec·Rec/(Prec + Rec) and BER are "
        "reported on test at this threshold. The second, τ_{low}, defines the security operating point. It is "
        "set on the set V of 120 validation covers so that, with s(c) the score of cover c,")
    d.equation(msub(mr("FPR"), mr("V", False)) + mparen(msub(mr("τ"), mr("low", True))) + mr("=", True) +
               mfrac(mparen(mparen(mr("c") + mr("∈", True) + mr("V") + mr(" : ", True) + mr("s") +
                                   mparen(mr("c")) + mr("≥", True) + msub(mr("τ"), mr("low", True)), "{", "}"),
                            "|", "|"), mparen(mr("V"), "|", "|")) +
               mr("≤", True) + mr("0.01", True), 1)
    d.p("With |V| = 120, this allows at most one validation false positive (0.83%). At τ_{low} we report "
        "recall, the share of the 120 test stego images with s ≥ τ_{low}, and the observed test FPR, the share "
        "of the 120 test covers with s ≥ τ_{low}. The first is the quantity of security interest; the second "
        "shows whether the 1% target transfers from validation to test, which Eq. (1) does not guarantee.",
        style="p1a")

    d.h2("Statistical Analysis and Reproducibility")
    d.p("Each comparison is a paired difference ΔAUC = AUC(shifted) − AUC(reference): HILL 0.4 minus WOW 0.4 "
        "under P1 (RQ1), P3 minus P2 on HILL 0.4 (RQ2), and 0.1 minus 0.4 bpp for each detector, protocol and "
        "algorithm (RQ3, 18 comparisons). Negative values mean a loss under the shift. The point estimate is the "
        "mean of the three per-seed differences, which equals the difference of the unrounded seed-mean AUCs "
        "(rounded table values may differ by 0.001). Its 95% interval comes from a paired bootstrap in which the "
        "resampling unit is the source test cover: each replicate draws 120 test cover IDs with replacement, "
        "and a drawn cover brings all of its cover and stego scores under both compared conditions, so the "
        "pairing is preserved.")
    d.p("Seed standard deviations (at most 0.028, Supplementary Table S1) describe training randomness on "
        "fixed data; the bootstrap describes the sampling of test covers given the trained models. Neither "
        "reflects a different choice of covers or split, so the intervals are conditional on this partition. A direction is called supported only when its interval excludes zero; an interval "
        "containing zero is inconclusive, not evidence of equivalence. The 18 RQ3 intervals are not adjusted "
        "for multiplicity. Every run stores its per-image prediction scores, and the manifest stores the "
        "embedding seed and SHA-256 hash of every image, so all tables can be recomputed from the saved "
        "files.")


# ====================================================================== Sect. 4
def results(d):
    d.h1("Results and Discussion")
    d.h2("Overall Detection Performance")
    d.p("{tab:auc} gives the ROC-AUC for every detector, protocol and test condition; F1, BER, recall and seed "
        "standard deviations are in Supplementary Table S1. All cells share the 120 test covers, so they are "
        "paired observations, not independent experiments. Residual-LR stays close to chance, with AUC of 0.500–0.570 and BER of at least 0.438. SRM+Ensemble "
        "separates covers from stego at 0.4 bpp (AUC 0.632–0.717, BER 0.347–0.400) but hardly at 0.1 bpp "
        "(0.517–0.550). As Residual-LR fails even in the matched condition, SRM+Ensemble carries the main "
        "evidence for the research questions.")
    hdr1 = ["Detector", "P", ("WOW", 2), ("S-UNIWARD", 2), ("HILL", 2)]
    hdr2 = ["", "", "0.4", "0.1", "0.4", "0.1", "0.4", "0.1"]
    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            r = [det if p == "P1" else "", p]
            for a in ALGORITHMS:
                for b in (0.4, 0.1):
                    cell = f"{MATRIX[(det, p, a, b)][0]:.3f}"
                    r.append(f"**{cell}**" if (p, a, b) == ("P1", "WOW", 0.4) else cell)
            rows.append(r)
    d.table("tab:auc", "ROC-AUC (mean over seeds 42–44) on the 120 test covers at 0.4 and 0.1 bpp. Bold: the "
            "matched condition of P1. HILL is unseen under all protocols; S-UNIWARD is unseen under P1.",
            [1350, 400, 861, 861, 861, 861, 861, 863], [hdr1, hdr2], rows, size=17,
            aligns=["left", "center"] + ["center"] * 6, group_rules=(3,))

    d.h2("RQ1: Unseen Embedding Algorithm")
    s, r = RQ1["SRM+Ensemble"], RQ1["Residual-LR"]
    d.p(f"Under P1, SRM+Ensemble falls from {f3(s[0])} on matched WOW 0.4 to {f3(s[1])} on unseen HILL 0.4 "
        f"({tab_ref('tab:rq12')}); the interval of the paired ΔAUC excludes zero, and BER rises from 0.347 to "
        f"0.386. For Residual-LR the difference is {f3(r[2], True)} {ci(*r[3])}, but with a matched AUC of only "
        f"{f3(r[0])} the matched signal is too weak to serve as a reference for a shift.")
    d.p("This loss need not be a pure effect of algorithm mismatch. HILL was designed to be harder to detect than "
        "WOW with rich-model features \\cite{hill}, so part of the gap may reflect its intrinsic difficulty; the "
        "P1 ordering WOW 0.714 > S-UNIWARD 0.689 > HILL 0.645 fits both explanations. Separating them needs a "
        "matched HILL reference (trained and tested on HILL), which this study did not run.")
    d.runin("Answer to RQ1.", "On this subset, SRM+Ensemble trained on WOW at 0.4 bpp detects unseen HILL at "
            "0.4 bpp less well than matched WOW on the same test covers (ΔAUC = −0.070, 95% CI [−0.093, "
            "−0.046]). This is a measured degradation under the tested shift; it does not establish "
            "robustness, or a general lack of it, for other algorithms, payloads or cover sources.")
    rows = []
    for name, rq, title in (("RQ1", RQ1, "RQ1: matched WOW 0.4 → unseen HILL 0.4, both under P1"),
                            ("RQ2", RQ2, "RQ2: P2 → P3, both tested on unseen HILL 0.4")):
        rows.append({"group": title})
        for det in DETECTORS:
            a, b, dd, (lo, hi) = rq[det]
            if det == "Residual-LR" and name == "RQ1":
                reading = "Weak matched signal"
            else:
                reading = "Loss, CI excludes 0" if hi < 0 else "Inconclusive"
            rows.append([det, f3(a), f3(b), f3(dd, True), ci(lo, hi), reading])
    d.table("tab:rq12", "Paired comparisons for RQ1 and RQ2 on the same 120 test covers. ΔAUC is computed "
            "from unrounded scores and may differ by 0.001 from the difference of the rounded AUCs.",
            [1400, 1000, 1000, 900, 1350, 1268],
            [["Detector", "Reference AUC", "Shifted AUC", "ΔAUC", "95% CI", "Reading"]], rows, size=17,
            aligns=["left", "center", "center", "center", "center", "left"], group_rules=(3,))
    d.h2("RQ2: Mixed Training")
    s, r = RQ2["SRM+Ensemble"], RQ2["Residual-LR"]
    d.p("P3 adds 0.1 bpp WOW and S-UNIWARD variants to the P2 pool at the same 360 pairs, so fewer training "
        "pairs carry the stronger 0.4 bpp signal. On unseen "
        f"HILL 0.4, SRM+Ensemble scores {f3(s[0])} under P2 and {f3(s[1])} under P3 (ΔAUC = {f3(s[2], True)}, "
        f"95% CI {ci(*s[3])}); for Residual-LR the difference is {f3(r[2], True)} {ci(*r[3])}. Both "
        "intervals include zero, so the data show neither an improvement nor equivalence of the two "
        "protocols. For SRM+Ensemble the point estimates also fall on matched 0.4 bpp conditions (WOW 0.713 → "
        "0.686, S-UNIWARD 0.717 → 0.677), and AUC at 0.1 bpp does not rise although 0.1 bpp is now trained on. "
        "One untested explanation is that, at fixed size, weak 0.1 bpp examples dilute the 0.4 bpp "
        "signal.")
    d.runin("Answer to RQ2.", "No reliable improvement was observed under the evaluated mixed-training "
            "protocol. This holds for WOW and S-UNIWARD as training algorithms, two payloads, 360 training "
            "pairs and this dataset; larger or differently weighted mixed training sets remain untested.")

    d.h2("RQ3: Payload Shift")
    d.p("{fig:rq3} shows ΔAUC between 0.1 and 0.4 bpp for all 18 comparisons, and {tab:rq3} summarizes them per "
        "detector and protocol; Supplementary Table S2 lists every interval. All 18 differences are negative "
        "and all 18 intervals lie below zero. The SRM+Ensemble losses are about three times those of "
        "Residual-LR, and one Residual-LR interval ends at −0.001 (P3 WOW). As the intervals are unadjusted and share covers and models, the common sign "
        "is not 18 independent confirmations.")
    d.figure("fig:rq3", FIG / "fig2_payload_shift.png", 4.46,
             "Payload shift for (a) Residual-LR and (b) SRM+Ensemble: seed-mean ΔAUC = AUC(0.1 bpp) − "
             "AUC(0.4 bpp) with 95% paired bootstrap intervals. Under P1 and P2 the 0.1 bpp payload is absent "
             "from training; under P3 it is included.")
    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            ds = [RQ3[(det, p, a)] for a in ALGORITHMS]
            a01 = [MATRIX[(det, p, a, 0.1)][0] for a in ALGORITHMS]
            deltas = [x[0] for x in ds]
            rows.append([det if p == "P1" else "", p, f"{f3(min(a01))}–{f3(max(a01))}",
                         f"{f3(min(deltas), True)} to {f3(max(deltas), True)}",
                         f3(sum(deltas) / 3, True), f3(max(x[2] for x in ds), True),
                         f"{sum(1 for x in ds if x[2] < 0)}/3"])
    d.table("tab:rq3", "RQ3 summary over the three algorithms, ΔAUC = AUC(0.1 bpp) − AUC(0.4 bpp), computed "
            "from unrounded AUCs.",
            [1350, 400, 1150, 1350, 900, 1000, 768],
            [["Detector", "P", "AUC at 0.1 bpp", "ΔAUC range", "Mean ΔAUC", "Highest CI upper bound",
              "CIs < 0"]], rows, size=17,
            aligns=["left", "center", "center", "center", "center", "center", "center"], group_rules=(3,))
    d.runin("Answer to RQ3.", "Lowering the payload from 0.4 to 0.1 bpp lowered the AUC point estimate in all "
            "18 combinations. The loss is clear for SRM+Ensemble, whose AUC of 0.517–0.550 at 0.1 bpp leaves "
            "little usable signal, whereas the weakest Residual-LR intervals end close to zero. "
            "The loss persists under P3, whose pool contains 0.1 bpp examples, so at 360 pairs training on the "
            "lower payload did not offset the weaker signal. The finding is limited to the three algorithms, "
            "two payloads and image size studied.")

    d.h2("Security Operating Point at Low FPR")
    d.p("{tab:lowfpr} reports the operating point of Eq. (1). The threshold allows at most one false positive "
        "among the 120 validation covers, yet on test covers every detector–protocol cell exceeds the 1% "
        "target, with observed FPRs of 0.022–0.053. Residual-LR under P1 has 15 false positives in 360 test "
        "cover evaluations; if its three runs are identical, as its zero seed spread suggests, that is 5/120 per "
        "run, whose exact 95% Clopper–Pearson interval, [1.4%, 9.5%], excludes 1%. A likely reason is that a 1% "
        "target on 120 covers places τ_{low} among the one or two highest validation scores, an extreme order "
        "statistic that varies strongly between samples. The least strict threshold allowed, just above the "
        "second-highest score, is exceeded by an exchangeable test cover with probability 2/121 ≈ 1.7%.")
    rows = []
    for r_ in low_fpr_summary():
        fp = r_["fp_total"]
        rows.append([r_["detector"] if r_["protocol"] == "P1" else "", r_["protocol"], f"{fp}/360",
                     f"{r_['fpr']:.3f}", f"{r_['recall_mean']:.3f}", f"{r_['recall_min']:.3f}–{r_['recall_max']:.3f}"])
    rows.append({"group": "Pooled: Residual-LR 49/1,080 (FPR 0.045, mean recall 0.062); SRM+Ensemble 37/1,080 "
                          "(FPR 0.034, mean recall 0.080)"})
    d.table("tab:lowfpr", "Operating point at τ_{low} (validation FPR ≤ 1%). False positives over seeds 42–44 "
            "(3 × 120 test covers) are implied by the reported mean test FPR (Suppl. Table S3); recall is the "
            "mean and range over the six test conditions.",
            [1450, 400, 1300, 1300, 1150, 1318],
            [["Detector", "P", "Test false positives", "Observed test FPR", "Mean recall", "Recall range"]],
            rows, size=17, aligns=["left", "center", "center", "center", "center", "center"], group_rules=(3, 6))
    d.p("Even the best cell, SRM+Ensemble on matched WOW 0.4 under P1, reached a recall of only 0.189 at a "
        "test FPR of 0.050. Each detector has 54 evaluation "
        "rows (3 protocols × 3 seeds × 6 conditions); in none of them were recall and FPR both zero, so the "
        "detectors were never completely silent. The rows hold 6,480 stego scores per detector, but these come "
        "from 720 distinct test stego images of 120 source covers and are repeated measurements, not 6,480 "
        "independent samples. The detectors thus did not demonstrate reliable operation at FPR ≤ 1%, and the "
        "results do not support deployment in an operational screening system.", style="p1a")

    d.h2("Discussion and Security Implications")
    write_discussion(d)


def tab_ref(key):
    return "{" + key + "}"


# ====================================================================== Sect. 5
def conclusion(d):
    d.h1("Conclusion")
    d.p("With the source-cover split fixed before embedding, the three research questions received different "
        "answers. For RQ1, SRM+Ensemble trained on WOW at 0.4 bpp detected unseen HILL less well than matched "
        "WOW (ΔAUC = −0.070, 95% CI [−0.093, −0.046]), although this loss cannot be separated from HILL "
        "being harder to detect. For RQ2, adding 0.1 bpp variants to the training pool gave no reliable "
        "improvement on unseen HILL. For RQ3, all 18 comparisons showed lower AUC at 0.1 than at 0.4 bpp, and "
        "SRM+Ensemble came close to chance at the lower payload.")
    d.p("These conclusions are limited to 600 BOSSbase covers resized to 256 × 256 and to two feature-based "
        "detectors, one of them close to chance. The 1% operating point was calibrated on 120 validation "
        "covers and was not met on test covers, and no cross-source data were evaluated.")
    d.p("Future work will use the full BOSSbase at its original resolution, add stronger detectors such as "
        "SRNet under the same split, include a matched HILL reference and test cover-source shift. StegaGuard "
        "is a controlled evaluation study rather than a new detector, and the results do not indicate readiness for "
        "deployment.")


def references(d):
    d.para(d.runs("References"), "heading1", '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>')
    for key in d.cite_order:
        d.para(d.runs(REFERENCES[key]), "referenceitem", '<w:spacing w:before="0" w:after="0"/><w:jc w:val="left"/>')


def build(template_src: Path, out: Path):
    work = out.parent / "_lncs_template"
    prepare_template(template_src, work)
    d = Doc(work)
    for k in ["tab:related", "tab:detectors", "tab:protocols", "tab:auc", "tab:rq12", "tab:rq3", "tab:lowfpr"]:
        d.reserve("Table", k)
    for k in ["fig:pipeline", "fig:rq3"]:
        d.reserve("Figure", k)
    front_matter(d)
    introduction(d)
    write_related_work(d)
    methodology(d)
    results(d)
    conclusion(d)
    references(d)
    d.save(out, SECT_PR)
    import shutil
    shutil.rmtree(work)
    return d, sorted(set(REFERENCES) - set(d.cite_order))


if __name__ == "__main__":
    tpl = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "templates" / "lncs"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "manuscript/StegaGuard_revised.docx"
    doc, unused = build(tpl, out)
    print("written", out)
    print("references cited:", len(doc.cite_order), "unused:", unused)
    print("placeholders:", len(doc.placeholders))
