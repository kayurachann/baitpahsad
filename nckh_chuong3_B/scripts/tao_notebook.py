"""Tạo notebook Colab của người B: B_3_5_1_3_5_2.ipynb (ô khởi tạo, kiểm tra mã hóa 3.3, 3.5.1, 3.5.2).

Code các ô 3.5.1 và 3.5.2 giữ đúng như file "Chương 3 – Kế hoạch phân tích và phân công chi tiết";
chỉ thêm vài dòng in số cần cho phần viết và đổi hình sang đen trắng.
Cách chạy: python3 tao_notebook.py
"""
import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

O_KHOI_TAO = '''\
# Ô khởi tạo dùng chung (chép đúng từ file kế hoạch). Chạy ô này trước mọi ô khác.
from google.colab import drive
drive.mount('/content/drive')
import os, itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

D = "/content/drive/My Drive/NCKH_giac_ngu/"
for t in ["bang", "hinh", "ghi_chu"]:
    os.makedirs(D + t, exist_ok=True)
df   = pd.read_csv(D + "cleaned_sleep_dataset.csv")
orig = pd.read_csv(D + "cleaned_sleep_dataset_original.csv")
y  = "sleep_quality_ordinal"
xs = ["bedtime_device_frequency_ordinal", "caffeine_frequency_ordinal",
      "physical_activity_frequency_ordinal", "academic_stress_ordinal"]
ten = {xs[0]: "Thiết bị trước giờ ngủ", xs[1]: "Caffeine",
       xs[2]: "Hoạt động thể chất", xs[3]: "Căng thẳng học tập"}
rng = np.random.default_rng(20261004)
print(df.shape, orig.shape)   # phải ra (996, 28) (791, 28)
'''

O_MA_HOA = '''\
# 3.3: đối chiếu cột trả lời gốc với cột mã thứ bậc để kiểm tra Bảng 3.1 (không lưu bảng)
cap_cot = {"sleep_quality": "sleep_quality_ordinal",
           "bedtime_device_frequency": "bedtime_device_frequency_ordinal",
           "caffeine_frequency": "caffeine_frequency_ordinal",
           "physical_activity_frequency": "physical_activity_frequency_ordinal",
           "academic_stress": "academic_stress_ordinal"}
for goc, ma in cap_cot.items():
    bang_cheo = pd.crosstab(df[goc], df[ma])
    print(bang_cheo, "\\n")
    print("=> Mỗi lựa chọn chỉ ứng với một mã:", bool(((bang_cheo > 0).sum(axis=1) == 1).all()), "\\n")
print("Giới tính:", sorted(df["gender"].unique()))
print("Năm học:", sorted(df["study_year"].unique()))
'''

O_3_5_1_1 = '''\
# 3.5.1 – Ô 1: bảng kiểm tra chất lượng
flags = ["flag_repeated_timestamp", "flag_identical_answers", "flag_near_duplicate"]
rows = []
for name, d in [("V2", df), ("Original", orig)]:
    rows.append([name, len(d), d.isnull().sum().sum(), d.duplicated().sum()]
                + [int(d[f].sum()) for f in flags])
bang = pd.DataFrame(rows, columns=["file", "so_dong", "o_thieu", "dong_trung",
                                   "ts_lap", "dap_an_giong_het", "gan_trung"])
bang.to_csv(D + "bang/bang_3_5_1.csv", index=False)
print("Số dòng V2 có ít nhất một cờ:", int(df[flags].astype(bool).any(axis=1).sum()))
print("Số dòng V2 nhiều hơn Original:", len(df) - len(orig))
bang
'''

O_3_5_1_2 = '''\
# 3.5.1 – Ô 2: 791 dòng Original có nằm trong V2 không (so từng dòng bằng mã băm)
import hashlib
raw = ["study_year", "gender", "sleep_onset_difficulty", "sleep_duration_group",
       "night_awakenings", "sleep_quality", "concentration_difficulty",
       "daytime_fatigue", "class_absence", "assignment_impact",
       "bedtime_device_frequency", "caffeine_frequency",
       "physical_activity_frequency", "academic_stress", "academic_performance"]
def bam(d):
    return d[raw].astype(str).agg("|".join, axis=1).map(
        lambda s: hashlib.md5(s.encode()).hexdigest())
so_khop = bam(orig).isin(set(bam(df))).sum()
print("Dong Original tim thay trong V2:", so_khop, "/", len(orig))
print("Cot present_in_original = True:", int(df["present_in_original"].sum()))
'''

O_3_5_2_BANG = '''\
# 3.5.2: bảng tần số 7 biến
cols = {
    "sleep_quality_ordinal": "Chất lượng giấc ngủ",
    "bedtime_device_frequency_ordinal": "Thiết bị trước giờ ngủ",
    "caffeine_frequency_ordinal": "Caffeine",
    "physical_activity_frequency_ordinal": "Hoạt động thể chất",
    "academic_stress_ordinal": "Căng thẳng học tập",
    "gender": "Giới tính",
    "study_year": "Năm học",
}
rows = []
for c, nhan in cols.items():
    dem = df[c].value_counts().sort_index()
    for muc, n in dem.items():
        rows.append([nhan, muc, int(n), round(100 * n / len(df), 1)])
mo_ta = pd.DataFrame(rows, columns=["bien", "muc", "so_luong", "ty_le_pct"])
mo_ta.to_csv(D + "bang/bang_3_5_2.csv", index=False)
mo_ta
'''

O_3_5_2_HINH = '''\
# Hình 3.3: phân bố 5 biến thứ bậc (đen trắng, chung trục tung)
from matplotlib import font_manager
co_san = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = [f for f in ["Times New Roman", "Liberation Serif"] if f in co_san] + ["DejaVu Serif"]
tieu_de = {
    "sleep_quality_ordinal": "Chất lượng giấc ngủ",
    "bedtime_device_frequency_ordinal": "Sử dụng thiết bị\\ntrước giờ ngủ",
    "caffeine_frequency_ordinal": "Tiêu thụ caffeine",
    "physical_activity_frequency_ordinal": "Hoạt động thể chất",
    "academic_stress_ordinal": "Căng thẳng học tập",
}
fig, axes = plt.subplots(1, 5, figsize=(6.5, 2.2), sharey=True)
for ax, c in zip(axes, tieu_de):
    dem = df[c].value_counts().sort_index()
    ax.bar(range(len(dem)), dem.values, width=0.7, color="0.55", edgecolor="black", linewidth=0.5)
    for i, n in enumerate(dem.values):
        ax.text(i, n + 8, str(n), ha="center", va="bottom", fontsize=6)
    ax.set_xticks(range(len(dem)), [str(m) for m in dem.index])
    ax.set_title(tieu_de[c], fontsize=8, pad=4)
    ax.set_xlabel("Mức", fontsize=8)
    ax.tick_params(length=2, width=0.6, labelsize=7)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("Số người", fontsize=8)
axes[0].set_ylim(0, 580)
plt.tight_layout(w_pad=0.6)
plt.savefig(D + "hinh/hinh_3_5_2.png", dpi=200)
plt.show()
'''

O_SO_VIET = '''\
# Các số dùng trong phần nhận xét 3.5.2 và Bảng 3.2 (chuyển cho C)
def pct(c, muc):
    return round(100 * df[c].isin(muc).sum() / len(df), 1)
print("Giấc ngủ tệ hoặc rất tệ (mức 1-2):", pct(y, [1, 2]), "%")
print("Giấc ngủ tốt hoặc rất tốt (mức 4-5):", pct(y, [4, 5]), "%")
print("Trung vị chất lượng giấc ngủ:", df[y].median())
for c in xs[:3]:
    print(ten[c], "- mức 4-5:", pct(c, [4, 5]), "%")
print(ten[xs[3]], "- mức 3-4:", pct(xs[3], [3, 4]), "%")
print("Số người ở mức 1:", {ten[c]: int((df[c] == 1).sum()) for c in xs})
print()
thu_tu = ["First year", "Second year", "Third year", "Graduate student"]
for c, ds in [("gender", ["Male", "Female"]), ("study_year", thu_tu)]:
    dem = df[c].value_counts().reindex(ds)
    print(pd.DataFrame({"so_luong": dem, "ty_le_pct": (100 * dem / len(df)).round(1)}), "\\n")
'''

O = [
    ("md", "# Phần của B – Chương 3: thang đo (3.3), kiểm tra chất lượng dữ liệu (3.5.1), mô tả dữ liệu (3.5.2)\n\n"
           "Chạy lần lượt từ trên xuống. Kết quả lưu vào `bang/bang_3_5_1.csv`, `bang/bang_3_5_2.csv`, "
           "`hinh/hinh_3_5_2.png` trong thư mục `NCKH_giac_ngu` trên Drive.\n\n"
           "Dòng cuối của ô khởi tạo phải in ra `(996, 28) (791, 28)`. Nếu in ra `(996, 28) (996, 28)` "
           "là đang đọc nhầm tệp Original."),
    ("code", O_KHOI_TAO),
    ("md", "## 3.3. Đối chiếu mã hóa với Bảng 3.1\n\n"
           "Mỗi bảng chéo cho biết mỗi lựa chọn trả lời gốc được đổi thành mã số nào. "
           "Đối chiếu với Bảng 3.1 trong Word; nếu khác thì sửa Bảng 3.1 theo dữ liệu."),
    ("code", O_MA_HOA),
    ("md", "## 3.5.1. Kiểm tra chất lượng dữ liệu\n\n"
           "Ô 2 phải in ra `791 / 791` và `791`."),
    ("code", O_3_5_1_1),
    ("code", O_3_5_1_2),
    ("md", "## 3.5.2. Mô tả dữ liệu"),
    ("code", O_3_5_2_BANG),
    ("code", O_3_5_2_HINH),
    ("code", O_SO_VIET),
]


def o_notebook(loai, nd):
    dong = nd.rstrip("\n").split("\n")
    nguon = [d + "\n" for d in dong[:-1]] + [dong[-1]]
    if loai == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": nguon}
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": nguon}


def main():
    nb = {
        "cells": [o_notebook(l, n) for l, n in O],
        "metadata": {"colab": {"provenance": []},
                     "kernelspec": {"display_name": "Python 3", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 0,
    }
    ra = GOC / "B_3_5_1_3_5_2.ipynb"
    ra.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("đã ghi", ra)


if __name__ == "__main__":
    main()
