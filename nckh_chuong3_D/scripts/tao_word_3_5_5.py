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
tw.doan("Mục 3.5.3 đã xem xét liên hệ của từng yếu tố riêng lẻ với chất lượng giấc ngủ. Tuy nhiên, bốn yếu tố có "
        "tương quan với nhau ở mức vừa phải: hệ số tương quan hạng Spearman giữa từng cặp nằm trong khoảng từ 0,33 "
        "(tiêu thụ caffeine – căng thẳng học tập) đến 0,45 (sử dụng thiết bị trước giờ ngủ – tiêu thụ caffeine). Vì "
        "vậy, một phần liên hệ quan sát được khi xét riêng một yếu tố có thể là phần chung với các yếu tố khác. Mục "
        "này đưa cả bốn yếu tố vào cùng một mô hình để xác định yếu tố nào còn liên hệ với chất lượng giấc ngủ sau "
        "khi đã tính đến ba yếu tố còn lại.")
tw.doan("Vì chất lượng giấc ngủ được đo bằng thang thứ bậc năm mức, nhóm dùng hồi quy logit thứ bậc. Mô hình được "
        "ước lượng theo ba bước: M1 gồm bốn mô hình đơn biến, mỗi mô hình chỉ có một yếu tố, dùng để đối chiếu; M2 "
        "đưa cả bốn yếu tố vào cùng lúc và là mô hình chính; M3 thêm giới tính và năm học vào M2, trong đó năm học "
        "được mã hóa thành ba biến giả với năm 1 là nhóm tham chiếu. Các yếu tố được chuẩn hóa (trừ đi giá trị trung "
        "bình rồi chia cho độ lệch chuẩn). Do đó, tỉ số odds (odds ratio, OR) cho biết odds rơi vào mức chất lượng "
        "giấc ngủ cao hơn thay đổi bao nhiêu lần khi yếu tố tăng một độ lệch chuẩn. OR lớn hơn 1 ứng với liên hệ "
        "thuận, nhỏ hơn 1 ứng với liên hệ nghịch, bằng 1 nghĩa là không có liên hệ theo một chiều. Ở M2 và M3, OR "
        "của mỗi yếu tố được hiểu khi các biến còn lại trong mô hình giữ nguyên. Mô hình giả định OR này như nhau ở "
        "mọi ngưỡng chia của thang năm mức (giả định odds tỉ lệ) và đưa mỗi yếu tố vào dưới dạng một hệ số duy nhất, "
        "nên không phản ánh được khác biệt không theo một chiều như dạng chữ U ở mục 3.5.4.")
tw.doan("Ngoài ra, nhóm ước lượng thêm hồi quy tuyến tính (OLS) trên điểm chất lượng giấc ngủ 1–5, coi như thang "
        "khoảng. Cả biến phụ thuộc và bốn yếu tố đều được chuẩn hóa để có hệ số hồi quy chuẩn hóa β, dùng làm thước "
        "chung so sánh mức độ liên hệ giữa các yếu tố ở mục 3.5.6; sai số chuẩn tính theo HC3 (sai số chuẩn vững, "
        "không cần giả định phương sai sai số bằng nhau). Nhóm cũng tính hệ số phóng đại phương sai (VIF) từ ma trận "
        "tương quan của bốn yếu tố để kiểm tra hiện tượng đa cộng tuyến. Các mô hình được chạy bằng thư viện "
        "statsmodels trên Google Colab. Kết quả hồi quy logit thứ bậc được trình bày ở Bảng 3.7.")

tw.chu_thich(f"Bảng 3.7. Tỉ số odds (OR) trong ba mô hình hồi quy logit thứ bậc của chất lượng giấc ngủ (n = 996)")
dong = [["Yếu tố", "M1 (từng yếu tố riêng)", "M2 (bốn yếu tố)", "M3 (thêm giới tính, năm học)"]]
for ten, gt in OR.items():
    dong.append([ten] + [o(x) for x in gt])
dong.append(["Nam (so với nữ)", "–", "–", o(NAM)])
dong.append(["McFadden R²", "–", MCFADDEN["M2"], MCFADDEN["M3"]])
tw.bang(dong, [4.6, 3.8, 3.6, 4.0], can_giua_tu=1)
tw.ghi_nguon("Ghi chú: Bốn yếu tố đã được chuẩn hóa nên OR ứng với mức tăng một độ lệch chuẩn; Nam là biến 0/1 nên "
             "OR so nam với nữ; số trong ngoặc là giá trị p; dấu – nghĩa là không áp dụng. M1 gồm bốn mô hình đơn "
             "biến nên không có một McFadden R² chung. M3 có thêm ba biến giả năm học (nhóm tham chiếu là năm 1, chỉ "
             "22 người); so với năm 1, không biến giả nào có ý nghĩa thống kê (p từ 0,12 đến 0,74), nhưng các so "
             "sánh này kém chính xác do nhóm tham chiếu nhỏ.", keep=True)
tw.ghi_nguon(tw.NGUON)

hd = OR[HD]
tw.doan(f"Hoạt động thể chất là yếu tố duy nhất giữ liên hệ ổn định ở cả ba mô hình. OR là {so(hd[0][0])} khi xét "
        f"riêng, tăng lên {so(hd[1][0])} khi có đủ bốn yếu tố và {so(hd[2][0])} khi thêm giới tính và năm học; p ở "
        "cả ba mô hình đều không quá 0,002. Nói cách khác, so giữa hai sinh viên có mức hoạt động thể chất chênh "
        "nhau một độ lệch chuẩn, người hoạt động nhiều hơn có odds rơi vào mức chất lượng giấc ngủ cao hơn gấp "
        f"khoảng {so(hd[0][0], 2)} lần khi xét riêng và khoảng {so(hd[1][0], 2)} lần sau khi đã tính đến các yếu "
        "tố còn lại.")
tb, ct = OR[TB], OR[CT]
tw.doan(f"Sử dụng thiết bị trước giờ ngủ và căng thẳng học tập có OR nhỉnh hơn 1 khi xét riêng ({so(tb[0][0])} và "
        f"{so(ct[0][0])}), phù hợp với hệ số tương quan nhỏ ở mục 3.5.3, nhưng không có ý nghĩa thống kê (p lần "
        f"lượt là {tb[0][1]} và {ct[0][1]}). Khi đưa cả bốn yếu tố vào mô hình (M2), OR của hai yếu tố này gần như "
        f"bằng 1 ({so(tb[1][0])} và {so(ct[1][0])}; p lần lượt là {tb[1][1]} và {ct[1][1]}). Như vậy, liên hệ nhỏ "
        "quan sát được khi xét riêng chủ yếu là phần chung với các yếu tố khác, không phải phần riêng của hai yếu "
        "tố này.")
cf = OR[CF]
tw.doan("Liên hệ của tiêu thụ caffeine chuyển từ gần như không có sang nghịch nhẹ, nhưng chưa có ý nghĩa thống kê. "
        f"Khi xét riêng, OR gần như bằng 1 ({so(cf[0][0])}; p = {cf[0][1]}). Khi tính đến các yếu tố còn lại, trong "
        "đó có hoạt động thể chất (hệ số Spearman 0,42 với tiêu thụ caffeine), OR giảm còn "
        f"{so(cf[1][0])} (p = {cf[1][1]}) ở M2 và {so(cf[2][0])} (p = {cf[2][1]}) ở M3. Vì p lớn hơn 0,05, kết quả "
        "này chỉ là gợi ý, chưa đủ cơ sở để khẳng định có liên hệ nghịch.")
tw.doan(f"Ở M3, odds rơi vào mức chất lượng giấc ngủ cao hơn của nam chỉ bằng khoảng {so(NAM[0], 2)} lần odds của "
        f"nữ (OR = {so(NAM[0])}; p = {NAM[1]}), tức thấp hơn khoảng {round((1 - NAM[0]) * 100)}%. So với năm 1 "
        "(nhóm tham chiếu, chỉ 22 người), không biến giả năm học nào có ý nghĩa thống kê (p từ 0,12 đến 0,74); vì "
        "nhóm tham chiếu quá nhỏ, các so sánh này kém chính xác và không đủ để kết luận năm học không liên hệ với "
        "chất lượng giấc ngủ. Khi thêm giới tính và năm học, kết quả của bốn yếu tố gần như không đổi.")
tw.doan("Hồi quy tuyến tính (OLS) cho kết quả cùng chiều với hồi quy logit thứ bậc: hệ số hồi quy chuẩn hóa (β) của "
        "hoạt động thể chất là 0,130 (p = 0,0008), của tiêu thụ caffeine là −0,073 (p = 0,056), còn của sử dụng "
        "thiết bị trước giờ ngủ và căng thẳng học tập đều chỉ khoảng 0,006. VIF của bốn yếu tố từ 1,34 đến 1,61, "
        "đều dưới 2, nên không có dấu hiệu đa cộng tuyến đáng kể. Tuy vậy, khả năng giải thích của mô hình rất "
        "thấp. Theo OLS, bốn yếu tố chỉ giải thích khoảng 1,3% sự khác biệt về chất lượng giấc ngủ (R² = 0,013; "
        f"R² hiệu chỉnh = 0,009). McFadden R² của M2 là {MCFADDEN['M2']} và tăng lên {MCFADDEN['M3']} ở M3 khi "
        "thêm giới tính và năm học. Phần lớn sự khác biệt về chất lượng giấc ngủ chưa được bốn yếu tố này giải "
        "thích.")
tw.doan(f"Kết luận: khi xem đồng thời, chỉ hoạt động thể chất còn liên hệ rõ với chất lượng giấc ngủ (OR = "
        f"{so(hd[1][0], 2)}; p = {hd[1][1]}); liên hệ theo một chiều của sử dụng thiết bị trước giờ ngủ và căng "
        "thẳng học tập không còn sau khi tính đến các yếu tố khác (OR gần bằng 1). Bốn yếu tố cùng chỉ giải thích "
        "khoảng 1,3% sự khác biệt.")

ra = GOC / "ch3_3_5_5_mohinh.docx"
tw.doc.save(ra)
print("đã ghi", ra)
