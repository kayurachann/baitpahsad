"""Gom 600 ảnh cover của bộ dữ liệu 600 ảnh (manifest SHA-256 13c01ca9...) thành vài file zip nhỏ.

Chạy trên máy đã chạy thí nghiệm (Windows):  py gom_cover_600.py
Script tự tìm thư mục dữ liệu trong thư mục người dùng (manifest.csv có SHA-256 đúng), kiểm
SHA-256 của từng cover.png theo manifest, rồi ghi covers600_phan1.zip, _phan2.zip, ... ra Desktop
(mỗi file khoảng 8 MB). Chỉ dùng thư viện có sẵn của Python, không sửa file nào trong thư mục dữ liệu.
"""
import csv
import hashlib
import os
import sys
import zipfile
from pathlib import Path

SHA_MANIFEST = "13c01ca998193e6925d599e43c6bf478021cac9759ff8a4b15e2a37a32799e8c"
MOI_PHAN = 200        # 200 ảnh mỗi file zip, khoảng 8-10 MB
BO_QUA = {"appdata", "site-packages", "node_modules", ".git", "$recycle.bin", "windows", "program files"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def tim_manifest(goc):
    print("Đang tìm manifest.csv của bộ 600 ảnh trong", goc, "...", flush=True)
    for thu_muc, con, tep in os.walk(goc):
        con[:] = [c for c in con if c.lower() not in BO_QUA]
        if "manifest.csv" in tep:
            p = Path(thu_muc) / "manifest.csv"
            try:
                if sha256(p) == SHA_MANIFEST:
                    return p
            except OSError:
                pass
    return None


def main():
    goc = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()
    man = tim_manifest(goc)
    if man is None:
        print("KHÔNG tìm thấy manifest.csv có SHA-256 13c01ca9... Hãy chạy: py gom_cover_600.py <thư mục chứa dữ liệu>")
        return 1
    du_lieu = man.parent
    print("Thấy bộ dữ liệu:", du_lieu)
    rows = [r for r in csv.DictReader(open(man, newline="", encoding="utf-8")) if r["label"] == "0"]
    thieu, sai = [], []
    for r in rows:
        p = du_lieu / r["path"]
        if not p.exists():
            thieu.append(r["path"])
        elif sha256(p) != r["sha256"]:
            sai.append(r["path"])
    print(f"{len(rows)} cover: thiếu {len(thieu)}, sai SHA-256 {len(sai)}")
    if thieu or sai:
        print("Dừng vì dữ liệu không khớp manifest. Ví dụ:", (thieu + sai)[:3])
        return 1
    ra = Path.home() / "Desktop"
    if not ra.exists():
        ra = Path.home()
    phan = [rows[i:i + MOI_PHAN] for i in range(0, len(rows), MOI_PHAN)]
    for k, nhom in enumerate(phan, 1):
        z = ra / f"covers600_phan{k}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            if k == 1:
                zf.write(man, "manifest.csv")
            for r in nhom:
                zf.write(du_lieu / r["path"], r["path"])
        print(f"Đã ghi {z} ({z.stat().st_size / 1e6:.1f} MB)")
    print(f"XONG. Kéo {len(phan)} file covers600_phan*.zip trên Desktop vào khung chat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
