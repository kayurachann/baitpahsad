# Báo cáo chỉnh sửa bản thảo StegaGuard theo góp ý của thầy

Tệp kết quả:

| Tệp | Nội dung |
|---|---|
| `manuscript/StegaGuard_revised.docm` | **Bản nộp**: bản thảo đã sửa, dựng trên template Springer LNCS của PaperID 581 (A4, lề 4,4/5,2 cm, Times 10pt). Cùng cấu trúc với `.docm` gốc của nhóm: content type macro-enabled, không chứa macro |
| `manuscript/StegaGuard_revised.docx` | Cùng nội dung, định dạng .docx |
| `manuscript/StegaGuard_revised.pdf` | Bản PDF xuất bằng LibreOffice: **12 trang**, kể cả References; trang cuối đầy khoảng 82% |
| `supplementary/StegaGuard_supplementary.docx/.pdf` | Table S1 (đủ 36 điều kiện: AUC±SD, F1, BER, Recall, FPR), Table S2 (18 so sánh payload kèm CI), Table S3 (số false positive) |
| `docs/references.ris` | 21 tài liệu tham khảo dạng RIS để import vào EndNote |
| `docs/reference_verification.md` | Kết quả kiểm chứng từng tài liệu tham khảo (nguồn, DOI, mục còn phải kiểm) |
| `scripts/verify_stats.py` | Tính lại AUC, ngưỡng, số FP và bootstrap ghép cặp từ prediction scores gốc |
| `scripts/audit_manifest.py` | Kiểm tra manifest: không có source cover nằm ở hai tập, đủ 6 biến thể mỗi cover, đúng 360/120/120 |

> **Quan trọng:** bản thảo **không còn chỗ trống hay tô vàng nào**. Một số thông tin thầy yêu cầu chỉ có trong code hoặc log thí nghiệm (danh sách 76 đặc trưng, tham số Logistic Regression, số lần bootstrap...). Thầy yêu cầu *không bổ sung tham số theo suy đoán*, nên các câu liên quan được viết lại để chỉ khẳng định những gì bản thảo gốc đã nêu. Các chi tiết này **vẫn chưa có trong bài**; danh sách ở Mục C. Nếu bổ sung được từ code, bài sẽ đáp ứng đầy đủ Mục 3 của thầy.

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
| 76 features, scaling, tham số LR, cấu hình SRM+Ensemble | Table 2 (cấu hình detector) và Mục 3.2 ghi những gì đã biết: 76 thống kê residual + LR (scikit-learn); SRM 106 submodel, 34.671 chiều + FLD ensemble L = 50, d_sub = 500; phần phụ thuộc seed. Danh sách đặc trưng và tham số LR **chưa có** vì cần code (Mục C) |
| Bảng tổng hợp P1–P3, quy tắc lấy mẫu, P2 khác P3 ở đâu | Table 3 có cột training pool, thành phần kỳ vọng và vai trò với RQ. Mục 3.3 nêu cách rút một biến thể cho mỗi cover theo seed, và nêu P2/P3 chỉ khác nhau ở biến thể 0,1 bpp |
| Metrics, ngưỡng chọn trên validation | Mục 3.4: τ_BER (cho F1, BER) và τ_low ở Eq. (1); ghi rõ "never from test labels" |
| Bootstrap: số lần, đơn vị resampling, giữ cặp, gộp 3 seed | Mục 3.5: đơn vị là source test cover; cùng một lần rút cho cả hai điều kiện và cả ba seed; khoảng CI theo phân vị của ΔAUC trung bình qua seed. **B** và cách gộp seed cần xác nhận với code |
| Môi trường thực nghiệm | Mục 3.5 nêu dữ liệu đã lưu (điểm từng ảnh, manifest, seed nhúng, hash). Phiên bản thư viện và phần cứng **chưa có** vì cần code/log (Mục C) |
| Figure 1 thể hiện đủ luồng, hai detector song song | Vẽ lại: BOSSbase → Source-cover split → Stego generation → Feature extraction và Detector training (**hai làn song song** Residual-LR / SRM+Ensemble) → P1/P2/P3 evaluation → 4 nhánh (RQ1, RQ2, RQ3, Operating point) → Robustness and security metrics |
| Bớt bảng audit/checklist trùng | Bỏ Table "Metric roles", Table "Reproducibility checklist" và Table "Detector implementation audit" cũ. Thông tin hữu ích được đưa vào chữ và Table 2 |

### 4. Results and Discussion

| Mục | Đã làm |
|---|---|
| 4.1 | Table 4 chỉ còn ma trận AUC 6×6 (bảng cũ 36 dòng chuyển sang Supplementary S1). Nêu Residual-LR gần ngẫu nhiên nên **SRM+Ensemble là bằng chứng chính** |
| 4.2 (RQ1) | Báo cáo ΔAUC kèm CI. Kiểm tra dấu: ΔAUC = điều kiện bị shift trừ điều kiện tham chiếu, thống nhất cho RQ1–RQ3. Nêu rằng WOW và HILL khác nhau cả về **độ khó phát hiện**, không chỉ về độ lệch thuật toán, nên cần một tham chiếu HILL matched mà nghiên cứu chưa chạy. Không khẳng định robustness. Có đoạn "Answer to RQ1" |
| 4.3 (RQ2) | Dùng đúng câu "No reliable improvement was observed under the evaluated mixed-training protocol." Nêu P3 khác P2 ở chỗ thêm 0,1 bpp, nên ít cặp huấn luyện mang tín hiệu 0,4 bpp hơn. CI chứa 0 thì "inconclusive", không phải "equivalence". Giới hạn phạm vi kết luận |
| 4.4 (RQ3) | Hình 2 (trước là Fig. 3) chuyển thành forest plot của ΔAUC kèm CI cho 18 so sánh, gọn hơn và không còn khoảng trắng. Table 6 tổng hợp theo detector × protocol; bảng 18 dòng chuyển sang S2. Tách *xu hướng nhất quán* khỏi *ý nghĩa thống kê*: CI chưa hiệu chỉnh đa so sánh, các so sánh dùng chung cover và mô hình, và một CI của Residual-LR chạm −0,001. Có đoạn "Answer to RQ3" |
| 4.5 (Low-FPR) | Phân biệt ngưỡng chọn trên validation với FPR quan sát trên test. **Số FP thực tế** suy ra duy nhất từ FPR đã báo cáo: Residual-LR 15/15/19 trên 360, SRM 18/11/8 trên 360, tổng 49 và 37 trên 1.080 (ghi rõ là suy ra từ FPR trung bình). Với Residual-LR P1 (SD theo seed = 0), nếu 3 lần chạy giống nhau thì là 5/120 mỗi lần; khoảng Clopper–Pearson [1,4%; 9,5%] không chứa 1%. Bổ sung lý do: ngưỡng ít chặt nhất được phép nằm ngay trên điểm validation cao thứ hai, nên một cover test bất kỳ vượt ngưỡng với xác suất 2/121 ≈ 1,7% > 1%. Giải thích "0/54" (54 = 3 protocol × 3 seed × 6 điều kiện; không dòng nào có cả recall và FPR bằng 0) và "6.480" (54 × 120 điểm, chỉ đến từ 720 ảnh stego test của 120 cover, không độc lập). Kết luận chưa chứng minh vận hành tin cậy ở FPR ≤ 1% và không sẵn sàng triển khai |
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
- Hình in đen trắng (không màu): hai detector phân biệt bằng kiểu nét và hình dạng marker. Biểu đồ không có viền trên và viền phải; vạch ΔAUC = 0 vẽ nét đứt. Cỡ chữ trong hình ở kích thước in là 6,6–7,6 pt (bản cũ khoảng 5 pt). Hình xuất 600 dpi; có thêm bản PDF vector trong `figures/`.
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

## C. Chi tiết thầy yêu cầu nhưng cần code mới bổ sung được

Bài **không bịa** các giá trị dưới đây. Câu chữ hiện tại chỉ nêu những gì bản thảo gốc đã có. Khi có code, thêm vào đúng vị trí (mỗi mục thường chỉ cần một mệnh đề hoặc thêm một dòng trong Table 2), rồi xuất lại PDF và kiểm tra vẫn đủ 12 trang.

| # | Nên thêm vào | Thông tin cần | Lấy ở đâu |
|---|---|---|---|
| 1 | 3.1 | Hàm resize và kiểu nội suy | code tiền xử lý |
| 2 | 3.1 | Cách chia 360/120/120 (hoán vị ngẫu nhiên với seed nào; có phân tầng không) | code chia tập / manifest |
| 3 | 3.1 | Thư viện và phiên bản nhúng WOW/S-UNIWARD/HILL; nhúng bằng simulator hay STC | code tạo stego |
| 4 | 3.2 + Table 2 | Các bộ lọc residual và thống kê tạo thành 76 đặc trưng | code trích đặc trưng Residual-LR |
| 5 | 3.2 + Table 2 | Bộ chuẩn hóa đặc trưng và xác nhận chỉ fit trên training pairs | code Residual-LR |
| 6 | Table 2 | LogisticRegression: `solver`, `penalty`/`C`, `class_weight`, `max_iter`, `random_state` | code Residual-LR |
| 7 | Table 2 | Điểm số của ensemble: tỉ lệ phiếu (`predict_confidence`, chỉ 51 mức khi L = 50) hay tổng phép chiếu FLD; có bootstrap không | code SRM+Ensemble. Ảnh hưởng tới τ_low vì điểm trùng nhau tại ngưỡng |
| 8 | 3.3 | Quy tắc rút biến thể (ngẫu nhiên đều hay cân bằng) và số cặp thực tế theo thuật toán/payload ở P2, P3 | code tạo protocol |
| 9 | 3.4 | Quy tắc chọn τ_low chính xác (bằng điểm nào; xử lý điểm trùng) và τ_BER (cực tiểu BER hay điểm P_FA = P_MD) | code ngưỡng |
| 10 | 3.5 | Số lần bootstrap B; cách gộp 3 seed (cùng một lần rút cho cả 3 seed rồi lấy trung bình ΔAUC?); kiểu khoảng (phân vị?) | code bootstrap, hoặc chạy lại `verify_stats.py` |
| 11 | 3.5 + Ref. 21 | Phiên bản Python, NumPy, scikit-learn, sealwatch; CPU/RAM/OS | `pip freeze`, máy chạy |
| 12 | 4.5 / S3 | Số false positive theo từng seed | file điểm số (`verify_stats.py` in ra) |

**Nên chạy lại trên dữ liệu gốc:**
- `scripts/verify_stats.py`: rà lại mọi AUC và CI của RQ1–RQ3 (thầy yêu cầu ở Mục 5).
- `scripts/audit_manifest.py`: kết quả phải là PASS, và SHA-256 khớp `13c01ca9…2799e8c`.
- Script hiện chọn τ_BER theo cực tiểu BER; nếu code gốc dùng điểm cân bằng P_FA = P_MD thì sửa hàm `tau_ber`.

## E. Đợt kiểm tra độc lập trước khi xuất bản .docm

Sáu agent soát bản thảo theo sáu góc nhìn:
1. căn cứ của Abstract, Mục 1–2 và Table 1;
2. căn cứ của Mục 3;
3. cách diễn giải ở Mục 4–5;
4. tính nhất quán số liệu;
5. đáp ứng góp ý của thầy;
6. ngôn ngữ và định dạng.

Có 70 lỗi được nêu. Từng lỗi được đối chiếu với bản thảo gốc, `results_data.py` và toàn văn các bài tham khảo đã tải về. Những sửa đổi chính:

- **Eq. (1):** bỏ quy tắc "min" vì bản gốc không nêu, và cực tiểu thực ra không tồn tại. Nay chỉ còn ràng buộc FPR_V(τ_low) ≤ 0,01.
- **τ_BER:** ghi "balanced-error point" đúng như bản gốc.
- **Các câu khẳng định quá mức đã sửa:**
  - "not a pure effect" → "need not be";
  - "did not help" → "no reliable improvement";
  - "both far weaker" → chỉ SRM+Ensemble giảm mạnh, Residual-LR giảm nhẹ;
  - "no matched signal" → "too weak to serve as a reference";
  - "mirrors [13]" → "agrees in direction with [13]", kèm khác biệt về thiết kế;
  - câu về FPR test trích đúng nội dung của [18].
- **Câu suy diễn không có căn cứ đã sửa:**
  - "audit kiểm tra đúng 6 biến thể" → chỉ ghi điều bản gốc nêu;
  - "HILL never enters validation" → "never used for model fitting or threshold selection";
  - "real-valued score" → "score";
  - "Residual-LR is deterministic" → "nếu 3 lần chạy giống nhau, như SD = 0 gợi ý".
- **Abstract:** ghi rõ số liệu nào thuộc detector nào.
- **Table 1:**
  - ô Low-FPR của [13] → "Not reported" ([13] báo cáo P_MD ở mức false alarm ngang nhau, không phải một FPR cố định; đã xác minh từ toàn văn);
  - ALASKA: cột Shift ghi thêm "algorithm";
  - CSM: ô detector chỉ ghi điều có trong tóm tắt;
  - chú thích bảng định nghĩa P_E, P_MD, CSM.
  - Ô "Pretrained SRNet" và "FPR 10⁻³–10⁻¹" của MODE được **giữ nguyên** vì toàn văn xác nhận.
- **Định dạng:**
  - tiêu đề cột "Protocol" bị cắt chữ → "P";
  - Hình 1 dùng τ_low, d_sub dạng chỉ số dưới, ghi "18 comparisons";
  - viết đầy đủ FLD, CNN, bpp ở lần dùng đầu;
  - Supplementary bỏ các câu dạng ghi chú nội bộ.
- **Số liệu:** recall trung bình được làm tròn bằng số thập phân chính xác (SRM P2 0,069 → 0,070). Các chú thích ghi rõ ΔAUC tính từ AUC chưa làm tròn.

Đã bác 4 đề xuất: ô MODE (đã đúng), đổi dấu phân cách Keywords (giữ đúng kiểu 581), trục x riêng cho Hình 2 (giữ chung trục để so sánh được hai detector), và xóa dòng SRM/CSM khỏi Table 1.

## D. Hoàn thiện trong Word và dựng lại từ mã nguồn

1. Mở `manuscript/StegaGuard_revised.docm`, nhấn Ctrl+A rồi F9 để cập nhật trường số bảng/hình.
2. Xuất PDF và kiểm tra đúng 12 trang. Bản xuất bằng LibreOffice: 12 trang, trang cuối đầy khoảng 82%.
3. Nếu dùng EndNote: import `docs/references.ris`, chèn lại trích dẫn bằng EndNote với style "Springer LNCS".


```bash
./build.sh   # sinh lại hình, bản thảo, supplementary và PDF (cần python3, matplotlib, scipy, lxml, Pillow, LibreOffice)
python3 scripts/verify_stats.py scores.csv --B 2000 --out report.json
python3 scripts/audit_manifest.py manifest.csv --check-files <thư mục ảnh>
```

Thông tin định dạng tệp `scores.csv` và `manifest.csv` có ở đầu từng script.
