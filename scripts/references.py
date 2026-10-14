"""Bibliography in Springer LNCS numbered style, keyed by citation key.

Numbering in the manuscript follows the order of first citation. Metadata were checked against
publisher / indexer / author pages (see docs/reference_verification.md); entries marked
CHECK there still need one Crossref pass before camera-ready.
"""

REFERENCES = {
    "stc": "Filler, T., Judas, J., Fridrich, J.: Minimizing additive distortion in steganography using "
           "syndrome-trellis codes. IEEE Trans. Inf. Forensics Secur. 6(3), 920–935 (2011). "
           "https://doi.org/10.1109/TIFS.2011.2134094",
    "wow": "Holub, V., Fridrich, J.: Designing steganographic distortion using directional filters. In: 2012 "
           "IEEE International Workshop on Information Forensics and Security (WIFS), pp. 234–239. IEEE (2012). "
           "https://doi.org/10.1109/WIFS.2012.6412655",
    "uniward": "Holub, V., Fridrich, J., Denemark, T.: Universal distortion function for steganography in an "
               "arbitrary domain. EURASIP J. Inf. Secur. 2014, 1 (2014). https://doi.org/10.1186/1687-417X-2014-1",
    "hill": "Li, B., Wang, M., Huang, J., Li, X.: A new cost function for spatial image steganography. In: 2014 "
            "IEEE International Conference on Image Processing (ICIP), pp. 4206–4210. IEEE (2014). "
            "https://doi.org/10.1109/ICIP.2014.7025854",
    "spam": "Pevný, T., Bas, P., Fridrich, J.: Steganalysis by subtractive pixel adjacency matrix. IEEE Trans. "
            "Inf. Forensics Secur. 5(2), 215–224 (2010). https://doi.org/10.1109/TIFS.2010.2045842",
    "srm": "Fridrich, J., Kodovský, J.: Rich models for steganalysis of digital images. IEEE Trans. Inf. "
           "Forensics Secur. 7(3), 868–882 (2012). https://doi.org/10.1109/TIFS.2012.2190402",
    "ens": "Kodovský, J., Fridrich, J., Holub, V.: Ensemble classifiers for steganalysis of digital media. IEEE "
           "Trans. Inf. Forensics Secur. 7(2), 432–444 (2012). https://doi.org/10.1109/TIFS.2011.2175919",

    "yedroudj": "Yedroudj, M., Comby, F., Chaumont, M.: Yedroudj-Net: An efficient CNN for spatial "
                "steganalysis. In: 2018 IEEE International Conference on Acoustics, Speech and Signal "
                "Processing (ICASSP), pp. 2092–2096. IEEE (2018). https://doi.org/10.1109/ICASSP.2018.8461438",
    "srnet": "Boroumand, M., Chen, M., Fridrich, J.: Deep residual network for steganalysis of digital images. "
             "IEEE Trans. Inf. Forensics Secur. 14(5), 1181–1193 (2019). https://doi.org/10.1109/TIFS.2018.2871749",
    "csm": "Kodovský, J., Sedighi, V., Fridrich, J.: Study of cover source mismatch in steganalysis and ways to "
           "mitigate its impact. In: Media Watermarking, Security, and Forensics 2014. Proc. SPIE, vol. 9028, "
           "p. 90280J. SPIE (2014). https://doi.org/10.1117/12.2039693",
    "giboulot": "Giboulot, Q., Cogranne, R., Borghys, D., Bas, P.: Effects and solutions of cover-source "
                "mismatch in image steganalysis. Signal Process. Image Commun. 86, 115888 (2020). "
                "https://doi.org/10.1016/j.image.2020.115888",

    "mallet": "Mallet, A., Beneš, M., Cogranne, R.: Cover-source mismatch in steganalysis: systematic review. "
              "EURASIP J. Inf. Secur. 2024, 26 (2024). https://doi.org/10.1186/s13635-024-00171-6",
    "butora19": "Butora, J., Fridrich, J.: Detection of diversified stego sources with CNNs. In: IS&T "
                "Electronic Imaging, Media Watermarking, Security, and Forensics 2019, paper MWSF-534 (2019). "
                "https://doi.org/10.2352/ISSN.2470-1173.2019.5.MWSF-534",
    "wang25": "Wang, F., Fu, Z., Zhang, X., Li, Z., He, Z., Wang, M.: Pair-wise confidence difference-based "
              "pseudo-label selection for universal mismatched steganalysis. In: Proceedings of the 33rd ACM "
              "International Conference on Multimedia (MM ’25), pp. 8673–8681. ACM (2025). "
              "https://doi.org/10.1145/3746027.3755614",
    "yu23": "Yu, L., Li, Y., Weng, S., Tian, H., Liu, J.: Adaptive multi-teacher softened relational knowledge "
            "distillation framework for payload mismatch in image steganalysis. J. Vis. Commun. Image "
            "Represent. 95, 103900 (2023). https://doi.org/10.1016/j.jvcir.2023.103900",
    "alaska": "Cogranne, R., Giboulot, Q., Bas, P.: The ALASKA steganalysis challenge: A first step towards "
              "steganalysis “into the wild”. In: Proceedings of the ACM Workshop on Information Hiding and "
              "Multimedia Security (IH&MMSec ’19), pp. 125–137. ACM (2019). https://doi.org/10.1145/3335203.3335726",
    "cogranne15": "Cogranne, R., Fridrich, J.: Modeling and extending the ensemble classifier for steganalysis "
                  "of digital images using hypothesis testing theory. IEEE Trans. Inf. Forensics Secur. 10(12), "
                  "2627–2642 (2015). https://doi.org/10.1109/TIFS.2015.2470220",

    "mode25": "Butora, J., Bas, P.: MODE: Loss function for deep steganalysis at low false positive rate. In: "
              "33rd European Signal Processing Conference (EUSIPCO 2025), Palermo, Italy (2025)",

    "boss": "Bas, P., Filler, T., Pevný, T.: “Break our steganographic system”: The ins and outs of organizing "
            "BOSS. In: Information Hiding, IH 2011. LNCS, vol. 6958, pp. 59–70. Springer, Heidelberg (2011). "
            "https://doi.org/10.1007/978-3-642-24178-9_5",
    "sklearn": "Pedregosa, F., et al.: Scikit-learn: Machine learning in Python. J. Mach. Learn. Res. 12, "
               "2825–2830 (2011)",
    "sealwatch": "Beneš, M., Lorch, B.: sealwatch: Python package for image steganalysis. University of "
                 "Innsbruck (2024). https://github.com/uibk-uncover/sealwatch",
}
