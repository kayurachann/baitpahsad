# Trạng thái chạy lại thí nghiệm 600 ảnh

BLOCKED: dde.binghamton.edu not reachable from this environment (HTTP code 000)

- Ngày kiểm tra: 2026-10-15
- Lệnh: `curl -sS -o /dev/null -w "%{http_code}\n" -r 0-99 --max-time 30 https://dde.binghamton.edu/download/ImageDB/BOSSbase_1.01.zip`
- Kết quả: `curl: (56) CONNECT tunnel failed, response 403`, mã HTTP in ra `000`.
  Proxy egress của môi trường từ chối kết nối tới `dde.binghamton.edu:443`
  (`connect_rejected`; host không nằm trong danh sách được phép của phiên này).
- Vì không tải được BOSSbase 1.01, các bước 1–7 (môi trường, tải ảnh, chuẩn bị,
  trích đặc trưng, chạy, gộp, kiểm chứng) **chưa được chạy**. Không có con số nào
  được tính lại trong phiên này.

Để chạy được: thêm `dde.binghamton.edu` vào danh sách host được phép trong cấu hình
mạng của môi trường (hoặc chạy trên máy có Internet), rồi chạy lại quy trình.
