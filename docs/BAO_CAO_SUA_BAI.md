# Báo cáo chỉnh sửa bản thảo StegaGuard theo góp ý của thầy

Tệp kết quả:

| Tệp | Nội dung |
|---|---|
| `manuscript/StegaGuard_revised.docx` | Bản thảo đã sửa, dựng trên template Springer LNCS của PaperID 581 (A4, lề 4,4/5,2 cm, Times 10pt) |
| `manuscript/StegaGuard_revised.pdf` | Bản PDF xuất bằng LibreOffice: **12 trang**, kể cả References; trang cuối đầy khoảng 82% |
| `supplementary/StegaGuard_supplementary.docx/.pdf` | Table S1 (đủ 36 điều kiện: AUC±SD, F1, BER, Recall, FPR), Table S2 (18 so sánh payload kèm CI), Table S3 (số false positive) |
| `docs/references.ris` | 21 tài liệu tham khảo dạng RIS để import vào EndNote |
| `docs/reference_verification.md` | Kết quả kiểm chứng từng tài liệu tham khảo (nguồn, DOI, mục còn phải kiểm) |
| `scripts/verify_stats.py` | Tính lại AUC, ngưỡng, số FP và bootstrap ghép cặp từ prediction scores gốc |
| `scripts/audit_manifest.py` | Kiểm tra manifest: không có source cover nằm ở hai tập, đủ 6 biến thể mỗi cover, đúng 360/120/120 |

> **Quan trọng:** bản thảo còn **28 chỗ tô vàng** `[...]`. Đó là các thông tin chỉ có trong code hoặc log thí nghiệm (tham số, phiên bản thư viện, quy tắc lấy mẫu...). Thầy yêu cầu *không bổ sung tham số theo suy đoán*, nên tôi không tự điền. Danh sách ở Mục C. Phải điền hết và bỏ tô vàng trước khi nộp.

---

## A. Hai yêu cầu chung

### A1. Tỉ lệ AI 36%

- Toàn bộ phần chữ đã được viết lại: cấu trúc câu khác, nội dung cụ thể hơn, và bỏ các đoạn bị Turnitin tô xanh (Mục 1.1, 1.2, 2.2, 2.3, 3.1, 4.1, 4.5, 4.6, 5 của bản cũ).
- **Cần nói rõ:** phần chữ mới cũng do trợ lý AI (Claude) soạn. Vì vậy nó **không** tự động làm giảm tỉ lệ AI, và tôi không dùng kỹ thuật nào để "né" công cụ phát hiện.
- Để đạt yêu cầu thật sự, nhóm nên:
  1. Đọc và viết lại bằng lời của mình, đặc biệt các đoạn diễn giải ở Mục 1, 2 và 4.6.
  2. Chạy lại Turnitin trước khi nộp.
  3. Kiểm tra quy định của hội thảo về khai báo việc dùng công cụ AI hỗ trợ viết.

### A2. Bố cục giống PaperID 581, không lấy nội dung

Bản thảo được dựng trực tiếp trên các style LNCS của tệp 581: `papertitle`, `author`, `address`, `abstract`, `keywords`, `heading1/heading2` (tự đánh số), `p1a`, `tablecaption`, `figurecaption`, `referenceitem` (tự đánh số).

Các điểm giống 581:
- "**Abstract.**" viết liền dòng, có thêm dòng **Keywords** (bản cũ không có).
- Câu hỏi nghiên cứu trình bày dạng bullet; mục "**Contributions.**" là đoạn có tiêu đề in đậm đầu đoạn.
- Chú thích bảng đặt **trên** bảng, chú thích hình đặt **dưới** hình.
- References theo kiểu Springer có đánh số.

Nội dung của 581 (văn bản, biểu đồ, dữ liệu EndNote, VBA) đã bị loại bỏ hoàn toàn khỏi template (`templates/lncs`). Footer nội bộ "StegaGuard 600-cover robustness manuscript" không còn.

---

## B. Đối chiếu từng nhận xét

### 1. Introduction

| Yêu cầu | Đã làm |
|---|---|
| Viết lại theo trình tự Background → Security Problem → Existing Limitations → Research Gap → Motivation | Bốn đoạn theo đúng trình tự này. Đoạn 4 tách khoảng trống thành hai phía: hạn chế của *detector* và hạn chế của *thiết kế đánh giá* |
| Xóa câu nhắc bản thảo cũ ("The first draft…", "This version…", "earlier 180-cover draft"…) | Đã xóa toàn bài, kể cả ở Mục 3.1 và 3.5 |
| Bỏ placeholder [X], [Y] | Bỏ câu chứa placeholder. Giá trị matched-condition (0,714 và 0,546) nằm ở Table 4 và Mục 4.2 |
| Làm rõ ba vấn đề: unseen algorithm, mixed training, payload shift | RQ1–RQ3 viết lại, mỗi RQ gắn với protocol: RQ1↔P1 (WOW 0,4 so với HILL 0,4); RQ2↔P3 so với P2; RQ3↔P1–P3, 0,4 so với 0,1 bpp. Table 3 có cột "Role" ánh xạ ngược lại |
| Contributions theo hướng controlled evaluation, leakage prevention, robustness assessment, security operating point | Viết lại đúng 4 ý (i)–(iv) |
| Không gọi là "novel detector" | Ghi rõ "evaluates two existing detectors and proposes no new detection algorithm". **Tên bài** đổi "Lightweight" → "Feature-Based", vì SRM+Ensemble (34.671 chiều) không phải detector nhẹ. Nhóm có thể đổi lại nếu thầy muốn giữ tên cũ |

### 2. Related Work

| Yêu cầu | Đã làm |
|---|---|
| Cấu trúc 2.1 / 2.2 / 2.3 | 2.1 Image Steganalysis Techniques; 2.2 Robustness under Algorithm and Payload Shifts; 2.3 Research Gap and Comparative Analysis |
| Phân biệt algorithm shift, payload shift, cover-source shift | Mục 2.2 định nghĩa từng loại, mỗi loại có dẫn chứng. Có thêm một đoạn về operating point (MD5 của ALASKA, ngưỡng FPR định trước, MODE) |
| Table 1: 6–8 nghiên cứu, có dataset, detector, protocol, loại robustness | 7 nghiên cứu (SRM, Yedroudj-Net, SRNet, CSM 2014, Butora & Fridrich 2019, ALASKA, MODE 2025) cộng dòng "This study". Các cột: Data, Detector, Protocol and metric, Shift, Low-FPR metric |
| Không ghi "No" nếu chưa xác minh | Dùng "Not reported" và có câu giải thích nghĩa của nó. Một số ô vẫn cần nhóm đọc PDF gốc để xác nhận (xem `reference_verification.md`, mục D) |
| Bổ sung nghiên cứu 2023–2026 | Yu et al. 2023 (payload mismatch), Mallet et al. 2024 (tổng quan CSM), Wang et al. 2025 (ACM MM, mismatch thuật toán và nguồn ảnh), Butora & Bas 2025 (MODE, FPR thấp). Thêm Butora & Fridrich 2019, nghiên cứu sát nhất với RQ1/RQ2: khi HILL là thuật toán bị giữ lại thì mất mát lớn nhất |
| Rút gọn mô tả từng công trình; viết đoạn tổng hợp gap cuối 2.3 | Đã làm. Mục 2.2 không còn bàn về gap, tránh trùng với 2.3 |

### 3. Methodology (ưu tiên dung lượng)

| Yêu cầu | Đã làm |
|---|---|
| 600 / 3.600 / 4.200; số ảnh theo thuật toán và payload | 600 stego cho mỗi điều kiện; train/val/test lần lượt 2.160/720/720 stego, tức 360/120/120 mỗi điều kiện (đã kiểm tra số học) |
| Chia tập trước hay sau khi tạo stego | Ghi rõ: chia source cover **trước**, nhúng **sau**. Mỗi stego kế thừa cover_id và split của cover gốc |
| Đối chiếu manifest | Có câu mô tả audit, kèm script `audit_manifest.py` để nhóm chạy lại trên manifest thật |
| 360 training pairs, 120 val, 120 test | Mục 3.1 và 3.3, Table 3 |
| 76 features, scaling, tham số LR, cấu hình SRM+Ensemble | Table 2 (cấu hình detector) và Mục 3.2. Các giá trị chưa có trong bản cũ được **tô vàng** (Mục C) |
| Bảng tổng hợp P1–P3, quy tắc lấy mẫu, P2 khác P3 ở đâu | Table 3 có cột training pool, thành phần kỳ vọng và vai trò với RQ. Mục 3.3 nêu cách rút một biến thể cho mỗi cover theo seed, và nêu P2/P3 chỉ khác nhau ở biến thể 0,1 bpp |
| Metrics, ngưỡng chọn trên validation | Mục 3.4: τ_BER (cho F1, BER) và τ_low ở Eq. (1); ghi rõ "never from test labels" |
| Bootstrap: số lần, đơn vị resampling, giữ cặp, gộp 3 seed | Mục 3.5: đơn vị là source test cover; cùng một lần rút cho cả hai điều kiện và cả ba seed; khoảng CI theo phân vị của ΔAUC trung bình qua seed. **B** và cách gộp seed cần xác nhận với code |
| Môi trường thực nghiệm | Mục 3.5 có các chỗ tô vàng cho phiên bản thư viện và phần cứng |
| Figure 1 thể hiện đủ luồng, hai detector song song | Vẽ lại: BOSSbase → Source-cover split → Stego generation → Feature extraction và Detector training (**hai làn song song** Residual-LR / SRM+Ensemble) → P1/P2/P3 evaluation → 4 nhánh (RQ1, RQ2, RQ3, Operating point) → Robustness and security metrics |
| Bớt bảng audit/checklist trùng | Bỏ Table "Metric roles", Table "Reproducibility checklist" và Table "Detector implementation audit" cũ. Thông tin hữu ích được đưa vào chữ và Table 2 |

### 4. Results and Discussion

| Mục | Đã làm |
|---|---|
| 4.1 | Table 4 chỉ còn ma trận AUC 6×6 (bảng cũ 36 dòng chuyển sang Supplementary S1). Nêu Residual-LR gần ngẫu nhiên nên **SRM+Ensemble là bằng chứng chính** |
| 4.2 (RQ1) | Báo cáo ΔAUC kèm CI. Kiểm tra dấu: ΔAUC = điều kiện bị shift trừ điều kiện tham chiếu, thống nhất cho RQ1–RQ3. Nêu rằng WOW và HILL khác nhau cả về **độ khó phát hiện**, không chỉ về độ lệch thuật toán, nên cần một tham chiếu HILL matched mà nghiên cứu chưa chạy. Không khẳng định robustness. Có đoạn "Answer to RQ1" |
| 4.3 (RQ2) | Dùng đúng câu "No reliable improvement was observed under the evaluated mixed-training protocol." Nêu P3 khác P2 ở chỗ thêm 0,1 bpp, khiến số mẫu 0,4 bpp còn khoảng một nửa. CI chứa 0 thì "inconclusive", không phải "equivalence". Giới hạn phạm vi kết luận |
| 4.4 (RQ3) | Hình 2 (trước là Fig. 3) chuyển thành forest plot của ΔAUC kèm CI cho 18 so sánh, gọn hơn và không còn khoảng trắng. Table 6 tổng hợp theo detector × protocol; bảng 18 dòng chuyển sang S2. Tách *xu hướng nhất quán* khỏi *ý nghĩa thống kê*: CI chưa hiệu chỉnh đa so sánh, các so sánh dùng chung cover và mô hình, và một CI của Residual-LR chạm −0,001. Có đoạn "Answer to RQ3" |
| 4.5 (Low-FPR) | Phân biệt ngưỡng chọn trên validation với FPR quan sát trên test. **Số FP thực tế** suy ra duy nhất từ FPR đã báo cáo: Residual-LR 15/15/19 trên 360 (P1 là 5 FP mỗi lần chạy), SRM 18/11/8 trên 360, tổng 49 và 37 trên 1.080. Khoảng Clopper–Pearson cho 5/120 là [1,4%; 9,5%], không chứa 1%. Giải thích "0/54" (54 = 3 protocol × 3 seed × 6 điều kiện; không dòng nào có cả recall và FPR bằng 0) và "6.480" (54 × 120 điểm, chỉ đến từ 720 ảnh stego test của 120 cover, không độc lập). Kết luận chưa chứng minh vận hành tin cậy ở FPR ≤ 1% và không sẵn sàng triển khai |
| 4.6 | Đối chiếu với [13] Butora & Fridrich, [6, 9] SRM/SRNet và [18] MODE. Tách *Observed evidence* khỏi *Possible explanations*. Giữ các giới hạn: kích thước dữ liệu, resize, sức mạnh detector, khả năng tổng quát hóa |

### 5. Statistical Analysis

- Đã viết rõ đơn vị resampling, việc giữ cặp, cách gộp seed và hai nguồn biến thiên: SD theo seed là ngẫu nhiên khi huấn luyện; bootstrap là ngẫu nhiên do mẫu test. Ghi rõ CI phụ thuộc vào đúng cách chia tập hiện tại.
- `scripts/verify_stats.py` cài đặt đúng thủ tục mô tả trong bài. Nhóm chạy nó trên prediction scores gốc để:
  1. rà lại toàn bộ AUC và CI của RQ1–RQ3;
  2. lấy số FP theo từng seed;
  3. kiểm tra B và cách gộp seed.

  Nếu code cũ làm khác, nhóm chọn một trong hai cách: sửa câu chữ cho khớp code cũ, hoặc dùng số liệu mới của script.

### 6. Hình, bảng, định dạng

- Bảng được đánh số tự động bằng trường SEQ, liên tục 1–7. Mọi chỗ "Table n" / "Fig. n" trong bài là **cross-reference** (trường REF), không gõ tay.
- Cỡ chữ trong hình ở kích thước in là 6,6–7,6 pt (bản cũ khoảng 5 pt). Hình xuất 600 dpi; có thêm bản PDF vector trong `figures/`.
- Các phần trùng lặp đã gộp hoặc bỏ:
  - Fig. 4 cũ trùng với Table 8 cũ, nay gộp thành Table 7 có thêm số FP.
  - Fig. 2 cũ chỉ lặp lại các giá trị AUC đã có ở Table 4 và 5, nên đã bỏ để giữ giới hạn 12 trang.
  - Table 11 "Claim boundary" cũ chuyển thành chữ ở Mục 4.6.
- Footer nội bộ đã xóa. Khổ trang và lề giữ đúng template, không thu nhỏ font.

### 7. Conclusion

- Dài 187 từ, gồm 3 đoạn: (1) trả lời RQ1–RQ3; (2) giới hạn: 600 cover, resize, detector, ngưỡng FPR thấp, chưa có cross-source; (3) hướng phát triển: toàn bộ BOSSbase, detector mạnh hơn (SRNet), tham chiếu HILL matched, cross-source.
- Không có kết quả mới. Không khẳng định StegaGuard là detector mới hay đã sẵn sàng triển khai.

### 8. References và giới hạn 12 trang

- Từ 14 lên **21 tài liệu**. Bỏ Xu-Net và Ye-Net vì bài không còn dùng. Có 4 tài liệu năm 2023–2025.
- Tên tác giả, tiêu đề, venue, năm và DOI đã được đối chiếu với trang nhà xuất bản hoặc chỉ mục (chi tiết trong `docs/reference_verification.md`). SPAM chuyển sang bản tạp chí IEEE TIFS 2010.
- **Số trang:** PDF xuất bằng LibreOffice là 12 trang (font Liberation Serif, cùng kích thước ký tự với Times New Roman). Word có thể dàn trang hơi khác, nhưng trang cuối còn trống khoảng 18%. Nếu Word ra 13 trang, nên rút ngắn theo thứ tự: chữ trong các ô của Table 1 → đoạn 2 của Mục 4.6 → đoạn 2 của Mục 4.5.

### 9. Kiểm tra nhất quán

- Mọi số trong bảng và hình được sinh từ một nguồn duy nhất (`scripts/results_data.py`). Script này tự kiểm tra:
  - dấu và giá trị của 18 ΔAUC so với hiệu của các AUC đã làm tròn;
  - mean recall 0,062 và 0,080;
  - FPR trung bình 0,045 và 0,034.
- Các số trong Abstract, Mục 4 và Conclusion đã được dò lại khớp với các bảng.
- **Lưu ý:** một số con số viết trực tiếp trong câu chữ (ví dụ "0.632–0.717", "−0.115 to −0.183"). Nếu `verify_stats.py` cho số khác, phải sửa cả `results_data.py` lẫn các câu đó.

---

## C. Checklist: 28 chỗ tô vàng cần điền từ code

| # | Vị trí | Cần điền | Lấy ở đâu |
|---|---|---|---|
| 1 | 3.1 | Hàm resize và kiểu nội suy (ví dụ PIL `LANCZOS`, OpenCV `INTER_AREA`, Matlab `imresize` bicubic) | code tiền xử lý |
| 2 | 3.1 | Cách chia 360/120/120 (hoán vị ngẫu nhiên với seed nào; có phân tầng không) | code chia tập / manifest |
| 3 | 3.1 | Thư viện và phiên bản nhúng WOW/S-UNIWARD/HILL; nhúng bằng simulator hay STC | code tạo stego |
| 4, 5 | 3.2 | K bộ lọc residual và M thống kê tạo thành 76 đặc trưng (nếu 76 không phải K × M thì sửa câu) | code trích đặc trưng Residual-LR |
| 6, 7 | 3.2 | Bộ chuẩn hóa (StandardScaler?) và xác nhận chỉ fit trên training pairs của từng lần chạy | code Residual-LR |
| 8 | Table 2 | Bộ chuẩn hóa của Residual-LR (giống #6) | code Residual-LR |
| 9 | Table 2 | Có chuẩn hóa đặc trưng SRM trước ensemble không | code SRM+Ensemble |
| 10, 11 | Table 2 | Phiên bản scikit-learn, sealwatch | `pip freeze` |
| 12–16 | Table 2 | LogisticRegression: `solver`, `penalty`/`C`, `class_weight`, `max_iter`, `random_state` | code Residual-LR |
| 17 | Table 2 | Điểm số dùng cho ROC/ngưỡng: tỉ lệ phiếu (`predict_confidence`, chỉ có 51 mức khi L = 50) hay tổng phép chiếu FLD | code SRM+Ensemble. **Ảnh hưởng tới τ_low** vì điểm trùng nhau tại ngưỡng |
| 18 | 3.3 | Quy tắc rút biến thể cho mỗi training cover: ngẫu nhiên đều hay cân bằng cố định | code tạo protocol |
| 19 | 3.3 | Validation stego lấy từ cùng pool với training không | code tạo protocol |
| 20 | 3.5 | Số lần bootstrap B | code bootstrap |
| 21 | 3.5 | Xác nhận cách gộp 3 seed và CI phân vị như mô tả | code bootstrap, hoặc chạy lại `verify_stats.py` |
| 22–25 | 3.5 | Phiên bản Python, NumPy, scikit-learn, sealwatch | `python --version`, `pip freeze` |
| 26 | 3.5 | Thư viện nhúng và phiên bản (giống #3) | `pip freeze` |
| 27 | 3.5 | CPU, RAM, hệ điều hành | máy chạy thí nghiệm |
| 28 | 3.5 | Link repository chứa code, manifest, scores (hoặc ghi "available from the authors on request") | nhóm |

(Một số thông tin xuất hiện hai lần, ở cả chữ lẫn Table 2, nên phải điền giống nhau.)

**Các khẳng định không tô vàng nhưng vẫn nên xác nhận:**
- SRM+Ensemble dùng `FldEnsembleTrainer` của sealwatch (thư viện này luôn bootstrap theo cặp cover–stego), với L = 50 và d_sub = 500 cố định.
- Chạy `audit_manifest.py` trên manifest thật phải ra `PASS` và SHA-256 khớp `13c01ca9…2799e8c`.
- Số FP theo từng seed (`verify_stats.py` in ra) khớp tổng 15/15/19 và 18/11/8.

**Cách hoàn thiện trong Word:**
1. Điền các chỗ tô vàng rồi bỏ tô vàng.
2. Ctrl+A rồi F9 để cập nhật trường số bảng/hình.
3. Xuất PDF và kiểm tra đúng 12 trang.
4. Nếu dùng EndNote, import `docs/references.ris` rồi chèn lại trích dẫn bằng EndNote, style "Springer LNCS".

## D. Dựng lại từ mã nguồn

```bash
./build.sh   # sinh lại hình, bản thảo, supplementary và PDF (cần python3, matplotlib, scipy, lxml, Pillow, LibreOffice)
python3 scripts/verify_stats.py scores.csv --B 2000 --out report.json
python3 scripts/audit_manifest.py manifest.csv --check-files <thư mục ảnh>
```

Thông tin định dạng tệp `scores.csv` và `manifest.csv` có ở đầu từng script.
