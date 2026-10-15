"""Đánh mã vị trí cho từng đoạn và từng ô bảng của đề án.

Mã đoạn ngoài bảng: P001, P002, ... (chỉ đếm đoạn có chữ).
Mã ô bảng: T05.r2.c1 = Bảng thứ 5 trong tệp (đúng số "Bảng 5" của đề án), hàng 2, cột 1 (đếm từ 0, hàng 0 là tiêu đề).

Dùng chung cho apply_edits.py và check_numbers.py để mọi thao tác chỉ vào cùng một vị trí.

    python3 extract_index.py <file.docx> [out.json] [out.md]
"""
import json
import sys

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn


def iter_units(doc):
    """Trả về (mã, Paragraph) theo đúng thứ tự trong thân văn bản."""
    p_no = 0
    t_no = 0
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            para = Paragraph(child, doc)
            if para.text.strip():
                p_no += 1
                yield f"P{p_no:03d}", para
        elif child.tag == qn("w:tbl"):
            t_no += 1
            table = Table(child, doc)
            for r, row in enumerate(table.rows):
                seen = set()
                for c, cell in enumerate(row.cells):
                    if id(cell._tc) in seen:  # ô gộp ngang
                        continue
                    seen.add(id(cell._tc))
                    for k, para in enumerate(cell.paragraphs):
                        if para.text.strip():
                            suffix = "" if k == 0 else f".p{k}"
                            yield f"T{t_no:02d}.r{r}.c{c}{suffix}", para


def build_index(path):
    doc = Document(path)
    units = []
    for uid, para in iter_units(doc):
        style = para.style.name if para.style is not None else ""
        units.append({"id": uid, "style": style, "text": para.text})
    return units


def main():
    src = sys.argv[1]
    units = build_index(src)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf8") as f:
            json.dump(units, f, ensure_ascii=False, indent=1)
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w", encoding="utf8") as f:
            for u in units:
                tag = f" ({u['style']})" if u["style"].startswith("Heading") else ""
                f.write(f"[{u['id']}]{tag} {u['text']}\n")
    print(f"{len(units)} units")


if __name__ == "__main__":
    main()
