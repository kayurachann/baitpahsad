# Mục 3.5.5 – Mô hình đồng thời bốn yếu tố (người D)

File: `ch3_3_5_5_mohinh.docx` (bản `.doc` đi kèm). Gồm đoạn mở đầu, phương pháp, Bảng 3.7, 5 đoạn nhận xét và kết luận, viết theo 6 ý "Viết vào Word" của file kế hoạch.

## Nguồn số liệu
Tất cả số lấy từ mục 3.5.5 của file "Chương 3 – Kế hoạch phân tích và phân công chi tiết":
- Bảng 3.7;
- OLS: R² 0,013, R² hiệu chỉnh 0,009, các β chuẩn hóa;
- VIF 1,34–1,61;
- tương quan giữa các yếu tố 0,33–0,45.

Script `scripts/kiem_tra_3_5_5.py` kiểm tự động: mọi số trong file Word đều có trong đoạn đó, hoặc tính ra từ đó. Ví dụ OR 1,191 → 19%, OR 0,621 → thấp hơn 38%.

**Cần D chạy lại.** File kế hoạch ghi rõ số logit thứ bậc là từ một bản tính tự viết, chưa chạy bằng `OrderedModel`. D chạy ô 3.5.5 trên Colab. Chữ số thập phân thứ ba lệch thì sửa theo số Colab; lệch nhiều thì báo nhóm trưởng.

## Hai chỗ viết khác mẫu (để không nói quá số liệu)
1. **Ý 6:** mẫu ghi "bốn yếu tố giải thích 1,3% (OLS) đến 1,4% (McFadden M3)". Nhưng M3 có thêm giới tính và năm học, nên 1,4% không phải của riêng bốn yếu tố. Bài ghi:
   - OLS: R² 0,013;
   - McFadden R² của M2: 0,004;
   - McFadden R² của M3: 0,014, tăng lên khi thêm giới tính và năm học.
2. **Ý 3:** mẫu ghi thiết bị và căng thẳng "có liên hệ nhỏ" rồi "mất hẳn". Ở M1, hai yếu tố này đã không có ý nghĩa (p = 0,300 và 0,197). Bài ghi: OR nhỉnh hơn 1, phù hợp với tương quan nhỏ ở 3.5.3, nhưng không có ý nghĩa; khi có đủ bốn yếu tố thì OR về sát 1.

## Việc D còn phải làm
- **Kiểm chéo:** sau khi chạy lại bằng SPSS/JASP (Analyze → Regression → Ordinal), thêm một câu cuối mục, ví dụ: "Kết quả chạy lại bằng SPSS cho cùng dấu và cùng mức ý nghĩa với Colab." Chỉ viết câu này sau khi đã chạy thật.
- **Một chỗ lệch nhỏ trong file kế hoạch:** β chuẩn hóa của thiết bị là 0,006 ở mục 3.5.5 nhưng 0,005 ở Bảng 3.8 (mục 3.5.6). D và E thống nhất theo số Colab.

## Cập nhật sau đợt rà soát nhiều chiều (24 lỗi đã xác nhận)
Đã sửa trong file Word:
- Câu năm học: chỉ nói "so với năm 1 không biến giả nào có ý nghĩa" và nêu rõ so sánh kém chính xác vì năm 1 chỉ có 22 người. Không kết luận rằng năm học không liên hệ với chất lượng giấc ngủ.
- Caffeine: bỏ chữ "đổi chiều". Viết là chuyển từ gần như không có liên hệ sang liên hệ nghịch nhẹ nhưng chưa có ý nghĩa.
- Kết luận: chỉ nói "liên hệ theo một chiều" của thiết bị và căng thẳng không còn, vì OR gần 1 không loại trừ dạng chữ U ở 3.5.4.
- Phần phương pháp: nêu giả định odds tỉ lệ; nói rõ OR ở M2 và M3 được hiểu khi các biến khác giữ nguyên; giải thích HC3 và VIF bằng thuật ngữ chuẩn (đa cộng tuyến, sai số chuẩn vững).
- Hoạt động thể chất: ghi riêng 1,19 lần (xét riêng) và 1,26 lần (sau khi tính các yếu tố khác), không gộp thành một khoảng 19–26%.
- Tên Bảng 3.7 và ghi chú bảng: biến Nam là biến 0/1, nên OR của nó so nam với nữ chứ không tính theo độ lệch chuẩn.

Không áp dụng một đề xuất: đổi dòng "Nguồn:" về tên file CSV. Lý do: cả chương đã thống nhất ghi nguồn là bộ dữ liệu.

## Việc thêm cho D khi chạy lại trên Colab
- **Kiểm định LR chung cho ba biến năm học:** tính 2 × (llf của M3 − llf của M3 khi bỏ ba biến năm học), so với phân phối χ² có 3 bậc tự do. Nếu p < 0,05 thì thêm một câu nêu kết quả này.
- **Test of Parallel Lines:** khi kiểm chéo bằng SPSS (Ordinal), lấy thêm kết quả này. Chỉ viết rằng giả định odds tỉ lệ thỏa hay không sau khi đã chạy thật.
