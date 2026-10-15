# Sửa bài StegaGuard theo góp ý cuối của thầy

**File nộp:** `manuscript/Paper_HoanChinh_2.docm`.
- Sửa trực tiếp trên `Paper_HoanChinh_1.docm` của nhóm: giữ nguyên cấu trúc, style, lề, cỡ chữ thân bài, các bảng và trường EndNote.
- Bản PDF xuất kiểm tra (LibreOffice) dài **12 trang**, kể cả References.
- Supplementary: `supplementary/StegaGuard_supplementary.docx` (3 trang, Bảng S1–S3).

## ⚠️ Điều nhóm cần biết trước khi nộp

Gói code gửi kèm (`StegaGuard_code_va_ket_qua.zip`) **chỉ là thí nghiệm pilot**:
- 180 cover chia 108/36/36, chỉ có Residual-LR;
- `run_boss_pilot.py` và `DOC_TRUOC.md` cũng tự ghi như vậy.

Bài báo thì báo cáo thí nghiệm **600 cover (360/120/120) với cả Residual-LR và SRM+Ensemble**; manifest của bài có SHA-256 bắt đầu bằng `13c01ca9`, còn pilot là `108fa1d7`. Gói code **không có**:
1. code SRM+Ensemble (trích đặc trưng bằng sealwatch, FLD ensemble L = 50, d_sub = 500);
2. kết quả và điểm dự đoán của các lần chạy 600 cover;
3. script tính ΔAUC ghép cặp và CI cho Table 5, Table 6, Fig. 2 và Bảng S2.

Vì vậy:
- **Đã xác nhận được từ code (`code/sg.py`):** cách tạo 76 đặc trưng, StandardScaler, tham số Logistic Regression, cách chọn ngưỡng τ_BER và τ_low, bootstrap (1.000 vòng, seed 2026, CI phân vị 2,5–97,5%), cách chia dữ liệu trước khi nhúng, audit chống rò rỉ, các cột của manifest. Code này dùng chung cho thí nghiệm 600 cover vì manifest của bài có đúng các cột mà `sg.py` tạo ra. Dù vậy nhóm vẫn nên khẳng định lại là đã chạy cùng `sg.py`.
- **Chưa xác nhận được bằng code hoặc dữ liệu gốc:**
  - cấu hình SRM+Ensemble;
  - cách gộp ΔAUC qua 3 seed: bài **không thêm** câu nào về việc này (xem mục 2 bên dưới);
  - số false positives của Table 7 so với điểm dự đoán từng seed;
  - toàn bộ số của Table 4–7 so với dữ liệu gốc.

  Hiện các số này chỉ khớp nhau và khớp `scripts/results_data.py`.
- **Việc nhóm cần làm:** tìm trên máy thư mục kết quả 600 cover (có `manifest.csv` với SHA-256 `13c01ca9…2799e8c`), code SRM+Ensemble và script phân tích ΔAUC, rồi gửi lại. Có các file đó thì:
  - xuất điểm dự đoán thành một file CSV theo cột ghi trong `scripts/verify_stats.py`;
  - chạy `python3 scripts/verify_stats.py scores.csv` để tính lại toàn bộ số trong bài;
  - nếu khớp thì có thể thêm một câu về cách gộp ΔAUC qua 3 seed vào mục 3.5; nếu không khớp thì sửa theo số tính lại.

  Không có các file này thì không thể trả lời trung thực mục 1 (SRM+Ensemble), mục 2 (cách gộp CI) và mục 3 (đối chiếu FP) của thầy.

## Thầy yêu cầu – đã làm gì

### 1. Section 3.2 – tái lập thực nghiệm
Thêm vào đoạn 3.2 (không thêm bảng) các thông tin lấy từ `sg.py` và 9 mô hình `model.joblib`. Mô hình được đọc an toàn, không thực thi file.
- **76 đặc trưng:** sai phân điểm ảnh bậc 1 và bậc 2 theo hai hướng (4 residual). Mỗi residual cho histogram chuẩn hóa 17 bin của giá trị đã cắt về [−8, 8], cộng trung bình trị tuyệt đối và độ lệch chuẩn, nên có 4 × 19 = 76 đặc trưng.
- **Chuẩn hóa:** StandardScaler nằm trong pipeline scikit-learn, chỉ fit trên đặc trưng train của từng lần chạy.
- **Logistic Regression:** L2, C = 1.0, solver lbfgs, không class weight (cặp train cân bằng 1:1), max_iter = 2000, random_state = seed của lần chạy. Mô hình lưu bằng scikit-learn 1.9.1. Điểm số là `decision_function`.
- **Mục 3.1:** thêm "bicubic interpolation", là cách thu nhỏ ảnh trong `prepare`.
- **SRM+Ensemble:** giữ nguyên câu cũ (106 submodel, 34,671 đặc trưng, L = 50, d_sub = 500). Mọi tài liệu của nhóm ghi giống nhau nhưng **chưa có code để đối chiếu** (xem phần ⚠️).

### 2. Section 3.5 – bootstrap
- Thêm: code đánh giá rút **B = 1.000** vòng cho mỗi điều kiện test, bộ sinh số cố định **seed 2026**. Vì bộ sinh được tạo lại cho mỗi điều kiện, mọi điều kiện, protocol và seed dùng **cùng một tập test cover được rút**. CI 95% là khoảng giữa phân vị 2,5% và 97,5% (`sg.py`, hàm `evaluate`).
- **Không thêm:** cách gộp ΔAUC và CI qua 3 seed. Script tính ΔAUC không có trong gói, và thầy yêu cầu chỉ ghi các bước đã chạy trong code, nên bài giữ nguyên mô tả cũ của nhóm: điểm ước lượng là trung bình của 3 hiệu theo từng seed, CI từ bootstrap ghép cặp theo test cover. Khi tìm được script, có thể thêm một câu như: "Each ΔAUC replicate is the difference of the two replicate AUCs, averaged over the three seeds" (chỉ thêm nếu script làm đúng như vậy).
- Thêm câu nói rõ CI chỉ phản ánh biến thiên trên 120 test cover cố định, không đại diện cho nguồn ảnh khác.
- Table 5, Table 6, Fig. 2 và S2: kiểm tự động bằng `scripts/kiem_tra_hoanchinh.py`, khớp `results_data.py`.

### 3. Section 4.5 – low FPR
- Bỏ câu "in none of them were recall and FPR both zero, so the detectors were never completely silent".
- Viết lại câu 54 rows / 6.480: đó là 6.480 lượt chấm điểm, do 9 mô hình của một detector chấm lặp lại trên cùng 720 ảnh stego (từ 120 cover), nên không phải mẫu độc lập. False positives trong Table 7 cũng là các lượt chấm lặp trên cùng 120 test cover.
- Kiểm số học Table 7: FP/360 khớp FPR từng ô; dòng gộp 49/1.080 = 0,045 và 37/1.080 = 0,034; recall trung bình 0,062 và 0,080 khớp Abstract.
- Code xác nhận: τ_low là giá trị ngay trên điểm validation cover cao thứ hai (cho phép tối đa 1 FP trên 120 cover), đúng như Eq. (1) và câu "just above the second-highest score".
- Giữ nguyên kết luận "did not demonstrate reliable operation at FPR ≤ 1%".
- **Chưa làm được:** đối chiếu FP với điểm dự đoán từng seed, vì cần kết quả 600 cover.

### 4. References
- **Thứ tự [1]–[20] giữ nguyên.** Đã kiểm bằng script: thứ tự xuất hiện lần đầu của 20 tài liệu trong bài không đổi.
- **Metadata:** từng tài liệu được kiểm qua nguồn chính thức hoặc chỉ mục (IEEE Xplore, ACM DL, SpringerOpen/Springer, SPIE, ScienceDirect, PyPI, dblp, OpenAlex, HAL). Kết quả: 18/20 khớp mọi trường.
  - Đã sửa [5] và [6]: năm và viết hoa tên tạp chí.
  - Đã sửa [8], [10], [11], [14], [15], [16], [17], [18]: tách đúng tên tác giả, bổ sung nơi đăng, tập, số, trang, DOI.
- **[17] MODE (EUSIPCO 2025):** xác nhận tác giả, tên, hội nghị (Palermo, 8–12/9/2025) và trang bắt đầu 810. Chưa có trang kết thúc và DOI trên IEEE Xplore nên không ghi, để tránh đoán. Khi IEEE Xplore đăng kỷ yếu thì bổ sung.
- **[20] sealwatch:** trích như phần mềm: Beneš, M., Lorch, B. (Đại học Innsbruck, 2024), tên theo PyPI "Implementation of modern image steganalysis algorithms", URL GitHub, ngày truy cập.
  - Gói code không ghi phiên bản sealwatch đã dùng. Nếu biết (ví dụ 2024.12) thì thêm ", version 2024.12" sau "Python package".
- **Trình bày theo Springer LNCS:**
  - nhãn "1." thay "[1]";
  - References dùng chữ 9 pt, giãn dòng 11 pt, thụt lề 341 twip, theo đúng style `referenceitem` của template. Đây là quy định của template, không phải giảm cỡ chữ để ép trang;
  - thân bài và lề giữ nguyên.
- **Trích dẫn trong bài:** câu mở đầu "…such as SPAM or the Spatial Rich Model (SRM) [5-7]" trỏ nhầm sang SRNet, Ensemble và Yedroudj-Net. Đã viết lại câu cho đúng ba tài liệu này và bỏ trích dẫn lặp "[5, 7]". Số thứ tự không đổi.
- **EndNote:** bản ghi nhúng trong 42 trường trích dẫn đã được cập nhật theo metadata mới. File `docs/endnote_sua_references.ris` có 20 bản ghi đã sửa. Xem các bước ở cuối file này.

### 5. Rà soát cuối
- **Hình 1, 2:** file của nhóm đang ở khoảng 220 dpi do Word nén. Đã thay bằng bản gốc 600 dpi, cùng tỉ lệ khung.
- **Bảng 1–7:** dùng trường SEQ nên đánh số liên tục; tên bảng và câu dẫn đúng vị trí.
- **Số liệu:** Abstract, Table 4–7, Results và Conclusion khớp nhau và khớp `results_data.py` (kiểm tự động).
- **Supplementary:** sửa tiêu đề cho trùng tên bài ("Lightweight…"); S1–S3 đầy đủ.
- **Placeholder và tô vàng:** không còn.
- **Số trang:** 12 trang trong LibreOffice, trang 12 còn khoảng 3 dòng trống. Khi mở bằng Word nên xuất PDF kiểm lại.
  - Để giữ 12 trang, đã bỏ một câu bị trùng ở 3.2: "Both detectors keep the same settings in every protocol and seed, so the configuration cannot explain differences between protocols." Ý này đã có ở Table 2 và mục 3.3.
- **Acknowledgement:** thêm trước References đúng câu của thầy: "This research is funded by the University of Economics Ho Chi Minh City, Vietnam (UEH)."

## Hướng dẫn EndNote (để References không bị đổi lại khi bấm Update)

References trong file đã đúng, nhưng EndNote sinh lại References từ **thư viện trên máy bạn**. Nếu thư viện còn bản ghi sai mà bấm *Update Citations and Bibliography* thì chữ sai sẽ quay lại. Làm theo thứ tự:

1. **Sửa thư viện EndNote.** Mở thư viện có các RecNum dưới đây. Sửa từng bản ghi theo `docs/endnote_sua_references.ris`: mỗi bản ghi có dòng `N1` ghi số thứ tự trong bài và RecNum. Mỗi tác giả một dòng, dạng "Họ, Tên viết tắt".
   - Các bản ghi cần sửa nhiều: RecNum 22 [8], 20 [10], 21 [11], 23 [14], 24 [15], 26 [16], 25 [17], 27 [18], 28 [20].
   - Các bản ghi chỉ sửa năm hoặc viết hoa: 14 [5], 8 [6], 7 [12], 17 [19].
   - Không xóa bản ghi cũ rồi nhập bản mới, vì như vậy đổi RecNum và EndNote sẽ không khớp trích dẫn trong file.
2. **Chọn output style:** Edit → Output Styles → chọn "Springer Lecture Notes Computer Sci" (hoặc tên tương tự trong Style Finder).
3. **Định dạng References:** Word → EndNote → Configure Bibliography → Layout, chọn cỡ chữ 9.
4. **Update Citations and Bibliography.** Thứ tự [1]–[20] không đổi vì đánh số theo thứ tự trích dẫn. Sau khi update, so References với file này.
5. **Giữ độ nét của hình:** trước khi lưu trong Word, vào File → Options → Advanced → Image Size and Quality, tick "Do not compress images in file".

## Kiểm tra đã chạy
- `python3 scripts/kiem_tra_hoanchinh.py manuscript/Paper_HoanChinh_2.docm`: khớp số Table 4–7, Abstract, Conclusion; 42 trích dẫn trỏ đúng tài liệu; thứ tự tài liệu không đổi; có Acknowledgement; References đúng danh mục.
- So văn bản cũ và mới bằng diff: chỉ đổi các đoạn ở 3.1, 3.2, 3.5, 4.5, câu mở đầu, Acknowledgement và References.
- Workflow rà soát 4 hướng (khớp code, checklist thầy, trích dẫn, văn phong): kết quả và các lỗi đã sửa ghi ở mục dưới.
