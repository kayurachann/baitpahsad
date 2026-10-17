"""Chạy lại thí nghiệm 600 cover của bài từ 600 ảnh PGM gốc, dùng nguyên code/sg.py của nhóm.

Các bước (mỗi bước một lệnh con, có thể chạy lại từng bước):
  kiem-anh  <thư_mục_pgm>                  SHA-256 từng ảnh khớp data/stegaguard_600/source_provenance.json
  chuan-bi  <thư_mục_pgm> <thư_mục_dữ_liệu>  sg.prepare (seed 20260918, 256 × 256, conseal), so manifest với bản của nhóm;
            <thư_mục_pgm> phải chứa đúng 600 ảnh của source_provenance.json (kiểm bằng kiem-anh)
  tu-cover  <thư_mục_zip> <thư_mục_dữ_liệu>  thay cho 2 bước trên khi chỉ có 600 cover (code_nhom/gom_cover_600.py):
            kiểm SHA-256 cover, tạo lại 3.600 stego bằng conseal với embedding_seed của manifest, so SHA-256
  dac-trung <thư_mục_dữ_liệu> <thư_mục_đặc_trưng> [--workers 4]
            76 đặc trưng residual (sg.residual_features) và 34.671 đặc trưng SRM (sealwatch) cho 4.200 ảnh;
            lưu vào .npy, chạy dở thì chạy lại sẽ làm tiếp
  dac-trung-residual <thư_mục_dữ_liệu> <thư_mục_đặc_trưng>   chỉ 76 đặc trưng residual (vài phút)
  chay      <thư_mục_dữ_liệu> <thư_mục_đặc_trưng> <thư_mục_kết_quả> [--chi-residual]
            9 lần Residual-LR (giống hệt nhánh residual_lr của sg.train/evaluate) và 9 lần SRM+Ensemble
            (sealwatch FldEnsembleTrainer, L = 50, d_sub = 500, seed của lần chạy; cột SRM theo
            srm_thu_tu_nhom.txt; biến thể train rút theo thứ tự cover_id; điểm = predict_confidence, trung bình phiếu ±1
            của 50 FLD).
            Kết quả theo đúng định dạng sg.py: <run>/config.json, thresholds.json; <run>_test/predictions.csv, metrics.csv.

Sau đó: python3 gop_ket_qua.py <thư_mục_kết_quả>/<loại> gop --manifest-sha256 ... và verify_stats.py.
"""
import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import os
import random
import sys
from pathlib import Path

# Máy chạy thí nghiệm của nhóm (laptop) dùng nhân AVX2 "Haswell" của OpenBLAS. Trên máy có AVX-512, OpenBLAS chọn
# nhân SkylakeX, cộng dồn theo thứ tự khác; với Residual-LR P1 (đặc trưng gần ngẫu nhiên) lbfgs khi đó dừng ở điểm
# hơi khác và F1/BER lệch tới 0,012. Đặt Haswell thì P1 khớp Table 4 ở cả 6 ô. Phải đặt trước khi nạp numpy.
os.environ.setdefault("OPENBLAS_CORETYPE", "Haswell")

import numpy as np  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "code_nhom"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sg  # noqa: E402  code của nhóm, không sửa

DU_LIEU_NHOM = GOC / "data" / "stegaguard_600"
SEED_CHUAN_BI = 20260918
PROTOCOL = {"P1": (["wow"], [0.4]), "P2": (["wow", "suniward"], [0.4]), "P3": (["wow", "suniward"], [0.1, 0.4])}
TEN_RUN = {"P1": "single_wow_04", "P2": "mixed_algorithms_04", "P3": "mixed_algorithms_payloads"}
SEEDS = (42, 43, 44)
SRM_DIM = 34671


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ 1. ảnh gốc
def kiem_anh(thu_muc):
    prov = json.loads((DU_LIEU_NHOM / "source_provenance.json").read_text(encoding="utf-8"))
    sai = thieu = 0
    for f in prov["files"]:
        p = Path(thu_muc) / f["filename"]
        if not p.exists():
            thieu += 1
        elif sha256(p) != f["sha256"]:
            sai += 1
    print(f"{len(prov['files'])} ảnh trong provenance: thiếu {thieu}, sai SHA-256 {sai}")
    return thieu + sai


# ------------------------------------------------------------------ 2. chuẩn bị dữ liệu
def chuan_bi(thu_muc_pgm, ra):
    args = argparse.Namespace(covers=str(thu_muc_pgm), out=str(ra), size=256, limit=0, seed=SEED_CHUAN_BI,
                              algorithms=["wow", "suniward", "hill"], payloads=[0.1, 0.4])
    sg.prepare(args)
    moi = sg.read_rows(ra)
    cu = list(csv.DictReader(open(DU_LIEU_NHOM / "manifest.csv", newline="", encoding="utf-8")))
    # cột sha256 là hash của file PNG, đổi theo bản Pillow/zlib nén PNG; điểm ảnh thì nằm trong cover_id
    # (hash điểm ảnh của cover) và trong kết quả huấn luyện. So mọi cột khác theo đúng thứ tự dòng.
    cot = [c for c in cu[0] if c != "sha256"]
    lech = sum(any(str(a[c]) != str(b[c]) for c in cot) for a, b in zip(moi, cu)) + abs(len(moi) - len(cu))
    khac_png = sum(a["sha256"] != b["sha256"] for a, b in zip(moi, cu))
    sha_moi = sha256(Path(ra) / "manifest.csv")
    print(f"manifest mới {sha_moi[:8]}…{sha_moi[-7:]} ({len(moi)} dòng, nhóm {len(cu)} dòng)")
    print(f"  dòng lệch ở các cột {', '.join(cot)}: {lech}")
    print(f"  file PNG khác byte (chỉ do bộ nén PNG): {khac_png}")
    return sha_moi


# ------------------------------------------------------------------ 2b. dựng lại từ 600 cover
def tu_cover(thu_muc_zip, ra):
    """Giải nén covers600_phan*.zip (từ code_nhom/gom_cover_600.py), kiểm SHA-256 của cover, tạo lại 3.600 ảnh
    stego bằng conseal với đúng embedding_seed trong manifest (giống sg.prepare), rồi so SHA-256 với manifest."""
    import zipfile
    import conseal
    from PIL import Image
    ra = Path(ra)
    ra.mkdir(parents=True, exist_ok=True)
    zips = sorted(Path(thu_muc_zip).glob("*.zip"))
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            for ten in zf.namelist():
                dich = (ra / ten).resolve()
                if not str(dich).startswith(str(ra.resolve())):
                    raise ValueError(f"đường dẫn lạ trong zip: {ten}")
            zf.extractall(ra)
    print(f"đã giải nén {len(zips)} file zip")
    import shutil
    if not (ra / "manifest.csv").exists():          # zip "phẳng" chỉ có <cover_id>.png: dùng manifest của nhóm
        shutil.copy(DU_LIEU_NHOM / "manifest.csv", ra / "manifest.csv")
    sha_man = sha256(ra / "manifest.csv")
    if sha_man != sha256(DU_LIEU_NHOM / "manifest.csv"):
        raise ValueError("manifest.csv trong zip khác bản data/stegaguard_600/manifest.csv")
    rows = sg.read_rows(ra)
    covers = {r["cover_id"]: r for r in rows if r["label"] == "0"}
    for p in list(ra.rglob("*.png")):               # <cover_id>.png -> images/<cover_id>/cover.png
        if p.stem in covers:
            dich = ra / covers[p.stem]["path"]
            dich.parent.mkdir(parents=True, exist_ok=True)
            if not dich.exists():
                shutil.move(str(p), str(dich))
    thieu_cover = [r["path"] for r in covers.values() if not (ra / r["path"]).exists()]
    if thieu_cover:
        raise ValueError(f"thiếu {len(thieu_cover)} cover, ví dụ {thieu_cover[:3]}")
    sai_cover = [r["path"] for r in covers.values() if sha256(ra / r["path"]) != r["sha256"]]
    print(f"{len(covers)} cover, sai SHA-256: {len(sai_cover)}")
    if sai_cover:
        raise ValueError(f"cover sai SHA-256: {sai_cover[:3]}")
    # Bộ mã PNG ở đây có ghi ra đúng từng byte như máy của nhóm không? (lưu lại một cover và so)
    r0 = next(iter(covers.values()))
    x0 = np.asarray(Image.open(ra / r0["path"]))
    tmp = ra / "_thu_png.png"
    Image.fromarray(x0).save(tmp)
    png_giong = sha256(tmp) == r0["sha256"]
    tmp.unlink()
    print("bộ mã PNG ghi giống byte của nhóm:", png_giong)
    khop = khac = 0
    lech = []
    for r in rows:
        if r["label"] != "1":
            continue
        c = covers[r["cover_id"]]
        x = np.asarray(Image.open(ra / c["path"]))
        y = getattr(conseal, r["algorithm"]).simulate_single_channel(
            x0=x, alpha=float(r["payload"]), seed=int(r["embedding_seed"]))
        y = np.asarray(y)
        if y.shape != x.shape or y.min() < 0 or y.max() > 255 or np.abs(y.astype(int) - x.astype(int)).max() > 1:
            raise ValueError(f"đầu ra conseal bất thường: {r['path']}")
        dich = ra / r["path"]
        Image.fromarray(y.astype(np.uint8)).save(dich)
        if sha256(dich) == r["sha256"]:
            khop += 1
        else:
            khac += 1
            lech.append(r["path"])
    import importlib.metadata as md
    print(f"conseal {md.version('conseal')}: stego khớp SHA-256 {khop}/{khop + khac}")
    (ra / "tu_cover_ket_qua.json").write_text(json.dumps(dict(
        conseal=md.version("conseal"), png_giong=png_giong, stego_khop=khop, stego_khac=khac,
        vi_du_khac=lech[:10]), ensure_ascii=False, indent=2), encoding="utf-8")
    return khac


# ------------------------------------------------------------------ 3. đặc trưng
def _mot_anh(args):
    goc, i, path = args
    import khong_torch  # noqa: F401  sealwatch import được mà không cần torch
    import sealwatch
    import srm_nhanh
    srm_nhanh.bat()   # cooccurrence4 đếm bằng np.bincount: cùng kết quả từng bit, nhanh hơn khoảng 5 lần
    x = sg.pixels(goc, {"path": path})                       # float32, giống sg.score_pairs
    res = sg.residual_features(x)
    f = sealwatch.srm.extract(x.astype(np.uint8).astype(np.float64))
    # Ghép theo tên submodel đã sắp xếp: thứ tự của dict sealwatch trả về đổi theo hash seed của tiến trình
    # (symm.post_process duyệt một set khi gộp các khối SPAM), nên không dùng f.values() trực tiếp.
    srm = np.concatenate([np.asarray(f[k], dtype=np.float64).ravel() for k in sorted(f)])
    return i, res, srm


def dac_trung(goc, ra, workers=4, chi_anh_san=False):
    """chi_anh_san: chỉ trích các ảnh đã ghi xong (dùng trong lúc chuan-bi chưa chạy xong)."""
    ra = Path(ra)
    ra.mkdir(parents=True, exist_ok=True)
    rows = sg.read_rows(goc)
    paths = [r["path"] for r in rows]
    (ra / "paths.json").write_text(json.dumps(paths), encoding="utf-8")
    n = len(paths)
    mo = lambda ten, d: (np.lib.format.open_memmap(ra / ten, mode="r+") if (ra / ten).exists()  # noqa: E731
                         else np.lib.format.open_memmap(ra / ten, mode="w+", dtype=np.float64, shape=(n, d)))
    res, srm = mo("residual.npy", 76), mo("srm.npy", SRM_DIM)
    xong_p = ra / "xong.txt"
    xong = set(int(x) for x in xong_p.read_text().split()) if xong_p.exists() else set()
    viec = [(str(goc), i, p) for i, p in enumerate(paths) if i not in xong]
    # cover và WOW 0.4 trước, rồi các ảnh test: đủ để chạy P1 sớm trong lúc trích nốt phần còn lại
    uu_tien = {r["path"]: (0 if r["label"] == "0" or (r["algorithm"] == "wow" and r["payload"] == "0.4")
                           else 1 if r["split"] == "test" else 2) for r in rows}
    viec.sort(key=lambda v: uu_tien[v[2]])
    if chi_anh_san:   # ảnh đã ghi xong ít nhất 30 giây (PNG có thể khác byte do bản Pillow, nên không so SHA ở đây)
        import time
        viec = [v for v in viec if (Path(goc) / v[2]).exists() and time.time() - (Path(goc) / v[2]).stat().st_mtime > 30]
    print(f"{n} ảnh, còn {len(viec)} ảnh cần trích", flush=True)
    with mp.get_context("spawn").Pool(workers) as pool, open(xong_p, "a") as log:
        for k, (i, r, s) in enumerate(pool.imap_unordered(_mot_anh, viec, chunksize=4), 1):
            if s.size != SRM_DIM:
                raise ValueError(f"SRM {s.size} chiều ở ảnh {paths[i]}")
            res[i], srm[i] = r, s
            if k % 20 == 0 or k == len(viec):
                res.flush(); srm.flush()
            log.write(f"{i}\n"); log.flush()
            if k % 100 == 0:
                print(f"  {k}/{len(viec)}", flush=True)
    res.flush(); srm.flush()


def _mot_anh_residual(args):
    goc, i, path = args
    return i, sg.residual_features(sg.pixels(goc, {"path": path}))


def dac_trung_residual(goc, ra, workers=4):
    """Chỉ 76 đặc trưng residual (vài phút), để chạy Residual-LR kiểm dữ liệu trước khi SRM xong."""
    ra = Path(ra)
    ra.mkdir(parents=True, exist_ok=True)
    paths = [r["path"] for r in sg.read_rows(goc)]
    (ra / "paths.json").write_text(json.dumps(paths), encoding="utf-8")
    res = np.zeros((len(paths), 76))
    with mp.get_context("spawn").Pool(workers) as pool:
        for i, r in pool.imap_unordered(_mot_anh_residual, [(str(goc), i, p) for i, p in enumerate(paths)], chunksize=16):
            res[i] = r
    np.save(ra / "residual.npy", res)
    print(f"{len(paths)} ảnh, residual {res.shape}", flush=True)


# ------------------------------------------------------------------ 4. huấn luyện và đánh giá
def cot_srm_nhom():
    """Chỉ số cột đưa vector SRM (lưu theo tên submodel đã sắp xếp) về thứ tự ghép của nhóm (srm_thu_tu_nhom.txt).
    Thứ tự cột quyết định các không gian con ngẫu nhiên của FLD ensemble, nên phải đúng thì mới ra đúng số."""
    dong = [x.split("\t") for x in (Path(__file__).resolve().parent / "srm_thu_tu_nhom.txt").read_text(
        encoding="utf-8").splitlines() if x and not x.startswith("#")]
    kt = {k: int(n) for k, n in dong}
    dau, o = {}, 0
    for k in sorted(kt):
        dau[k] = o
        o += kt[k]
    assert o == SRM_DIM
    return np.concatenate([np.arange(dau[k], dau[k] + kt[k]) for k, _ in dong])


class DacTrung:
    def __init__(self, thu_muc):
        thu_muc = Path(thu_muc)
        paths = json.loads((thu_muc / "paths.json").read_text(encoding="utf-8"))
        self.idx = {p: i for i, p in enumerate(paths)}
        self.res = np.load(thu_muc / "residual.npy", mmap_mode="r")
        self.srm = np.load(thu_muc / "srm.npy", mmap_mode="r") if (thu_muc / "srm.npy").exists() else None
        self.cot = cot_srm_nhom()

    def lay(self, records, loai):
        ii = [self.idx[r["path"]] for r in records]
        if loai == "residual":
            return np.asarray(self.res[ii])
        return np.asarray(self.srm[ii])[:, self.cot]


def _chon_cap(goc, algorithms, payloads, seed, theo_cover_id=False):
    """Giống sg.train: một biến thể cho mỗi cover train, random.Random(seed).choice theo thứ tự manifest.
    theo_cover_id: duyệt cover theo cover_id tăng dần (cách của script SRM của nhóm)."""
    tr = sg.pairs(goc, "train", algorithms, payloads)
    groups = {}
    for c, s in tr:
        groups.setdefault(c["cover_id"], []).append((c, s))
    rr = random.Random(seed)
    keys = sorted(groups) if theo_cover_id else list(groups)
    return [rr.choice(groups[k]) for k in keys]



def _ghi_run(ra, ten, model, algorithms, payloads, seed, sha, th, du_doan, chi_so):
    run = Path(ra) / ten
    test = Path(ra) / f"{ten}_test"
    run.mkdir(parents=True, exist_ok=True)
    test.mkdir(parents=True, exist_ok=True)
    (run / "config.json").write_text(json.dumps(dict(model=model, algorithms=algorithms, payloads=payloads,
                                                     seed=seed, manifest_sha256=sha), indent=2), encoding="utf-8")
    (run / "thresholds.json").write_text(json.dumps(th, indent=2), encoding="utf-8")
    for ten_f, rows in (("predictions.csv", du_doan), ("metrics.csv", chi_so)):
        with open(test / ten_f, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def chay(goc, thu_muc_dt, ra, chi_residual=False):
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    import khong_torch  # noqa: F401
    from sealwatch.ensemble_classifier.fld_ensemble_trainer import FldEnsembleTrainer
    import verify_stats as V

    dt = DacTrung(thu_muc_dt)
    sha = sha256(Path(goc) / "manifest.csv")
    va_tat_ca = {p: sg.pairs(goc, "val", *PROTOCOL[p]) for p in PROTOCOL}
    test = {(a, b): sg.pairs(goc, "test", [a], [b]) for a in ("wow", "suniward", "hill") for b in (0.1, 0.4)}

    def danh_gia(score_fn, th):
        du_doan, chi_so = [], []
        for (a, b), pp in test.items():
            recs = [r for pair in pp for r in pair]
            y = [int(r["label"]) for r in recs]
            s = np.asarray(score_fn(recs), dtype=float)
            m = sg.scores_metrics(y, s, th["balanced"])
            low = sg.scores_metrics(y, s, th["low_fpr"])
            lo, hi = V.auc_ci(s[0::2], s[1::2], 1000, 2026)
            chi_so.append(dict(algorithm=a, payload=b, threshold=th["balanced"], **m,
                               recall_at_validation_low_fpr=low["recall"], actual_test_fpr=low["fpr"],
                               auc_ci_low=lo, auc_ci_high=hi))
            du_doan += [dict(cover_id=r["cover_id"], path=r["path"], label=int(r["label"]), test_algorithm=a,
                             payload=b, score=float(v)) for r, v in zip(recs, s)]
        return du_doan, chi_so

    def nguong(score_fn, va):
        flat = [r for pair in va for r in pair]
        seen, keep = set(), []
        for i, r in enumerate(flat):
            if r["path"] not in seen:
                keep.append(i)
                seen.add(r["path"])
        y = np.asarray([int(r["label"]) for r in flat])[keep]
        s = np.asarray(score_fn(flat), dtype=float)[keep]
        return sg.thresholds(y, s)

    for p, (algs, pls) in PROTOCOL.items():
        for seed in SEEDS:
            ten = f"{TEN_RUN[p]}_seed{seed}"
            chon = _chon_cap(goc, algs, pls, seed)
            records = [r for pair in chon for r in pair]
            # Residual-LR: giống nhánh residual_lr của sg.train
            model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed))
            model.fit(dt.lay(records, "residual"), [int(r["label"]) for r in records])
            fn = lambda recs: model.decision_function(dt.lay(recs, "residual"))  # noqa: E731
            th = nguong(fn, va_tat_ca[p])
            _ghi_run(Path(ra) / "residual_lr", ten, "residual_lr", algs, pls, seed, sha, th, *danh_gia(fn, th))
            if chi_residual:
                print(f"xong {ten} (Residual-LR)", flush=True)
                continue
            # SRM+Ensemble: FLD ensemble của sealwatch (L = 50, d_sub = 500, seed = seed của lần chạy), điểm =
            # trung bình phiếu ±1 của 50 FLD (predict_confidence). Script SRM của nhóm duyệt các cover train theo
            # cover_id (sg.py theo thứ tự manifest) khi rút một biến thể bằng random.Random(seed).choice, và đưa cặp
            # vào FLD theo thứ tự đó.
            # Cách này cho ra đúng 36/36 giá trị SRM+Ensemble của mỗi protocol trong Table 4/S1.
            chon_srm = _chon_cap(goc, algs, pls, seed, theo_cover_id=True)
            Xc = np.ascontiguousarray(dt.lay([c for c, _ in chon_srm], "srm"))
            Xs = np.ascontiguousarray(dt.lay([s for _, s in chon_srm], "srm"))
            ens, _ = FldEnsembleTrainer(Xc, Xs, seed=seed, L=50, d_sub=500, verbose=0).train()
            fn = lambda recs: ens.predict_confidence(dt.lay(recs, "srm"))  # noqa: E731
            th = nguong(fn, va_tat_ca[p])
            _ghi_run(Path(ra) / "srm_ensemble", ten, "srm_ensemble", algs, pls, seed, sha, th, *danh_gia(fn, th))
            print(f"xong {ten}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    a = sub.add_parser("kiem-anh"); a.add_argument("pgm")
    b = sub.add_parser("chuan-bi"); b.add_argument("pgm"); b.add_argument("ra")
    t = sub.add_parser("tu-cover"); t.add_argument("zip"); t.add_argument("ra")
    c = sub.add_parser("dac-trung"); c.add_argument("du_lieu"); c.add_argument("ra"); c.add_argument("--workers", type=int, default=4)
    c.add_argument("--chi-anh-san", action="store_true")
    r = sub.add_parser("dac-trung-residual"); r.add_argument("du_lieu"); r.add_argument("ra"); r.add_argument("--workers", type=int, default=4)
    d = sub.add_parser("chay"); d.add_argument("du_lieu"); d.add_argument("dac_trung"); d.add_argument("ra")
    d.add_argument("--chi-residual", action="store_true")
    x = ap.parse_args()
    if x.lenh == "kiem-anh":
        sys.exit(1 if kiem_anh(x.pgm) else 0)
    elif x.lenh == "chuan-bi":
        chuan_bi(x.pgm, x.ra)
    elif x.lenh == "tu-cover":
        sys.exit(1 if tu_cover(x.zip, x.ra) else 0)
    elif x.lenh == "dac-trung":
        dac_trung(x.du_lieu, x.ra, x.workers, x.chi_anh_san)
    elif x.lenh == "dac-trung-residual":
        dac_trung_residual(x.du_lieu, x.ra, x.workers)
    else:
        chay(x.du_lieu, x.dac_trung, x.ra, x.chi_residual)
