Dạ em chào thầy,

Nhóm em đã sửa bài StegaGuard theo 5 góp ý của thầy và thêm phần Acknowledgement. Em gửi thầy bản mới (12 trang, kể cả References) và file Supplementary. Để trả lời đúng các mục về cấu hình và thống kê, nhóm đã chạy lại toàn bộ thí nghiệm 600 ảnh từ ảnh gốc BOSSbase. Kết quả chạy lại khớp toàn bộ Table 4 và bảng S1 (216/216 giá trị). Nhóm em xin báo lại từng mục ạ:

1. Mục 3.2: nhóm đã ghi rõ:
   - cách tạo 76 đặc trưng residual;
   - StandardScaler chỉ fit trên tập train;
   - tham số của Logistic Regression: L2, C = 1.0, lbfgs, không class weight, max_iter = 2000.

   Cấu hình SRM+Ensemble (34.671 đặc trưng sealwatch, FLD ensemble L = 50, d_sub = 500) đã được chạy lại xác nhận. Nhóm thêm một câu nói điểm số của ensemble là trung bình phiếu ±1 của 50 bộ FLD.

2. Mục 3.5: nhóm đã ghi đầy đủ cách tính CI 95% của ΔAUC:
   - bootstrap theo test cover, mỗi lần rút dùng chung cho cả 3 seed;
   - ΔAUC của mỗi lần rút là trung bình 3 seed;
   - B = 10.000, bộ sinh NumPy seed 2026, lấy phân vị 2,5 và 97,5.

   Script tính CI cũ không còn nên không biết lúc trước dùng bao nhiêu vòng. Vì vậy nhóm tính lại mọi CI bằng đúng thủ tục ghi trong bài. Các cận chỉ đổi tối đa 0,003 và các kết luận giữ nguyên. Riêng khoảng của Residual-LR P3 WOW nay là [−0.046, 0.000], chạm 0, nên nhóm sửa câu ở mục 4.4 thành 17/18 khoảng nằm dưới 0. Nhóm cũng ghi rõ CI chỉ phản ánh việc lấy mẫu lại 120 test cover.

3. Mục 4.5:
   - nhóm đã bỏ câu "never completely silent" và viết lại câu về 54 rows và 6.480 lượt chấm (không phải mẫu độc lập);
   - số false positive ở Table 7 đã được đếm lại từ điểm từng ảnh của từng seed, khớp cả 6 dòng; số theo từng seed nằm ở bảng S3;
   - mean recall của SRM+Ensemble P2 sửa từ 0.070 thành 0.069 (tính từ số đếm 150/2.160).

   Kết luận về FPR ≤ 1% giữ nguyên.

4. References: nhóm đã trình bày theo LNCS, giữ nguyên thứ tự và sửa metadata theo nguồn của nhà xuất bản. Mục [20] nay ghi phiên bản sealwatch 2025.9 đã dùng. Riêng [17] (EUSIPCO 2025) chưa có trang cuối và DOI trên IEEE Xplore.

5. Rà soát cuối:
   - hình 600 dpi; Fig. 2 được vẽ lại theo CI mới;
   - Table 1–7 đánh số liên tục; Supplementary S1–S3 đầy đủ, có ghi phiên bản phần mềm;
   - bài 12 trang, không đổi font hay lề.

   Điểm số từng ảnh và script chạy lại được lưu kèm để tính lại được mọi bảng.

Em cảm ơn thầy.
