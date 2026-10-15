"""Dựng kịch bản thuyết trình 7 phút (.docx) từ content/kich_ban.json.

    python3 build_script_doc.py   # tạo ../Kich-ban-thuyet-trinh-7-phut.docx

Đếm "tiếng" = số token cách nhau bởi khoảng trắng trong phần lời nói (bỏ ký hiệu in đậm).
"""
import json
import re
import subprocess
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

import docx_style as ds

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = HERE / "content" / "kich_ban.json"
OUT = ROOT / "Kich-ban-thuyet-trinh-7-phut.docx"


def syllables(text):
    clean = re.sub(r"[*_#>\[\]()“”\"'…–—−:;,.!?]", " ", text)
    return len([t for t in clean.split() if re.search(r"\w", t)])


def mmss(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def main():
    k = json.loads(CONTENT.read_text(encoding="utf8"))
    secs = k["sections"]
    total = sum(syllables(s["speech"]) for s in secs)

    doc = ds.new_document(title="Kịch bản thuyết trình 7 phút – Nét Việt Travel",
                          subject="Đề án thành lập Công ty TNHH Du lịch Nét Việt",
                          author="Nhóm sinh viên Khoa Du lịch, Trường Đại học Văn hóa Hà Nội")
    ds.para(doc, "KỊCH BẢN THUYẾT TRÌNH 7 PHÚT", indent=False, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True,
            size=15, space_after=2)
    ds.para(doc, "Đề án thành lập Công ty TNHH Du lịch Nét Việt – Nét Việt Travel", indent=False,
            align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, space_after=2)
    ds.para(doc, "Sản phẩm khởi đầu: Kim Bôi – Nghỉ cuối tuần theo cách mình (2 ngày 1 đêm)", indent=False,
            align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, space_after=10)

    minutes = total / 165
    ds.para(doc, (f"Một người trình bày, khoảng **{total} tiếng** lời nói; đọc ở tốc độ 160–170 tiếng/phút, "
                  f"có ngắt nghỉ để chỉ sơ đồ, là khoảng {minutes:.1f} phút. Sơ đồ tư duy khổ A3 đặt cạnh người nói; "
                  "nhánh ① đến ④ ở bên phải (từ trên xuống), nhánh ⑤ đến ⑧ ở bên trái (từ dưới lên)."),
            indent=False, space_after=4)
    ds.para(doc, "Chữ **in đậm** là chỗ nhấn giọng. Dòng in nghiêng trong ngoặc vuông là động tác, không đọc thành lời.",
            indent=False, space_after=8)

    ds.caption(doc, "Phân bổ thời gian")
    rows = []
    for s in secs:
        a, b = [x.strip() for x in s["time"].replace("–", "-").split("-")]
        rows.append([s["time"], s["heading"], s["branch"], f"{mmss(b) - mmss(a)} giây", str(syllables(s["speech"]))])
    rows.append(["**Tổng**", "", "", "**7 phút**", f"**{total}**"])
    ds.table(doc, ["Mốc", "Phần", "Nhánh", "Thời lượng", "Số tiếng"], rows,
             widths=[17, 43, 14, 14, 12], numeric_cols=[3, 4], bold_first_col=False)

    for s in secs:
        ds.heading(doc, f"{s['time']}  ·  {s['heading']}  ·  {s['branch']}", 2)
        ds.para(doc, f"[{s['cue'].strip().rstrip('.')}]", indent=False, italic=True, space_after=3, size=12)
        for chunk in [c.strip() for c in re.split(r"\n\s*\n|\n", s["speech"]) if c.strip()]:
            ds.para(doc, chunk)

    ds.page_break(doc)
    ds.heading(doc, "PHỤ LỤC 1. THẺ NHẮC (cầm tay)", 1)
    for line in k["cue_card"]:
        p = ds.para(doc, "▪\t" + line, indent=False, space_after=2, line_spacing=1.2)
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(0.6))
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ds.heading(doc, "PHỤ LỤC 2. CÂU HỎI CÓ THỂ GẶP VÀ GỢI Ý TRẢ LỜI", 1)
    for i, qa in enumerate(k["qa"], 1):
        ds.para(doc, f"Hỏi {i}. {qa['q']}", indent=False, bold=True, space_after=2, keep_next=True)
        ds.para(doc, qa["a"], indent=False, space_after=8)

    ds.page_number_footer(doc, skip_first=False)
    doc.save(OUT)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(ROOT), str(OUT)],
                   check=True, capture_output=True, timeout=180)
    print(f"{OUT.name}: {total} tiếng (~{minutes:.1f} phút ở 165 tiếng/phút)")
    for s in secs:
        print(f"  {s['time']:>11}  {syllables(s['speech']):>4}  {s['heading']}")


if __name__ == "__main__":
    main()
