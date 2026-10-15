"""Gộp thư mục kết quả của code/sg.py thành đầu vào cho verify_stats.py.

Mỗi lần chạy của sg.py có thư mục <run>/ (config.json, thresholds.json) và <run>_test/ (predictions.csv).
Script tạo:
- scores.csv: detector, protocol, seed, split, cover_id, algorithm, payload, score (chỉ dòng test,
  giữ thứ tự của predictions.csv, tức thứ tự manifest mà bootstrap của sg.py dùng);
- thresholds.csv: detector, protocol, seed, tau_ber ("balanced"), tau_low ("low_fpr").

Protocol suy từ config.json: P1 = WOW 0.4; P2 = WOW + S-UNIWARD 0.4; P3 = WOW + S-UNIWARD 0.1 + 0.4.

Cách chạy: python3 gop_ket_qua.py <thư_mục_kết_quả> <thư_mục_ra> [--manifest-sha256 HASH]
"""
import argparse
import csv
import json
from pathlib import Path

PROTOCOL = {
    (("wow",), (0.4,)): "P1",
    (("suniward", "wow"), (0.4,)): "P2",
    (("suniward", "wow"), (0.1, 0.4)): "P3",
}
TEN_THUAT_TOAN = {"wow": "WOW", "suniward": "S-UNIWARD", "hill": "HILL"}


def ten_detector(model):
    m = model.lower()
    if m == "residual_lr":
        return "Residual-LR"
    if "srm" in m or "ensemble" in m:
        return "SRM+Ensemble"
    return model


def gop(goc, ra, sha=None):
    goc, ra = Path(goc), Path(ra)
    ra.mkdir(parents=True, exist_ok=True)
    dong_diem, dong_nguong, loi = [], [], []
    for cfg_path in sorted(goc.glob("*/config.json")):
        run = cfg_path.parent
        test = run.parent / f"{run.name}_test"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        if sha and cfg.get("manifest_sha256") != sha:
            loi.append(f"{run.name}: manifest_sha256 {cfg.get('manifest_sha256')} khác {sha}")
        khoa = (tuple(sorted(cfg["algorithms"])), tuple(sorted(float(p) for p in cfg["payloads"])))
        if khoa not in PROTOCOL:
            loi.append(f"{run.name}: không nhận ra protocol {khoa}")
            continue
        det, p, seed = ten_detector(cfg["model"]), PROTOCOL[khoa], int(cfg["seed"])
        th = json.loads((run / "thresholds.json").read_text(encoding="utf-8"))
        dong_nguong.append([det, p, seed, repr(float(th["balanced"])), repr(float(th["low_fpr"]))])
        if not (test / "predictions.csv").exists():
            loi.append(f"{run.name}: thiếu {test.name}/predictions.csv")
            continue
        with open(test / "predictions.csv", newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                cover = r["label"] == "0"
                dong_diem.append([det, p, seed, "test", r["cover_id"],
                                  "cover" if cover else TEN_THUAT_TOAN[r["test_algorithm"]],
                                  0 if cover else r["payload"], r["score"]])
    with open(ra / "scores.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["detector", "protocol", "seed", "split", "cover_id", "algorithm", "payload", "score"])
        w.writerows(dong_diem)
    with open(ra / "thresholds.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["detector", "protocol", "seed", "tau_ber", "tau_low"])
        w.writerows(dong_nguong)
    print(f"{len(dong_nguong)} lần chạy, {len(dong_diem)} dòng điểm -> {ra}")
    for x in loi:
        print("LỖI:", x)
    return loi


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("goc")
    ap.add_argument("ra")
    ap.add_argument("--manifest-sha256", default=None)
    a = ap.parse_args()
    raise SystemExit(1 if gop(a.goc, a.ra, a.manifest_sha256) else 0)
