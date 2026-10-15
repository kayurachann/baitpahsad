"""Sửa Paper_HoanChinh_1.docm theo 5 góp ý cuối của thầy, giữ nguyên cấu trúc, style và trường EndNote.

Cách chạy: python3 sua_hoanchinh.py <vao.docm> <ra.docm>

Nội dung sửa (chi tiết ở docs/PHAN_HOI_THAY_LAN_CUOI.md):
  - Mở đầu: câu trích [5-7] được viết lại cho đúng ba tài liệu nó trích (SRNet, ensemble, Yedroudj-Net);
    bỏ trích dẫn lặp [5, 7]. Thứ tự xuất hiện lần đầu của các tài liệu không đổi.
  - 3.1: ghi phép nội suy bicubic khi thu nhỏ ảnh (sg.py, prepare).
  - 3.2: cách tạo 76 đặc trưng, chuẩn hóa và tham số logistic regression, lấy từ code/sg.py và các mô hình đã lưu.
  - 3.5: số vòng bootstrap, seed của bộ sinh, cách lấy khoảng phân vị (sg.py, evaluate); phần gộp ΔAUC qua 3 seed
    chưa có script nên được tô vàng; nói rõ giới hạn của khoảng tin cậy.
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
            ". Steganalysis detectors either feed statistics of noise residuals, such as Spatial Rich Model (SRM) "
            "features, to a classifier such as an ensemble of linear discriminants, or train a convolutional neural "
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
        "The residuals are the first- and second-order horizontal and vertical pixel differences; each is "
        "summarized by a normalized 17-bin histogram of its values clipped to [−8, 8] plus its mean absolute value "
        "and standard deviation, giving 4 × 19 = 76 features. A StandardScaler fitted on the training features of "
        "each run only rescales all splits, and the L2-regularized classifier uses C = 1.0, the lbfgs solver, no "
        "class weights (training pairs are balanced), max_iter = 2,000 and the run seed as random_state; its "
        "decision function is the score. ",
        False)])

    # 3.5: bootstrap
    p = tim(blks, "Each comparison is a paired difference")
    de.chen_sau(p, " images are never resampled on their own.", [
        (" The evaluation code draws B = 1,000 replicates per test condition from a generator with the fixed seed "
         "2026, so all conditions, protocols and seeds share the same resampled cover IDs, and takes the 2.5th and "
         "97.5th percentiles as the 95% interval.", False),
        (" Each ΔAUC replicate is the difference of the two replicate AUCs, averaged over the three seeds.", True),
    ])
    p = tim(blks, "Seed standard deviations (at most 0.028")
    de.thay(p, "so the intervals are conditional on this partition.",
            "so the intervals are conditional on this partition: they describe variation over the fixed 120 test "
            "covers only and do not represent other image sources.")

    # 4.5: 54 dòng / 6.480 lượt chấm
    p = tim(blks, "Even the best cell")
    de.thay(p, "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions); in none of them were "
               "recall and FPR both zero, so the detectors were never completely silent. The rows hold 6,480 stego "
               "scores per detector, but these come from 720 distinct test stego images of 120 source covers and "
               "are repeated measurements, not 6,480 independent samples.",
            "Each detector has 54 evaluation rows (3 protocols × 3 seeds × 6 conditions) and 6,480 stego-score "
            "evaluations, but its nine models all score the same 720 test stego images of 120 source covers, so "
            "these are repeated measurements, not independent samples; the false positives in Table 7 are likewise "
            "repeated evaluations of the same 120 test covers.")

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
        if ref.get("url") and lien_ket is not None:
            de._dat(t, ref["lncs_truoc_url"])
            p.append(r)
            for tt in lien_ket.iter(W + "t"):
                de._dat(tt, ref["url"])
            p.append(lien_ket)
            r2 = copy.deepcopy(nhan)
            de._dat(r2.find(W + "t"), ref["lncs_sau_url"])
            p.append(r2)
        else:
            de._dat(t, ref["lncs"])
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
            elif item.filename in HINH:
                data = HINH[item.filename].read_bytes()
            else:
                data = zin.read(item.filename)
            zout.writestr(item, data)
    print("đã ghi", ra)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
