"""Tạo ch3_3_5_5_mohinh.docx: mục 3.5.5 Mô hình đồng thời bốn yếu tố (người D).

Số liệu lấy từ file "Chương 3 – Kế hoạch phân tích và phân công chi tiết", mục 3.5.5 (Bảng 3.7, OLS, VIF,
tương quan giữa các yếu tố). Theo ghi chú của file kế hoạch, số logit thứ bậc là từ một bản tính tự viết
cùng mô hình; D chạy lại ô 3.5.5 trên Colab và sửa nếu chữ số thập phân thứ ba lệch.
Định dạng dùng lại từ nckh_chuong3_B/scripts/tao_word.py.
Cách chạy: python3 tao_word_3_5_5.py
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC.parent / "nckh_chuong3_B" / "scripts"))
import tao_word as tw  # noqa: E402

# ---------------------------------------------------------------- số liệu (file kế hoạch, mục 3.5.5)
# OR theo 1 độ lệch chuẩn và p: (M1, M2, M3)
OR = {
    "Sử dụng thiết bị trước giờ ngủ": [(1.058, "0,300"), (1.001, "0,985"), (0.991, "0,895")],
    "Tiêu thụ caffeine": [(1.003, "0,953"), (0.884, "0,078"), (0.879, "0,069")],
    "Hoạt động thể chất": [(1.191, "0,002"), (1.261, "0,001"), (1.262, "0,001")],
    "Căng thẳng học tập": [(1.074, "0,197"), (1.015, "0,814"), (1.005, "0,933")],
}
NAM = (0.621, "0,0002")
MCFADDEN = {"M2": "0,004", "M3": "0,014"}
TB, CF, HD, CT = OR


def so(x, le=3):
    return f"{x:.{le}f}".replace(".", ",")


def o(gt):
    x, p = gt
    return f"{so(x)} ({p})"


tw.doc = tw.moi_doc()
tw.tieu_de("3.5.5. Mô hình đồng thời bốn yếu tố", 3)
tw.doan("Mục 3.5.3 xem xét từng yếu tố riêng lẻ với chất lượng giấc ngủ. Tuy nhiên, bốn yếu tố có tương quan với "
        "nhau ở mức vừa phải: hệ số tương quan hạng Spearman giữa từng cặp nằm trong khoảng từ 0,33 (tiêu thụ caffeine – "
        "căng thẳng học tập) đến 0,45 (sử dụng thiết bị trước giờ ngủ – tiêu thụ caffeine). Vì vậy, liên hệ thấy được khi xét riêng một yếu tố có thể một phần là phần chung với "
        "các yếu tố khác. Mục này đưa cả bốn yếu tố vào cùng một mô hình để xem yếu tố nào còn liên hệ với chất lượng "
        "giấc ngủ sau khi đã tính đến ba yếu tố còn lại.")
tw.doan("Vì chất lượng giấc ngủ là thang thứ bậc năm mức, nhóm dùng hồi quy logit thứ bậc. Ba mô hình được ước "
        "lượng: M1 gồm bốn mô hình riêng, mỗi mô hình chỉ có một yếu tố, dùng để đối chiếu; M2 đưa cả bốn yếu tố vào "
        "cùng lúc và là mô hình chính; M3 thêm giới tính và năm học vào M2, với năm 1 làm nhóm mốc. Các yếu tố được "
        "chuẩn hóa (trừ trung bình, chia độ lệch chuẩn), nên tỉ số odds (OR) cho biết odds rơi vào mức chất lượng "
        "giấc ngủ cao hơn thay đổi bao nhiêu lần khi yếu tố tăng một độ lệch chuẩn: OR lớn hơn 1 là liên hệ thuận, "
        "nhỏ hơn 1 là liên hệ nghịch, bằng 1 là không có liên hệ. Ngoài ra, nhóm chạy thêm hồi quy tuyến tính (OLS, "
        "sai số chuẩn HC3) với hệ số chuẩn hóa để dùng ở mục 3.5.6, và tính hệ số phóng đại phương sai (VIF) để kiểm "
        "tra mức chồng lấn giữa các yếu tố. Các mô hình được chạy bằng thư viện statsmodels trên Google Colab. Kết "
        "quả hồi quy logit thứ bậc được trình bày ở Bảng 3.7.")

tw.chu_thich("Bảng 3.7. Kết quả hồi quy logit thứ bậc: OR theo một độ lệch chuẩn (p trong ngoặc)")
dong = [["Yếu tố", "M1 (từng yếu tố riêng)", "M2 (bốn yếu tố)", "M3 (thêm giới tính, năm học)"]]
for ten, gt in OR.items():
    dong.append([ten] + [o(x) for x in gt])
dong.append(["Nam (so với nữ)", "–", "–", o(NAM)])
dong.append(["McFadden R²", "–", MCFADDEN["M2"], MCFADDEN["M3"]])
tw.bang(dong, [4.6, 3.8, 3.6, 4.0], can_giua_tu=1)
tw.ghi_nguon("Ghi chú: Các yếu tố đã chuẩn hóa nên OR tính cho mỗi một độ lệch chuẩn; số trong ngoặc là giá trị p. "
             "M1 gồm bốn mô hình riêng nên không có một McFadden R² chung. M3 có thêm ba biến năm học (mốc là năm 1, "
             "22 người); không biến nào có ý nghĩa thống kê (p từ 0,12 đến 0,74).", keep=True)
tw.ghi_nguon(tw.NGUON)

hd = OR[HD]
tw.doan(f"Hoạt động thể chất là yếu tố duy nhất giữ liên hệ ổn định ở cả ba mô hình. OR là {so(hd[0][0])} khi xét "
        f"riêng, tăng lên {so(hd[1][0])} khi có đủ bốn yếu tố và {so(hd[2][0])} khi thêm giới tính, năm học; p ở cả "
        "ba mô hình đều không quá 0,002. Nói cách khác, khi hoạt động thể chất tăng một độ lệch chuẩn, odds rơi vào "
        f"mức chất lượng giấc ngủ cao hơn lớn hơn khoảng {round((hd[0][0] - 1) * 100)}% đến "
        f"{round((hd[2][0] - 1) * 100)}%, kể cả sau khi đã tính đến các yếu tố còn lại.")
tb, ct = OR[TB], OR[CT]
tw.doan(f"Sử dụng thiết bị trước giờ ngủ và căng thẳng học tập có OR nhỉnh hơn 1 khi xét riêng ({so(tb[0][0])} và "
        f"{so(ct[0][0])}), phù hợp với hệ số tương quan nhỏ ở mục 3.5.3, nhưng không có ý nghĩa thống kê (p = "
        f"{tb[0][1]} và {ct[0][1]}). Khi đưa cả bốn yếu tố vào, OR của hai yếu tố này về sát 1 ({so(tb[1][0])} và "
        f"{so(ct[1][0])}; p lần lượt là {tb[1][1]} và {ct[1][1]}). Như vậy, phần liên hệ nhỏ thấy được khi xét riêng "
        "chủ yếu là phần chung với các yếu tố khác, không phải phần riêng của hai yếu tố này.")
cf = OR[CF]
tw.doan(f"Tiêu thụ caffeine đổi chiều liên hệ. Khi xét riêng, OR gần như bằng 1 ({so(cf[0][0])}; p = {cf[0][1]}). Khi "
        "tính đến các yếu tố còn lại, trong đó có hoạt động thể chất (tương quan 0,42 với tiêu thụ caffeine), OR giảm còn "
        f"{so(cf[1][0])} (p = {cf[1][1]}) ở M2 và {so(cf[2][0])} (p = {cf[2][1]}) ở M3, tức là liên hệ nghịch nhẹ. "
        "Vì p lớn hơn 0,05, kết quả này chỉ là gợi ý, chưa đủ để khẳng định.")
tw.doan(f"Ở M3, nam có odds rơi vào mức chất lượng giấc ngủ cao hơn thấp hơn nữ (OR = {so(NAM[0])}; p = {NAM[1]}), "
        f"tức thấp hơn khoảng {round((1 - NAM[0]) * 100)}%. Các mức năm học không có ý nghĩa thống kê. Khi thêm giới "
        "tính và năm học, kết quả của bốn yếu tố gần như không đổi.")
tw.doan("Hồi quy tuyến tính cho kết quả cùng chiều: hệ số chuẩn hóa β của hoạt động thể chất là 0,130 (p = 0,0008), "
        "của tiêu thụ caffeine là −0,073 (p = 0,056), còn của sử dụng thiết bị trước giờ ngủ và căng thẳng học tập "
        "đều chỉ khoảng 0,006. VIF của bốn yếu tố "
        "từ 1,34 đến 1,61, đều dưới 2, nên chưa có vấn đề chồng lấn đáng kể giữa các yếu tố. Tuy vậy, mức giải thích "
        "của mô hình rất thấp: theo OLS, bốn yếu tố chỉ giải thích khoảng 1,3% sự khác biệt về chất lượng giấc ngủ "
        f"(R² = 0,013; R² hiệu chỉnh = 0,009); McFadden R² của M2 là {MCFADDEN['M2']} và tăng lên "
        f"{MCFADDEN['M3']} khi thêm giới tính, năm học ở M3. Phần lớn sự khác biệt về chất lượng giấc ngủ chưa được "
        "bốn yếu tố này giải thích.")
tw.doan(f"Kết luận: khi xem đồng thời, chỉ hoạt động thể chất còn liên hệ rõ với chất lượng giấc ngủ (OR = "
        f"{so(hd[1][0], 2)}; p = {hd[1][1]}); liên hệ của sử dụng thiết bị trước giờ ngủ và căng thẳng học tập không "
        "còn sau khi tính đến các yếu tố khác. Bốn yếu tố cùng chỉ giải thích khoảng 1,3% sự khác biệt.")

ra = GOC / "ch3_3_5_5_mohinh.docx"
tw.doc.save(ra)
print("đã ghi", ra)
