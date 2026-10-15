Dạ em chào thầy,

Nhóm em đã sửa bài StegaGuard theo 5 góp ý của thầy và thêm phần Acknowledgement. Em gửi thầy bản mới (12 trang, kể cả References). Nhóm em xin báo lại từng mục ạ:

1. Mục 3.2: nhóm đã ghi rõ cách tạo 76 đặc trưng residual, StandardScaler chỉ fit trên tập train, và các tham số của Logistic Regression (L2, C = 1.0, lbfgs, không class weight, max_iter = 2000). Các thông số này khớp với code. Riêng cấu hình SRM+Ensemble (34.671 đặc trưng, L = 50, d_sub = 500), nhóm vẫn giữ như bản trước vì chưa tìm lại được code và log của phần SRM để đối chiếu.

2. Mục 3.5: nhóm đã ghi CI 95% lấy theo phân vị, bootstrap theo test cover, và nói rõ CI chỉ phản ánh biến thiên trên 120 test cover cố định. Số vòng bootstrap của CI ΔAUC thì nhóm chưa ghi vào bài, vì chưa tìm lại được script tính ΔAUC của bản 600 ảnh. Code pilot dùng 2.000 vòng, còn code đánh giá dùng 1.000 vòng cho AUC từng điều kiện, nên nhóm không muốn ghi khi chưa chắc.

3. Mục 4.5: nhóm đã bỏ câu "never completely silent", viết lại câu về 54 rows và 6.480 lượt chấm (không phải mẫu độc lập), và sửa mean recall của SRM+Ensemble P2 từ 0.070 thành 0.069 (tính từ số đếm 150/2.160). Kết luận về FPR ≤ 1% giữ nguyên. Số false positive theo từng seed nhóm chưa đối chiếu được với file dự đoán, trừ Residual-LR P1: code cho thấy 3 lần chạy giống nhau, nên là 5/120 mỗi lần.

4. References: nhóm đã trình bày theo LNCS, giữ nguyên thứ tự và sửa lại metadata theo nguồn của nhà xuất bản. Riêng [17] (EUSIPCO 2025) chưa có trang và DOI trên IEEE Xplore, và [20] chưa ghi được phiên bản sealwatch đã dùng.

5. Rà soát cuối: hình 600 dpi, Table 1–7 đánh số liên tục, Supplementary S1–S3 đầy đủ, bài 12 trang. Nhóm cũng đã kiểm lại bộ dữ liệu 600 ảnh: việc chọn ảnh, chia tập, 3.600 seed nhúng và mã hash của manifest đều tái lập đúng với code.

Nhóm em đang tìm lại kết quả chạy phần SRM để bổ sung các điểm còn thiếu nếu thầy cần ạ. Em cảm ơn thầy.
