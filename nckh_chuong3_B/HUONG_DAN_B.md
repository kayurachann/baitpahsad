# Phần của người B – Chương 3

## B làm gì

Theo bảng phân công, B phụ trách **thang đo và kiểm tra dữ liệu**. B làm sau A (A chuẩn bị Drive và ô khởi tạo) và bàn giao cho C.

| Mục | Loại việc | Nội dung | Sản phẩm |
|---|---|---|---|
| 3.3 Xây dựng thang đo và bảng hỏi | Viết, khoảng 2 trang | Bảng hỏi gốc 15 câu, nhóm dùng 7 câu; Bảng 3.1; cách mã hóa thứ bậc; hạn chế đo lường (không tính Cronbach alpha); lý do bỏ Q3–Q5, Q7–Q10, Q15 | Phần Word |
| 3.5.1 Kiểm tra chất lượng dữ liệu | Chạy Colab rồi viết | Ô thiếu, dòng trùng, ba loại cờ, kiểm tra 791 dòng Original bằng mã băm MD5 | `bang_3_5_1.csv`, Bảng 3.3, 4 câu nhận xét và kết luận |
| 3.5.2 Mô tả dữ liệu | Chạy Colab rồi viết | Tần số 7 biến; biểu đồ 5 biến thứ bậc | `bang_3_5_2.csv`, `hinh_3_5_2.png`, Bảng 3.4, Hình 3.3, nhận xét và kết luận |
| Bàn giao cho C | Số liệu | Giới tính và năm học, dùng cho Bảng 3.2 ở mục 3.4 | Trang cuối của file Word |

## Các file trong thư mục này

| File | Dùng để |
|---|---|
| `ch3_3_3_3_5_1_3_5_2.docx` | Phần Word của B (3.3, 3.5.1, 3.5.2) và trang Bảng 3.2 chuyển cho C |
| `B_3_5_1_3_5_2.ipynb` | Notebook Colab đã sửa lỗi; mở trên Colab và chạy từ trên xuống |
| `bang/bang_3_5_2.csv` | Bảng tần số, đúng số của lần chạy thật trong notebook của nhóm |
| `hinh/hinh_3_5_2.png` | Hình 3.3, đen trắng |
| `scripts/` | Script tạo bảng, hình, notebook, file Word; script chạy thử notebook và đối chiếu số |

`bang_3_5_1.csv` không có sẵn ở đây. Notebook sẽ tạo ra tệp này khi chạy với tệp Original đúng.

## Lỗi trong notebook cũ ("code của pp nghiên cứu.ipynb") đã được sửa

1. `orig = pd.read_csv(D + "cleaned_sleep_dataset.csv")` đọc nhầm tệp chính. Hậu quả là dòng tệp Original trong `bang_3_5_1.csv` cũ ra 996 dòng, với các cờ 6/33/204 giống hệt tệp chính. Đã sửa thành `cleaned_sleep_dataset_original.csv`. Ô khởi tạo phải in ra `(996, 28) (791, 28)`.
2. Thiếu ô 2 của 3.5.1 (so khớp bằng mã băm MD5). Đã thêm đúng code trong file kế hoạch; ô này phải in ra `791 / 791` và `791`.
3. `y = "sleep_quality_ordina"` thiếu chữ `l`, và `"caffein_frequency_ordinal"` thiếu chữ `e`. Hai lỗi này làm các mục 3.5.3–3.5.7 của C, D, E báo `KeyError`. Đã sửa trong ô khởi tạo.
4. Thư mục `"ghi chu"` có dấu cách; đã đổi thành `"ghi_chu"`.
5. `plt.tight_layout` thiếu `()` nên lệnh không chạy; đã sửa.
6. Tên cột `gia_tri` và `ti_le_%` khác quy ước; đã đổi thành `muc` và `ty_le_pct` để Power BI/Tableau của D đọc đúng.
7. Thêm hai ô hỗ trợ phần viết:
   - ô đối chiếu cột trả lời gốc với cột mã, để kiểm Bảng 3.1;
   - ô in các tỉ lệ dùng trong nhận xét 3.5.2 và Bảng 3.2.

Notebook mới đã được chạy thử trọn vẹn trên một bộ dữ liệu giả cùng 28 cột (`scripts/thu_notebook.py`). Kết quả:
- ra đúng các đáp án đã biết;
- ô 2 trả về 791/791;
- khi cố ý sửa một ô của tệp Original thì ô 2 trả về 790/791.

## Số nào đã chắc, số nào phải chạy lại

**Đã chắc** (lấy từ lần chạy thật trong notebook của nhóm, trên tệp chính 996 dòng):
- Bảng 3.3, dòng tệp chính: 996 dòng, 0 ô thiếu, 0 dòng trùng, cờ 6 / 33 / 204;
- `present_in_original` = 791;
- toàn bộ Bảng 3.4, Hình 3.3, Bảng 3.2 và các tỉ lệ trong nhận xét 3.5.2.

Lưu ý: hoạt động thể chất mức 5 là **37,7%** (375/996), không phải 37,6% như số chạy thử trong file kế hoạch.

**Đang tô vàng trong Word.** Đây là số chạy thử của file kế hoạch; chạy lại `B_3_5_1_3_5_2.ipynb` để xác nhận:

| Chỗ tô vàng | Ô notebook in ra số đó |
|---|---|
| Dòng tệp Original của Bảng 3.3 (791; 0; 0; 2; 33; 183) | 3.5.1 – Ô 1 (bảng `bang`) |
| "216 dòng" có ít nhất một cờ | 3.5.1 – Ô 1, dòng "Số dòng V2 có ít nhất một cờ" |
| "205" dòng chênh lệch giữa hai tệp | 3.5.1 – Ô 1, dòng "Số dòng V2 nhiều hơn Original" |
| "cả 791 trên 791 dòng… tìm thấy" | 3.5.1 – Ô 2 |
| "Cả hai tệp" không có ô thiếu, dòng trùng | 3.5.1 – Ô 1 (cột `o_thieu`, `dong_trung` của dòng Original) |
| Câu "mỗi lựa chọn chỉ ứng với một mã" ở 3.3 | Ô 3.3 (bảng chéo); cần in ra `True` cho cả 5 biến |

Số in ra giống thì bỏ tô vàng. Số khác thì sửa trong Word theo số in ra, kể cả câu kết luận. Ô 3.3 cũng in ra các lựa chọn trả lời gốc; nhớ đối chiếu với Bảng 3.1, nhất là cách ghi "1–2 lần/tuần" của Q12 và Q13.

## Cách dùng
1. Mở `B_3_5_1_3_5_2.ipynb` trên Colab (File → Upload notebook). Thư mục `NCKH_giac_ngu` phải có `cleaned_sleep_dataset.csv` và `cleaned_sleep_dataset_original.csv`. Bấm Runtime → Run all.
2. Đối chiếu số in ra với các chỗ tô vàng ở bảng trên, rồi bỏ tô vàng.
3. Xóa đoạn "Ghi chú cho nhóm" ở đầu file Word.
4. Gửi A file Word (phần 3.3, 3.5.1, 3.5.2) cùng tên file `bang_3_5_1.csv`, `bang_3_5_2.csv`, `hinh_3_5_2.png` trên Drive.
5. Gửi C trang cuối (Bảng 3.2).

## Lưu ý thêm
- **Nguồn bộ dữ liệu:** file kế hoạch ghi "Abdullah & Rahman, v3". Khi tìm trên Mendeley Data thấy một bộ có cấu trúc 15 câu giống hệt, là "Student Insomnia and Educational Outcomes Dataset" (người đóng góp Akik Abdullah, DOI 10.17632/5mvrx4v62z). Môi trường làm việc này không mở được trang Mendeley, nên C và E cần tự mở trang để kiểm tác giả, năm và số dòng trước khi ghi trích dẫn.
- **Hình 3.3** để đen trắng cho đồng bộ khi in. Muốn dùng màu xanh như file kế hoạch thì trong ô hình đổi `color="0.55"` thành `color="#4C78A8"`.
- **Quy ước viết:** cả file Word chỉ dùng "liên hệ", không dùng "ảnh hưởng", "tác động", "gây ra". Đã kiểm tự động bằng `scripts/kiem_tra_word.py`.
