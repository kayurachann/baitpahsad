"""Tính lại ΔAUC và CI 95% của mọi so sánh RQ1-RQ3 từ điểm từng ảnh (scores.csv của gop_ket_qua.py).

Cách tính giống verify_stats.paired_bootstrap: mỗi replicate rút 120 test cover có hoàn lại bằng một
np.random.default_rng(boot_seed) mới cho mỗi so sánh, theo thứ tự manifest; lần rút này dùng chung cho cả
hai điều kiện và cả ba seed; ΔAUC của replicate là trung bình ΔAUC của ba seed; CI là phân vị 2,5 và 97,5.

AUC của một replicate tính bằng wᵀPw / n², với w[i] là số lần cover i được rút và P[i, j] = 1 nếu stego j có
điểm cao hơn cover i (0,5 nếu bằng). Đây đúng là AUC Mann-Whitney trên mẫu đã rút (cover i và stego của nó
cùng đi theo w[i]), nên kết quả trùng verify_stats.paired_bootstrap nhưng nhanh hơn nhiều; --kiem so hai cách.

Cách chạy: python3 tinh_lai_ci.py scores.csv [--B 10000] [--boot-seed 2026] [--out ci.json] [--kiem]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_stats as V  # noqa: E402


def _P(cover, stego):
    return (cover[:, None] < stego[None, :]) + 0.5 * (cover[:, None] == stego[None, :])


def paired_bootstrap_nhanh(runs, det, ref, shf, B, boot_seed, khoi=1000):
    seeds = sorted({k[2] for k in runs if k[:2] == (det, ref[0])})
    ids = runs[(det, ref[0], seeds[0])]["test_order"]
    n = len(ids)
    cap = [(_P(*V.vectors(runs[(det, ref[0], sd)], ref[1:], ids)), _P(*V.vectors(runs[(det, shf[0], sd)], shf[1:], ids)))
           for sd in seeds]
    per_seed = [V.auc(*V.vectors(runs[(det, shf[0], sd)], shf[1:], ids)) - V.auc(*V.vectors(runs[(det, ref[0], sd)], ref[1:], ids))
                for sd in seeds]
    rng = np.random.default_rng(boot_seed)
    ix = np.stack([rng.integers(0, n, n) for _ in range(B)])        # cùng chuỗi rút với verify_stats
    reps = np.empty(B)
    for a in range(0, B, khoi):
        W = np.zeros((min(khoi, B - a), n))
        np.add.at(W, (np.repeat(np.arange(len(W)), n), ix[a:a + khoi].ravel()), 1)
        reps[a:a + len(W)] = np.mean([(np.einsum("bi,bi->b", W @ Pb, W) - np.einsum("bi,bi->b", W @ Pa, W)) / n ** 2
                                      for Pa, Pb in cap], axis=0)
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return {"delta": float(np.mean(per_seed)), "ci": [float(lo), float(hi)], "per_seed_delta": per_seed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scores")
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--boot-seed", type=int, default=2026)
    ap.add_argument("--out")
    ap.add_argument("--kiem", action="store_true", help="so với verify_stats.paired_bootstrap (B = 300)")
    a = ap.parse_args()
    runs = V.load(a.scores)
    kq = []
    for rq, det, ref, shf in V.comparisons():
        if not any(k[:2] == (det, ref[0]) for k in runs) or not any(k[:2] == (det, shf[0]) for k in runs):
            continue
        if a.kiem:
            x, y = paired_bootstrap_nhanh(runs, det, ref, shf, 300, a.boot_seed), V.paired_bootstrap(runs, det, ref, shf, 300, a.boot_seed)
            lech = max(abs(x["delta"] - y["delta"]), *(abs(p - q) for p, q in zip(x["ci"], y["ci"])))
            print(f"kiểm {rq} {det} {ref}->{shf}: lệch {lech:.2e}")
            if lech > 1e-12:
                sys.exit(1)
        r = paired_bootstrap_nhanh(runs, det, ref, shf, a.B, a.boot_seed)
        d_bai, (lo_bai, hi_bai) = V.reported_delta(rq, det, ref, shf)
        kq.append(dict(rq=rq, detector=det, reference=list(ref), shifted=list(shf), delta=r["delta"], ci=r["ci"],
                       per_seed_delta=r["per_seed_delta"], paper=[d_bai, lo_bai, hi_bai]))
        print(f"{rq} {det:13s} {ref[0]} {ref[1]} {ref[2]} -> {shf[0]} {shf[1]} {shf[2]}: {r['delta']:+.3f} "
              f"[{r['ci'][0]:+.3f}, {r['ci'][1]:+.3f}]   bài {d_bai:+.3f} [{lo_bai:+.3f}, {hi_bai:+.3f}]")
    if a.out:
        Path(a.out).write_text(json.dumps(dict(B=a.B, boot_seed=a.boot_seed, comparisons=kq), indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
