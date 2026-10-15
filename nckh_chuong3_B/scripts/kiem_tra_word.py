"""Đối chiếu số trong ch3_3_3_3_5_1_3_5_2.docx với bang_3_5_2.csv và rà quy ước viết của chương.

Kiểm tra:
  1. Mỗi biến trong bang_3_5_2.csv cộng lại đúng 996 người, tỉ lệ cộng lại khoảng 100%.
  2. Mọi tỉ lệ "x,y%" trong phần chữ là tỉ lệ của một mức, của một dải mức liền nhau, hoặc tổng các tỉ lệ
     đã làm tròn của một biến trong CSV.
  3. Mọi ô số của Bảng 3.2 và 3.4 khớp CSV; dòng tệp chính của Bảng 3.3 khớp lần chạy thật trong notebook.
  4. Không có "ảnh hưởng", "tác động", "gây ra", không còn chỗ trống "[...]".
  5. Bản hoàn chỉnh: không còn chữ tô vàng và đoạn "Ghi chú cho nhóm".
Cách chạy: python3 kiem_tra_word.py
"""
import re
import sys
from itertools import combinations
from pathlib import Path

import pandas as pd
from docx import Document

GOC = Path(__file__).resolve().parent.parent
b2 = pd.read_csv(GOC / "bang" / "bang_3_5_2.csv")
doc = Document(GOC / "ch3_3_3_3_5_1_3_5_2.docx")
loi = []

# 1. tổng mỗi biến
for bien, d in b2.groupby("bien", sort=False):
    if d["so_luong"].sum() != 996:
        loi.append(f"{bien}: tổng {d['so_luong'].sum()} khác 996")
    if abs(d["ty_le_pct"].sum() - 100) > 0.2:
        loi.append(f"{bien}: tổng tỉ lệ {d['ty_le_pct'].sum():.1f}")

# 2. tỉ lệ trong phần chữ
hop_le = set()
for _, d in b2.groupby("bien", sort=False):
    n = d["so_luong"].tolist()
    for a, b in combinations(range(len(n) + 1), 2):
        hop_le.add(f"{round(100 * sum(n[a:b]) / 996, 1):.1f}".replace(".", ","))
    # tổng các tỉ lệ đã làm tròn của một dòng (nêu trong ghi chú về làm tròn của Bảng 3.4)
    hop_le.add(f"{round(d['ty_le_pct'].sum(), 1):.1f}".replace(".", ","))
chu = "\n".join(p.text for p in doc.paragraphs)
for x in re.findall(r"(\d+,\d)\s*%", chu):
    if x not in hop_le:
        loi.append(f"tỉ lệ {x}% trong phần chữ không có trong bang_3_5_2.csv")

# 3. các bảng
bang = {}
for t in doc.tables:
    o = [[c.text for c in r.cells] for r in t.rows]
    bang[o[0][0] + "|" + o[0][-1]] = o
b34 = bang["Biến|Mức 5"]
ten = {"Chất lượng giấc ngủ": "Chất lượng giấc ngủ", "Sử dụng thiết bị trước giờ ngủ": "Thiết bị trước giờ ngủ",
       "Tiêu thụ caffeine": "Caffeine", "Hoạt động thể chất": "Hoạt động thể chất",
       "Căng thẳng học tập": "Căng thẳng học tập"}
for hang in b34[1:]:
    d = b2[b2["bien"] == ten[hang[0]]]
    mong = [f"{n} ({t:.1f})".replace(".", ",") for n, t in zip(d["so_luong"], d["ty_le_pct"])]
    mong += ["–"] * (5 - len(mong))
    if hang[1:] != mong:
        loi.append(f"Bảng 3.4, dòng {hang[0]}: {hang[1:]} khác CSV {mong}")
b32 = bang["Đặc điểm|Tỉ lệ (%)"]
ma = {"Nam": "Male", "Nữ": "Female", "Năm 1": "First year", "Năm 2": "Second year", "Năm 3": "Third year",
      "Sau đại học": "Graduate student"}
for _, nhom, sl, tl in b32[1:]:
    d = b2[b2["muc"] == ma[nhom]].iloc[0]
    if (int(sl), tl) != (int(d["so_luong"]), f"{d['ty_le_pct']:.1f}".replace(".", ",")):
        loi.append(f"Bảng 3.2, {nhom}: {sl} ({tl}) khác CSV")
b33 = bang["Tệp|Gần trùng"]
# dòng tệp chính: kết quả in ra trong notebook của nhóm (ô 3.5.1, chạy trên cleaned_sleep_dataset.csv)
if b33[1][1:] != ["996", "0", "0", "6", "33", "204"]:
    loi.append(f"Bảng 3.3, tệp chính: {b33[1][1:]}")

# 4. quy ước viết
toan_van = chu + "\n" + "\n".join(c.text for t in doc.tables for r in t.rows for c in r.cells)
for tu in ("ảnh hưởng", "tác động", "gây ra"):
    if tu in toan_van.lower():
        loi.append(f"còn từ '{tu}'")
if re.search(r"\[[^\]]*\]", toan_van):
    loi.append("còn chỗ trống [...]")

# 5. bản hoàn chỉnh
if any(el.tag.endswith("}highlight") for el in doc.element.body.iter()):
    loi.append("còn chữ tô vàng")
if "Ghi chú cho nhóm" in chu:
    loi.append("còn đoạn Ghi chú cho nhóm")

print(f"Đã kiểm {len(re.findall(r'(\d+,\d)\s*%', chu))} tỉ lệ trong phần chữ, {len(b34) - 1} dòng Bảng 3.4, "
      f"{len(b32) - 1} dòng Bảng 3.2.")
if loi:
    print("LỖI:\n  " + "\n  ".join(loi))
    sys.exit(1)
print("OK: mọi số khớp bang_3_5_2.csv, không có từ cấm, không còn chỗ trống.")
