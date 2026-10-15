"""Danh mục tài liệu tham khảo của Paper_HoanChinh (giữ đúng thứ tự [1]–[20] của EndNote trong file nhóm).

Mỗi mục có: số thứ tự, RecNum trong thư viện EndNote của nhóm, chuỗi trình bày theo Springer LNCS, và các trường
có cấu trúc để ghi lại bản ghi EndNote nhúng trong file và xuất RIS. Metadata đã đối chiếu nguồn xuất bản/chỉ mục
(xem docs/reference_verification.md và docs/PHAN_HOI_THAY_LAN_CUOI.md).
"""

REFS = [
    dict(n=1, recnum="2", typ="JOUR", authors=["Filler, T.", "Judas, J.", "Fridrich, J."],
         title="Minimizing additive distortion in steganography using syndrome-trellis codes",
         container="IEEE Transactions on Information Forensics and Security", volume="6", number="3",
         pages="920-935", year="2011", doi="10.1109/TIFS.2011.2134094",
         lncs="Filler, T., Judas, J., Fridrich, J.: Minimizing additive distortion in steganography using "
              "syndrome-trellis codes. IEEE Trans. Inf. Forensics Secur. 6(3), 920–935 (2011). "
              "https://doi.org/10.1109/TIFS.2011.2134094"),
    dict(n=2, recnum="3", typ="CONF", authors=["Holub, V.", "Fridrich, J."],
         title="Designing steganographic distortion using directional filters",
         container="2012 IEEE International Workshop on Information Forensics and Security (WIFS)",
         pages="234-239", year="2012", publisher="IEEE", doi="10.1109/WIFS.2012.6412655",
         lncs="Holub, V., Fridrich, J.: Designing steganographic distortion using directional filters. In: IEEE "
              "International Workshop on Information Forensics and Security (WIFS 2012), pp. 234–239. IEEE (2012). "
              "https://doi.org/10.1109/WIFS.2012.6412655"),
    dict(n=3, recnum="4", typ="JOUR", authors=["Holub, V.", "Fridrich, J.", "Denemark, T."],
         title="Universal distortion function for steganography in an arbitrary domain",
         container="EURASIP Journal on Information Security", volume="2014", pages="1", year="2014",
         doi="10.1186/1687-417X-2014-1",
         lncs="Holub, V., Fridrich, J., Denemark, T.: Universal distortion function for steganography in an "
              "arbitrary domain. EURASIP J. Inf. Secur. 2014, 1 (2014). https://doi.org/10.1186/1687-417X-2014-1"),
    dict(n=4, recnum="5", typ="CONF", authors=["Li, B.", "Wang, M.", "Huang, J.", "Li, X."],
         title="A new cost function for spatial image steganography",
         container="2014 IEEE International Conference on Image Processing (ICIP)", pages="4206-4210",
         year="2014", publisher="IEEE", doi="10.1109/ICIP.2014.7025854",
         lncs="Li, B., Wang, M., Huang, J., Li, X.: A new cost function for spatial image steganography. In: IEEE "
              "International Conference on Image Processing (ICIP 2014), pp. 4206–4210. IEEE (2014). "
              "https://doi.org/10.1109/ICIP.2014.7025854"),
    dict(n=5, recnum="14", typ="JOUR", authors=["Boroumand, M.", "Chen, M.", "Fridrich, J."],
         title="Deep residual network for steganalysis of digital images",
         container="IEEE Transactions on Information Forensics and Security", volume="14", number="5",
         pages="1181-1193", year="2019", doi="10.1109/TIFS.2018.2871749",
         lncs="Boroumand, M., Chen, M., Fridrich, J.: Deep residual network for steganalysis of digital images. "
              "IEEE Trans. Inf. Forensics Secur. 14(5), 1181–1193 (2019). https://doi.org/10.1109/TIFS.2018.2871749"),
    dict(n=6, recnum="8", typ="JOUR", authors=["Kodovský, J.", "Fridrich, J.", "Holub, V."],
         title="Ensemble classifiers for steganalysis of digital media",
         container="IEEE Transactions on Information Forensics and Security", volume="7", number="2",
         pages="432-444", year="2012", doi="10.1109/TIFS.2011.2175919",
         lncs="Kodovský, J., Fridrich, J., Holub, V.: Ensemble classifiers for steganalysis of digital media. IEEE "
              "Trans. Inf. Forensics Secur. 7(2), 432–444 (2012). https://doi.org/10.1109/TIFS.2011.2175919"),
    dict(n=7, recnum="13", typ="CONF", authors=["Yedroudj, M.", "Comby, F.", "Chaumont, M."],
         title="Yedroudj-Net: An efficient CNN for spatial steganalysis",
         container="2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
         pages="2092-2096", year="2018", publisher="IEEE", doi="10.1109/ICASSP.2018.8461438",
         lncs="Yedroudj, M., Comby, F., Chaumont, M.: Yedroudj-Net: An efficient CNN for spatial steganalysis. In: "
              "IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP 2018), pp. "
              "2092–2096. IEEE (2018). https://doi.org/10.1109/ICASSP.2018.8461438"),
    dict(n=8, recnum="22", typ="JOUR", authors=["Mallet, A.", "Beneš, M.", "Cogranne, R."],
         title="Cover-source mismatch in steganalysis: systematic review",
         container="EURASIP Journal on Information Security", volume="2024", pages="26", year="2024",
         doi="10.1186/s13635-024-00171-6",
         lncs="Mallet, A., Beneš, M., Cogranne, R.: Cover-source mismatch in steganalysis: systematic review. "
              "EURASIP J. Inf. Secur. 2024, 26 (2024). https://doi.org/10.1186/s13635-024-00171-6"),
    dict(n=9, recnum="9", typ="CONF", authors=["Kodovský, J.", "Sedighi, V.", "Fridrich, J."],
         title="Study of cover source mismatch in steganalysis and ways to mitigate its impact",
         container="Media Watermarking, Security, and Forensics 2014, Proc. SPIE vol. 9028", volume="9028",
         pages="90280J", year="2014", publisher="SPIE", doi="10.1117/12.2039693",
         lncs="Kodovský, J., Sedighi, V., Fridrich, J.: Study of cover source mismatch in steganalysis and ways to "
              "mitigate its impact. In: Media Watermarking, Security, and Forensics 2014. Proc. SPIE, vol. 9028, "
              "p. 90280J. SPIE (2014). https://doi.org/10.1117/12.2039693"),
    dict(n=10, recnum="20", typ="CONF", authors=["Butora, J.", "Fridrich, J."],
         title="Detection of diversified stego sources with CNNs",
         container="IS&T International Symposium on Electronic Imaging: Media Watermarking, Security, and "
                   "Forensics 2019", pages="534-1–534-11", year="2019", publisher="Society for Imaging Science and Technology",
         doi="10.2352/ISSN.2470-1173.2019.5.MWSF-534",
         lncs="Butora, J., Fridrich, J.: Detection of diversified stego sources with CNNs. In: Electronic Imaging, "
              "Media Watermarking, Security, and Forensics 2019, pp. 534-1–534-11. IS&T (2019). "
              "https://doi.org/10.2352/ISSN.2470-1173.2019.5.MWSF-534"),
    dict(n=11, recnum="21", typ="CONF",
         authors=["Wang, F.", "Fu, Z.", "Zhang, X.", "Li, Z.", "He, Z.", "Wang, M."],
         title="Pair-wise confidence difference-based pseudo-label selection for universal mismatched steganalysis",
         container="Proceedings of the 33rd ACM International Conference on Multimedia (MM '25)",
         pages="8673-8681", year="2025", publisher="ACM", doi="10.1145/3746027.3755614",
         lncs="Wang, F., Fu, Z., Zhang, X., Li, Z., He, Z., Wang, M.: Pair-wise confidence difference-based "
              "pseudo-label selection for universal mismatched steganalysis. In: 33rd ACM International "
              "Conference on Multimedia (MM 2025), pp. 8673–8681. ACM (2025). "
              "https://doi.org/10.1145/3746027.3755614"),
    dict(n=12, recnum="7", typ="JOUR", authors=["Fridrich, J.", "Kodovský, J."],
         title="Rich models for steganalysis of digital images",
         container="IEEE Transactions on Information Forensics and Security", volume="7", number="3",
         pages="868-882", year="2012", doi="10.1109/TIFS.2012.2190402",
         lncs="Fridrich, J., Kodovský, J.: Rich models for steganalysis of digital images. IEEE Trans. Inf. "
              "Forensics Secur. 7(3), 868–882 (2012). https://doi.org/10.1109/TIFS.2012.2190402"),
    dict(n=13, recnum="6", typ="CONF", authors=["Pevný, T.", "Bas, P.", "Fridrich, J."],
         title="Steganalysis by subtractive pixel adjacency matrix",
         container="Proceedings of the 11th ACM Workshop on Multimedia and Security (MM&Sec '09)",
         pages="75-84", year="2009", publisher="ACM", doi="10.1145/1597817.1597831",
         lncs="Pevný, T., Bas, P., Fridrich, J.: Steganalysis by subtractive pixel adjacency matrix. In: 11th"
              " ACM Workshop on Multimedia and Security (MM&Sec 2009), pp. 75–84. ACM (2009). "
              "https://doi.org/10.1145/1597817.1597831"),
    dict(n=14, recnum="23", typ="JOUR", authors=["Yu, L.", "Li, Y.", "Weng, S.", "Tian, H.", "Liu, J."],
         title="Adaptive multi-teacher softened relational knowledge distillation framework for payload mismatch "
               "in image steganalysis",
         container="Journal of Visual Communication and Image Representation", volume="95", pages="103900",
         year="2023", doi="10.1016/j.jvcir.2023.103900",
         lncs="Yu, L., Li, Y., Weng, S., Tian, H., Liu, J.: Adaptive multi-teacher softened relational knowledge "
              "distillation framework for payload mismatch in image steganalysis. J. Vis. Commun. Image Represent. "
              "95, 103900 (2023). https://doi.org/10.1016/j.jvcir.2023.103900"),
    dict(n=15, recnum="24", typ="CONF", authors=["Cogranne, R.", "Giboulot, Q.", "Bas, P."],
         title="The ALASKA steganalysis challenge: A first step towards steganalysis \"into the wild\"",
         container="Proceedings of the ACM Workshop on Information Hiding and Multimedia Security (IH&MMSec '19)",
         pages="125-137", year="2019", publisher="ACM", doi="10.1145/3335203.3335726",
         lncs="Cogranne, R., Giboulot, Q., Bas, P.: The ALASKA steganalysis challenge: A first step towards "
              "steganalysis “into the wild”. In: ACM Workshop on Information Hiding and Multimedia Security "
              "(IH&MMSec 2019), pp. 125–137. ACM (2019). https://doi.org/10.1145/3335203.3335726"),
    dict(n=16, recnum="26", typ="JOUR", authors=["Cogranne, R.", "Fridrich, J."],
         title="Modeling and extending the ensemble classifier for steganalysis of digital images using hypothesis "
               "testing theory",
         container="IEEE Transactions on Information Forensics and Security", volume="10", number="12",
         pages="2627-2642", year="2015", doi="10.1109/TIFS.2015.2470220",
         lncs="Cogranne, R., Fridrich, J.: Modeling and extending the ensemble classifier for steganalysis of "
              "digital images using hypothesis testing theory. IEEE Trans. Inf. Forensics Secur. 10(12), "
              "2627–2642 (2015). https://doi.org/10.1109/TIFS.2015.2470220"),
    dict(n=17, recnum="25", typ="CONF", authors=["Butora, J.", "Bas, P."],
         title="MODE: Loss function for deep steganalysis at low false positive rate",
         container="33rd European Signal Processing Conference (EUSIPCO 2025)", year="2025",
         place="Palermo, Italy", url="https://hal.science/hal-05101274",
         lncs="Butora, J., Bas, P.: MODE: Loss function for deep steganalysis at low false positive rate. In: "
              "33rd European Signal Processing Conference (EUSIPCO 2025), Palermo, Italy (2025). "
              "https://hal.science/hal-05101274"),
    dict(n=18, recnum="27", typ="CHAP", authors=["Bas, P.", "Filler, T.", "Pevný, T."],
         title="\"Break our steganographic system\": The ins and outs of organizing BOSS",
         container="Information Hiding, IH 2011, Lecture Notes in Computer Science, vol. 6958", volume="6958",
         pages="59-70", year="2011", publisher="Springer", place="Heidelberg", doi="10.1007/978-3-642-24178-9_5",
         lncs="Bas, P., Filler, T., Pevný, T.: “Break our steganographic system”: The ins and outs of organizing "
              "BOSS. In: Information Hiding, IH 2011. LNCS, vol. 6958, pp. 59–70. Springer, Heidelberg (2011). "
              "https://doi.org/10.1007/978-3-642-24178-9_5"),
    dict(n=19, recnum="17", typ="JOUR",
         authors=["Pedregosa, F.", "Varoquaux, G.", "Gramfort, A.", "Michel, V.", "Thirion, B.", "Grisel, O.",
                  "Blondel, M.", "Prettenhofer, P.", "Weiss, R.", "Dubourg, V.", "Vanderplas, J.", "Passos, A.",
                  "Cournapeau, D.", "Brucher, M.", "Perrot, M.", "Duchesnay, E."],
         title="Scikit-learn: Machine learning in Python", container="Journal of Machine Learning Research",
         volume="12", pages="2825-2830", year="2011",
         lncs="Pedregosa, F., et al.: Scikit-learn: Machine learning in Python. J. Mach. Learn. Res. 12, "
              "2825–2830 (2011)"),
    dict(n=20, recnum="28", typ="COMP", authors=["Beneš, M.", "Lorch, B."],
         title="sealwatch: Implementation of modern image steganalysis algorithms", container="Python package",
         year="2024", publisher="University of Innsbruck", url="https://github.com/uibk-uncover/sealwatch",
         lncs_truoc_url="Beneš, M., Lorch, B.: sealwatch: Implementation of modern image steganalysis algorithms. "
                        "Python package, University of Innsbruck (2024). ",
         lncs_sau_url=", last accessed 2026/10/15",
         lncs="Beneš, M., Lorch, B.: sealwatch: Implementation of modern image steganalysis algorithms. Python "
              "package, University of Innsbruck (2024). https://github.com/uibk-uncover/sealwatch, last accessed "
              "2026/10/15"),
]

# kiểu tài liệu EndNote (tên, mã) theo loại
ENDNOTE_TYPE = {"JOUR": ("Journal Article", "17"), "CONF": ("Conference Proceedings", "10"),
                "CHAP": ("Book Section", "5"), "COMP": ("Computer Program", "9")}


def ris(refs=REFS):
    """Xuất RIS để nhập/sửa thư viện EndNote."""
    out = []
    for r in refs:
        out.append(f"TY  - {r['typ']}")
        for a in r["authors"]:
            out.append(f"AU  - {a}")
        out.append(f"TI  - {r['title']}")
        out.append(("JO  - " if r["typ"] == "JOUR" else "T2  - ") + r["container"])
        for k, tag in (("volume", "VL"), ("number", "IS"), ("year", "PY"), ("publisher", "PB"), ("place", "CY"),
                       ("doi", "DO"), ("url", "UR")):
            if r.get(k):
                out.append(f"{tag}  - {r[k]}")
        if r.get("pages"):
            # trang dạng "534-1–534-11" tách ở gạch nối dài
            sp, _, ep = r["pages"].partition("–" if "–" in r["pages"] else "-")
            out.append(f"SP  - {sp}")
            if ep:
                out.append(f"EP  - {ep}")
        out.append(f"N1  - StegaGuard reference [{r['n']}], EndNote RecNum {r['recnum']}")
        out.append("ER  - ")
        out.append("")
    return "\n".join(out)
