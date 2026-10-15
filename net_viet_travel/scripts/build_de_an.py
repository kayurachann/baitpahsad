"""Dựng bản đề án theo format bản cũ từ content/de_an.json, rồi điền số trang Mục lục.

    python3 build_de_an.py            # tạo ../De-an-Net-Viet-Travel-Kim-Boi.docx và .pdf

content/de_an.json: {"sections": [[block, ...], ...]} theo thứ tự trong bài; block theo đặc tả
(h1, h2, p, caption, table, steps, note, ref). Chú thích bảng viết "Bảng X." và được đánh số lại ở đây.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

import docx_style as ds

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = HERE / "content" / "de_an.json"
OUT = ROOT / "De-an-Net-Viet-Travel-Kim-Boi.docx"

SUBTITLE = "Sản phẩm khởi đầu: Kim Bôi – Nghỉ cuối tuần theo cách mình (2 ngày 1 đêm)"


def cover(doc):
    def line(text, size=13, bold=True, italic=False, before=0, after=0, align=WD_ALIGN_PARAGRAPH.CENTER, left=None):
        p = ds.para(doc, text, indent=False, align=align, size=size, bold=bold, italic=italic,
                    space_after=after, space_before=before, line_spacing=1.15)
        if left is not None:
            p.paragraph_format.left_indent = Cm(left)
        return p

    line("BỘ VĂN HÓA, THỂ THAO VÀ DU LỊCH")
    line("TRƯỜNG ĐẠI HỌC VĂN HÓA HÀ NỘI")
    line("KHOA DU LỊCH")
    line("HỌC PHẦN: KINH DOANH LỮ HÀNH", before=24)
    line("ĐỀ ÁN", size=18, before=84, after=6)
    line("THÀNH LẬP CÔNG TY TNHH DU LỊCH", size=15, after=4)
    line("NÉT VIỆT TRAVEL", size=15, after=6)
    line(SUBTITLE, size=13, bold=False, italic=True, after=18)
    dots = "." * 52
    line(f"Giảng viên: {dots}", bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, left=2.4, after=4)
    line(f"Nhóm sinh viên: {'.' * 44}", bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, left=2.4, after=4)
    line(f"Lớp: {'.' * 63}", bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, left=2.4, after=4)
    line("Hà Nội, 2026", bold=False, before=60)


def h1_titles(sections):
    return [b["text"] for sec in sections for b in sec if b["type"] == "h1"]


def build(sections, toc_pages):
    doc = ds.new_document(
        title="Đề án thành lập Công ty TNHH Du lịch Nét Việt – Nét Việt Travel",
        subject="Học phần Kinh doanh lữ hành – doanh nghiệp giả định; sản phẩm Kim Bôi 2 ngày 1 đêm",
        author="Nhóm sinh viên Khoa Du lịch, Trường Đại học Văn hóa Hà Nội",
    )
    cover(doc)
    ds.page_break(doc)
    ds.para(doc, "MỤC LỤC", indent=False, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, space_after=12)
    for title in h1_titles(sections):
        ds.toc_line(doc, title, toc_pages.get(title, ""))
    ds.page_break(doc)

    table_no = 0
    first_h1 = True
    for sec in sections:
        for b in sec:
            t = b["type"]
            if t == "h1":
                if b["text"].startswith("TÀI LIỆU THAM KHẢO"):
                    ds.page_break(doc)
                ds.heading(doc, b["text"], 1)
                first_h1 = False
            elif t == "h2":
                ds.heading(doc, b["text"], 2)
            elif t == "p":
                ds.para(doc, b.get("text", ""), lead=b.get("lead"))
            elif t == "caption":
                table_no += 1
                ds.caption(doc, re.sub(r"^Bảng\s+[^.\s]+\.", f"Bảng {table_no}.", b["text"].strip()))
            elif t == "table":
                ds.table(doc, b["header"], b["rows"], widths=b.get("widths"), numeric_cols=b.get("numeric_cols") or ())
            elif t == "steps":
                ds.steps(doc, b["items"])
            elif t == "note":
                ds.note(doc, b["text"])
            elif t == "ref":
                ds.ref(doc, b["text"])
            else:
                raise ValueError(f"unknown block {t}")
    ds.page_number_footer(doc)
    return doc


def to_pdf(docx_path, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(docx_path)],
                   check=True, capture_output=True, timeout=180)
    return Path(outdir) / (Path(docx_path).stem + ".pdf")


def heading_pages(pdf, titles):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    pages = {}
    for i in range(3, n + 1):  # bỏ bìa và mục lục
        txt = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", str(pdf), "-"],
                             capture_output=True, text=True).stdout
        lines = [re.sub(r"\s+", " ", l).strip() for l in txt.splitlines()]
        for t in titles:
            if t not in pages and t in lines:
                pages[t] = i
    return pages, n


def main():
    global OUT, ROOT
    content = Path(sys.argv[1]) if len(sys.argv) > 1 else CONTENT
    if len(sys.argv) > 2:
        OUT = Path(sys.argv[2]).resolve()
        ROOT = OUT.parent
    sections = json.loads(content.read_text(encoding="utf8"))["sections"]
    titles = h1_titles(sections)
    pages = {t: 0 for t in titles}
    with tempfile.TemporaryDirectory() as tmp:
        for _ in range(3):
            doc = build(sections, pages)
            doc.save(OUT)
            pdf = to_pdf(OUT, tmp)
            found, n = heading_pages(pdf, titles)
            missing = [t for t in titles if t not in found]
            if missing:
                sys.exit(f"không tìm thấy tiêu đề trong PDF: {missing}")
            if found == pages:
                break
            pages = found
        final_pdf = to_pdf(OUT, ROOT)
    print(f"{OUT.name}: {n} trang; mục lục: " + ", ".join(f"{t.split('.')[0]}→{p}" for t, p in pages.items()))
    print(final_pdf.name)


if __name__ == "__main__":
    main()
