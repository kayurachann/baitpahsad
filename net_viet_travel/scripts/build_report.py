"""Dựng báo cáo rà soát (Markdown + .docx) từ content/review.json.

    python3 build_report.py   # tạo ../Bao-cao-ra-soat.md và ../Bao-cao-ra-soat.docx

content/review.json: {"summary", "items": [...], "math_checks": [...], "changes": [...], "stats": {...}}
"""
import json
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

import docx_style as ds

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = HERE / "content" / "review.json"

GROUPS = ["Phép toán", "Logic", "Văn phong", "Nguồn và pháp lý"]
HANDLING = {"sửa trong bản viết lại": "Đã sửa", "cần nhóm quyết": "Nhóm quyết", "ghi chú": "Ghi chú"}


def md_cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def build_md(r):
    out = ["# Báo cáo rà soát đề án Nét Việt Travel (bản Kim Bôi 2N1Đ)", ""]
    out += ["## 1. Kết luận nhanh", "", r["summary"], ""]
    st = r.get("stats")
    if st:
        out += [f"Quy trình: {st['reviewers']} lượt rà soát độc lập (toán, logic, văn phong, nguồn); mỗi phát hiện được "
                f"hai lượt kiểm chứng phản biện. Giữ lại {st['kept']} trên {st['total']} phát hiện; "
                f"{st['rejected']} phát hiện bị bác vì không đứng vững.", ""]
    checks = r["math_checks"]
    ok = sum(1 for c in checks if c["ok"])
    out += ["## 2. Kiểm tra phép toán", "", f"Đã tính lại {len(checks)} phép tính; {ok} khớp với đề án.", "",
            "| # | Nội dung | Cách tính | Trong đề án | Tính lại | Kết quả |", "|---|---|---|---|---|---|"]
    for i, c in enumerate(checks, 1):
        out.append(f"| {i} | {md_cell(c['item'])} | {md_cell(c['formula'])} | {md_cell(c['doc_value'])} | "
                   f"{md_cell(c['recomputed'])} | {'✓' if c['ok'] else '✗'} |")
    out.append("")
    n = 3
    for g in GROUPS[1:] + GROUPS[:1]:
        items = [it for it in r["items"] if it["group"] == g]
        if not items:
            continue
        out += [f"## {n}. {g}", ""]
        n += 1
        for it in items:
            out += [f"**{it['title']}** ({it['severity']}; {HANDLING[it['handling']]}; vị trí: {it['location']})", "",
                    f"{it['detail']}", "", f"*Đề xuất:* {it['recommendation']}", ""]
    if r.get("changes"):
        out += [f"## {n}. Những thay đổi khi chuyển sang format bản cũ", ""]
        out += [f"- {c}" for c in r["changes"]] + [""]
    return "\n".join(out)


def build_docx(r, path):
    doc = ds.new_document(title="Báo cáo rà soát đề án Nét Việt Travel", subject="Rà soát văn phong, logic, phép toán",
                          author="Nhóm sinh viên Khoa Du lịch, Trường Đại học Văn hóa Hà Nội")
    ds.para(doc, "BÁO CÁO RÀ SOÁT ĐỀ ÁN NÉT VIỆT TRAVEL", indent=False, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True,
            size=15, space_after=2)
    ds.para(doc, "Bản Kim Bôi 2 ngày 1 đêm – văn phong, logic, phép toán và nguồn", indent=False,
            align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, space_after=10)
    ds.heading(doc, "1. Kết luận nhanh", 1)
    ds.para(doc, r["summary"])
    st = r.get("stats")
    if st:
        ds.para(doc, f"Quy trình: {st['reviewers']} lượt rà soát độc lập (toán, logic, văn phong, nguồn); mỗi phát hiện "
                     f"được hai lượt kiểm chứng phản biện. Giữ lại {st['kept']} trên {st['total']} phát hiện; "
                     f"{st['rejected']} phát hiện bị bác vì không đứng vững.")
    checks = r["math_checks"]
    ok = sum(1 for c in checks if c["ok"])
    ds.heading(doc, "2. Kiểm tra phép toán", 1)
    ds.para(doc, f"Đã tính lại {len(checks)} phép tính; {ok} khớp với đề án.")
    ds.caption(doc, "Bảng 1. Các phép tính đã kiểm tra (đơn vị triệu đồng nếu không ghi khác)")
    ds.table(doc, ["#", "Nội dung", "Cách tính", "Trong đề án", "Tính lại", "KQ"],
             [[str(i), c["item"], c["formula"], c["doc_value"], c["recomputed"], "✓" if c["ok"] else "✗"]
              for i, c in enumerate(checks, 1)],
             widths=[5, 27, 32, 13, 15, 8], bold_first_col=False, size=10)
    n = 3
    for g in GROUPS[1:] + GROUPS[:1]:
        items = [it for it in r["items"] if it["group"] == g]
        if not items:
            continue
        ds.heading(doc, f"{n}. {g}", 1)
        n += 1
        for it in items:
            ds.para(doc, f"({it['severity']}; {HANDLING[it['handling']]}; vị trí: {it['location']})",
                    lead=it["title"], indent=False, space_after=2, keep_next=True)
            ds.para(doc, it["detail"], indent=False, space_after=2)
            ds.para(doc, it["recommendation"], lead="Đề xuất:", indent=False, italic=False, space_after=8)
    if r.get("changes"):
        ds.heading(doc, f"{n}. Những thay đổi khi chuyển sang format bản cũ", 1)
        for c in r["changes"]:
            p = ds.para(doc, "▪\t" + c, indent=False, space_after=2)
            p.paragraph_format.tab_stops.add_tab_stop(ds.Cm(0.6))
            p.paragraph_format.left_indent = ds.Cm(0.6)
            p.paragraph_format.first_line_indent = ds.Cm(-0.6)
    ds.page_number_footer(doc, skip_first=False)
    doc.save(path)


def main():
    r = json.loads(CONTENT.read_text(encoding="utf8"))
    (ROOT / "Bao-cao-ra-soat.md").write_text(build_md(r), encoding="utf8")
    build_docx(r, ROOT / "Bao-cao-ra-soat.docx")
    print("ok")


if __name__ == "__main__":
    main()
