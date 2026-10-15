"""Vẽ sơ đồ tư duy toàn bài từ content/mindmap.json, xuất PDF khổ A3 ngang và PNG độ phân giải cao.

    python3 mindmap.py [mindmap.json] [thư_mục_ra]

Bố cục: nút trung tâm ở giữa; nhánh 1–4 bên phải (trên xuống), nhánh 5–8 bên trái (dưới lên),
tức là đọc theo chiều kim đồng hồ từ góc trên bên phải. Đường nối được tính trong trình duyệt
sau khi chữ đã dàn trang, nên không phụ thuộc vào việc ước lượng bề rộng chữ.
Dựng bằng Chromium qua Playwright (render_mindmap.js).
"""
import html
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

COLORS = {
    1: "#2563A8", 2: "#0F8577", 3: "#C9601A", 4: "#7646B8",
    5: "#9A7410", 6: "#C03A68", 7: "#1E7B3C", 8: "#B3261E",
}
CIRCLED = "①②③④⑤⑥⑦⑧"

CSS = """
@page { size: 420mm 297mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 420mm; height: 297mm; background: #ffffff; }
body { font-family: 'Be Vietnam Pro', 'Inter', 'DejaVu Sans', sans-serif; color: #1d2733;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
#page { position: relative; width: 420mm; height: 297mm; padding: 9mm 10mm 8mm; display: flex; flex-direction: column; }
#top { display: flex; justify-content: space-between; align-items: baseline; font-size: 9.5pt;
       color: #5b6673; letter-spacing: .02em; }
#top b { color: #1d2733; letter-spacing: .06em; }
#main { position: relative; flex: 1; display: flex; align-items: stretch; margin-top: 4mm; }
.side { flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; gap: 3mm; z-index: 1; }
.group { display: flex; align-items: center; gap: 9mm; }
.left .group { flex-direction: row-reverse; }
.bnode { flex: 0 0 48mm; color: #fff; border-radius: 3.2mm; padding: 2.6mm 3mm; font-weight: 700;
         font-size: 12pt; line-height: 1.22; display: flex; gap: 2mm; align-items: center; }
.bnode .no { font-size: 15pt; line-height: 1; }
.items { flex: 1; display: flex; flex-direction: column; gap: 1.3mm; }
.item { font-size: 10.1pt; line-height: 1.28; padding: 1.15mm 2.4mm; border-radius: 1.8mm; background: #fff;
        border: .35mm solid; }
.left .item { text-align: right; }
.item b { font-weight: 700; }
#center { flex: 0 0 88mm; display: flex; align-items: center; justify-content: center; z-index: 1; }
#cnode { width: 66mm; background: #1b2b3a; color: #fff; border-radius: 5mm; padding: 6mm 5mm; text-align: center; }
#cnode .t { font-size: 19pt; font-weight: 800; letter-spacing: .04em; line-height: 1.15; }
#cnode .s { font-size: 10.5pt; margin-top: 2.5mm; line-height: 1.35; color: #dfe7ef; }
#cnode .f { font-size: 9pt; margin-top: 3mm; padding-top: 2.5mm; border-top: .3mm solid #4a5d70; color: #c3cfdb; line-height: 1.4; }
#links { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; overflow: visible; }
#foot { margin-top: 3mm; font-size: 8.6pt; color: #6b7682; display: flex; justify-content: space-between; }
"""

JS = """
function draw() {
  const svg = document.getElementById('links');
  const main = document.getElementById('main').getBoundingClientRect();
  const c = document.getElementById('cnode').getBoundingClientRect();
  const P = (x, y) => [x - main.left, y - main.top];
  const path = (a, b, color, w) => {
    const [x1, y1] = a, [x2, y2] = b, dx = (x2 - x1) * 0.5;
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`);
    p.setAttribute('fill', 'none'); p.setAttribute('stroke', color);
    p.setAttribute('stroke-width', w); p.setAttribute('stroke-linecap', 'round');
    svg.appendChild(p);
  };
  for (const side of ['left', 'right']) {
    const groups = [...document.querySelectorAll(`.${side} .group`)];
    groups.forEach((g, i) => {
      const color = g.dataset.color;
      const b = g.querySelector('.bnode').getBoundingClientRect();
      const n = groups.length, frac = (i + 1) / (n + 1);
      const cy = c.top + c.height * (0.18 + 0.64 * frac);
      const start = side === 'right' ? P(c.right - 2, cy) : P(c.left + 2, cy);
      const end = side === 'right' ? P(b.left + 1, b.top + b.height / 2) : P(b.right - 1, b.top + b.height / 2);
      path(start, end, color, 3.4);
      const bx = side === 'right' ? b.right - 1 : b.left + 1;
      g.querySelectorAll('.item').forEach(it => {
        const r = it.getBoundingClientRect();
        const ix = side === 'right' ? r.left + 0.5 : r.right - 0.5;
        path(P(bx, b.top + b.height / 2), P(ix, r.top + r.height / 2), color, 1.3);
      });
    });
  }
  document.body.dataset.ready = '1';
}
document.fonts.ready.then(() => requestAnimationFrame(draw));
"""


def esc(s):
    """Thoát HTML, giữ **in đậm**."""
    parts = str(s).split("**")
    return "".join(f"<b>{html.escape(p)}</b>" if i % 2 else html.escape(p) for i, p in enumerate(parts))


def tint(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    mix = lambda v: round(255 - (255 - v) * alpha)
    return f"#{mix(r):02X}{mix(g):02X}{mix(b):02X}"


def group_html(br):
    no = br["no"]
    color = COLORS[no]
    items = "".join(
        f'<div class="item" style="border-color:{tint(color, .55)};background:{tint(color, .07)}">{esc(t)}</div>'
        for t in br["items"])
    return (f'<div class="group" data-color="{color}">'
            f'<div class="bnode" style="background:{color}"><span class="no">{CIRCLED[no - 1]}</span>'
            f'<span>{esc(br["title"])}</span></div><div class="items">{items}</div></div>')


def build_html(m):
    by = {b["no"]: b for b in m["branches"]}
    right = "".join(group_html(by[n]) for n in (1, 2, 3, 4))
    left = "".join(group_html(by[n]) for n in (8, 7, 6, 5))  # trên xuống: 8,7,6,5 = chiều kim đồng hồ
    facts = esc(m.get("center_facts", ""))
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div id="page">
<div id="top"><span><b>SƠ ĐỒ TƯ DUY</b> · Đề án thành lập Công ty TNHH Du lịch Nét Việt</span>
<span>Học phần Kinh doanh lữ hành · Khoa Du lịch · Trường Đại học Văn hóa Hà Nội</span></div>
<div id="main"><svg id="links"></svg>
<div class="side left">{left}</div>
<div id="center"><div id="cnode"><div class="t">{esc(m["center_title"])}</div><div class="s">{esc(m["center_sub"])}</div>
{f'<div class="f">{facts}</div>' if facts else ''}</div></div>
<div class="side right">{right}</div></div>
<div id="foot"><span>{esc(m.get("footer_left", ""))}</span><span>{esc(m.get("footer_right", ""))}</span></div>
</div><script>{JS}</script></body></html>"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "content" / "mindmap.json"
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT
    m = json.loads(src.read_text(encoding="utf8"))
    assert sorted(b["no"] for b in m["branches"]) == list(range(1, 9)), "cần đủ 8 nhánh"
    page = outdir / "So-do-tu-duy.html"
    page.write_text(build_html(m), encoding="utf8")
    subprocess.run(["node", str(HERE / "render_mindmap.js"), str(page), str(outdir / "So-do-tu-duy.pdf"),
                    str(outdir / "So-do-tu-duy.png")], check=True)
    page.unlink()
    print("ok:", outdir / "So-do-tu-duy.pdf", outdir / "So-do-tu-duy.png")


if __name__ == "__main__":
    main()
