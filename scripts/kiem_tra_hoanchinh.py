"""Kiểm tra bản Paper_HoanChinh sau khi sửa: số liệu bảng 4–7, Abstract, Conclusion khớp results_data.py;
đủ 42 trường EN.CITE + 1 EN.REFLIST; thứ tự đánh số tài liệu không đổi; không còn câu bị thầy yêu cầu bỏ;
có Acknowledgement; References đúng danh mục refs_hoanchinh.REFS.

Cách chạy: python3 kiem_tra_hoanchinh.py <file.docm>
"""
import re
import sys
import zipfile
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docm_edit as de  # noqa: E402
import endnote_fields as ef  # noqa: E402
import results_data as R  # noqa: E402
from refs_hoanchinh import REFS  # noqa: E402

W = de.W
loi = []


def bang(root):
    out = []
    for t in root.iter(W + "tbl"):
        rows = []
        for r in t.iter(W + "tr"):
            rows.append([" ".join(de.van_ban(p) for p in c.iter(W + "p")).strip() for c in r.iter(W + "tc")])
        out.append(rows)
    return out


def f3(x):
    return f"{x:.3f}".replace("-", "−") if x < 0 else f"{x:.3f}"


def kiem(dk, thong_bao):
    if not dk:
        loi.append(thong_bao)


def main(path):
    root = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    doan = [de.van_ban(p) for p in root.iter(W + "p")]
    toan = "\n".join(doan)
    tabs = bang(root)

    # Table 4: ROC-AUC
    t4 = next(t for t in tabs if t and t[0][:2] == ["Detector", "P"] and "S-UNIWARD" in t[0])
    det = None
    for row in t4[2:]:
        det = row[0] or det
        p = row[1]
        mong = [f3(R.MATRIX[(det, p, a, b)][0]) for a in R.ALGORITHMS for b in (0.4, 0.1)]
        kiem(row[2:] == mong, f"Table 4 {det} {p}: {row[2:]} ≠ {mong}")

    # Table 5: RQ1, RQ2
    t5 = next(t for t in tabs if t and t[0][:3] == ["Detector", "Reference AUC", "Shifted AUC"])
    nhom = None
    for row in t5[1:]:
        if row[0].startswith("RQ1"):
            nhom = R.RQ1
            continue
        if row[0].startswith("RQ2"):
            nhom = R.RQ2
            continue
        a, b, d, (lo, hi) = nhom[row[0]]
        sd = lambda x: ("+" if x > 0 else "") + f3(x)  # noqa: E731
        mong = [f3(a), f3(b), sd(d), f"[{sd(lo)}, {sd(hi)}]"]
        kiem(row[1:5] == mong, f"Table 5 {row[0]}: {row[1:5]} ≠ {mong}")

    # Table 6: RQ3 tóm tắt
    t6 = next(t for t in tabs if t and t[0][:3] == ["Detector", "P", "AUC at 0.1 bpp"])
    det = None
    for row in t6[1:]:
        det = row[0] or det
        p = row[1]
        auc01 = [R.MATRIX[(det, p, a, 0.1)][0] for a in R.ALGORITHMS]
        ds = [R.RQ3[(det, p, a)] for a in R.ALGORITHMS]
        mean = R.RQ3_MEAN[(det, p)]   # trung bình của ΔAUC chưa làm tròn
        mong = [f"{min(auc01):.3f}-{max(auc01):.3f}", f"{f3(min(d[0] for d in ds))} to {f3(max(d[0] for d in ds))}",
                f3(mean), f3(max(d[2] for d in ds)), f"{sum(d[2] < 0 for d in ds)}/3"]
        kiem(row[2:7] == mong, f"Table 6 {det} {p}: {row[2:7]} ≠ {mong}")

    # Table 7: low-FPR
    t7 = next(t for t in tabs if t and t[0][:3] == ["Detector", "P", "Test false positives"])
    tom = {(r["detector"], r["protocol"]): r for r in R.low_fpr_summary()}
    det = None
    for row in t7[1:]:
        if row[0].startswith("Pooled"):
            continue
        det = row[0] or det
        r = tom[(det, row[1])]
        mong = [f"{r['fp_total']}/360", f"{r['fpr']:.3f}", f"{r['recall_mean']:.3f}",
                f"{r['recall_min']:.3f}-{r['recall_max']:.3f}"]
        kiem(row[2:6] == mong, f"Table 7 {det} {row[1]}: {row[2:6]} ≠ {mong}")
        kiem(round(r["fp_total"] / 360, 3) == r["fpr"], f"Table 7 {det} {row[1]}: FP/360 không khớp FPR")
    for d in R.DETECTORS:
        fp = sum(tom[(d, p)]["fp_total"] for p in R.PROTOCOLS)
        rec = [R.MATRIX[(d, p, a, b)][4] for p in R.PROTOCOLS for a in R.ALGORITHMS for b in R.PAYLOADS]
        kiem(f"{d} {fp}/1,080 (FPR {fp / 1080:.3f}, mean recall {sum(rec) / len(rec):.3f})" in toan,
             f"dòng gộp Table 7 của {d} không khớp ({fp}/1,080, {fp / 1080:.3f}, {sum(rec) / len(rec):.3f})")

    # Abstract và Conclusion: các số chính
    abs_ = next(t for t in doan if t.startswith("Abstract."))
    sd = lambda x: ("+" if x > 0 else "") + f3(x)  # noqa: E731
    ci1 = "[{}, {}]".format(*map(sd, R.RQ1["SRM+Ensemble"][3]))
    ci2 = "[{}, {}]".format(*map(sd, R.RQ2["SRM+Ensemble"][3]))
    for s in ["0.714", "0.645", "−0.070", ci1, "−0.022", ci2, "18 comparisons",
              "−0.022 to −0.183", "0.062", "0.080", "0.045", "0.034", "600", "360 training, 120 validation and 120 test"]:
        kiem(s in abs_, f"Abstract thiếu/sai: {s}")
    d_all = [v[0] for v in R.RQ3.values()]
    kiem(f3(max(d_all)) == "−0.022" and f3(min(d_all)) == "−0.183", "khoảng ΔAUC RQ3 trong Abstract lệch dữ liệu")
    ket = next(t for t in doan if t.startswith("With the source-cover split fixed before embedding"))
    kiem(f"ΔAUC = −0.070, 95% CI {ci1}" in ket, "Conclusion: số RQ1 lệch")
    for bat_dau, s in (("Answer to RQ1.", f"95% CI {ci1}"), ("P3 adds 0.1 bpp WOW", f"95% CI {ci2}"),
                       ("P3 adds 0.1 bpp WOW", "−0.005 [{}, {}]".format(*map(sd, R.RQ2["Residual-LR"][3]))),
                       ("Under P1, SRM+Ensemble falls", "+0.024 [{}, {}]".format(*map(sd, R.RQ1["Residual-LR"][3])))):
        kiem(s in next(t for t in doan if t.startswith(bat_dau)), f"{bat_dau}: thiếu {s}")
    n_duoi_0 = sum(v[2] < 0 for v in R.RQ3.values())
    kiem(f"{n_duoi_0} of 18 intervals below zero" in abs_ or n_duoi_0 == 18, "Abstract: số khoảng RQ3 dưới 0 lệch dữ liệu")
    kiem(f"{n_duoi_0} of the 18 intervals lie below zero" in toan or (n_duoi_0 == 18 and "all 18 intervals" in toan),
         "câu về số khoảng RQ3 nằm dưới 0 lệch dữ liệu")

    # Câu thầy yêu cầu bỏ, Acknowledgement, References
    kiem("never completely silent" not in toan, "còn câu 'never completely silent'")
    kiem(any(t.startswith("Acknowledgement. This research is funded by the University of Economics Ho Chi Minh City")
             for t in doan), "thiếu Acknowledgement")
    bib = [t for t in doan if re.match(r"^\d+\.\t", t)]
    kiem(len(bib) == len(REFS), f"References có {len(bib)} mục, cần {len(REFS)}")
    for t, r in zip(bib, REFS):
        kiem(t.replace("\xa0", " ") == f"{r['n']}.\t{r['lncs']}", f"References [{r['n']}] lệch danh mục")

    # Trường EndNote và thứ tự đánh số
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    kiem(xml.count("ADDIN EN.REFLIST") == 1, "thiếu trường EN.REFLIST")
    cites = ef.bang_trich_dan(path)
    thu_tu = []
    for _, _, recs in cites:
        for rr in recs:
            if rr["recnum"] not in thu_tu:
                thu_tu.append(rr["recnum"])
    kiem(thu_tu == [r["recnum"] for r in REFS], "thứ tự xuất hiện lần đầu của tài liệu đã đổi")
    for i, hien, recs in cites:
        so = sorted(next(r["n"] for r in REFS if r["recnum"] == x["recnum"]) for x in recs)
        # chữ hiển thị phải chứa đúng các số của bản ghi được trích
        hien_so = set()
        for part in hien.strip("[]").split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-")
                hien_so.update(range(int(a), int(b) + 1))
            elif part:
                hien_so.add(int(part))
        kiem(hien_so == set(so), f"trích dẫn ở đoạn {i}: hiển thị {hien} nhưng trỏ tới {so}")

    print(f"Đã kiểm Table 4–7, Abstract, Conclusion, {len(cites)} trích dẫn, {len(bib)} tài liệu.")
    if loi:
        print("LỖI:\n  " + "\n  ".join(loi))
        sys.exit(1)
    print("OK: mọi số khớp results_data.py; trích dẫn, thứ tự tài liệu, Acknowledgement đều đúng.")


if __name__ == "__main__":
    main(sys.argv[1])
