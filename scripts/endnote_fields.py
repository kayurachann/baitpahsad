"""Đọc các trường EndNote (ADDIN EN.CITE / EN.CITE.DATA / EN.REFLIST) trong document.xml của file .docm/.docx.

Dùng chung cho kiểm tra trích dẫn và cho script sửa bài: mỗi trường EN.CITE trả về đoạn chứa nó, chữ hiển thị
(ví dụ "[5-7]"), danh sách bản ghi được trích (RecNum, tác giả đầu, năm, tiêu đề) và vị trí trong đoạn.
Cách chạy (in bảng trích dẫn): python3 endnote_fields.py <file.docm>
"""
import base64
import html
import re
import sys
import zipfile

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def doan_va_bang(body):
    """Liệt kê các đoạn của thân bài theo thứ tự, kể cả đoạn trong bảng (giống chỉ số của dump_docm)."""
    for blk in body:
        if blk.tag in (W + "p", W + "tbl"):
            yield blk


def cac_truong(p):
    """Tách các trường trong một đoạn (hoặc bảng). Mỗi trường: instr (mã), data (fldData), ket_qua (chữ hiển thị),
    long (độ lồng), cùng chỉ số run bắt đầu/kết thúc."""
    ket = []
    ngan_xep = []
    for el in p.iter():
        if el.tag == W + "fldChar":
            t = el.get(W + "fldCharType")
            if t == "begin":
                data = el.find(W + "fldData")
                ngan_xep.append({"instr": [], "data": data.text if data is not None else None,
                                 "ket_qua": [], "giai_doan": "instr", "long": len(ngan_xep), "begin": el})
            elif t == "separate" and ngan_xep:
                ngan_xep[-1]["giai_doan"] = "result"
            elif t == "end" and ngan_xep:
                f = ngan_xep.pop()
                f["end"] = el
                ket.append(f)
        elif el.tag == W + "instrText" and ngan_xep:
            ngan_xep[-1]["instr"].append(el.text or "")
        elif el.tag == W + "t" and ngan_xep and ngan_xep[-1]["giai_doan"] == "result":
            for f in ngan_xep:
                f["ket_qua"].append(el.text or "")
    for f in ket:
        f["instr"] = "".join(f["instr"])
        f["ket_qua"] = "".join(f["ket_qua"])
    return ket


def ban_ghi(instr, data):
    """Lấy XML <EndNote> của một EN.CITE: nằm ngay trong mã trường, hoặc trong fldData (base64) của EN.CITE.DATA."""
    if "<EndNote>" in instr:
        xml = instr[instr.index("<EndNote>"):]
    elif data:
        xml = base64.b64decode(data).decode("utf-8", "replace")
        xml = xml[xml.index("<EndNote>"):] if "<EndNote>" in xml else xml
    else:
        return []
    xml = xml[: xml.rindex("</EndNote>") + len("</EndNote>")]
    goc = etree.fromstring(xml.encode("utf-8"), etree.XMLParser(recover=True))
    out = []
    for cite in goc.iter("Cite"):
        rec = cite.find("record")
        tieu_de = rec.findtext("titles/title") if rec is not None else None
        out.append({
            "author": cite.findtext("Author"), "year": cite.findtext("Year"), "recnum": cite.findtext("RecNum"),
            "title": "".join(rec.find("titles/title").itertext()) if rec is not None and rec.find("titles/title") is not None else tieu_de,
        })
    return out


def doc_document(duong_dan):
    z = zipfile.ZipFile(duong_dan)
    return etree.fromstring(z.read("word/document.xml"))


def bang_trich_dan(duong_dan):
    """Trả về danh sách trích dẫn theo thứ tự trong bài: (chỉ số đoạn, chữ hiển thị, các bản ghi)."""
    root = doc_document(duong_dan)
    body = root.find(W + "body")
    out = []
    for i, blk in enumerate(doan_va_bang(body)):
        fields = cac_truong(blk)
        for k, f in enumerate(fields):
            ins = f["instr"].strip()
            if ins.startswith("ADDIN EN.CITE") and "EN.CITE.DATA" not in ins:
                data = None
                if "<EndNote>" not in f["instr"]:
                    # trường EN.CITE.DATA lồng bên trong kết thúc ngay trước trường cha nên đứng liền trước nó
                    con = fields[k - 1] if k else None
                    if con is not None and "EN.CITE.DATA" in con["instr"] and con["long"] == f["long"] + 1:
                        data = con["data"]
                out.append((i, f["ket_qua"], ban_ghi(f["instr"], data)))
    return out


if __name__ == "__main__":
    for i, hien, recs in bang_trich_dan(sys.argv[1]):
        ten = "; ".join(f"#{r['recnum']} {r['author']} {r['year']}: {html.unescape(r['title'] or '')[:60]}" for r in recs)
        print(f"[{i}] {hien!r:12} {ten}")
