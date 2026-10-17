# Kết quả chạy lại thí nghiệm 600 cover

Chạy lại ngày 15/10/2026 từ 600 ảnh PGM gốc của BOSSbase 1.01, bằng `scripts/chay_lai_600.py`. Code xử lý dữ liệu, Residual-LR và ngưỡng là nguyên `code_nhom/sg.py` của nhóm. Phiên bản phần mềm và các lệnh nằm trong `moi_truong.json`.

## Các file
- `scores.csv`: điểm test của từng ảnh, cho 18 lần chạy (2 detector × 3 protocol × 3 seed). Định dạng của `verify_stats.py`.
- `thresholds.csv`: τBER và τlow của từng lần chạy, chọn trên tập validation.
- `ci_deltaauc_B10000.json`: ΔAUC và CI 95% của 22 so sánh (RQ1–RQ3), B = 10.000, `default_rng(2026)`. Cột `paper` là số của bản trước.
- `so_sanh_voi_bai.md`: so lần chạy lại với số trong bản trước (Table 4/S1, FP từng seed, CI theo nhiều cách bootstrap).
- `verify_report.json`: kết quả `verify_stats.py` trên các file này.

## Kết quả đối chiếu
- **Table 4 và S1:** khớp 216/216 giá trị (2 detector × 18 ô × AUC, SD, F1, BER, recall, FPR).
- **Table 7:** tổng false positive khớp ở cả 6 dòng. Số theo từng seed (trên 120 test cover):

  | Detector | P1 | P2 | P3 |
  |---|---|---|---|
  | Residual-LR | 5, 5, 5 | 4, 6, 5 | 6, 7, 6 |
  | SRM+Ensemble | 7, 3, 8 | 7, 2, 2 | 5, 1, 2 |

- **ΔAUC:** cả 22 ước lượng điểm khớp bài.
  - Cách gộp CI trong bản trước là rút một lần cover cho cả ba seed và lấy trung bình ΔAUC theo replicate. Các cách khác lệch 0,013–0,021.
  - Không khôi phục được B và dòng số ngẫu nhiên của script ΔAUC gốc (script đã mất). Vì vậy bài dùng CI tính lại ở đây; các cận đổi tối đa 0,003.
  - Riêng khoảng Residual-LR P3 WOW thành [−0,046; 0,000] (cận trên +0,0003), tức chạm 0.
