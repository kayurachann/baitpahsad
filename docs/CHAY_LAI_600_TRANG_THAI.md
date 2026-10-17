# Trạng thái chạy lại thí nghiệm 600 ảnh

**XONG (15/10/2026).** Kết quả, phiên bản phần mềm và lệnh tái lập nằm trong `data/stegaguard_600/ket_qua_chay_lai/`.

- Nguồn ảnh: máy chủ dde.binghamton.edu bị chặn từ môi trường này, nên nhóm gửi trực tiếp 600 ảnh PGM gốc (`covers.zip`, cắt 5 phần). Cả 600 ảnh khớp SHA-256 trong `source_provenance.json`.
- Chuẩn bị dữ liệu (`sg.prepare`, seed 20260918): manifest khớp bản của nhóm ở mọi cột. Chỉ SHA của file PNG khác do bản Pillow/zlib, còn điểm ảnh trùng.
- Trích đặc trưng: 4.200 ảnh × (76 đặc trưng residual + 34.671 đặc trưng SRM).
- 18 lần huấn luyện: 2 detector × 3 protocol × 3 seed.
- Đối chiếu:
  - Table 4/S1 khớp 216/216 giá trị;
  - FP từng seed khớp các tổng của Table 7;
  - 22 ΔAUC khớp bài;
  - CI tính lại với B = 10.000.
