# StegaGuard: bản thảo đã chỉnh sửa (LNCS, 12 trang)

Bản sửa của bài *StegaGuard: A Controlled Robustness Study of Feature-Based Image Steganalysis under
Algorithm and Payload Shift*, làm theo góp ý của thầy, với bố cục theo template Springer LNCS của PaperID 581.

| Thư mục | Nội dung |
|---|---|
| `manuscript/` | `Paper_HoanChinh_2.docm` (bản nộp) và `.pdf` (12 trang), sửa từ `Paper_HoanChinh_1_goc.docm` của nhóm. `StegaGuard_revised.*` là bản nháp cũ dựng từ template, không nộp và không cập nhật theo lần chạy lại |
| `supplementary/` | Bảng đầy đủ S1–S3, chuyển ra khỏi bài chính để giữ giới hạn 12 trang |
| `figures/` | Hình 1 (pipeline) và Hình 2 (payload shift), dạng PNG 600 dpi và PDF vector |
| `docs/PHAN_HOI_THAY_LAN_CUOI.md` | Báo cáo sửa bài theo 5 góp ý cuối của thầy và kết quả chạy lại; `docs/TIN_NHAN_GUI_THAY.md` là tin nhắn gửi thầy (`docs/BAO_CAO_SUA_BAI.md` là báo cáo của vòng sửa trước) |
| `docs/reference_verification.md` | Kiểm chứng 21 tài liệu tham khảo và các ô của Table 1 |
| `docs/endnote_sua_references.ris` | 20 bản ghi References đã sửa, để cập nhật thư viện EndNote |
| `data/stegaguard_600/` | Manifest và file chuẩn bị dữ liệu 600 cover của nhóm; `ket_qua_chay_lai/` là điểm từng ảnh, ngưỡng, CI và môi trường của lần chạy lại |
| `scripts/` | Mã sinh hình, bản thảo và supplementary; `verify_stats.py` và `audit_manifest.py` để kiểm chứng lại số liệu từ dữ liệu gốc |
| `templates/lncs/` | Template LNCS lấy từ tệp 581, đã xóa toàn bộ nội dung, macro và dữ liệu EndNote |

Dựng lại bản nộp: `./build.sh` (hình, `Paper_HoanChinh_2.docm`, bộ kiểm `kiem_tra_hoanchinh.py`, supplementary). Cần python3 cùng matplotlib, numpy, scipy, Pillow, lxml; muốn xuất PDF thì cần thêm LibreOffice.

Số liệu kết quả nằm ở một nơi duy nhất là `scripts/results_data.py`. Mọi số trong đó đã được kiểm lại bằng
`verify_stats.py` trên điểm của lần chạy lại (`data/stegaguard_600/ket_qua_chay_lai/`). Cách chạy lại thí nghiệm từ
ảnh gốc: xem `data/stegaguard_600/ket_qua_chay_lai/README.md` và `moi_truong.json`.
