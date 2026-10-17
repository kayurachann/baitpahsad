"""Bản nhanh của sealwatch.srm.cooccurrence.cooccurrence4 (cho ra cùng kết quả, từng bit).

Bản gốc đếm bảng đồng xuất hiện 4 chiều [-T, T]^4 bằng bốn vòng lặp Python lồng nhau (khoảng 7 trong 9 giây
trích SRM của một ảnh 256 × 256). Ở đây đếm cùng các bộ (L, C, E, R) có cả bốn giá trị là số nguyên trong
[-T, T], bằng np.bincount, rồi chia cho tổng như bản gốc. Bảng đếm là số nguyên nên kết quả trùng khít.

Dùng: import srm_nhanh; srm_nhanh.bat()  (thay hàm trong module sealwatch.srm.cooccurrence)
Kiểm: python3 srm_nhanh.py <thư_mục_dữ_liệu> [số_ảnh]   so toàn bộ 34.671 đặc trưng với bản gốc
"""
import numpy as np


def cooccurrence4(D, type, T):
    B = 2 * T + 1
    if type == "hor":
        L, C, E, R = D[:, :-3], D[:, 1:-2], D[:, 2:-1], D[:, 3:]
    elif type == "ver":
        L, C, E, R = D[:-3], D[1:-2], D[2:-1], D[3:]
    elif type == "diag":
        L, C, E, R = D[:-3, :-3], D[1:-2, 1:-2], D[2:-1, 2:-1], D[3:, 3:]
    elif type == "mdiag":
        L, C, E, R = D[3:, :-3], D[2:-1, 1:-2], D[1:-2, 2:-1], D[:-3, 3:]
    elif type == "square":
        L, C, E, R = D[1:, :-1], D[1:, 1:], D[:-1, 1:], D[:-1, :-1]
    else:
        raise NotImplementedError(f"type {type} not implemented")   # bản gốc lỗi với 'square-ori'
    ma = np.ones(L.shape, dtype=bool)
    for A in (L, C, E, R):
        ma &= (A >= -T) & (A <= T) & (A == np.round(A))
    idx = np.zeros(int(ma.sum()), dtype=np.int64)
    for A in (L, C, E, R):
        idx = idx * B + (A[ma].astype(np.int64) + T)
    cooc_mat = np.bincount(idx, minlength=B ** 4).reshape(B, B, B, B).astype(int)
    return cooc_mat / np.sum(cooc_mat)


SO_LAN_GOI = [0]


def _dem(D, type, T):
    SO_LAN_GOI[0] += 1
    return cooccurrence4(D, type, T)


def bat(ham=None):
    """Thay hàm gốc bằng `ham` (mặc định bản nhanh, có đếm số lần gọi). Các hàm all1st ... all5x5 nhận hàm
    đếm qua tham số mặc định CoocN = cooccurrence4 gắn lúc định nghĩa, nên phải thay trong __defaults__ và
    __kwdefaults__ chứ gán lại tên trong module là không đủ."""
    import sealwatch.srm.cooccurrence as co
    if not hasattr(co, "_cooccurrence4_goc"):
        co._cooccurrence4_goc = co.cooccurrence4
    goc, moi = co._cooccurrence4_goc, ham or _dem
    for f in vars(co).values():
        if callable(f) and hasattr(f, "__defaults__"):
            if f.__defaults__:
                f.__defaults__ = tuple(moi if (d is goc or d is _dem) else d for d in f.__defaults__)
            if f.__kwdefaults__:
                f.__kwdefaults__ = {k: (moi if (d is goc or d is _dem) else d) for k, d in f.__kwdefaults__.items()}
    co.cooccurrence4 = moi


def bo():
    import sealwatch.srm.cooccurrence as co
    if hasattr(co, "_cooccurrence4_goc"):
        bat(co._cooccurrence4_goc)


if __name__ == "__main__":
    import csv
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code_nhom"))
    import khong_torch  # noqa: F401
    import sealwatch
    import sealwatch.srm.cooccurrence as co
    import sg
    goc = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    rows = list(csv.DictReader(open(Path(goc) / "manifest.csv", newline="", encoding="utf-8")))
    chon = rows[::max(1, len(rows) // n)][:n]
    import time
    lech = 0
    for r in chon:
        x = sg.pixels(goc, r).astype(np.uint8).astype(np.float64)
        bo()
        t0 = time.time(); a = sealwatch.srm.extract(x); t1 = time.time()
        bat()
        truoc = SO_LAN_GOI[0]
        b = sealwatch.srm.extract(x); t2 = time.time()
        goi = SO_LAN_GOI[0] - truoc
        same = list(a) == list(b) and all(np.array_equal(a[k], b[k]) and a[k].dtype == b[k].dtype for k in a)
        lech += (not same) or goi == 0
        print(f"{r['path']}: {'trùng từng bit' if same else 'KHÁC'}; bản nhanh được gọi {goi} lần; "
              f"{t1 - t0:.1f} s -> {t2 - t1:.1f} s")
    print(f"{len(chon)} ảnh, {lech} ảnh khác hoặc không gọi bản nhanh")
    sys.exit(1 if lech else 0)
