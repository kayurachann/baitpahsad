"""Recompute every number of the manuscript from the stored per-image prediction scores.

Input: one CSV with one row per scored image and run, columns
    detector   Residual-LR | SRM+Ensemble
    protocol   P1 | P2 | P3
    seed       42 | 43 | 44
    split      val | test
    cover_id   source cover identifier (shared by a cover and all of its stego variants)
    algorithm  cover | WOW | S-UNIWARD | HILL
    payload    0 for covers, 0.1 or 0.4 for stego
    score      detector output, higher = more likely stego

Validation rows hold the cover and stego scores used to set thresholds; test rows hold the 120 test
covers and their stego variants in all six conditions. As in sg.py, validation rows of a run should hold
each validation cover once and only the stego variants of that protocol's training pool. Keep the test
rows in manifest order (the order of sg.py's predictions.csv): the bootstrap indexes covers in that order.

sg.py does not save validation scores, only each run's thresholds.json. For such runs leave out the
validation rows and pass --thresholds, a CSV with columns detector, protocol, seed, tau_ber, tau_low
(tau_ber = "balanced" and tau_low = "low_fpr" of that run's thresholds.json).

Usage:
    python3 verify_stats.py scores.csv [--thresholds thresholds.csv] [--B 1000] [--boot-seed 2026] [--out report.json]
    python3 verify_stats.py --selftest

The script prints each recomputed value next to the value reported in the manuscript
(results_data.py) so that mismatches are visible. Threshold and bootstrap rules follow sg.py:
tau_low is just above the second-highest validation cover score, tau_ber minimises the balanced
error (ties: highest threshold, as argmin over sklearn's descending roc_curve thresholds), and every
bootstrap starts a fresh np.random.default_rng(2026) so all conditions and runs draw the same cover
indices. sg.py only bootstraps the AUC of single conditions; how the paper's ΔAUC intervals were
aggregated over seeds is not in the code package. ``paired_bootstrap`` averages each replicate's ΔAUC
over the three seeds; if the original analysis did otherwise, change it and the text of Sect. 3.5.
"""
import argparse
import csv
import json
import math
from collections import defaultdict

import numpy as np
from scipy.stats import rankdata

import results_data as R

CONDITIONS = [(a, b) for a in R.ALGORITHMS for b in (0.4, 0.1)]


# ---------------------------------------------------------------------- metrics
def auc(neg, pos):
    """ROC-AUC via the Mann-Whitney statistic with average ranks for ties."""
    neg, pos = np.asarray(neg, float), np.asarray(pos, float)
    ranks = rankdata(np.concatenate([neg, pos]))
    n0, n1 = len(neg), len(pos)
    return (ranks[n0:].sum() - n1 * (n1 + 1) / 2) / (n0 * n1)


def tau_low(val_cover_scores, target=0.01):
    """Smallest threshold with at most floor(target * |V|) validation covers scoring >= tau (Eq. 1)."""
    s = np.sort(np.asarray(val_cover_scores, float))[::-1]
    k = int(math.floor(target * len(s)))          # 1 for |V| = 120
    return np.nextafter(s[k], np.inf)             # just above the (k+1)-th highest cover score


def tau_ber(val_cover, val_stego):
    """Threshold minimising the balanced error rate on validation, computed exactly as sg.py does:
    err = .5 * (fpr + 1 - tpr) over the descending score thresholds, first minimum (np.argmin)."""
    c, st = np.asarray(val_cover, float), np.asarray(val_stego, float)
    best, best_t = None, None
    for t in np.unique(np.concatenate([c, st]))[::-1]:
        err = .5 * (np.float64((c >= t).sum()) / len(c) + 1 - np.float64((st >= t).sum()) / len(st))
        if best is None or err < best:
            best, best_t = err, t
    return best_t


def f1_ber(cover, stego, t):
    cover, stego = np.asarray(cover), np.asarray(stego)
    tp, fn, fp = (stego >= t).sum(), (stego < t).sum(), (cover >= t).sum()
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn)
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return f1, 0.5 * ((cover >= t).mean() + (stego < t).mean())


# ---------------------------------------------------------------------- data access
def load(path):
    runs = defaultdict(lambda: {"val_cover": {}, "val_stego": [], "test_cover": {}, "test_stego": defaultdict(dict),
                                "test_order": []})
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            key = (row["detector"], row["protocol"], int(row["seed"]))
            run, cid, sc = runs[key], row["cover_id"], float(row["score"])
            if row["split"] == "val":
                if row["algorithm"] == "cover":
                    run["val_cover"][cid] = sc
                else:
                    run["val_stego"].append(sc)
            elif row["algorithm"] == "cover":
                if cid not in run["test_cover"]:
                    run["test_order"].append(cid)   # manifest order, used for bootstrap indices
                run["test_cover"][cid] = sc
            else:
                run["test_stego"][(row["algorithm"], float(row["payload"]))][cid] = sc
    return runs


def load_thresholds(path):
    """thresholds.csv -> {(detector, protocol, seed): (tau_ber, tau_low)}"""
    with open(path, newline="") as fh:
        return {(r["detector"], r["protocol"], int(r["seed"])): (float(r["tau_ber"]), float(r["tau_low"]))
                for r in csv.DictReader(fh)}


def check_structure(runs, thr=None):
    problems = []
    for key, run in runs.items():
        ids = set(run["test_cover"])
        if len(ids) != R.N_TEST_COVERS:
            problems.append(f"{key}: {len(ids)} test covers")
        if not run["val_cover"] and thr and key in thr:
            pass                                    # thresholds taken from the run's thresholds.json
        elif len(run["val_cover"]) != R.N_VAL_COVERS:
            problems.append(f"{key}: {len(run['val_cover'])} validation covers")
        if ids & set(run["val_cover"]):
            problems.append(f"{key}: validation/test cover_id overlap")
        for cond in CONDITIONS:
            if set(run["test_stego"][cond]) != ids:
                problems.append(f"{key} {cond}: stego cover_ids differ from test cover_ids")
    return problems


def auc_ci(cover, stego, B, boot_seed=2026):
    """Percentile 95% CI of one condition's AUC, resampling cover-stego pairs as sg.py evaluate() does."""
    rng = np.random.default_rng(boot_seed)
    reps = [auc(cover[ix], stego[ix]) for ix in (rng.integers(0, len(cover), len(cover)) for _ in range(B))]
    return float(np.quantile(reps, .025)), float(np.quantile(reps, .975))


def vectors(run, cond, ids):
    return (np.array([run["test_cover"][i] for i in ids]),
            np.array([run["test_stego"][cond][i] for i in ids]))


# ---------------------------------------------------------------------- per-run metrics
def per_run_metrics(runs, thr=None):
    out = {}
    for (det, p, seed), run in sorted(runs.items()):
        ids = run["test_order"]
        if run["val_cover"]:
            t_low = tau_low(list(run["val_cover"].values()))
            t_ber = tau_ber(list(run["val_cover"].values()), run["val_stego"])
        else:
            t_ber, t_low = thr[(det, p, seed)]
        cover = np.array([run["test_cover"][i] for i in ids])
        fp = int((cover >= t_low).sum())
        for cond in CONDITIONS:
            c, s = vectors(run, cond, ids)
            f1, ber = f1_ber(c, s, t_ber)
            out[(det, p, seed) + cond] = {"auc": auc(c, s), "f1": f1, "ber": ber,
                                          "recall_low": float((s >= t_low).mean()), "fpr_low": fp / len(ids),
                                          "fp_low": fp}
    return out


def summarise(metrics):
    rows = {}
    for det in R.DETECTORS:
        for p in R.PROTOCOLS:
            for a, b in CONDITIONS:
                ms = [v for k, v in metrics.items() if k[:2] == (det, p) and k[3:] == (a, b)]
                if not ms:
                    continue
                aucs = [m["auc"] for m in ms]
                rows[(det, p, a, b)] = {
                    "auc_mean": float(np.mean(aucs)), "auc_sd": float(np.std(aucs, ddof=1)) if len(aucs) > 1 else 0.0,
                    **{k: float(np.mean([m[k] for m in ms])) for k in ("f1", "ber", "recall_low", "fpr_low")},
                    "fp_per_seed": [m["fp_low"] for m in ms]}
    return rows


# ---------------------------------------------------------------------- paired bootstrap
def comparisons():
    out = []
    for det in R.DETECTORS:
        out.append(("RQ1", det, ("P1", "WOW", 0.4), ("P1", "HILL", 0.4)))
        out.append(("RQ2", det, ("P2", "HILL", 0.4), ("P3", "HILL", 0.4)))
        for p in R.PROTOCOLS:
            for a in R.ALGORITHMS:
                out.append(("RQ3", det, (p, a, 0.4), (p, a, 0.1)))
    return out


def paired_bootstrap(runs, det, ref, shf, B, boot_seed):
    """Seed-averaged ΔAUC = AUC(shifted) − AUC(reference) with a cover-level paired bootstrap.

    The resampling unit is the source test cover; one draw of cover IDs is shared by both
    conditions and by all seeds, so every cover keeps its cover score and its paired stego scores.
    A fresh generator per comparison gives every comparison the same draws, as sg.py does per condition.
    """
    rng = np.random.default_rng(boot_seed)
    seeds = sorted({k[2] for k in runs if k[:2] == (det, ref[0])})
    ids = runs[(det, ref[0], seeds[0])]["test_order"]
    data = []
    for sd in seeds:
        ra, rb = runs[(det, ref[0], sd)], runs[(det, shf[0], sd)]
        data.append((vectors(ra, ref[1:], ids), vectors(rb, shf[1:], ids)))

    def delta(idx):
        return float(np.mean([auc(cb[idx], sb[idx]) - auc(ca[idx], sa[idx]) for (ca, sa), (cb, sb) in data]))

    point = delta(np.arange(len(ids)))
    reps = np.array([delta(rng.integers(0, len(ids), len(ids))) for _ in range(B)])
    lo, hi = np.percentile(reps, [2.5, 97.5])
    per_seed = [auc(cb, sb) - auc(ca, sa) for (ca, sa), (cb, sb) in data]
    return {"delta": point, "ci": [float(lo), float(hi)], "per_seed_delta": per_seed,
            "seed_sd_of_delta": float(np.std(per_seed, ddof=1)) if len(per_seed) > 1 else 0.0}


def reported_delta(rq, det, ref, shf):
    if rq == "RQ1":
        _, _, d, ci = R.RQ1[det]
        return d, ci
    if rq == "RQ2":
        _, _, d, ci = R.RQ2[det]
        return d, ci
    d, lo, hi = R.RQ3[(det, ref[0], ref[1])]
    return d, (lo, hi)


# ---------------------------------------------------------------------- main
def run(path, B, boot_seed, out_path, thr_path=None):
    runs = load(path)
    thr = load_thresholds(thr_path) if thr_path else None
    problems = check_structure(runs, thr)
    print("structure check:", "OK" if not problems else f"{len(problems)} problems")
    for pr in problems[:20]:
        print("  ", pr)
    summary = summarise(per_run_metrics(runs, thr))
    report = {"matrix": {}, "comparisons": []}
    print("\nAUC (recomputed vs reported), test FP per seed at tau_low:")
    for key, v in summary.items():
        rep = R.MATRIX.get(key)
        flag = "" if rep is None or abs(round(v["auc_mean"], 3) - rep[0]) < 0.0015 else "  <-- differs"
        print(f"  {key}: AUC {v['auc_mean']:.3f}±{v['auc_sd']:.3f} (reported {rep[0] if rep else '-'}),"
              f" BER {v['ber']:.3f}, F1 {v['f1']:.3f}, recall {v['recall_low']:.3f}, FPR {v['fpr_low']:.3f},"
              f" FP/seed {v['fp_per_seed']}{flag}")
        report["matrix"]["|".join(map(str, key))] = v
    print(f"\nPaired bootstrap, B = {B}, resampling unit = source test cover, shared across seeds:")
    for rq, det, ref, shf in comparisons():
        res = paired_bootstrap(runs, det, ref, shf, B, boot_seed)
        d_rep, ci_rep = reported_delta(rq, det, ref, shf)
        print(f"  {rq} {det} {ref}->{shf}: Δ {res['delta']:+.3f} CI [{res['ci'][0]:+.3f}, {res['ci'][1]:+.3f}]"
              f"  (reported {d_rep:+.3f} [{ci_rep[0]:+.3f}, {ci_rep[1]:+.3f}]); seed SD of Δ {res['seed_sd_of_delta']:.3f}")
        report["comparisons"].append({"rq": rq, "detector": det, "reference": ref, "shifted": shf, **res})
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(report, fh, indent=1, default=str)
        print("\nreport written to", out_path)


def selftest(path="selftest_scores.csv"):
    """Write a synthetic score file with the expected structure and run the full pipeline on it."""
    rng = np.random.default_rng(0)
    test_ids = [f"t{i:03d}" for i in range(120)]
    val_ids = [f"v{i:03d}" for i in range(120)]
    shift = {("WOW", 0.4): 0.8, ("S-UNIWARD", 0.4): 0.7, ("HILL", 0.4): 0.5,
             ("WOW", 0.1): 0.15, ("S-UNIWARD", 0.1): 0.1, ("HILL", 0.1): 0.08}
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["detector", "protocol", "seed", "split", "cover_id", "algorithm", "payload", "score"])
        for det in R.DETECTORS:
            for p in R.PROTOCOLS:
                for seed in R.SEEDS:
                    for i in val_ids:
                        w.writerow([det, p, seed, "val", i, "cover", 0, rng.normal()])
                        w.writerow([det, p, seed, "val", i, "WOW", 0.4, rng.normal(0.8)])
                    base = {i: rng.normal() for i in test_ids}
                    for i in test_ids:
                        w.writerow([det, p, seed, "test", i, "cover", 0, base[i]])
                        for (a, b), m in shift.items():
                            w.writerow([det, p, seed, "test", i, a, b, base[i] * 0.3 + rng.normal(m)])
    run(path, B=200, boot_seed=1, out_path=None)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scores", nargs="?")
    ap.add_argument("--B", type=int, default=1000, help="bootstrap replicates (sg.py evaluate uses 1000)")
    ap.add_argument("--boot-seed", type=int, default=2026)
    ap.add_argument("--out", default=None, help="optional JSON report")
    ap.add_argument("--thresholds", default=None, help="CSV of per-run tau_ber/tau_low from thresholds.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.scores:
        run(a.scores, a.B, a.boot_seed, a.out, a.thresholds)
    else:
        ap.error("give a score CSV or --selftest")
