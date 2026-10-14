"""Reported results of the StegaGuard 600-cover experiment.

Single source of truth for every number that appears in the manuscript tables,
figures and supplementary material. Values are transcribed from the previous
manuscript version (seed means over seeds 42, 43, 44); they must be regenerated
from the stored per-image prediction scores with ``verify_stats.py`` before
submission.
"""

from decimal import Decimal, ROUND_HALF_EVEN

DETECTORS = ["Residual-LR", "SRM+Ensemble"]
PROTOCOLS = ["P1", "P2", "P3"]
ALGORITHMS = ["WOW", "S-UNIWARD", "HILL"]
PAYLOADS = [0.1, 0.4]

N_TEST_COVERS = 120
N_VAL_COVERS = 120
N_TRAIN_COVERS = 360
SEEDS = [42, 43, 44]

# (detector, protocol, algorithm, payload) -> (AUC mean, AUC SD, F1, BER, recall@low, FPR@low)
MATRIX = {
    ("Residual-LR", "P1", "WOW", 0.1): (0.510, 0.000, 0.509, 0.475, 0.050, 0.042),
    ("Residual-LR", "P1", "WOW", 0.4): (0.546, 0.000, 0.528, 0.463, 0.058, 0.042),
    ("Residual-LR", "P1", "S-UNIWARD", 0.1): (0.505, 0.000, 0.476, 0.496, 0.050, 0.042),
    ("Residual-LR", "P1", "S-UNIWARD", 0.4): (0.565, 0.000, 0.540, 0.454, 0.050, 0.042),
    ("Residual-LR", "P1", "HILL", 0.1): (0.514, 0.000, 0.482, 0.492, 0.042, 0.042),
    ("Residual-LR", "P1", "HILL", 0.4): (0.570, 0.000, 0.564, 0.438, 0.042, 0.042),
    ("Residual-LR", "P2", "WOW", 0.1): (0.500, 0.001, 0.547, 0.487, 0.056, 0.042),
    ("Residual-LR", "P2", "WOW", 0.4): (0.534, 0.005, 0.566, 0.472, 0.072, 0.042),
    ("Residual-LR", "P2", "S-UNIWARD", 0.1): (0.504, 0.002, 0.539, 0.493, 0.053, 0.042),
    ("Residual-LR", "P2", "S-UNIWARD", 0.4): (0.549, 0.001, 0.577, 0.464, 0.097, 0.042),
    ("Residual-LR", "P2", "HILL", 0.1): (0.505, 0.002, 0.541, 0.492, 0.056, 0.042),
    ("Residual-LR", "P2", "HILL", 0.4): (0.551, 0.004, 0.595, 0.450, 0.089, 0.042),
    ("Residual-LR", "P3", "WOW", 0.1): (0.501, 0.002, 0.562, 0.500, 0.056, 0.053),
    ("Residual-LR", "P3", "WOW", 0.4): (0.523, 0.002, 0.584, 0.482, 0.061, 0.053),
    ("Residual-LR", "P3", "S-UNIWARD", 0.1): (0.502, 0.004, 0.572, 0.492, 0.064, 0.053),
    ("Residual-LR", "P3", "S-UNIWARD", 0.4): (0.555, 0.016, 0.603, 0.467, 0.092, 0.053),
    ("Residual-LR", "P3", "HILL", 0.1): (0.511, 0.007, 0.562, 0.500, 0.056, 0.053),
    ("Residual-LR", "P3", "HILL", 0.4): (0.546, 0.012, 0.596, 0.472, 0.078, 0.053),
    ("SRM+Ensemble", "P1", "WOW", 0.1): (0.539, 0.002, 0.498, 0.483, 0.053, 0.050),
    ("SRM+Ensemble", "P1", "WOW", 0.4): (0.714, 0.026, 0.684, 0.347, 0.189, 0.050),
    ("SRM+Ensemble", "P1", "S-UNIWARD", 0.1): (0.532, 0.015, 0.501, 0.482, 0.061, 0.050),
    ("SRM+Ensemble", "P1", "S-UNIWARD", 0.4): (0.689, 0.008, 0.669, 0.360, 0.114, 0.050),
    ("SRM+Ensemble", "P1", "HILL", 0.1): (0.525, 0.009, 0.501, 0.482, 0.056, 0.050),
    ("SRM+Ensemble", "P1", "HILL", 0.4): (0.645, 0.009, 0.636, 0.386, 0.108, 0.050),
    ("SRM+Ensemble", "P2", "WOW", 0.1): (0.550, 0.012, 0.465, 0.469, 0.039, 0.031),
    ("SRM+Ensemble", "P2", "WOW", 0.4): (0.713, 0.009, 0.650, 0.351, 0.156, 0.031),
    ("SRM+Ensemble", "P2", "S-UNIWARD", 0.1): (0.534, 0.009, 0.464, 0.471, 0.025, 0.031),
    ("SRM+Ensemble", "P2", "S-UNIWARD", 0.4): (0.717, 0.006, 0.648, 0.353, 0.097, 0.031),
    ("SRM+Ensemble", "P2", "HILL", 0.1): (0.534, 0.007, 0.459, 0.475, 0.028, 0.031),
    ("SRM+Ensemble", "P2", "HILL", 0.4): (0.653, 0.018, 0.585, 0.394, 0.072, 0.031),
    ("SRM+Ensemble", "P3", "WOW", 0.1): (0.546, 0.016, 0.474, 0.469, 0.033, 0.022),
    ("SRM+Ensemble", "P3", "WOW", 0.4): (0.686, 0.028, 0.647, 0.358, 0.147, 0.022),
    ("SRM+Ensemble", "P3", "S-UNIWARD", 0.1): (0.528, 0.005, 0.450, 0.485, 0.019, 0.022),
    ("SRM+Ensemble", "P3", "S-UNIWARD", 0.4): (0.677, 0.022, 0.610, 0.383, 0.131, 0.022),
    ("SRM+Ensemble", "P3", "HILL", 0.1): (0.517, 0.010, 0.445, 0.489, 0.036, 0.022),
    ("SRM+Ensemble", "P3", "HILL", 0.4): (0.632, 0.010, 0.586, 0.400, 0.083, 0.022),
}

# Paired comparisons as reported (delta computed from unrounded AUCs; 95% paired bootstrap CI).
# RQ1: HILL 0.4 minus WOW 0.4 under P1.
RQ1 = {
    "Residual-LR": (0.546, 0.570, +0.024, (-0.007, +0.056)),
    "SRM+Ensemble": (0.714, 0.645, -0.070, (-0.093, -0.046)),
}
# RQ2: P3 minus P2 on HILL 0.4.
RQ2 = {
    "Residual-LR": (0.551, 0.546, -0.005, (-0.020, +0.007)),
    "SRM+Ensemble": (0.653, 0.632, -0.022, (-0.050, +0.005)),
}
# RQ3: AUC at 0.1 bpp minus AUC at 0.4 bpp, (detector, protocol, algorithm) -> (delta, lo, hi).
RQ3 = {
    ("Residual-LR", "P1", "WOW"): (-0.036, -0.063, -0.008),
    ("Residual-LR", "P1", "S-UNIWARD"): (-0.060, -0.096, -0.029),
    ("Residual-LR", "P1", "HILL"): (-0.056, -0.093, -0.020),
    ("Residual-LR", "P2", "WOW"): (-0.034, -0.058, -0.012),
    ("Residual-LR", "P2", "S-UNIWARD"): (-0.045, -0.070, -0.022),
    ("Residual-LR", "P2", "HILL"): (-0.046, -0.072, -0.020),
    ("Residual-LR", "P3", "WOW"): (-0.022, -0.046, -0.001),
    ("Residual-LR", "P3", "S-UNIWARD"): (-0.054, -0.078, -0.030),
    ("Residual-LR", "P3", "HILL"): (-0.035, -0.064, -0.006),
    ("SRM+Ensemble", "P1", "WOW"): (-0.175, -0.206, -0.144),
    ("SRM+Ensemble", "P1", "S-UNIWARD"): (-0.157, -0.186, -0.127),
    ("SRM+Ensemble", "P1", "HILL"): (-0.120, -0.149, -0.092),
    ("SRM+Ensemble", "P2", "WOW"): (-0.163, -0.193, -0.134),
    ("SRM+Ensemble", "P2", "S-UNIWARD"): (-0.183, -0.211, -0.155),
    ("SRM+Ensemble", "P2", "HILL"): (-0.119, -0.150, -0.088),
    ("SRM+Ensemble", "P3", "WOW"): (-0.140, -0.168, -0.111),
    ("SRM+Ensemble", "P3", "S-UNIWARD"): (-0.149, -0.177, -0.122),
    ("SRM+Ensemble", "P3", "HILL"): (-0.115, -0.145, -0.089),
}


def fpr_to_fp_total(fpr_mean, n_runs=3, n_covers=N_TEST_COVERS):
    """Smallest integer false-positive total over ``n_runs`` runs whose mean FPR rounds to ``fpr_mean``."""
    denom = n_runs * n_covers
    hits = [k for k in range(denom + 1) if round(k / denom, 3) == round(fpr_mean, 3)]
    if len(hits) != 1:
        raise ValueError(f"FPR {fpr_mean} does not identify a unique FP count: {hits}")
    return hits[0]


def low_fpr_summary():
    """Per (detector, protocol): FP total over 3 seeds, observed FPR, mean/min/max recall over 6 conditions."""
    rows = []
    for det in DETECTORS:
        for p in PROTOCOLS:
            cells = [MATRIX[(det, p, a, b)] for a in ALGORITHMS for b in PAYLOADS]
            fprs = {c[5] for c in cells}
            assert len(fprs) == 1, "test FPR must not depend on the stego condition"
            fpr = fprs.pop()
            recalls = [Decimal(str(c[4])) for c in cells]
            rows.append({
                "detector": det, "protocol": p, "fpr": fpr,
                "fp_total": fpr_to_fp_total(fpr),
                # exact decimal mean of the reported 3-decimal recalls, rounded half-even
                "recall_mean": float((sum(recalls) / len(recalls)).quantize(Decimal("0.001"), ROUND_HALF_EVEN)),
                "recall_min": float(min(recalls)), "recall_max": float(max(recalls)),
            })
    return rows


if __name__ == "__main__":
    for r in low_fpr_summary():
        print(r)
    for det in DETECTORS:
        rec = [MATRIX[(det, p, a, b)][4] for p in PROTOCOLS for a in ALGORITHMS for b in PAYLOADS]
        fpr = [MATRIX[(det, p, a, b)][5] for p in PROTOCOLS for a in ALGORITHMS for b in PAYLOADS]
        print(det, "mean recall", round(sum(rec) / len(rec), 4), "mean FPR", round(sum(fpr) / len(fpr), 4))
    # sign / arithmetic check of reported deltas against rounded seed means
    for (det, p, a), (d, lo, hi) in RQ3.items():
        calc = MATRIX[(det, p, a, 0.1)][0] - MATRIX[(det, p, a, 0.4)][0]
        assert abs(calc - d) <= 0.0015, (det, p, a, calc, d)
        assert lo <= d <= hi
    for name, rq in (("RQ1", RQ1), ("RQ2", RQ2)):
        for det, (a, b, d, (lo, hi)) in rq.items():
            print(name, det, "reported", d, "from rounded means", round(b - a, 3), "CI", lo, hi)
