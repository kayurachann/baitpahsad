"""Section 2 (Related Work) and Section 4.6 (Discussion) of the revised manuscript.

Statements about prior studies are limited to facts confirmed from the papers themselves
(see docs/reference_verification.md).
"""


def write_related_work(d):
    d.h1("Related Work")
    d.h2("Image Steganalysis Techniques")
    d.p("Content-adaptive embedding places changes where the cover is noisy. WOW derives its costs from "
        "directional wavelet residuals, S-UNIWARD from the relative change of a wavelet decomposition, and "
        "HILL from a high-pass residual smoothed by low-pass filters \\cite{wow,uniward,hill}. Because the "
        "three cost functions favor different structures, a detector trained on one algorithm meets a partly "
        "different change pattern when tested on another. Feature-based steganalysis models the noise "
        "residual: SPAM uses Markov transition probabilities of pixel differences \\cite{spam}, and SRM gathers "
        "co-occurrences of many linear and non-linear residuals into 34,671 features \\cite{srm}, usually "
        "classified by the Fisher linear discriminant (FLD) ensemble, which handles this dimension through "
        "random subspaces and bagging \\cite{ens}. CNN detectors such as Yedroudj-Net and SRNet report lower "
        "error than SRM with the ensemble in most tested BOSSbase-derived settings, at a higher training cost "
        "\\cite{yedroudj,srnet}.")
    d.h2("Robustness under Algorithm and Payload Shifts")
    d.p("Three kinds of train–test shift should be kept apart. *Algorithm shift*, or stego-source mismatch, "
        "occurs when test stego images come from an embedding method absent from training. Butora and "
        "Fridrich trained SRNet on three of WOW, S-UNIWARD, HILL and MiPOD at 0.4 bpp and tested on the "
        "fourth; the largest loss occurred when HILL was held out, while training on several algorithms cost "
        "little against dedicated detectors \\cite{butora19}. Recent work adapts to algorithm and cover-source "
        "mismatch with unlabeled target data \\cite{wang25}. *Payload shift* occurs when the "
        "message length differs between training and test. Detection error grows as the payload falls; SRNet "
        "built its low-payload detectors by curriculum training across payloads \\cite{srnet}, and knowledge "
        "distillation has been proposed for test payloads unseen in training \\cite{yu23}. *Cover-source shift* "
        "arises when test covers come from other cameras or processing pipelines and can raise the error even "
        "when algorithm and payload match \\cite{csm,giboulot,mallet}. This study varies the algorithm and the "
        "payload and holds the cover source fixed.")
    d.p("Robustness also depends on the operating point. The ALASKA challenge ranked detectors by the "
        "missed-detection rate at 5% false alarms (MD5) \\cite{alaska}, and the FLD ensemble has been extended "
        "to meet a prescribed false-alarm probability \\cite{cogranne15}. Butora and Bas reported that two detectors with "
        "almost equal error differed by about ten points in detection rate at an FPR of 10^{−3}, while noting "
        "that such estimates from 2,000 test images are noisy \\cite{mode25}.")
    d.h2("Research Gap and Comparative Analysis")
    d.p("{tab:related} compares representative studies; “Not reported” means the paper does not report the "
        "item.")
    rows = [
        ["SRM \\cite{srm}", "BOSSbase 0.92, 512 × 512", "SRM + FLD ensemble",
         "Matched algorithm and payload; P_{E}", "None", "Not reported"],
        ["Yedroudj-Net \\cite{yedroudj}", "BOSSbase 1.01, resized to 256 × 256", "CNN",
         "WOW, S-UNIWARD 0.2/0.4 bpp; matched; P_{E}", "None", "Not reported"],
        ["SRNet \\cite{srnet}", "BOSSbase 1.01 + BOWS2, 256 × 256", "Residual CNN",
         "0.1–0.5 bpp, curriculum over payloads; P_{E}", "None", "Not reported"],
        ["CSM \\cite{csm}", "Several cover sources, spatial and JPEG", "Feature-based, various dimensions",
         "Train and test on different sources", "Cover source", "Not reported"],
        ["Butora & Fridrich \\cite{butora19}", "BOSSbase 1.01 + BOWS2, 256 × 256", "SRNet variants",
         "Leave one of 4 algorithms out, 0.4 bpp; P_{MD}", "Algorithm",
         "Not reported"],
        ["ALASKA \\cite{alaska}", "JPEG images with diverse processing", "Challenge entries",
         "Challenge ranking", "Cover source, algorithm", "MD5 (5% FPR)"],
        ["MODE \\cite{mode25}", "BOSSbase, 512 × 512", "Pretrained SRNet", "HILL 0.3 bpp; P_{E}, detection at "
         "fixed FPR", "None", "FPR 10^{−3}–10^{−1}"],
        ["This study", "BOSSbase 1.01, 600 covers, 256 × 256", "Residual-LR; SRM+Ensemble",
         "Split before embedding; paired bootstrap", "Algorithm, payload",
         "Recall, test FPR at 1% val. FPR"],
    ]
    d.table("tab:related", "Comparison with representative steganalysis studies. P_{E}: minimum average "
            "error under equal priors; P_{MD}: missed-detection probability; CSM: cover-source mismatch.",
            [1150, 1300, 1150, 1600, 800, 918],
            [["Study", "Data", "Detector", "Protocol and metric", "Shift", "Low-FPR metric"]], rows,
            size=15, aligns=["left"] * 6, group_rules=(7,))
    d.p("Detector papers evaluate the matched condition, shift studies mostly concern the cover source or "
        "use large CNN training sets \\cite{butora19}, and low-FPR evaluation is rarely combined with "
        "algorithm or payload shift \\cite{alaska,mode25}. To our knowledge, no study measures algorithm and payload shift for feature-based detectors under a split "
        "fixed before embedding, with paired intervals on identical test covers, while also reporting the FPR "
        "actually reached at a validation-selected threshold. StegaGuard addresses this gap.")


def write_discussion(d):
    d.p("*Observed evidence.* SRM+Ensemble lost AUC when moving from matched WOW to unseen HILL. This agrees "
        "in direction with the largest loss for held-out HILL reported for SRNet \\cite{butora19}, although "
        "that study trained on three algorithms and about 28,000 images rather than one algorithm and 720 "
        "images. Mixing payloads at a fixed training size gave no reliable improvement on HILL; Butora and "
        "Fridrich likewise found in preliminary tests that a random mixture of payloads trained no better than "
        "a single mid payload \\cite{butora19}. SRM+Ensemble was far weaker at 0.1 bpp and the near-chance "
        "Residual-LR slightly weaker, in line with the payload dependence reported for SRM and SRNet "
        "\\cite{srm,srnet}. The observed test FPR exceeded the validation target in every cell; \\cite{mode25} "
        "likewise cautions that low-FPR estimates from 2,000 test images are noisy, and here the threshold "
        "rests on only 120 validation covers.")
    d.p("*Possible explanations.* The higher intrinsic security of HILL \\cite{hill}, the small training set "
        "and the resizing to 256 × 256 may contribute to these AUC losses; none of them was tested here.",
        style="p1a")
    d.p("For a defender, ranking quality and operational usefulness diverge: an AUC of 0.71 still meant "
        "missing over 80% of stego images at a threshold meant to keep false alarms near 1%. For an adversary, "
        "lowering the payload to 0.1 bpp, or using HILL against WOW-trained SRM+Ensemble, was enough to weaken "
        "detection. The main limits are the dataset size (600 covers, one split, so the intervals are "
        "conditional on that partition), the resizing to 256 × 256, detector strength (two feature-based "
        "detectors, one near chance, and no matched HILL reference) and generalization (one cover source, and "
        "a 1% threshold calibrated on 120 covers).")
