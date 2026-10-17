# Sửa bài StegaGuard theo góp ý cuối của thầy

**File nộp:** `manuscript/Paper_HoanChinh_2.docm`.
- Sửa trực tiếp trên `Paper_HoanChinh_1.docm` của nhóm: giữ nguyên cấu trúc, lề, cỡ chữ thân bài, các bảng và trường EndNote.
- Chỉ đổi style "EndNote Bibliography" của References: chữ 10 → 9 pt, giãn dòng 11 pt, thụt lề 341 twip, canh trái. Đây là đúng style `referenceitem` có sẵn trong template LNCS của file (9 pt, line 220). Thân bài, lề và cỡ chữ thân bài giữ nguyên.
- Bản PDF xuất kiểm tra (LibreOffice) dài **12 trang**, kể cả References.
- Supplementary: `supplementary/StegaGuard_supplementary.docx` và `.pdf` (3 trang, Bảng S1–S3).


## Đã chạy lại toàn bộ thí nghiệm 600 cover

Nhóm gửi 600 ảnh PGM gốc của BOSSbase (`covers.zip`, 5 phần). Mình chạy lại toàn bộ thí nghiệm bằng `scripts/chay_lai_600.py`. Phần dữ liệu, Residual-LR và cách chọn ngưỡng dùng nguyên `code_nhom/sg.py` của nhóm. Kết quả và cách tái lập nằm trong `data/stegaguard_600/ket_qua_chay_lai/` (xem `README.md` trong thư mục đó).

**Dữ liệu**
- 600/600 ảnh PGM khớp SHA-256 trong `source_provenance.json`.
- `sg.prepare` (seed 20260918, 256 × 256) cho manifest khớp bản của nhóm ở mọi cột: thứ tự 4.200 dòng, cover_id (là hash điểm ảnh), split, seed nhúng, nguồn.
- Chỉ cột SHA-256 của file PNG khác, vì bản Pillow/zlib dùng để nén PNG khác. Điểm ảnh thì trùng. Kiểm thêm bằng bộ pilot: tạo lại bộ pilot 180 cover (1.260 ảnh) rồi chấm bằng chính `model.joblib` của nhóm, điểm trùng tuyệt đối với `predictions.csv` của nhóm ở cả 3.888 dòng (9 lần chạy × 432 dòng, trên 252 ảnh test).

**Kết quả: khớp 216/216 giá trị của Table 4 và Bảng S1** (2 detector × 18 ô × AUC, SD, F1, BER, recall, FPR). Để khớp hoàn toàn cần ba chi tiết của máy và code gốc:
1. **Nhân tính toán của OpenBLAS.** Laptop của nhóm không có AVX-512 nên OpenBLAS dùng nhân Haswell. Trên máy có AVX-512, Residual-LR P1 (đặc trưng gần như ngẫu nhiên) dừng lbfgs ở điểm hơi khác, F1/BER lệch tới 0,012. Đặt `OPENBLAS_CORETYPE=Haswell` thì khớp hết.
2. **Thứ tự ghép đặc trưng SRM.** Hàm `srm.extract` của sealwatch trả về dict có thứ tự phụ thuộc hash seed của Python (khi gộp các khối SPAM, hàm duyệt một `set`), nên có 8 thứ tự khả dĩ. Chỉ một thứ tự cho ra đúng 36/36 giá trị SRM P1. Thứ tự này được lưu trong `scripts/srm_thu_tu_nhom.txt`.
3. **Cách rút cặp train của SRM.** Script SRM của nhóm duyệt các cover train theo cover_id (sg.py thì theo thứ tự manifest) khi rút một biến thể bằng `random.Random(seed)`. Bộ phân loại là `FldEnsembleTrainer(seed=seed, L=50, d_sub=500)` của sealwatch; điểm là `predict_confidence`, tức trung bình phiếu ±1 của 50 FLD. Với cách này P2 và P3 cũng khớp 36/36.

**Phiên bản phần mềm** đã tái lập đúng mọi số: Python 3.13, NumPy 2.5.3, SciPy 1.18.1, scikit-learn 1.9.1 (trùng bản ghi trong `model.joblib` của nhóm), Pillow 12.3.0, conseal 2025.11, sealwatch 2025.9. Hai bản conseal và sealwatch này là bản mới nhất trên PyPI lúc nhóm chạy; `requirements.txt` của nhóm không ghim phiên bản.

**ΔAUC và CI (Table 5, Table 6, Fig. 2, Bảng S2)**
- Cả 22 ước lượng điểm ΔAUC khớp bài.
- **Cách gộp qua 3 seed** của bản trước đã xác định được: mỗi replicate rút một lần 120 test cover, dùng chung cho cả 3 seed; ΔAUC của replicate là trung bình 3 seed. Cách này cho CI lệch bài trung bình khoảng 0,002 (đúng mức sai số Monte Carlo), trong khi lấy CI riêng từng seed rồi gộp thì lệch trung bình 0,013–0,021 với SRM+Ensemble và 0,004–0,007 với Residual-LR.
- **B và dòng số ngẫu nhiên của script gốc thì không khôi phục được.** Đã thử B = 1.000–10.000, nhiều seed và hai loại bộ sinh, không bộ nào cho ra đúng từng chữ số. Script gốc không còn.
- Vì vậy mọi CI được **tính lại** từ điểm của lần chạy lại bằng `scripts/tinh_lai_ci.py`: B = 10.000, `numpy.random.default_rng(2026)` (seed bootstrap của `sg.py`), phân vị 2,5 và 97,5. Script này cho kết quả giống `verify_stats.paired_bootstrap` (đã kiểm). Bài ghi đúng thủ tục này ở 3.5.
- Các cận CI đổi tối đa 0,003 và mọi kết luận giữ nguyên, trừ một chỗ: khoảng của **Residual-LR P3 WOW** trước là [−0.046, −0.001], nay là [−0.046, 0.000] (cận trên +0,0003), tức chạm 0. Câu "all 18 intervals lie below zero" vì vậy sửa thành "17 of the 18 intervals lie below zero; the Residual-LR interval for P3 WOW reaches zero". Table 6 ghi 2/3 cho dòng này.

**Kiểm độc lập:** `verify_stats.py` chạy trên `ket_qua_chay_lai/scores.csv` và `thresholds.csv` (B = 10.000) cho ra đúng mọi số trong `results_data.py`, gồm Table 4/S1, FP từng seed và 22 CI (`verify_report.json`).

### Báo cáo CheckAI (Turnitin) nhóm gửi
- `CheckAI.pdf` ngày 14/10 chấm **một bản cũ** của bài (13 trang, có Table 11 và Fig. 4): 36% bị đánh dấu AI, gồm 21 đoạn.
- Đã đối chiếu tự động từng đoạn bị đánh dấu với bản hiện tại. Gần như không đoạn nào còn nguyên, chỉ còn tên Table 1 (gần giống) và 2 câu na ná ở 4.1 và Conclusion. Vì vậy con số 36% không áp dụng cho file hiện tại.
- Nhóm nên nộp bản `Paper_HoanChinh_2` lên Turnitin để chấm lại. Nếu còn đoạn bị đánh dấu, gửi báo cáo mới để xem đúng các đoạn đó; tốt nhất là nhóm tự viết lại các đoạn đó bằng lời của mình.
- Làm theo quy định của trường và hội nghị về việc dùng AI hỗ trợ viết. Springer yêu cầu ghi rõ việc dùng LLM nếu vượt quá mức sửa câu chữ.


## Thầy yêu cầu – đã làm gì

### 1. Section 3.2 – tái lập thực nghiệm
Thêm vào đoạn 3.2 (không thêm bảng) các thông tin lấy từ `sg.py` và các mô hình `model.joblib` của nhóm. Mô hình được đọc bằng joblib, không chạy code lạ.
- **76 đặc trưng:** sai phân điểm ảnh bậc 1 và bậc 2 theo hai hướng (4 residual). Mỗi residual cho histogram chuẩn hóa 17 bin của giá trị đã cắt về [−8, 8], cộng trung bình trị tuyệt đối và độ lệch chuẩn của residual **chưa cắt**, nên có 4 × 19 = 76 đặc trưng.
- **Chuẩn hóa:** StandardScaler nằm trong pipeline scikit-learn, chỉ fit trên đặc trưng train của từng lần chạy.
- **Logistic Regression:** L2, C = 1.0, solver lbfgs, không class weight (cặp train cân bằng 1:1), max_iter = 2000. Điểm số là `decision_function`.
  - random_state = seed của lần chạy, nhưng lbfgs không dùng tới nên việc fit là tất định.
  - Vì vậy đã sửa ô "Seed-dependent parts" của Residual-LR trong Table 2 thành "variant sampling (P2, P3)".
  - Câu ở 3.3 sửa thành "Seeds 42-44 control the variant draws and the random parts of SRM+Ensemble fitting."
- **Mục 3.1:** ghi rõ ảnh được thu nhỏ bằng bicubic ("bicubically downsampled", đúng như `prepare` trong `sg.py`) và ảnh stego được tạo bằng mô phỏng nhúng của conseal.
- **SRM+Ensemble:** câu cũ (106 submodel, 34.671 đặc trưng, sealwatch, L = 50, d_sub = 500) nay đã được chạy lại xác nhận. Thêm một câu về điểm số: "Its score is the mean of the 50 base-learner votes (±1)." Đây là `predict_confidence` của sealwatch, cách duy nhất cho ra đúng số của bài.

### 2. Section 3.5 – bootstrap
- Thêm vào cuối đoạn đầu 3.5: "One draw serves all three seeds, and the replicate ΔAUC is the mean of the three per-seed differences. The 2.5th and 97.5th percentiles of B = 10,000 replicates (NumPy default_rng, seed 2026) give the 95% interval."
- Đây đúng là thủ tục đã chạy để ra mọi CI trong bài (`scripts/tinh_lai_ci.py`). Cách gộp qua seed giống bản trước; B và seed là của lần tính lại (xem phần "Đã chạy lại").
- Các CI mới được cập nhật ở Abstract, mục 4.2 và 4.3, Answer to RQ1, Conclusion, Table 5, Table 6, Fig. 2 (vẽ lại bằng `scripts/make_figures.py`, đúng kiểu cũ) và Bảng S2.
- Câu giới hạn CI: CI chỉ phản ánh biến thiên khi lấy mẫu lại 120 test cover cố định, không mở rộng sang nguồn ảnh khác ("they account only for test-cover sampling and do not extend to other image sources").
- Câu lưu trữ sửa cho đúng code: mỗi lần chạy lưu điểm test từng ảnh và ngưỡng chọn trên validation. Các file này của lần chạy lại nay nằm trong repo, nên câu "All tables can be recomputed from these files" đúng.

### 3. Section 4.5 – low FPR
- Bỏ câu "in none of them were recall and FPR both zero, so the detectors were never completely silent".
- Viết lại câu 54 rows / 6.480: đó là 6.480 lượt chấm, do 9 mô hình của một detector chấm lặp lại trên cùng 720 ảnh stego (từ 120 cover), nên không phải mẫu độc lập. False positives trong Table 7 cũng là các lượt chấm lặp trên cùng 120 test cover.
- **Đối chiếu FP với điểm từng seed** (đếm từ điểm test của từng lần chạy, trên 120 test cover):

  | Detector | P1 (seed 42/43/44) | P2 | P3 |
  |---|---|---|---|
  | Residual-LR | 5/5/5 = 15 | 4/6/5 = 15 | 6/7/6 = 19 |
  | SRM+Ensemble | 7/3/8 = 18 | 7/2/2 = 11 | 5/1/2 = 8 |

  Cả 6 tổng khớp Table 7. Chú thích Table 7 sửa thành "False positives are counted over seeds 42-44 (3 × 120 test covers; per seed in Suppl. Table S3)"; Bảng S3 nay ghi số theo từng seed.
- **Sửa một số trong Table 7:** mean recall của SRM+Ensemble P2 từ 0.070 thành **0.069** (150/2.160 = 0,0694; số cũ do lấy trung bình 6 giá trị đã làm tròn).
- **Residual-LR P1:** ba lần chạy giống hệt nhau (5/5/5), nên câu ở 4.5 khẳng định 5/120 FP mỗi lần chạy.
- Câu giải thích τ_low viết lại cho khớp code: τ_low nằm ngay trên điểm validation cover cao thứ hai (`thresholds()` của `sg.py`), nên một test cover có thể hoán đổi vượt ngưỡng với xác suất 2/121 ≈ 1,7% (nhỏ hơn một chút khi điểm bị trùng, như điểm phiếu của SRM+Ensemble; bài đã ghi "or less when scores are tied").
- Giữ nguyên kết luận "did not demonstrate reliable operation at FPR ≤ 1%".

### 4. References
- **Thứ tự [1]–[20] giữ nguyên.** Đã kiểm bằng script: thứ tự xuất hiện lần đầu của 20 tài liệu trong bài không đổi.
- **Metadata:** đối chiếu với bản ghi của nhà xuất bản hoặc chỉ mục (IEEE Xplore, ACM DL, SpringerOpen, SPIE, ScienceDirect, JMLR, PyPI, dblp, OpenAlex, HAL). Kết quả: 19/20 khớp, riêng [17] chỉ khớp một phần.
  - **Lưu ý trung thực:** mạng của phiên làm việc chặn mở trực tiếp IEEE Xplore, ACM DL, Crossref, doi.org và dblp. Vì vậy phần lớn thông tin lấy qua đoạn trích của các trang đó trong kết quả tìm kiếm; chỉ PyPI được mở trực tiếp. Trước khi nộp, một bạn nên bấm thử từng DOI.
  - Đã sửa [5], [6] (năm, viết hoa tên tạp chí), [8], [10], [11], [14]–[18] (tên tác giả, nơi đăng, tập, số, trang, DOI); [9] ghi số bài SPIE "p. 90280J". [1]–[16] và [18] đều ghi DOI; [17], [19], [20] không có DOI.
- **[17] MODE (EUSIPCO 2025):** xác nhận tác giả, tên, hội nghị (Palermo, 8–12/9/2025), thêm bản HAL https://hal.science/hal-05101274. Chưa ghi số trang và DOI vì IEEE Xplore chưa đăng kỷ yếu; cần bổ sung khi có.
- **[10]:** trang 534-1–534-11, nhà xuất bản IS&T. **[11], [13], [15]:** ghi tên hội nghị như các mục IEEE.
- **[20] sealwatch:** nay ghi phiên bản đã dùng: "Python package, version 2025.9, University of Innsbruck (2025)". Bản 2025.9 phát hành ngày 18/9/2025 và cho ra đúng từng giá trị SRM của bài. Không ghi "last accessed" vì chưa mở được trang GitHub để xác nhận ngày; nếu hội nghị yêu cầu thì thêm ", last accessed YYYY/MM/DD" sau URL.
- **Trình bày theo Springer LNCS:** nhãn "1."; References chữ 9 pt, giãn dòng 11 pt, thụt lề 341 twip theo style `referenceitem` của template; khoảng trắng không ngắt sau "pp.", "p.", "vol.".
- **Trích dẫn trong bài:** câu mở đầu "[5-7]" được viết lại cho đúng ba tài liệu (SRM features + FLD ensemble [6], SRNet [5], Yedroudj-Net [7]); ở 2.3, [10] chỉ đỡ vế "for algorithm shift, use large CNN training sets".
- **EndNote:** bản ghi nhúng trong 42 trường trích dẫn đã cập nhật theo metadata mới (kể cả [20]); `docs/endnote_sua_references.ris` có cả 20 bản ghi; Instant Formatting đã tắt trong file.

### 5. Rà soát cuối
- **Hình 1, 2:** bản 600 dpi. Fig. 2 được vẽ lại với CI mới bằng đúng script đã tạo hình cũ (chạy với số cũ thì ra file trùng từng byte với hình cũ).
- **Bảng 1–7:** đánh số liên tục bằng trường SEQ.
- **Số liệu:** mọi số của Table 4–7 và Bảng S1–S3 đã được tái lập từ ảnh gốc. `kiem_tra_hoanchinh.py` kiểm Table 4–7, Abstract, Conclusion, các CI ở mục 4 và câu 17/18 so với `results_data.py`.
- **Supplementary:** S2 có CI mới và ghi rõ cách bootstrap; S3 có FP từng seed; thêm một đoạn ngắn ghi phiên bản phần mềm đã tái lập mọi số.
- **Placeholder và tô vàng:** không còn.
- **Số trang:** 12 trang trong LibreOffice; lề và cỡ chữ thân bài giữ nguyên, References 9 pt theo style `referenceitem` của template (xem đầu báo cáo). Khi mở bằng Word nên xuất PDF kiểm lại.
- **Acknowledgement:** "This research is funded by the University of Economics Ho Chi Minh City, Vietnam (UEH)."

### Văn phong (tránh văn kiểu AI)
- Chỉ viết lại các câu đã thêm hoặc sửa (liệt kê ở mục "Các chỗ đổi trong bài"); phần còn lại giữ nguyên văn của nhóm. Vẫn nên chấm lại bản `Paper_HoanChinh_2` trên Turnitin trước khi nộp (xem mục CheckAI ở trên).
- Các câu mới ngắn, viết như mô tả phương pháp thông thường, không thêm khẳng định mới.
- Các công cụ dò AI không chính xác, nên không ai đảm bảo được một điểm số cụ thể.

## Hướng dẫn EndNote (để References không bị đổi lại khi bấm Update)

**Cách an toàn nhất: nộp file như hiện tại, không bấm Update.** References trong file đã là bản cuối. Instant Formatting đã được tắt trong file. Nếu tab EndNote trong Word vẫn hiện Instant Formatting đang bật thì chọn *Turn Instant Formatting Off* trước khi sửa gì.

EndNote sinh lại References từ **thư viện trên máy bạn** và từ **style đang chọn trong file**. File vẫn ghi style IEEE (của nhóm cũ). Nếu bấm *Update Citations and Bibliography* khi chưa sửa thư viện và chưa đổi style, References sẽ quay về dạng IEEE "[1] T. Filler, …" với dữ liệu cũ. Nếu vẫn muốn dùng EndNote, làm đúng thứ tự:

1. **Sửa thư viện EndNote.** Sửa **cả 20 bản ghi** theo `docs/endnote_sua_references.ris`. Mỗi bản ghi có dòng `N1` ghi số thứ tự trong bài và RecNum (RecNum 2, 3, 4, 5, 14, 8, 13, 22, 9, 20, 21, 7, 6, 23, 24, 26, 25, 27, 17, 28 ứng với [1]–[20]). Mỗi tác giả một dòng, dạng "Họ, Tên viết tắt".
   - Không xóa bản ghi cũ rồi nhập bản mới, vì như vậy đổi RecNum và EndNote sẽ không khớp trích dẫn trong file.
2. **Đổi style trong Word:** tab EndNote → ô *Style* → *Select Another Style…* → chọn style Springer LNCS (tên trong EndNote thường có chữ "Lecture Notes"). Nếu không có thì tải từ trang Output Styles của EndNote. Đổi trong menu của chương trình EndNote (Edit → Output Styles) không đổi style của file Word.
3. **Định dạng References:** tab EndNote → *Configure Bibliography* → *Layout*, chọn cỡ chữ 9, hanging indent 0,6 cm.
4. **Update Citations and Bibliography.** Thứ tự [1]–[20] không đổi vì đánh số theo thứ tự trích dẫn. Sau khi update, so từng dòng References với bản PDF kèm theo. Chỗ nào khác (ví dụ cách ghi "LNCS, vol." ở [18] hay "Proc. SPIE" ở [9], phụ thuộc style) thì sửa tay hoặc quay lại file gốc.
5. **Giữ độ nét của hình:** trước khi lưu trong Word, vào File → Options → Advanced → Image Size and Quality, tick "Do not compress images in file".


## Các chỗ đổi trong bài (để nhóm biết khi chạy kiểm tra đạo văn)
- Đoạn 1 của Introduction; đoạn cuối 2.3; câu mở đầu mục 3 (Fig. 1).
- Hai đoạn của 3.1; đoạn 3.2 và ô "Seed-dependent parts" của Table 2; câu Seeds ở 3.3.
- Hai đoạn của 3.5; hai đoạn của 4.5 và một ô của Table 7.
- Lần này (sau khi chạy lại):
  - CI ở Abstract, 4.2 (đoạn Under P1… và Answer to RQ1), 4.3, 4.4 (câu 17/18 và Answer to RQ3), Conclusion;
  - Table 5, Table 6 (cận trên cao nhất, số CI < 0), Fig. 2;
  - một câu mới ở 3.2 (điểm SRM), hai câu ở 3.5 (cách gộp, B, seed);
  - Abstract thêm "17 of 18 intervals below zero"; Conclusion đổi "all 18 comparisons" thành "all 18 point estimates";
  - Table 6: trung bình ΔAUC của SRM+Ensemble P1 từ −0.151 thành −0.150 (bản trước lấy trung bình ba số đã làm tròn; chú thích bảng ghi tính từ số chưa làm tròn);
  - câu xác suất 2/121 ở 4.5 thêm "or less when scores are tied";
  - chú thích Table 7; mục [20].
- Acknowledgement và References.

## Kiểm tra đã chạy
- `python3 scripts/kiem_tra_hoanchinh.py manuscript/Paper_HoanChinh_2.docm`: OK. Kiểm số Table 4–7, Abstract, Conclusion, CI ở mục 4, câu 17/18; 42 trích dẫn trỏ đúng tài liệu; thứ tự tài liệu không đổi; có Acknowledgement; References đúng danh mục.
- `verify_stats.py` trên kết quả chạy lại (B = 10.000): mọi số khớp `results_data.py`.
- `scripts/kiem_verify_stats.py <bossbase_pilot_results>`: `verify_stats.py` tính giống `sg.py` (AUC và CI 54/54 điều kiện pilot, ngưỡng trên 2.000 bộ dữ liệu thử).
- `scripts/srm_nhanh.py`: bản đếm đồng xuất hiện nhanh cho ra đặc trưng SRM trùng từng bit với sealwatch (14/14 ảnh kiểm).
- Hai chỗ cố ý giữ nguyên: chữ "Acknowledgement" (đúng chữ thầy đưa) và mã băm manifest "13c01ca9…2799e8c" (khớp `manifest.csv`).
