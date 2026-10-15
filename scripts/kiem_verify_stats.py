"""Kiểm verify_stats.py có tính giống code của nhóm (code/sg.py) không.

1. Ngưỡng: so tau_ber/tau_low với logic hàm thresholds() của sg.py (chép nguyên ở dưới) trên
   2.000 bộ dữ liệu ngẫu nhiên có nhiều điểm trùng. Cần scikit-learn.
2. Bootstrap: nếu đưa thư mục kết quả pilot (bossbase_pilot_results), so AUC và CI 95% của từng
   điều kiện với auc, auc_ci_low, auc_ci_high mà sg.py evaluate() ghi trong metrics.csv.
3. Gộp kết quả: chạy gop_ket_qua.py trên cùng thư mục, rồi verify_stats (ngưỡng lấy từ thresholds.json)
   tính lại AUC, recall và FPR tại τlow, F1 và BER tại τBER của từng lần chạy, so với metrics.csv.

Cách chạy: python3 kiem_verify_stats.py [thư_mục_bossbase_pilot_results]
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_curve

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_stats as V  # noqa: E402


def sg_thresholds(labels, scores, target=.01):
    """Logic của sg.py thresholds() (dòng 159-168)."""
    y = np.asarray(labels)
    s = np.asarray(scores)
    fpr, tpr, t = roc_curve(y, s, drop_intermediate=False)
    finite = np.isfinite(t)
    t = t[finite]
    err = .5 * (fpr[finite] + 1 - tpr[finite])
    best = float(t[np.argmin(err)])
    cover = np.sort(s[y == 0])[::-1]
    k = int(np.floor(target * len(cover)))
    return best, float(np.nextafter(cover[k], np.inf))


def kiem_nguong(lan=2000):
    rng = np.random.default_rng(1)
    lech = 0
    for _ in range(lan):
        nc, ns = 120, int(rng.choice([120, 240]))
        q = rng.choice([0.05, 0.2, 1.0])  # làm tròn thô để có nhiều điểm trùng
        c = np.round(rng.normal(0, 1, nc) / q) * q
        s = np.round(rng.normal(rng.uniform(0, 1), 1, ns) / q) * q
        if sg_thresholds(np.r_[np.zeros(nc), np.ones(ns)], np.r_[c, s]) != (V.tau_ber(c, s), V.tau_low(c)):
            lech += 1
    print(f"ngưỡng: {lan} bộ dữ liệu, {lech} lệch so với sg.py")
    return lech


def kiem_pilot(goc):
    n = lech = 0
    for run in sorted(Path(goc).glob("*_test")):
        rows = list(csv.DictReader(open(run / "predictions.csv", newline="", encoding="utf-8")))
        thu_tu = None
        for m in csv.DictReader(open(run / "metrics.csv", newline="", encoding="utf-8")):
            rr = [r for r in rows if r["test_algorithm"] == m["algorithm"] and r["payload"] == m["payload"]]
            cov = [r for r in rr if r["label"] == "0"]
            st = [r for r in rr if r["label"] == "1"]
            ids = [r["cover_id"] for r in cov]
            if ids != [r["cover_id"] for r in st] or (thu_tu is not None and ids != thu_tu):
                print("thứ tự cover khác nhau:", run.name, m["algorithm"], m["payload"])
                lech += 1
            thu_tu = thu_tu or ids
            c = np.array([float(r["score"]) for r in cov])
            s = np.array([float(r["score"]) for r in st])
            tinh = (V.auc(c, s), *V.auc_ci(c, s, 1000, 2026))
            ghi = (float(m["auc"]), float(m["auc_ci_low"]), float(m["auc_ci_high"]))
            n += 1
            if max(abs(a - b) for a, b in zip(tinh, ghi)) > 1e-12:
                lech += 1
                print("lệch:", run.name, m["algorithm"], m["payload"], tinh, ghi)
    print(f"bootstrap: {n} điều kiện pilot, {lech} lệch so với metrics.csv của sg.py")
    return lech


def kiem_gop(goc):
    import tempfile
    import gop_ket_qua as G
    ten = {"wow": "WOW", "suniward": "S-UNIWARD", "hill": "HILL"}
    with tempfile.TemporaryDirectory() as ra:
        if G.gop(goc, ra):
            return 1
        m = V.per_run_metrics(V.load(Path(ra) / "scores.csv"), V.load_thresholds(Path(ra) / "thresholds.csv"))
    nguong = {}
    for run in Path(goc).glob("*/config.json"):
        cfg = json.loads(run.read_text(encoding="utf-8"))
        khoa = (tuple(sorted(cfg["algorithms"])), tuple(sorted(float(p) for p in cfg["payloads"])))
        nguong[run.parent.name] = (G.ten_detector(cfg["model"]), G.PROTOCOL[khoa], int(cfg["seed"]))
    n = lech = 0
    for test in sorted(Path(goc).glob("*_test")):
        det, p, seed = nguong[test.name[:-5]]
        for r in csv.DictReader(open(test / "metrics.csv", newline="", encoding="utf-8")):
            v = m[(det, p, seed, ten[r["algorithm"]], float(r["payload"]))]
            cap = [(v["auc"], r["auc"]), (v["recall_low"], r["recall_at_validation_low_fpr"]),
                   (v["fpr_low"], r["actual_test_fpr"]), (v["f1"], r["f1"]), (v["ber"], r["balanced_error"])]
            n += 1
            if max(abs(a - float(b)) for a, b in cap) > 1e-12:
                lech += 1
                print("lệch:", test.name, r["algorithm"], r["payload"], cap)
    print(f"gộp kết quả: {n} điều kiện × 5 chỉ số, {lech} lệch so với metrics.csv của sg.py")
    return lech


if __name__ == "__main__":
    loi = kiem_nguong()
    if len(sys.argv) > 1:
        loi += kiem_pilot(sys.argv[1])
        loi += kiem_gop(sys.argv[1])
    sys.exit(1 if loi else 0)
