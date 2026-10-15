# Sửa bài StegaGuard theo góp ý cuối của thầy

**File nộp:** `manuscript/Paper_HoanChinh_2.docm`.
- Sửa trực tiếp trên `Paper_HoanChinh_1.docm` của nhóm: giữ nguyên cấu trúc, lề, cỡ chữ thân bài, các bảng và trường EndNote.
- Chỉ đổi style "EndNote Bibliography" của References: chữ 10 → 9 pt, giãn dòng 11 pt, thụt lề 341 twip, canh trái. Đây là đúng style `referenceitem` có sẵn trong template LNCS của file (9 pt, line 220), không phải giảm chữ để ép trang.
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

**Cập nhật: nhóm đã gửi 4 file chuẩn bị dữ liệu của bộ 600 cover** (`manifest.csv`, `preparation.json`, `audit.json`, `source_provenance.json`, nay lưu ở `data/stegaguard_600/`). Đã kiểm bằng `python3 scripts/kiem_du_lieu_600.py`, đạt 16/16 mục:
- SHA-256 của `manifest.csv` đúng `13c01ca9…2799e8c` như bài ghi, và khớp `preparation.json`;
- seed 20260918; ảnh thu về 256 × 256 trước khi nhúng; 600 cover, 4.200 ảnh PNG; 360/120/120 cover và 2.160/720/720 stego theo split; audit PASS, không cover nào rò sang split khác;
- tái lập được 3 bước:
  - việc chọn 600/10.000 ảnh BOSSbase: `random.Random(20260918).sample(...)` ra đúng 600/600 file;
  - việc chia split của `sg.py prepare`: 600/600 cover;
  - seed nhúng: 3.600/3.600;
- ảnh stego tạo bằng **mô phỏng nhúng của thư viện conseal** (không chứa thông điệp thật). Bài đã thêm chi tiết này vào 3.1 ("by the simulators in the conseal library (https://github.com/uibk-uncover/conseal)", URL kiểm qua PyPI). Không thêm mục mới vào References vì sẽ đổi số [19], [20] và làm bài vượt 12 trang. Khi có `pip freeze`, nên ghi phiên bản conseal (và sealwatch) vào Supplementary. Câu bicubic cũng được viết gọn lại để bài vẫn 12 trang.

Như vậy phần **dữ liệu** của bài đã được xác nhận đầy đủ, và `sg.py` chính là code đã dùng cho bộ 600 cover. Phần **kết quả** thì vẫn chưa có file. Để làm nốt các chỗ còn thiếu, nhóm cần gửi:
- thư mục kết quả của 18 lần chạy (2 detector × 3 protocol × 3 seed). Mỗi lần chạy gồm `config.json`, `thresholds.json`, và thư mục `*_test` có `predictions.csv`, `metrics.csv`, `evaluation.json`;
- code hoặc log chạy SRM+Ensemble;
- kết quả `pip freeze` của máy đã chạy SRM, để biết phiên bản sealwatch.

Trang cuối và DOI của [17] không nằm trong dữ liệu của nhóm; cần tra IEEE Xplore khi kỷ yếu EUSIPCO 2025 được đăng.

Vì vậy:
- **Đã xác nhận được từ code (`code/sg.py`):** cách tạo 76 đặc trưng, StandardScaler, tham số Logistic Regression, cách chọn ngưỡng τ_BER và τ_low, bootstrap (1.000 vòng, seed 2026, CI phân vị 2,5–97,5%), cách chia dữ liệu trước khi nhúng, audit chống rò rỉ, các cột của manifest. Code này dùng chung cho thí nghiệm 600 cover vì manifest của bài có đúng các cột mà `sg.py` tạo ra. Dù vậy nhóm vẫn nên khẳng định lại là đã chạy cùng `sg.py`.
- **Chưa xác nhận được bằng code hoặc dữ liệu gốc:**
  - cấu hình SRM+Ensemble;
  - cách gộp ΔAUC qua 3 seed: bài **không thêm** câu nào về việc này (xem mục 2 bên dưới);
  - số false positives của Table 7 so với điểm dự đoán từng seed;
  - toàn bộ số của Table 4–7 so với dữ liệu gốc.

  Hiện các số này chỉ khớp nhau và khớp `scripts/results_data.py`.
- **Việc nhóm cần làm:** tìm trên máy thư mục kết quả 600 cover (có `manifest.csv` với SHA-256 `13c01ca9…2799e8c`), code SRM+Ensemble và script phân tích ΔAUC, rồi gửi lại. Có các file đó thì:
  - gộp kết quả bằng `python3 scripts/gop_ket_qua.py <thư mục kết quả> gop --manifest-sha256 13c01ca998193e6925d599e43c6bf478021cac9759ff8a4b15e2a37a32799e8c`. Lệnh này tạo `gop/scores.csv` (điểm test) và `gop/thresholds.csv` (ngưỡng trong `thresholds.json`, vì `sg.py` không lưu điểm validation). Đã thử trên pilot: tính lại khớp `metrics.csv` của `sg.py` ở 54 điều kiện × 5 chỉ số;
  - chạy `python3 scripts/verify_stats.py gop/scores.csv --thresholds gop/thresholds.csv` để tính lại số của Table 4–7 và các ΔAUC/CI;
  - nếu khớp thì có thể thêm một câu về cách gộp ΔAUC qua 3 seed vào mục 3.5; nếu không khớp thì sửa theo số tính lại.

  Không có các file này thì không thể trả lời trung thực mục 1 (SRM+Ensemble), mục 2 (cách gộp CI) và mục 3 (đối chiếu FP) của thầy.
- **Với SRM+Ensemble, khi tìm được code hoặc log, cần xác nhận:**
  - (a) 106 submodel, 34.671 chiều;
  - (b) L = 50 và d_sub = 500 được cố định, không tự tối ưu;
  - (c) thư viện huấn luyện FLD ensemble;
  - (d) điểm nào của ensemble được dùng cho ROC và ngưỡng (tổng hay trung bình projection, hay số phiếu).

  Nếu (d) khác cách hiểu "score" ở 3.2 thì thêm nửa câu cho rõ.
- **Câu cuối mục 3.5** ("All tables can be recomputed from these files.") chỉ đúng khi nhóm còn giữ `predictions.csv`, `thresholds.json` và `manifest.csv` của bản 600 cover cho cả hai detector. Nếu không còn thì bỏ câu này trước khi nộp.
- **Cách gửi dữ liệu:** phiên Claude này chạy trên máy chủ đám mây nên không vào được máy của nhóm. Có hai cách:
  - nén thư mục kết quả 600 cover và code SRM+Ensemble rồi gửi vào khung chat (hoặc đẩy lên repo);
  - mở Claude ngay trên máy có dữ liệu: ứng dụng Claude Desktop, hoặc lệnh `claude remote-control` chạy trong thư mục đó.

### Các file đã tìm (không có kết quả 600 cover)
- Phiên Claude này chạy trên máy chủ đám mây, nên không vào được máy của nhóm để tự tìm. Đã xem hết mọi file nhóm gửi vào chat, nhưng không file nào là kết quả chạy 600 cover hay code SRM:
  - zip code (pilot 180 ảnh);
  - 4 file chuẩn bị dữ liệu 600 ảnh;
  - notebook `code_c_a_pp_nghi_n_c_u.ipynb` (code Chương 3, khảo sát giấc ngủ);
  - 5 script làm video hướng dẫn và mô tả dữ liệu, đều cho bản pilot 180 ảnh.
- Các script này khớp với bài ở hai điểm: ảnh được thu nhỏ bằng bicubic (Pillow), và ảnh stego được tạo bằng conseal.
- Kết quả thường nằm cạnh thư mục `bossbase_pilot_results` trên máy đã chạy, ví dụ `C:\Users\ACER\Downloads\paper\...`. Tìm các thư mục có `thresholds.json` mà `config.json` ghi `manifest_sha256` = `13c01ca9…`.

### Báo cáo CheckAI (Turnitin) nhóm gửi
- `CheckAI.pdf` ngày 14/10 chấm **một bản cũ** của bài (13 trang, có Table 11 và Fig. 4): 36% bị đánh dấu AI, gồm 21 đoạn.
- Đã đối chiếu tự động từng đoạn bị đánh dấu với bản hiện tại. Gần như không đoạn nào còn nguyên, chỉ còn tên Table 1 (gần giống) và 2 câu na ná ở 4.1 và Conclusion. Vì vậy con số 36% không áp dụng cho file hiện tại.
- Nhóm nên nộp bản `Paper_HoanChinh_2` lên Turnitin để chấm lại. Nếu còn đoạn bị đánh dấu, gửi báo cáo mới để xem đúng các đoạn đó; tốt nhất là nhóm tự viết lại các đoạn đó bằng lời của mình.
- Làm theo quy định của trường và hội nghị về việc dùng AI hỗ trợ viết. Springer yêu cầu ghi rõ việc dùng LLM nếu vượt quá mức sửa câu chữ.

## Thầy yêu cầu – đã làm gì

### 1. Section 3.2 – tái lập thực nghiệm
Thêm vào đoạn 3.2 (không thêm bảng) các thông tin lấy từ `sg.py` và 9 mô hình `model.joblib`. Mô hình được đọc an toàn, không thực thi file.
- **76 đặc trưng:** sai phân điểm ảnh bậc 1 và bậc 2 theo hai hướng (4 residual). Mỗi residual cho histogram chuẩn hóa 17 bin của giá trị đã cắt về [−8, 8], cộng trung bình trị tuyệt đối và độ lệch chuẩn của residual **chưa cắt**, nên có 4 × 19 = 76 đặc trưng.
- **Chuẩn hóa:** StandardScaler nằm trong pipeline scikit-learn, chỉ fit trên đặc trưng train của từng lần chạy.
- **Logistic Regression:** L2, C = 1.0, solver lbfgs, không class weight (cặp train cân bằng 1:1), max_iter = 2000. Mô hình lưu bằng scikit-learn 1.9.1. Điểm số là `decision_function`.
  - random_state = seed của lần chạy, nhưng lbfgs không dùng tới nên việc fit là tất định.
  - Vì vậy đã sửa ô "Seed-dependent parts" của Residual-LR trong Table 2 thành "variant sampling (P2, P3)".
  - Câu ở 3.3 sửa thành "Seeds 42-44 control the variant draws and the random parts of SRM+Ensemble fitting." 
- **Mục 3.1:** ghi rõ ảnh được thu nhỏ bằng bicubic ("bicubically downsampled", đúng như `prepare` trong `sg.py`), và ảnh stego được tạo bằng mô phỏng nhúng của conseal (`preparation.json`).
- **SRM+Ensemble:** giữ nguyên câu cũ (106 submodel, 34,671 đặc trưng, L = 50, d_sub = 500). Mọi tài liệu của nhóm ghi giống nhau nhưng **chưa có code để đối chiếu** (xem phần ⚠️).

### 2. Section 3.5 – bootstrap
- Thêm (câu cuối đoạn đầu 3.5): code đánh giá rút **B = 1.000** vòng cho mỗi điều kiện test, bộ sinh số cố định **seed 2026**. Vì bộ sinh được tạo lại cho mỗi điều kiện, mọi điều kiện, protocol và seed dùng **cùng một tập test cover được rút**. CI 95% là khoảng giữa phân vị 2,5% và 97,5% (`sg.py`, hàm `evaluate`).
- **Không thêm:** cách gộp ΔAUC và CI qua 3 seed. Script tính ΔAUC không có trong gói, và thầy yêu cầu chỉ ghi các bước đã chạy trong code, nên bài giữ nguyên mô tả cũ của nhóm: điểm ước lượng là trung bình của 3 hiệu theo từng seed, CI từ bootstrap ghép cặp theo test cover. Khi tìm được script, có thể thêm một câu như: "Each ΔAUC replicate is the difference of the two replicate AUCs, averaged over the three seeds" (chỉ thêm nếu script làm đúng như vậy).
- Thêm câu nói rõ CI chỉ phản ánh biến thiên khi lấy mẫu lại 120 test cover cố định, không mở rộng sang nguồn ảnh khác ("they account only for test-cover sampling and do not extend to other image sources").
- Sửa câu lưu trữ cho đúng code: mỗi lần chạy lưu điểm test từng ảnh và ngưỡng chọn trên validation (code không lưu điểm validation).
- Table 5 và Table 6: kiểm tự động bằng `scripts/kiem_tra_hoanchinh.py`, khớp `results_data.py`. Fig. 2 và Bảng S2 không được script này đọc, nhưng được vẽ và sinh từ chính `results_data.py` (`make_figures.py`, `build_supplementary.py`).

### 3. Section 4.5 – low FPR
- Bỏ câu "in none of them were recall and FPR both zero, so the detectors were never completely silent".
- Viết lại câu 54 rows / 6.480: đó là 6.480 lượt chấm điểm, do 9 mô hình của một detector chấm lặp lại trên cùng 720 ảnh stego (từ 120 cover), nên không phải mẫu độc lập. False positives trong Table 7 cũng là các lượt chấm lặp trên cùng 120 test cover.
- Kiểm số học Table 7: FP/360 khớp FPR từng ô; dòng gộp 49/1.080 = 0,045 và 37/1.080 = 0,034; recall trung bình 0,062 và 0,080 khớp Abstract.
- **Sửa một số trong Table 7:** mean recall của SRM+Ensemble P2 từ 0.070 thành **0.069**.
  - Mỗi recall trong S1 là (số stego bắt được qua 3 seed)/360. Sáu ô của P2 ứng với 14, 56, 9, 35, 10 và 26 ảnh, tổng 150/2.160 = 0,0694, làm tròn là 0,069.
  - Số 0.070 cũ do lấy trung bình 6 giá trị đã làm tròn (0,0695). Các ô khác của Table 7 không đổi.
- **Residual-LR P1:** code cho thấy ba lần chạy giống hệt nhau (P1 không rút biến thể, lbfgs tất định). Vì vậy câu ở 4.5 khẳng định chắc 5/120 FP mỗi lần chạy, thay vì viết "nếu".
- Câu giải thích τ_low viết lại cho khớp code: "τlow rests on the second-highest of only 120 validation cover scores … An exchangeable test cover exceeds this threshold with probability 2/121 ≈ 1.7%". Hàm `thresholds()` của `sg.py` đặt τ_low ngay trên điểm validation cover cao thứ hai (`np.nextafter`), tức là ngưỡng nhỏ nhất thỏa Eq. (1), cho phép tối đa 1 FP trên 120 cover.
- Giữ nguyên kết luận "did not demonstrate reliable operation at FPR ≤ 1%".
- **Chưa làm được:** đối chiếu FP với điểm dự đoán từng seed, vì cần kết quả 600 cover.

### 4. References
- **Thứ tự [1]–[20] giữ nguyên.** Đã kiểm bằng script: thứ tự xuất hiện lần đầu của 20 tài liệu trong bài không đổi.
- **Metadata:** đối chiếu với bản ghi của nhà xuất bản hoặc chỉ mục (IEEE Xplore, ACM DL, SpringerOpen, SPIE, ScienceDirect, JMLR, PyPI, dblp, OpenAlex, HAL). Kết quả: 19/20 khớp, riêng [17] chỉ khớp một phần.
  - **Lưu ý trung thực:** mạng của phiên làm việc chặn mở trực tiếp IEEE Xplore, ACM DL, Crossref, doi.org và dblp. Vì vậy phần lớn thông tin lấy qua đoạn trích của các trang đó trong kết quả tìm kiếm; chỉ PyPI được mở trực tiếp.
  - Vài trường chỉ có nguồn phụ: DOI của [2] (ResearchGate và bài trích dẫn), số trang của [7] (tóm tắt tìm kiếm), [4] (OpenAlex).
  - Trước khi nộp, một bạn nên bấm thử từng DOI để chắc chắn.
  - Đã sửa [5] và [6]: năm và viết hoa tên tạp chí.
  - Đã sửa [8], [10], [11], [14], [15], [16], [17], [18]: tách đúng tên tác giả, bổ sung nơi đăng, tập, số, trang, DOI.
  - [9]: ghi số bài SPIE "p. 90280J" thay cho "pp. 204–215" (số bài chính thức của Proc. SPIE 9028).
  - Mọi mục có DOI ([1]–[16], [18]) đều được thêm DOI.
- **[17] MODE (EUSIPCO 2025):** xác nhận tác giả, tên, hội nghị (Palermo, 8–12/9/2025) và trang bắt đầu 810.
  - Đã thêm đường dẫn bản HAL đã kiểm: https://hal.science/hal-05101274.
  - Chưa có trang kết thúc và DOI trên IEEE Xplore nên không ghi, để tránh đoán. Khi IEEE Xplore đăng kỷ yếu thì bổ sung.
- **[10]:** ghi trang 534-1–534-11 và nhà xuất bản IS&T thay cho "paper MWSF-534", để thống nhất với các mục kỷ yếu khác.
- **[11], [13], [15]:** bỏ "Proc." và năm dạng ’25. Ghi giống các mục IEEE, ví dụ "In: 33rd ACM International Conference on Multimedia (MM 2025)".
- Sau "pp.", "p." và "vol." dùng khoảng trắng không ngắt, như LNCS, để số trang không bị tách xuống dòng. EndNote Update sẽ đổi lại khoảng trắng thường; khi đó chỉ ảnh hưởng chỗ ngắt dòng.
- **[20] sealwatch:** trích như phần mềm: Beneš, M., Lorch, B. (Đại học Innsbruck, 2024), tên theo PyPI "Implementation of modern image steganalysis algorithms", URL GitHub (xác nhận qua mục Source trên PyPI).
  - Không ghi "last accessed …", vì chưa mở được trang GitHub để xác nhận ngày.
  - Nếu hội nghị yêu cầu ngày truy cập: một bạn mở https://github.com/uibk-uncover/sealwatch rồi thêm ", last accessed YYYY/MM/DD" (ngày mở thật) sau URL.
  - Gói code không ghi phiên bản sealwatch đã dùng. Nếu biết (ví dụ 2024.12) thì thêm ", version 2024.12" sau "Python package".
- **Trình bày theo Springer LNCS:**
  - nhãn "1." thay "[1]";
  - References dùng chữ 9 pt, giãn dòng 11 pt, thụt lề 341 twip, theo đúng style `referenceitem` của template. Đây là quy định của template, không phải giảm cỡ chữ để ép trang;
  - thân bài và lề giữ nguyên.
- **Trích dẫn trong bài:**
  - Câu mở đầu "…such as SPAM or the Spatial Rich Model (SRM) [5-7]" trỏ nhầm sang SRNet, Ensemble và Yedroudj-Net. Đã viết lại câu cho đúng ba tài liệu này (SRM features + Fisher linear discriminant ensemble [6], SRNet [5], Yedroudj-Net [7]) và bỏ trích dẫn lặp "[5, 7]". Số thứ tự không đổi.
  - Mục 2.3: [10] chỉ nói về algorithm shift với tập train CNN lớn. Câu sửa thành "…or, for algorithm shift, use large CNN training sets [10]" để trích dẫn đỡ đúng vế của nó.
- **EndNote:**
  - Bản ghi nhúng trong 42 trường trích dẫn đã được cập nhật theo metadata mới, tên kỷ yếu ghi giống hệt References đang in.
  - File `docs/endnote_sua_references.ris` có cả 20 bản ghi đã sửa.
  - **Đã tắt Instant Formatting của EndNote trong file**, để khi mở bằng máy có EndNote, References không tự sinh lại theo style IEEE và thư viện cũ. Xem các bước ở cuối file này.

### 5. Rà soát cuối
- **Hình 1, 2:** file của nhóm đang ở khoảng 220 dpi do Word nén. Đã thay bằng bản gốc 600 dpi, cùng tỉ lệ khung.
- **Bảng 1–7:** dùng trường SEQ nên đánh số liên tục; tên bảng và câu dẫn đúng vị trí.
- **Số liệu:** Table 4–7, các số chính của Abstract và số RQ1 ở Conclusion được kiểm tự động, khớp `results_data.py`. Các số khác trong Results được dò tay.
- **Supplementary:** sửa tiêu đề cho trùng tên bài ("Lightweight…"); S1–S3 đầy đủ.
- **Placeholder và tô vàng:** không còn.
- **Hình 1:** hình không đánh số stage, nên câu dẫn "Stages 1-3 … stages 4-5 … stages 6-7" được sửa thành mô tả theo vị trí trong hình (left column, two middle lanes, right side).
- **Số trang:** 12 trang trong LibreOffice, trang 12 còn khoảng 2 dòng trống. Khi mở bằng Word nên xuất PDF kiểm lại.
  - Để giữ 12 trang mà không đổi font hay lề, đã bỏ một câu bị trùng ở 3.2: "Both detectors keep the same settings in every protocol and seed, so the configuration cannot explain differences between protocols." Ý này đã có ở Table 2 và mục 3.3.
  - Bỏ thêm chữ "also" ở 2.3.
  - Viết "Seeds 42-44" thay "Seeds 42, 43 and 44" ở 3.3.
- **Acknowledgement:** thêm trước References đúng câu của thầy: "This research is funded by the University of Economics Ho Chi Minh City, Vietnam (UEH)."

### Văn phong (tránh văn kiểu AI)
- Chỉ viết lại các câu đã thêm hoặc sửa trong lần này. Văn bản gốc của nhóm giữ nguyên, nên kết quả kiểm tra đạo văn trước đó vẫn dùng được.
- Cách làm:
  - hai người viết độc lập đề xuất bản viết lại;
  - người phản biện chọn bản giữ đúng ý và số liệu (đối chiếu `sg.py`, `results_data.py`), không dài hơn câu cũ, không thêm khẳng định mới.
- Đã viết lại:
  - câu SRM/CNN ở Introduction;
  - câu dẫn Fig. 1;
  - hai câu mới ở 3.2: tách câu nối bằng dấu chấm phẩy;
  - câu bootstrap ở 3.5 ("We resample the 120 test covers B = 1,000 times …");
  - câu giới hạn CI và câu lưu trữ ở 3.5;
  - câu τ_low ở 4.5;
  - câu 54 rows / 6.480 ở 4.5 (tách làm ba câu ngắn).
- Giữ nguyên vì bản mới không tốt hơn: vế [10] ở 2.3, câu Seeds ở 3.3, câu 5/120 ở 4.5.
- Các câu mới không còn chuỗi mệnh đề nối bằng dấu chấm phẩy. Các dấu chấm phẩy còn lại trong bài là của nhóm.
- Lưu ý: các công cụ dò AI không chính xác, nên không ai đảm bảo được một điểm số cụ thể. Lần sửa này chỉ làm cho các câu mới tự nhiên và giống giọng phần nhóm tự viết.

## Hướng dẫn EndNote (để References không bị đổi lại khi bấm Update)

**Cách an toàn nhất: nộp file như hiện tại, không bấm Update.** References trong file đã là bản cuối. Instant Formatting đã được tắt trong file. Nếu tab EndNote trong Word vẫn hiện Instant Formatting đang bật thì chọn *Turn Instant Formatting Off* trước khi sửa gì.

EndNote sinh lại References từ **thư viện trên máy bạn** và từ **style đang chọn trong file**. File vẫn ghi style IEEE (của nhóm cũ). Nếu bấm *Update Citations and Bibliography* khi chưa sửa thư viện và chưa đổi style, References sẽ quay về dạng IEEE "[1] T. Filler, …" với dữ liệu cũ. Nếu vẫn muốn dùng EndNote, làm đúng thứ tự:

1. **Sửa thư viện EndNote.** Sửa **cả 20 bản ghi** theo `docs/endnote_sua_references.ris`. Mỗi bản ghi có dòng `N1` ghi số thứ tự trong bài và RecNum (RecNum 2, 3, 4, 5, 14, 8, 13, 22, 9, 20, 21, 7, 6, 23, 24, 26, 25, 27, 17, 28 ứng với [1]–[20]). Mỗi tác giả một dòng, dạng "Họ, Tên viết tắt".
   - Không xóa bản ghi cũ rồi nhập bản mới, vì như vậy đổi RecNum và EndNote sẽ không khớp trích dẫn trong file.
2. **Đổi style trong Word:** tab EndNote → ô *Style* → *Select Another Style…* → chọn style Springer LNCS (tên trong EndNote thường có chữ "Lecture Notes"). Nếu không có thì tải từ trang Output Styles của EndNote. Đổi trong menu của chương trình EndNote (Edit → Output Styles) không đổi style của file Word.
3. **Định dạng References:** tab EndNote → *Configure Bibliography* → *Layout*, chọn cỡ chữ 9, hanging indent 0,6 cm.
4. **Update Citations and Bibliography.** Thứ tự [1]–[20] không đổi vì đánh số theo thứ tự trích dẫn. Sau khi update, so từng dòng References với bản PDF kèm theo. Chỗ nào khác (ví dụ cách ghi "LNCS, vol." ở [18] hay "Proc. SPIE" ở [9], phụ thuộc style) thì sửa tay hoặc quay lại file gốc.
5. **Giữ độ nét của hình:** trước khi lưu trong Word, vào File → Options → Advanced → Image Size and Quality, tick "Do not compress images in file".

## Kiểm tra đã chạy
- `python3 scripts/kiem_tra_hoanchinh.py manuscript/Paper_HoanChinh_2.docm`: khớp số Table 4–7, Abstract, Conclusion; 42 trích dẫn trỏ đúng tài liệu; thứ tự tài liệu không đổi; có Acknowledgement; References đúng danh mục.
- So văn bản cũ và mới bằng diff. Chỉ đổi các chỗ sau (để nhóm biết khi chạy kiểm tra đạo văn):
  - đoạn 1 của Introduction;
  - đoạn cuối 2.3;
  - câu mở đầu mục 3 (Fig. 1);
  - hai đoạn của 3.1;
  - đoạn 3.2 và ô "Seed-dependent parts" của Table 2;
  - câu Seeds ở 3.3;
  - hai đoạn của 3.5;
  - hai đoạn của 4.5 và một ô của Table 7;
  - Acknowledgement và References.
- Workflow rà soát 4 hướng (khớp code, checklist thầy, trích dẫn, văn phong). Các lỗi đã sửa đều ghi ở các mục trên.
- Không làm theo hai đề xuất:
  - Đổi "Acknowledgement" thành "Acknowledgments": giữ đúng chữ thầy đưa.
  - Sửa mã băm manifest "13c01ca9…2799e8c": giữ nguyên. Nay đã kiểm với `manifest.csv` nhóm gửi: mã đầy đủ là `13c01ca9…a32799e8c`, nên cách viết tắt trong bài đúng.
- **`scripts/verify_stats.py`** (script tính lại số liệu từ điểm từng ảnh) đã sửa cho khớp `sg.py`:
  - B = 1000;
  - mỗi lần bootstrap dùng một bộ sinh mới `default_rng(2026)`;
  - cover lấy theo thứ tự manifest;
  - τ_BER tính giống hệt `sg.py`, kể cả khi có điểm trùng;
  - đọc được ngưỡng có sẵn từ `thresholds.json` (tùy chọn `--thresholds`), vì `sg.py` không lưu điểm validation.

  Đã kiểm bằng `python3 scripts/kiem_verify_stats.py <thư mục bossbase_pilot_results>`:
  - AUC và CI 95% khớp `metrics.csv` của `sg.py` ở cả 54/54 điều kiện pilot (sai khác < 1e-12);
  - τ_BER và τ_low khớp `sg.py` trên 2.000 bộ dữ liệu thử.

  Khi có điểm 600 cover, chạy `verify_stats.py` để kiểm lại toàn bộ Table 4–7 và CI của ΔAUC. Riêng cách gộp CI qua 3 seed là lựa chọn của script (lấy trung bình ΔAUC của từng replicate), chưa có trong code nhóm.
