"""Sửa Paper_HoanChinh_1.docm theo 5 góp ý cuối của thầy, giữ nguyên cấu trúc, style và trường EndNote.

Cách chạy: python3 sua_hoanchinh.py <vao.docm> <ra.docm>

Nội dung sửa (chi tiết ở docs/PHAN_HOI_THAY_LAN_CUOI.md):
  - Mở đầu: câu trích [5-7] được viết lại cho đúng ba tài liệu nó trích (SRNet, ensemble, Yedroudj-Net);
    bỏ trích dẫn lặp [5, 7]. Thứ tự xuất hiện lần đầu của các tài liệu không đổi.
  - 3.1: ghi phép nội suy bicubic khi thu nhỏ ảnh (sg.py, prepare).
  - 3.2: cách tạo 76 đặc trưng, chuẩn hóa và tham số logistic regression, lấy từ code/sg.py và các mô hình đã lưu.
  - 3.5: số vòng bootstrap, seed của bộ sinh, cách lấy khoảng phân vị (sg.py, evaluate); nói rõ giới hạn của
    khoảng tin cậy. Cách gộp ΔAUC qua 3 seed không được thêm vì chưa có script phân tích để đối chiếu.
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
            ". Steganalysis detectors either feed noise-residual statistics, such as Spatial Rich Model (SRM) "
            "features, to a classifier like the Fisher linear discriminant ensemble, or train a convolutional neural "
            "network (CNN) such as SRNet or Yedroudj-Net ")
    de.thay(p, ", or train a convolutional neural network (CNN) such as Yedroudj-Net or SRNet ", "")
    de.xoa_truong(p, 2)  # trích dẫn lặp [5, 7]

    # 3.1: nội suy khi thu nhỏ ảnh
    p = tim(blks, "BOSSbase 1.01 contains 10,000 grayscale images")
    de.thay(p, "downsampled each to 256 × 256 before embedding",
            "downsampled each to 256 × 256 with bicubic interpolation before embedding")

    # 3.2: 76 đặc trưng, chuẩn hóa, tham số LR
    p = tim(blks, "Both detectors output a score")
    de.chen_sau(p, "regression . ", [(
        "The residuals are the first- and second-order horizontal and vertical pixel differences; each gives a "
        "normalized 17-bin histogram of its values clipped to [−8, 8] plus the mean absolute value and standard "
        "deviation of the unclipped residual (4 × 19 = 76 features). A StandardScaler fitted only on each run's "
        "training features standardizes all splits; the classifier uses L2 regularization with C = 1.0, the "
        "deterministic lbfgs solver, no class weights and max_iter = 2000, and its decision function is the score. ",
        False)])

    # câu thừa (đã có ở Table 2 và mục 3.3), bỏ để giữ 12 trang
    de.thay(p, " Both detectors keep the same settings in every protocol and seed, so the configuration cannot "
               "explain differences between protocols.", "")

    # 3.5: bootstrap
    p = tim(blks, "Each comparison is a paired difference")
    de.chen_sau(p, " images are never resampled on their own.", [
        (" The evaluation code resamples the 120 test covers B = 1,000 times with seed 2026, so every condition "
         "and run uses the same resampled cover IDs; the 2.5th and 97.5th percentiles give the 95% interval.", False),
    ])
    p = tim(blks, "Seed standard deviations (at most 0.028")
    de.thay(p, "so the intervals are conditional on this partition.",
            "so the intervals are conditional on this partition: they capture only test-cover sampling variation "
            "and do not extend to other image sources.")

    # 4.5: 54 dòng / 6.480 lượt chấm
    p = tim(blks, "Even the best cell")
    de.thay(p, "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions); in none of them were "
               "recall and FPR both zero, so the detectors were never completely silent. The rows hold 6,480 stego "
               "scores per detector, but these come from 720 distinct test stego images of 120 source covers and "
               "are repeated measurements, not 6,480 independent samples.",
            "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions) and 6,480 stego-score "
            "evaluations, but its nine models all score the same 720 test stego images of 120 source covers, so "
            "these are repeated measurements, not independent samples; the false positives in Table\xa07 are also "
            "repeated evaluations of the same 120 test covers.")


    # 3 (mở đầu): Fig. 1 không đánh số stage
    p = tim(blks, "Fig.\xa01 summarizes the pipeline")
    de.thay(p, " summarizes the pipeline. Stages 1-3 build a leakage-controlled dataset, stages 4-5 train the two "
               "detectors in parallel under protocols P1-P3, and stages 6-7 evaluate every trained model on one fixed "
               "set of test covers.",
            " summarizes the pipeline: the left column builds a leakage-controlled dataset, the two middle lanes "
            "train the detectors in parallel under protocols P1-P3, and the right side evaluates every trained model "
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
    de.thay(p, "Every run stores its per-image prediction scores,",
            "Every run stores its per-image test scores and validation thresholds,")

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
            "strongly between samples; an exchangeable test cover exceeds it with probability 2/121 ≈ 1.7%.")


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
