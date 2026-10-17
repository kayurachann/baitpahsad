"""So kết quả chạy lại (scores.csv + thresholds.csv từ gop_ket_qua.py) với số trong bài (results_data.py).

In ra:
- Table 4: AUC trung bình, SD, F1, BER, recall và FPR tại τlow của từng ô; số ô lệch quá 0.0015 (sai số làm tròn);
- Table 7: số false positive của từng seed tại τlow;
- Table 5/6 và S2: ΔAUC và CI 95% theo nhiều cách bootstrap, để xem cách nào cho ra đúng CI của bản trước
  (results_data.RQ*_TRUOC, tính bằng script ΔAUC gốc đã mất):
    A1000 / A2000  thay replicate ΔAUC lấy trung bình qua 3 seed, rng(2026) mới cho mỗi so sánh, thứ tự manifest;
    S2000_meanCI   từng seed riêng như paired_auc_confidence của nhóm (B = 2000, rng(2026 + seed), cover
                   sắp theo ID), rồi lấy trung bình cận dưới/cận trên của 3 seed;
    S2000_pooled   như trên nhưng gộp 3 × 2000 replicate rồi lấy phân vị;
    S1000_meanCI   từng seed, B = 1000, rng(2026), thứ tự manifest (như sg.py evaluate), trung bình cận.

Cách chạy: python3 so_sanh_chay_lai.py scores.csv thresholds.csv [--out ket_qua.md]
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import results_data as R  # noqa: E402
import verify_stats as V  # noqa: E402

TEN_CHI_SO = ("auc_mean", "auc_sd", "f1", "ber", "recall_low", "fpr_low")


def _vec(runs, det, cond, seed, thu_tu):
    run = runs[(det, cond[0], seed)]
    ids = sorted(run["test_cover"]) if thu_tu == "sorted" else run["test_order"]
    return V.vectors(run, cond[1:], ids)


def _mot_seed(runs, det, ref, shf, seed, B, rng_seed, thu_tu):
    (ca, sa), (cb, sb) = _vec(runs, det, ref, seed, thu_tu), _vec(runs, det, shf, seed, thu_tu)
    rng = np.random.default_rng(rng_seed)
    n = len(ca)
    reps = np.empty(B)
    for b in range(B):
        ix = rng.integers(0, n, n)
        reps[b] = V.auc(cb[ix], sb[ix]) - V.auc(ca[ix], sa[ix])
    return V.auc(cb, sb) - V.auc(ca, sa), reps


def cac_cach_ci(runs, det, ref, shf):
    seeds = sorted({k[2] for k in runs if k[:2] == (det, ref[0])})
    out = {}
    for B in (1000, 2000):
        r = V.paired_bootstrap(runs, det, ref, shf, B, 2026)
        out[f"A{B}"] = (r["delta"], *r["ci"])
    per = [_mot_seed(runs, det, ref, shf, s, 2000, 2026 + s, "sorted") for s in seeds]
    d = float(np.mean([p[0] for p in per]))
    los = [np.quantile(p[1], .025) for p in per]
    his = [np.quantile(p[1], .975) for p in per]
    out["S2000_meanCI"] = (d, float(np.mean(los)), float(np.mean(his)))
    allr = np.concatenate([p[1] for p in per])
    out["S2000_pooled"] = (d, float(np.quantile(allr, .025)), float(np.quantile(allr, .975)))
    per1 = [_mot_seed(runs, det, ref, shf, s, 1000, 2026, "manifest") for s in seeds]
    out["S1000_meanCI"] = (d, float(np.mean([np.quantile(p[1], .025) for p in per1])),
                           float(np.mean([np.quantile(p[1], .975) for p in per1])))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scores")
    ap.add_argument("thresholds")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    runs = V.load(a.scores)
    thr = V.load_thresholds(a.thresholds)
    tom = V.summarise(V.per_run_metrics(runs, thr))
    dong = []
    p = dong.append

    p("## Table 4 (và S1): chạy lại so với bài\n")
    for det in R.DETECTORS:
        khoa = [k for k in R.MATRIX if k[0] == det and k in tom]
        if not khoa:
            continue
        lech = {c: 0 for c in TEN_CHI_SO}
        lon_nhat = {c: 0.0 for c in TEN_CHI_SO}
        for k in khoa:
            for i, c in enumerate(TEN_CHI_SO):
                d = abs(round(tom[k][c], 3) - R.MATRIX[k][i])
                lon_nhat[c] = max(lon_nhat[c], d)
                lech[c] += d > 0.0015
        p(f"- {det} ({len(khoa)} ô): " + "; ".join(f"{c} lệch >0.0015 ở {lech[c]} ô (lớn nhất {lon_nhat[c]:.3f})"
                                                 for c in TEN_CHI_SO))
        for k in khoa:
            v = tom[k]
            p(f"    {k[1]} {k[2]} {k[3]}: AUC {v['auc_mean']:.3f}±{v['auc_sd']:.3f} (bài {R.MATRIX[k][0]:.3f}"
              f"±{R.MATRIX[k][1]:.3f}), recall {v['recall_low']:.3f} (bài {R.MATRIX[k][4]:.3f}), "
              f"FPR {v['fpr_low']:.3f} (bài {R.MATRIX[k][5]:.3f})")

    p("\n## Table 7: false positive từng seed tại τlow (trên 120 test cover)\n")
    for det in R.DETECTORS:
        for pr in R.PROTOCOLS:
            k = next((k for k in tom if k[:2] == (det, pr)), None)
            if k:
                fp = tom[k]["fp_per_seed"]
                p(f"- {det} {pr}: FP theo seed 42/43/44 = {fp}, tổng {sum(fp)}/360")

    p("\n## Table 5/6, S2: ΔAUC và CI theo từng cách bootstrap\n")
    tong = {}
    for rq, det, ref, shf in V.comparisons():
        if not any(k[:2] == (det, ref[0]) for k in runs) or not any(k[:2] == (det, shf[0]) for k in runs):
            continue
        d_bai, (lo_bai, hi_bai) = R.ban_truoc(rq, det, ref, shf)   # CI của bản trước (script ΔAUC gốc)
        cc = cac_cach_ci(runs, det, ref, shf)
        p(f"- {rq} {det} {ref}->{shf}: bản trước {d_bai:+.3f} [{lo_bai:+.3f}, {hi_bai:+.3f}]")
        for ten, (d, lo, hi) in cc.items():
            sai = max(abs(round(d, 3) - d_bai), abs(round(lo, 3) - lo_bai), abs(round(hi, 3) - hi_bai))
            tong.setdefault((det, ten), []).append(sai)
            p(f"    {ten:13s} {d:+.3f} [{lo:+.3f}, {hi:+.3f}]  lệch lớn nhất {sai:.3f}")
    p("\n### Tóm tắt: lệch lớn nhất / trung bình của mỗi cách (so với CI của bản trước)\n")
    for (det, ten), v in sorted(tong.items()):
        p(f"- {det:13s} {ten:13s}: lớn nhất {max(v):.3f}, trung bình {np.mean(v):.4f}, khớp ≤0.001 ở {sum(x <= 0.0011 for x in v)}/{len(v)}")
    txt = "\n".join(dong)
    print(txt)
    if a.out:
        Path(a.out).write_text(txt + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
