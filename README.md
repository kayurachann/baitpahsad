# StegaGuard: bản thảo đã chỉnh sửa (LNCS, 12 trang)

Bản sửa của bài *StegaGuard: A Controlled Robustness Study of Feature-Based Image Steganalysis under
Algorithm and Payload Shift*, làm theo góp ý của thầy, với bố cục theo template Springer LNCS của PaperID 581.

| Thư mục | Nội dung |
|---|---|
| `manuscript/` | `StegaGuard_revised.docx` (bản để chỉnh tiếp trong Word) và `.pdf` (12 trang) |
| `supplementary/` | Bảng đầy đủ S1–S3, chuyển ra khỏi bài chính để giữ giới hạn 12 trang |
| `figures/` | Hình 1 (pipeline) và Hình 2 (payload shift), dạng PNG 600 dpi và PDF vector |
| `docs/BAO_CAO_SUA_BAI.md` | Đối chiếu từng góp ý với phần đã sửa, kèm **checklist 28 chỗ tô vàng cần điền từ code** |
| `docs/reference_verification.md` | Kiểm chứng 21 tài liệu tham khảo và các ô của Table 1 |
| `docs/references.ris` | Danh mục tài liệu để import vào EndNote |
| `scripts/` | Mã sinh hình, bản thảo và supplementary; `verify_stats.py` và `audit_manifest.py` để kiểm chứng lại số liệu từ dữ liệu gốc |
| `templates/lncs/` | Template LNCS lấy từ tệp 581, đã xóa toàn bộ nội dung, macro và dữ liệu EndNote |

Dựng lại toàn bộ: `./build.sh`. Cần python3 cùng matplotlib, numpy, scipy, Pillow, lxml; muốn xuất PDF thì cần thêm LibreOffice.

Số liệu kết quả nằm ở một nơi duy nhất là `scripts/results_data.py`. Sau khi chạy `verify_stats.py` trên prediction
scores gốc, sửa số ở file này rồi chạy lại `./build.sh`. Một số con số viết trực tiếp trong câu chữ của
`build_manuscript.py` và `related_work.py` cũng phải soát lại.
