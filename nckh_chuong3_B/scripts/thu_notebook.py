"""Chạy thử toàn bộ code của B_3_5_1_3_5_2.ipynb trên dữ liệu giả (không phải dữ liệu thật).

Dữ liệu giả có đúng tên 28 cột, đúng số người ở từng mức như lần chạy thật, cờ đặt sẵn 6/33/204
(216 dòng có ít nhất một cờ) và tệp Original là 791 dòng chép từ tệp chính, nên biết trước đáp án.
Cách chạy: python3 thu_notebook.py
"""
import json
import os
import sys
import tempfile
import types
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
import numpy as np
import pandas as pd

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tao_bang_hinh import DEM  # noqa: E402

N, N_ORIG = 996, 791
NHAN = {
    "sleep_quality": ["Very poor", "Poor", "Average", "Good", "Very good"],
    "bedtime_device_frequency": ["Never", "1-2 times a week", "3-4 times a week", "5-6 times a week", "Every night"],
    "caffeine_frequency": ["Never", "1-2 times a week", "3-4 times a week", "5-6 times a week", "Every day"],
    "physical_activity_frequency": ["Never", "1-2 times a week", "3-4 times a week", "5-6 times a week", "Every day"],
    "academic_stress": ["No stress", "Low stress", "High stress", "Extremely high stress"],
}
KHAC = ["sleep_onset_difficulty", "sleep_duration_group", "night_awakenings", "concentration_difficulty",
        "daytime_fatigue", "class_absence", "assignment_impact", "academic_performance"]


def du_lieu_gia():
    r = np.random.default_rng(1)
    d = {}
    for c, (_, dem) in DEM.items():
        v = np.repeat(list(dem.keys()), list(dem.values()))
        d[c] = r.permutation(v)
    df = pd.DataFrame({"study_year": d["study_year"], "gender": d["gender"]})
    for c in KHAC:
        df[c] = r.choice(["A", "B", "C", "D"], N)
    for goc, nhan in NHAN.items():
        df[goc] = [nhan[k - 1] for k in d[goc + "_ordinal"]]
        df[goc + "_ordinal"] = d[goc + "_ordinal"]
    co = np.zeros((N, 3), bool)
    co[210:216, 0] = True     # lặp mốc thời gian: 6
    co[0:33, 1] = True        # đáp án giống hệt: 33
    co[6:210, 2] = True       # gần trùng: 204; hợp ba cờ = 216 dòng
    df["flag_repeated_timestamp"], df["flag_identical_answers"], df["flag_near_duplicate"] = co.T
    trong_orig = np.zeros(N, bool)
    trong_orig[r.choice(N, N_ORIG, replace=False)] = True
    df["present_in_original"] = trong_orig
    df["source_dataset"] = np.where(trong_orig, "original", "v2")
    df["source_row"] = np.arange(N)
    df["timestamp_iso"] = pd.date_range("2024-01-01", periods=N, freq="min").astype(str)
    df["timestamp_raw"] = df["timestamp_iso"]
    assert df.shape == (N, 28)
    orig = df[trong_orig].copy()
    orig[["flag_repeated_timestamp", "flag_identical_answers", "flag_near_duplicate"]] = False
    orig.iloc[:2, orig.columns.get_loc("flag_repeated_timestamp")] = True
    orig.iloc[:33, orig.columns.get_loc("flag_identical_answers")] = True
    orig.iloc[:183, orig.columns.get_loc("flag_near_duplicate")] = True
    return df, orig.sample(frac=1, random_state=2)


def main():
    tmp = Path(tempfile.mkdtemp()) / "NCKH_giac_ngu"
    tmp.mkdir()
    df, orig = du_lieu_gia()
    df.to_csv(tmp / "cleaned_sleep_dataset.csv", index=False)
    orig.to_csv(tmp / "cleaned_sleep_dataset_original.csv", index=False)

    google = types.ModuleType("google")
    colab = types.ModuleType("google.colab")
    colab.drive = types.SimpleNamespace(mount=lambda p: print("(giả) mount", p))
    google.colab = colab
    sys.modules.update({"google": google, "google.colab": colab})

    nb = json.loads((GOC / "B_3_5_1_3_5_2.ipynb").read_text(encoding="utf-8"))
    ns = {}
    for o in nb["cells"]:
        if o["cell_type"] != "code":
            continue
        code = "".join(o["source"]).replace("/content/drive/My Drive/NCKH_giac_ngu/", str(tmp) + "/")
        print("-" * 70)
        exec(compile(code, "<o>", "exec"), ns)

    b1 = pd.read_csv(tmp / "bang" / "bang_3_5_1.csv")
    print(b1.to_string(index=False))
    assert b1.values.tolist() == [["V2", 996, 0, 0, 6, 33, 204], ["Original", 791, 0, 0, 2, 33, 183]]
    assert ns["so_khop"] == N_ORIG
    # đổi một ô trả lời trong Original: phép so bằng mã băm phải còn 790 / 791
    sai = orig.copy()
    sai.iloc[0, sai.columns.get_loc("academic_performance")] = "Z"
    assert ns["bam"](sai).isin(set(ns["bam"](df))).sum() == N_ORIG - 1
    b2 = pd.read_csv(tmp / "bang" / "bang_3_5_2.csv")
    that = pd.read_csv(GOC / "bang" / "bang_3_5_2.csv")
    assert b2.astype(str).equals(that.astype(str)), "bang_3_5_2 khác bảng từ lần chạy thật"
    assert (tmp / "hinh" / "hinh_3_5_2.png").exists()
    print("\nOK: notebook chạy hết; bang_3_5_1, mã băm (791/791 và 790/791 khi sửa 1 ô), bang_3_5_2 đều đúng.")


if __name__ == "__main__":
    main()
