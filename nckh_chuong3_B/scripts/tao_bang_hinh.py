"""Tạo bang_3_5_2.csv và hinh_3_5_2.png (mục 3.5.2) từ số đếm của lần chạy thật.

Nguồn số: notebook Colab của nhóm ("code của pp nghiên cứu.ipynb"), ô 3.5.2, chạy trên
cleaned_sleep_dataset.csv (996 dòng). Các số dưới đây chép đúng từ bảng kết quả in ra trong
notebook; cách tính tỉ lệ giữ nguyên như code trong file kế hoạch: round(100 * n / len(df), 1).

Cách chạy: python3 tao_bang_hinh.py   (ghi vào ../bang và ../hinh)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

GOC = Path(__file__).resolve().parent.parent
N = 996

# (nhãn trong bang_3_5_2.csv như code của file kế hoạch, {mức: số người} theo thứ tự sort_index)
DEM = {
    "sleep_quality_ordinal": ("Chất lượng giấc ngủ", {1: 290, 2: 166, 3: 75, 4: 214, 5: 251}),
    "bedtime_device_frequency_ordinal": ("Thiết bị trước giờ ngủ", {1: 17, 2: 43, 3: 107, 4: 508, 5: 321}),
    "caffeine_frequency_ordinal": ("Caffeine", {1: 10, 2: 53, 3: 95, 4: 500, 5: 338}),
    "physical_activity_frequency_ordinal": ("Hoạt động thể chất", {1: 8, 2: 38, 3: 122, 4: 453, 5: 375}),
    "academic_stress_ordinal": ("Căng thẳng học tập", {1: 11, 2: 63, 3: 432, 4: 490}),
    "gender": ("Giới tính", {"Female": 305, "Male": 691}),
    "study_year": ("Năm học", {"First year": 22, "Graduate student": 481, "Second year": 74, "Third year": 419}),
}

# tên đầy đủ dùng làm tiêu đề từng ô của Hình 3.3 (thuật ngữ thống nhất của chương)
TIEU_DE = {
    "sleep_quality_ordinal": "Chất lượng giấc ngủ",
    "bedtime_device_frequency_ordinal": "Sử dụng thiết bị\ntrước giờ ngủ",
    "caffeine_frequency_ordinal": "Tiêu thụ caffeine",
    "physical_activity_frequency_ordinal": "Hoạt động thể chất",
    "academic_stress_ordinal": "Căng thẳng học tập",
}


def ve_hinh(dem_theo_bien, duong_dan):
    """Hình 3.3: 5 biểu đồ cột đen trắng, chung trục tung, có số người trên mỗi cột."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
        "font.size": 8,
        "axes.linewidth": 0.6,
    })
    fig, axes = plt.subplots(1, 5, figsize=(6.5, 2.2), sharey=True)
    for ax, (c, dem) in zip(axes, dem_theo_bien.items()):
        muc, so = list(dem.keys()), list(dem.values())
        ax.bar(range(len(muc)), so, width=0.7, color="0.55", edgecolor="black", linewidth=0.5)
        for i, n in enumerate(so):
            ax.text(i, n + 8, str(n), ha="center", va="bottom", fontsize=6)
        ax.set_xticks(range(len(muc)), [str(m) for m in muc])
        ax.set_title(TIEU_DE[c], fontsize=8, pad=4)
        ax.set_xlabel("Mức", fontsize=8)
        ax.tick_params(length=2, width=0.6, labelsize=7)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_ylabel("Số người", fontsize=8)
    axes[0].set_ylim(0, 580)
    fig.tight_layout(w_pad=0.6)
    fig.savefig(duong_dan, dpi=200)
    plt.close(fig)
    from PIL import Image
    Image.open(duong_dan).convert("L").save(duong_dan, dpi=(200, 200))


def main():
    rows = []
    for c, (nhan, dem) in DEM.items():
        assert sum(dem.values()) == N, c
        for muc, n in dem.items():
            rows.append([nhan, muc, int(n), round(100 * n / N, 1)])
    mo_ta = pd.DataFrame(rows, columns=["bien", "muc", "so_luong", "ty_le_pct"])
    (GOC / "bang").mkdir(exist_ok=True)
    (GOC / "hinh").mkdir(exist_ok=True)
    mo_ta.to_csv(GOC / "bang" / "bang_3_5_2.csv", index=False)
    ve_hinh({c: DEM[c][1] for c in TIEU_DE}, GOC / "hinh" / "hinh_3_5_2.png")
    print(mo_ta.to_string(index=False))


if __name__ == "__main__":
    main()
