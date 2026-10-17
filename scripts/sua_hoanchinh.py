"""Sửa Paper_HoanChinh_1.docm theo 5 góp ý cuối của thầy, giữ nguyên cấu trúc, style và trường EndNote.

Cách chạy: python3 sua_hoanchinh.py <vao.docm> <ra.docm>

Nội dung sửa (chi tiết ở docs/PHAN_HOI_THAY_LAN_CUOI.md):
  - Mở đầu: câu trích [5-7] được viết lại cho đúng ba tài liệu nó trích (SRNet, ensemble, Yedroudj-Net);
    bỏ trích dẫn lặp [5, 7]. Thứ tự xuất hiện lần đầu của các tài liệu không đổi.
  - 3.1: ghi phép nội suy bicubic khi thu nhỏ ảnh (sg.py, prepare).
  - 3.2: cách tạo 76 đặc trưng, chuẩn hóa và tham số logistic regression, lấy từ code/sg.py và các mô hình đã lưu.
  - 3.5: cách gộp ΔAUC qua 3 seed (rút chung một lần cho cả 3 seed, ΔAUC của replicate = trung bình 3 seed),
    B = 10.000, default_rng(2026), phân vị 2,5/97,5, đúng thủ tục của scripts/tinh_lai_ci.py (script ΔAUC gốc không
    còn); nói rõ giới hạn của khoảng tin cậy.
  - Kết quả chạy lại 600 cover (scripts/chay_lai_600.py, tinh_lai_ci.py): CI mới ở Abstract, mục 4, Kết luận,
    Table 5-6 và Fig. 2; câu 17/18 khoảng dưới 0; trung bình ΔAUC của Table 6 tính từ số chưa làm tròn; câu về
    điểm SRM ở 3.2; chú thích Table 7; [20] ghi sealwatch 2025.9.
  - 4.5: bỏ câu "never completely silent", viết lại câu 54 dòng / 6.480 lượt chấm.
  - Acknowledgement (UEH) trước References.
  - References: trình bày theo Springer LNCS, đúng thứ tự [1]–[20], metadata đã kiểm chứng; cập nhật luôn bản ghi
    EndNote nhúng trong các trường EN.CITE / EN.CITE.DATA.
  - Hình 1, 2: thay bằng bản 600 dpi gốc (cùng tỉ lệ khung).
"""
import base64
import copy
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docm_edit as de  # noqa: E402
from refs_hoanchinh import ENDNOTE_TYPE, REFS  # noqa: E402
from results_data import RQ1, RQ1_TRUOC, RQ2, RQ2_TRUOC, RQ3, RQ3_MEAN  # noqa: E402

# CI của RQ1/RQ2 trong bản trước (script ΔAUC gốc), để tìm đúng chỗ cần thay
RQ1_CU = {d: v[3] for d, v in RQ1_TRUOC.items()}
RQ2_CU = {d: v[3] for d, v in RQ2_TRUOC.items()}


def so(x):
    """Số có dấu kiểu bài: −0.093, +0.005; số 0 viết 0.000 (như kiem_tra_hoanchinh.py)."""
    x = round(x, 3) + 0.0
    return ("+" if x > 0 else "−" if x < 0 else "") + f"{abs(x):.3f}"

W = de.W
GOC = Path(__file__).resolve().parent.parent
HINH = {"word/media/image1.png": GOC / "figures" / "fig1_pipeline.png",
        "word/media/image2.png": GOC / "figures" / "fig2_payload_shift.png"}


def cac_khoi(root):
    return [b for b in root.find(W + "body") if b.tag in (W + "p", W + "tbl")]


def tim(blks, bat_dau):
    """Đoạn duy nhất có chữ bắt đầu bằng `bat_dau`."""
    hits = [b for b in blks if b.tag == W + "p" and de.van_ban(b).startswith(bat_dau)]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} đoạn bắt đầu bằng {bat_dau!r}")
    return hits[0]


# ---------------------------------------------------------------- nội dung
def sua_noi_dung(blks):
    # Mở đầu: câu trích [5-7]
    p = tim(blks, "Image steganography hides a message")
    de.thay(p, ". Steganalysis detectors either train a classifier on statistics of noise residuals, such as SPAM "
               "or the Spatial Rich Model (SRM) ",
            ". Steganalysis detectors either train a classifier such as the Fisher linear discriminant ensemble on "
            "noise-residual statistics like Spatial Rich Model (SRM) features, or train a convolutional neural "
            "network (CNN) such as SRNet or Yedroudj-Net ")
    de.thay(p, ", or train a convolutional neural network (CNN) such as Yedroudj-Net or SRNet ", "")
    de.xoa_truong(p, 2)  # trích dẫn lặp [5, 7]

    # 3.1: nội suy khi thu nhỏ ảnh
    p = tim(blks, "BOSSbase 1.01 contains 10,000 grayscale images")
    de.thay(p, "downsampled each to 256 × 256 before embedding",
            "bicubically downsampled each to 256 × 256 before embedding")
    # 3.1: ảnh stego tạo bằng mô phỏng nhúng của conseal (preparation.json của bộ 600 cover)
    p = tim(blks, "Leakage is prevented by the order of operations")
    de.thay(p, " at 0.1 and 0.4 bpp, giving six variants per cover",
            " at 0.1 and 0.4 bpp by the simulators in the conseal library (https://github.com/uibk-uncover/conseal), "
            "giving six variants per cover")

    # 3.2: 76 đặc trưng, chuẩn hóa, tham số LR
    p = tim(blks, "Both detectors output a score")
    de.chen_sau(p, "regression . ", [(
        "The residuals are the first- and second-order horizontal and vertical pixel differences. Each gives a "
        "normalized 17-bin histogram of its values clipped to [−8, 8] plus the mean absolute value and standard "
        "deviation of the unclipped residual (4 × 19 = 76 features). A StandardScaler fitted only on each run's "
        "training features standardizes all splits. The classifier uses L2 regularization with C = 1.0, the "
        "deterministic lbfgs solver, no class weights and max_iter = 2000. Its decision function is the score. ",
        False)])

    # câu thừa (đã có ở Table 2 và mục 3.3), bỏ để giữ 12 trang
    de.thay(p, " Both detectors keep the same settings in every protocol and seed, so the configuration cannot "
               "explain differences between protocols.", "")

    # 3.5: bootstrap
    p = tim(blks, "Each comparison is a paired difference")
    de.chen_sau(p, " images are never resampled on their own.", [
        # Script ΔAUC gốc của nhóm không còn. Chạy lại cho thấy CI trong bài theo cách gộp này (rút chung một lần
        # cho cả 3 seed, ΔAUC của replicate = trung bình 3 seed; lấy CI riêng từng seed thì lệch nhiều hơn hẳn), nhưng không khôi
        # phục được B và dòng số ngẫu nhiên. Mọi CI được tính lại bằng scripts/tinh_lai_ci.py (B = 10.000,
        # default_rng(2026)) từ điểm của lần chạy lại, nên bài ghi đúng thủ tục đã chạy.
        (" One draw serves all three seeds, and the replicate ΔAUC is the mean of the three per-seed differences. "
         "The 2.5th and 97.5th percentiles of B\xa0=\xa010,000 replicates (NumPy default_rng, seed 2026) give the "
         "95% interval.", False),
    ])
    p = tim(blks, "Seed standard deviations (at most 0.028")
    de.thay(p, "so the intervals are conditional on this partition.",
            "so the intervals are conditional on this partition: they account only for test-cover sampling and do "
            "not extend to other image sources.")

    # 4.5: 54 dòng / 6.480 lượt chấm
    p = tim(blks, "Even the best cell")
    de.thay(p, "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions); in none of them were "
               "recall and FPR both zero, so the detectors were never completely silent. The rows hold 6,480 stego "
               "scores per detector, but these come from 720 distinct test stego images of 120 source covers and "
               "are repeated measurements, not 6,480 independent samples.",
            "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions) and 6,480 stego-score "
            "evaluations, but its nine models all score the same 720 test stego images of 120 source covers. These "
            "scores are repeated measurements, not independent samples. The false positives in Table\xa07 are also "
            "repeated evaluations of the same 120 test covers.")


    # 3 (mở đầu): Fig. 1 không đánh số stage
    p = tim(blks, "Fig.\xa01 summarizes the pipeline")
    de.thay(p, " summarizes the pipeline. Stages 1-3 build a leakage-controlled dataset, stages 4-5 train the two "
               "detectors in parallel under protocols P1-P3, and stages 6-7 evaluate every trained model on one fixed "
               "set of test covers.",
            " shows the pipeline. The left column builds a leakage-controlled dataset, and the two middle lanes "
            "train both detectors in parallel under protocols P1-P3. The right side evaluates every trained model "
            "on one fixed set of test covers.")

    # Table 2 và 3.3: với Residual-LR (lbfgs, tất định) seed chỉ điều khiển việc rút biến thể
    t2 = next(b for b in blks if b.tag == W + "tbl" and de.van_ban(next(b.iter(W + "p"))) == "Setting")
    hang = [r for r in t2.iter(W + "tr") if de.van_ban(next(r.iter(W + "p"))) == "Seed-dependent parts"][0]
    o_lr = list(hang.iter(W + "tc"))[1]
    de.thay(next(o_lr.iter(W + "p")), "; random parts of model fitting", "")
    p = tim(blks, "The protocols in Table")
    de.thay(p, "Seeds 42, 43 and 44 control the variant draws and the random parts of model fitting.",
            "Seeds 42-44 control the variant draws and the random parts of SRM+Ensemble fitting.")

    # 3.5: điểm lưu theo code (điểm test và ngưỡng validation)
    p = tim(blks, "Seed standard deviations (at most 0.028")
    de.thay(p, "Every run stores its per-image prediction scores, and the manifest stores the embedding seed and "
               "SHA-256 hash of every image, so all tables can be recomputed from the saved files.",
            "Each run saves its per-image test scores and validation thresholds, and the manifest records the "
            "embedding seed and SHA-256 hash of every image. All tables can be recomputed from these files.")

    # 4.5: ba lần chạy Residual-LR P1 chắc chắn trùng nhau; câu về τlow
    p = tim(blks, "Table\xa07 reports the operating point")
    de.thay(p, "if its three runs are identical, as its zero seed spread suggests, that is 5/120 per run",
            "its three runs are identical (P1 has no variant sampling and the lbfgs fit is deterministic), so that is "
            "5/120 per run")
    de.thay(p, "A likely reason is that a 1% target on 120 covers places ", "A likely reason is that ")
    de.thay(p, " among the one or two highest validation scores, an extreme order statistic that varies strongly "
               "between samples. The least strict threshold allowed, just above the second-highest score, is exceeded "
               "by an exchangeable test cover with probability 2/121 ≈ 1.7%.",
            " rests on the second-highest of only 120 validation cover scores, an extreme order statistic that varies "
            "strongly between samples. An exchangeable test cover exceeds this threshold with probability "
            "2/121 ≈ 1.7%, or less when scores are tied.")


    # 2.3: [10] chỉ đỡ vế "algorithm shift … large CNN training sets"
    p = tim(blks, "Detector papers evaluate the matched condition")
    de.thay(p, "shift studies mostly concern the cover source or use large CNN training sets ",
            "shift studies mostly concern the cover source or, for algorithm shift, use large CNN training sets ")
    de.thay(p, "while also reporting the FPR", "while reporting the FPR")

    # Table 7: mean recall của SRM+Ensemble P2 tính từ số đếm nguyên (150/2,160 = 0.0694), không từ số đã làm tròn
    t7 = next(b for b in blks if b.tag == W + "tbl" and de.van_ban(next(b.iter(W + "p"))) == "Detector"
              and "Test false positives" in " ".join(de.van_ban(x) for x in b.iter(W + "p")))
    hang = [r for r in t7.iter(W + "tr") if [de.van_ban(x) for x in r.iter(W + "p")][1:3] == ["P2", "11/360"]]
    assert len(hang) == 1
    o = list(hang[0].iter(W + "tc"))[4]
    de.thay(next(o.iter(W + "p")), "0.070", "0.069")

    # ---- kết quả chạy lại 600 cover (scripts/chay_lai_600.py): Table 4/S1 trùng 216/216 giá trị; CI ΔAUC tính lại
    # với B = 10.000 (scripts/tinh_lai_ci.py), ước lượng điểm không đổi, cận CI đổi tối đa 0,003
    ci = lambda lo, hi: f"[{so(lo)}, {so(hi)}]"  # noqa: E731
    for d in ("Residual-LR", "SRM+Ensemble"):
        assert RQ1_CU[d] != RQ1[d][3] and RQ2_CU[d] != RQ2[d][3]
    cu1, moi1 = ci(*RQ1_CU["SRM+Ensemble"]), ci(*RQ1["SRM+Ensemble"][3])
    cu2, moi2 = ci(*RQ2_CU["SRM+Ensemble"]), ci(*RQ2["SRM+Ensemble"][3])
    p = tim(blks, "Abstract.")
    de.thay(p, "in all 18 comparisons (ΔAUC −0.022 to −0.183).",
            "in all 18 comparisons (ΔAUC −0.022 to −0.183; 17 of 18 intervals below zero).")
    de.thay(p, f"95% CI {cu1}", f"95% CI {moi1}")
    de.thay(p, f"95% CI {cu2}", f"95% CI {moi2}")
    de.thay(tim(blks, "Under P1, SRM+Ensemble falls from 0.714"), f"+0.024 {ci(*RQ1_CU['Residual-LR'])}",
            f"+0.024 {ci(*RQ1['Residual-LR'][3])}")
    de.thay(tim(blks, "Answer to RQ1."), f"95% CI {cu1}", f"95% CI {moi1}")
    p = tim(blks, "P3 adds 0.1 bpp WOW and S-UNIWARD variants")
    de.thay(p, f"95% CI {cu2}", f"95% CI {moi2}")
    de.thay(p, f"−0.005 {ci(*RQ2_CU['Residual-LR'])}", f"−0.005 {ci(*RQ2['Residual-LR'][3])}")
    p = tim(blks, "With the source-cover split fixed before embedding")
    de.thay(p, f"95% CI {cu1}", f"95% CI {moi1}")
    de.thay(p, "For RQ3, all 18 comparisons showed lower AUC", "For RQ3, all 18 point estimates showed lower AUC")
    # Fig. 2: khoảng Residual-LR P3 WOW giờ chạm 0 (cận trên +0,0003)
    assert RQ3[("Residual-LR", "P3", "WOW")][2] >= 0 and sum(v[2] < 0 for v in RQ3.values()) == 17
    p = tim(blks, "Fig.\xa02 shows ΔAUC between 0.1 and 0.4 bpp")
    de.thay(p, "All 18 differences are negative and all 18 intervals lie below zero. The SRM+Ensemble losses are about "
               "three times those of Residual-LR, and one Residual-LR interval ends at −0.001 (P3 WOW).",
            "All 18 differences are negative, and 17 of the 18 intervals lie below zero; the Residual-LR interval for "
            "P3 WOW reaches zero. The SRM+Ensemble losses are about three times those of Residual-LR.")
    de.thay(tim(blks, "Answer to RQ3."), "the weakest Residual-LR intervals end close to zero",
            "the weakest Residual-LR intervals end at or near zero")
    # Table 5
    t5 = next(b for b in blks if b.tag == W + "tbl" and "Reference AUC" in " ".join(de.van_ban(x) for x in b.iter(W + "p")))
    for cu, moi in ((RQ1_CU, RQ1), (RQ2_CU, RQ2)):
        for d in ("Residual-LR", "SRM+Ensemble"):
            o = [x for x in t5.iter(W + "p") if de.van_ban(x) == ci(*cu[d])]
            assert len(o) == 1, (d, ci(*cu[d]))
            de.thay(o[0], ci(*cu[d]), ci(*moi[d][3]))
    # Table 6: cận trên cao nhất và số CI < 0 của mỗi detector × protocol
    t6 = next(b for b in blks if b.tag == W + "tbl" and "Highest CI upper bound" in " ".join(de.van_ban(x) for x in b.iter(W + "p")))
    det = None
    for r in list(t6.iter(W + "tr"))[1:]:
        o = list(r.iter(W + "tc"))
        chu = [de.van_ban(next(c.iter(W + "p"))) for c in o]
        det = chu[0] or det
        his = [RQ3[(det, chu[1], a)][2] for a in ("WOW", "S-UNIWARD", "HILL")]
        # cột 4: trung bình ΔAUC từ số chưa làm tròn (bản trước lấy trung bình số đã làm tròn: SRM P1 −0.151)
        for i, moi in ((4, so(RQ3_MEAN[(det, chu[1])])), (5, so(max(his))), (6, f"{sum(h < 0 for h in his)}/3")):
            if chu[i] != moi:
                de.thay(next(o[i].iter(W + "p")), chu[i], moi)
    # 3.2: điểm của SRM+Ensemble (predict_confidence của sealwatch)
    de.thay(tim(blks, "Both detectors output a score"), "random feature subspaces of dimension dsub = 500.",
            "random feature subspaces of dimension dsub = 500. Its score is the mean of the 50 base-learner votes "
            "(±1).")
    # Table 7: số false positive đếm từ điểm test của từng lần chạy (từng seed ở Table S3)
    de.thay(tim(blks, "Table 7. Operating point at"),
            "False positives over seeds 42-44 (3 × 120 test covers) are implied by the reported mean test FPR "
            "(Suppl. Table S3)",
            "False positives are counted over seeds 42-44 (3 × 120 test covers; per seed in Suppl. Table S3)")

    # Acknowledgement trước References
    tieu_de = tim(blks, "References")
    truoc = tieu_de.getprevious()
    mau = tim(blks, "With the source-cover split fixed before embedding")
    de.doan_moi_sau(truoc, mau, [("Acknowledgement. ", False, True),
                                 ("This research is funded by the University of Economics Ho Chi Minh City, "
                                  "Vietnam (UEH).", False, False)])


# ---------------------------------------------------------------- References
def sua_tai_lieu(root):
    blks = cac_khoi(root)
    bib = [b for b in blks if b.tag == W + "p" and (b.find(f"{W}pPr/{W}pStyle") is not None)
           and b.find(f"{W}pPr/{W}pStyle").get(W + "val") == "EndNoteBibliography"]
    # đoạn tiếp nối của [8] (" vol. 2024, 2024.") bị tách dòng: xóa
    con = [b for b in bib if not re.match(r"^\[\d+\]", de.van_ban(b))]
    for b in con:
        b.getparent().remove(b)
    bib = [b for b in bib if b not in con]
    if len(bib) != len(REFS):
        raise ValueError(f"{len(bib)} đoạn tài liệu, cần {len(REFS)}")
    for p, ref in zip(bib, REFS):
        nhan = None
        for r in p.findall(W + "r"):
            t = r.find(W + "t")
            if t is not None and re.fullmatch(r"\[\d+\]", t.text or ""):
                nhan = r
                break
        if nhan is None or int(nhan.find(W + "t").text.strip("[]")) != ref["n"]:
            raise ValueError(f"không thấy nhãn [{ref['n']}]")
        lien_ket = p.find(W + "hyperlink")
        lien_ket = copy.deepcopy(lien_ket) if lien_ket is not None else None
        # xóa mọi thứ sau nhãn
        dang = False
        for x in list(p):
            if x is nhan:
                dang = True
                continue
            if dang:
                p.remove(x)
        de._dat(nhan.find(W + "t"), f"{ref['n']}.")
        r = copy.deepcopy(nhan)
        for t in r.findall(W + "t"):
            r.remove(t)
        etree.SubElement(r, W + "tab")
        t = etree.SubElement(r, W + "t")
        # thụt lề và giãn dòng theo style referenceitem của template LNCS (nhãn 0, chữ từ 341 twip)
        ind = p.find(f"{W}pPr/{W}ind")
        if ind is not None:
            ind.set(W + "left", "341")
            ind.set(W + "hanging", "341")
        # không ngắt dòng giữa "pp."/"p."/"vol." và số (như "pp.~" của LNCS)
        nb = lambda x: re.sub(r"\b(pp|p|vol)\. ", "\\1.\xa0", x)  # noqa: E731
        if ref.get("url") and lien_ket is not None:
            de._dat(t, nb(ref["lncs_truoc_url"]))
            p.append(r)
            for tt in lien_ket.iter(W + "t"):
                de._dat(tt, ref["url"])
            p.append(lien_ket)
            if ref["lncs_sau_url"]:
                r2 = copy.deepcopy(nhan)
                de._dat(r2.find(W + "t"), nb(ref["lncs_sau_url"]))
                p.append(r2)
        else:
            de._dat(t, nb(ref["lncs"]))
            p.append(r)


def ban_ghi_moi(ref, cu):
    """Bản ghi EndNote mới cho tài liệu `ref`, giữ rec-number và foreign-keys của bản ghi cũ."""
    rec = etree.Element("record")
    for tag in ("rec-number", "foreign-keys"):
        x = cu.find(tag)
        if x is not None:
            rec.append(copy.deepcopy(x))
    ten, ma = ENDNOTE_TYPE[ref["typ"]]
    rt = etree.SubElement(rec, "ref-type", name=ten)
    rt.text = ma
    au = etree.SubElement(etree.SubElement(rec, "contributors"), "authors")
    for a in ref["authors"]:
        etree.SubElement(au, "author").text = a
    ti = etree.SubElement(rec, "titles")
    etree.SubElement(ti, "title").text = ref["title"]
    etree.SubElement(ti, "secondary-title").text = ref["container"]
    if ref["typ"] == "JOUR":
        etree.SubElement(etree.SubElement(rec, "periodical"), "full-title").text = ref["container"]
    for k in ("pages", "volume", "number"):
        if ref.get(k):
            etree.SubElement(rec, k).text = ref[k]
    etree.SubElement(etree.SubElement(rec, "dates"), "year").text = ref["year"]
    if ref.get("place"):
        etree.SubElement(rec, "pub-location").text = ref["place"]
    if ref.get("publisher"):
        etree.SubElement(rec, "publisher").text = ref["publisher"]
    if ref.get("doi"):
        etree.SubElement(rec, "electronic-resource-num").text = ref["doi"]
    urls = etree.SubElement(rec, "urls")
    if ref.get("url"):
        etree.SubElement(etree.SubElement(urls, "related-urls"), "url").text = ref["url"]
    return rec


def sua_xml_endnote(chu):
    """Sửa chuỗi chứa <EndNote>…</EndNote>: Author/Year của mỗi Cite và bản ghi đi kèm."""
    a, b = chu.index("<EndNote>"), chu.rindex("</EndNote>") + len("</EndNote>")
    goc = etree.fromstring(chu[a:b].encode("utf-8"))
    theo_rec = {r["recnum"]: r for r in REFS}
    for cite in goc.iter("Cite"):
        rn = cite.findtext("RecNum")
        ref = theo_rec.get(rn)
        if ref is None:
            raise ValueError(f"RecNum {rn} không có trong danh mục")
        cite.find("Author").text = ref["authors"][0].split(",")[0]
        y = cite.find("Year")
        if y is None:
            y = etree.Element("Year")
            cite.find("Author").addnext(y)
        y.text = ref["year"]
        cu = cite.find("record")
        moi = ban_ghi_moi(ref, cu)
        cite.replace(cu, moi)
    return chu[:a] + etree.tostring(goc, encoding="unicode") + chu[b:]


def sua_ban_ghi_endnote(root):
    """Duyệt mọi trường EN.CITE (mã trong instrText) và EN.CITE.DATA (base64 trong fldData)."""
    so_truong = 0
    for p in root.iter(W + "p"):
        ngan = []
        for el in p.iter():
            if el.tag == W + "fldChar":
                t = el.get(W + "fldCharType")
                if t == "begin":
                    ngan.append({"instr": [], "data": el.find(W + "fldData"), "gd": "instr"})
                elif t == "separate" and ngan:
                    ngan[-1]["gd"] = "result"
                elif t == "end" and ngan:
                    f = ngan.pop()
                    chu = "".join(x.text or "" for x in f["instr"])
                    if "ADDIN EN.CITE" in chu and "<EndNote>" in chu:
                        moi = sua_xml_endnote(chu)
                        de._dat(f["instr"][0], moi)
                        for x in f["instr"][1:]:
                            de._dat(x, "")
                        so_truong += 1
                    elif "EN.CITE.DATA" in chu and f["data"] is not None:
                        goc_b64 = f["data"].text or ""
                        raw = base64.b64decode(goc_b64).decode("utf-8")
                        moi = base64.encodebytes(sua_xml_endnote(raw).encode("utf-8")).decode("ascii")
                        f["data"].text = moi if goc_b64.endswith("\n") else moi.rstrip("\n")
                        so_truong += 1
            elif el.tag == W + "instrText" and ngan and ngan[-1]["gd"] == "instr":
                ngan[-1]["instr"].append(el)
    return so_truong


# ---------------------------------------------------------------- đóng gói
def sua_style_tai_lieu(styles_xml):
    """Style "EndNote Bibliography" theo referenceitem của template LNCS: chữ 9 pt, giãn dòng 11 pt, canh trái."""
    st = etree.fromstring(styles_xml)
    s = next(x for x in st.iter(W + "style") if x.get(W + "styleId") == "EndNoteBibliography")
    ppr = s.find(W + "pPr")
    if ppr is None:
        ppr = etree.Element(W + "pPr")
        s.find(W + "rPr").addprevious(ppr)
    for tag in ("spacing", "ind", "jc"):
        for x in ppr.findall(W + tag):
            ppr.remove(x)
    sp = etree.SubElement(ppr, W + "spacing")
    sp.set(W + "line", "220")
    sp.set(W + "lineRule", "atLeast")
    ind = etree.SubElement(ppr, W + "ind")
    ind.set(W + "left", "341")
    ind.set(W + "hanging", "341")
    jc = etree.SubElement(ppr, W + "jc")
    jc.set(W + "val", "left")
    rpr = s.find(W + "rPr")
    for tag in ("sz", "szCs"):
        x = etree.SubElement(rpr, W + tag)
        x.set(W + "val", "18")
    return etree.tostring(st, xml_declaration=True, encoding="UTF-8", standalone=True)


def sua_cai_dat_endnote(data):
    """settings.xml: tắt Instant Formatting của EndNote để References đã sửa không bị sinh lại tự động
    theo style IEEE và thư viện cũ khi mở file; cỡ chữ và thụt lề của EN.Layout theo style referenceitem."""
    s = data.decode("utf-8")
    cu = ["&lt;Enabled&gt;1&lt;/Enabled&gt;", "&lt;FontSize&gt;10&lt;/FontSize&gt;",
          "&lt;HangingIndent&gt;720&lt;/HangingIndent&gt;"]
    moi = ["&lt;Enabled&gt;0&lt;/Enabled&gt;", "&lt;FontSize&gt;9&lt;/FontSize&gt;",
           "&lt;HangingIndent&gt;341&lt;/HangingIndent&gt;"]
    for a, b in zip(cu, moi):
        if s.count(a) != 1:
            raise ValueError(f"settings.xml: không thấy đúng một {a}")
        s = s.replace(a, b)
    return s.encode("utf-8")


def main(vao, ra):
    zin = zipfile.ZipFile(vao)
    root = etree.fromstring(zin.read("word/document.xml"))
    sua_noi_dung(cac_khoi(root))
    sua_tai_lieu(root)
    n = sua_ban_ghi_endnote(root)
    print("đã cập nhật bản ghi EndNote trong", n, "trường")
    xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(ra, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/document.xml":
                data = xml
            elif item.filename == "word/styles.xml":
                data = sua_style_tai_lieu(zin.read(item.filename))
            elif item.filename == "word/settings.xml":
                data = sua_cai_dat_endnote(zin.read(item.filename))
            elif item.filename in HINH:
                data = HINH[item.filename].read_bytes()
            else:
                data = zin.read(item.filename)
            zout.writestr(item, data)
    print("đã ghi", ra)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
