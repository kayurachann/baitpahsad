"""Export the manuscript bibliography as RIS for import into EndNote / Zotero / Mendeley.

Usage: python3 export_ris.py [output.ris]   (default: ../docs/references.ris)
Entries are written in citation order; the check at the bottom makes sure every RIS title also
appears in the LNCS reference strings of references.py.
"""
import sys
from pathlib import Path

from references import REFERENCES

E = {
    "stc": dict(TY="JOUR", AU=["Filler, T.", "Judas, J.", "Fridrich, J."], PY="2011",
                TI="Minimizing additive distortion in steganography using syndrome-trellis codes",
                T2="IEEE Transactions on Information Forensics and Security", VL="6", IS="3", SP="920", EP="935",
                DO="10.1109/TIFS.2011.2134094"),
    "wow": dict(TY="CONF", AU=["Holub, V.", "Fridrich, J."], PY="2012",
                TI="Designing steganographic distortion using directional filters",
                T2="2012 IEEE International Workshop on Information Forensics and Security (WIFS)", SP="234",
                EP="239", PB="IEEE", DO="10.1109/WIFS.2012.6412655"),
    "uniward": dict(TY="JOUR", AU=["Holub, V.", "Fridrich, J.", "Denemark, T."], PY="2014",
                    TI="Universal distortion function for steganography in an arbitrary domain",
                    T2="EURASIP Journal on Information Security", VL="2014", SP="1", DO="10.1186/1687-417X-2014-1"),
    "hill": dict(TY="CONF", AU=["Li, B.", "Wang, M.", "Huang, J.", "Li, X."], PY="2014",
                 TI="A new cost function for spatial image steganography",
                 T2="2014 IEEE International Conference on Image Processing (ICIP)", SP="4206", EP="4210",
                 PB="IEEE", DO="10.1109/ICIP.2014.7025854"),
    "spam": dict(TY="JOUR", AU=["Pevný, T.", "Bas, P.", "Fridrich, J."], PY="2010",
                 TI="Steganalysis by subtractive pixel adjacency matrix",
                 T2="IEEE Transactions on Information Forensics and Security", VL="5", IS="2", SP="215", EP="224",
                 DO="10.1109/TIFS.2010.2045842"),
    "srm": dict(TY="JOUR", AU=["Fridrich, J.", "Kodovský, J."], PY="2012",
                TI="Rich models for steganalysis of digital images",
                T2="IEEE Transactions on Information Forensics and Security", VL="7", IS="3", SP="868", EP="882",
                DO="10.1109/TIFS.2012.2190402"),
    "ens": dict(TY="JOUR", AU=["Kodovský, J.", "Fridrich, J.", "Holub, V."], PY="2012",
                TI="Ensemble classifiers for steganalysis of digital media",
                T2="IEEE Transactions on Information Forensics and Security", VL="7", IS="2", SP="432", EP="444",
                DO="10.1109/TIFS.2011.2175919"),
    "yedroudj": dict(TY="CONF", AU=["Yedroudj, M.", "Comby, F.", "Chaumont, M."], PY="2018",
                     TI="Yedroudj-Net: An efficient CNN for spatial steganalysis",
                     T2="2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
                     SP="2092", EP="2096", PB="IEEE", DO="10.1109/ICASSP.2018.8461438"),
    "srnet": dict(TY="JOUR", AU=["Boroumand, M.", "Chen, M.", "Fridrich, J."], PY="2019",
                  TI="Deep residual network for steganalysis of digital images",
                  T2="IEEE Transactions on Information Forensics and Security", VL="14", IS="5", SP="1181", EP="1193",
                  DO="10.1109/TIFS.2018.2871749"),
    "csm": dict(TY="CONF", AU=["Kodovský, J.", "Sedighi, V.", "Fridrich, J."], PY="2014",
                TI="Study of cover source mismatch in steganalysis and ways to mitigate its impact",
                T2="Media Watermarking, Security, and Forensics 2014", T3="Proc. SPIE", VL="9028", SP="90280J",
                PB="SPIE", DO="10.1117/12.2039693"),
    "giboulot": dict(TY="JOUR", AU=["Giboulot, Q.", "Cogranne, R.", "Borghys, D.", "Bas, P."], PY="2020",
                     TI="Effects and solutions of cover-source mismatch in image steganalysis",
                     T2="Signal Processing: Image Communication", VL="86", SP="115888",
                     DO="10.1016/j.image.2020.115888"),
    "mallet": dict(TY="JOUR", AU=["Mallet, A.", "Beneš, M.", "Cogranne, R."], PY="2024",
                   TI="Cover-source mismatch in steganalysis: systematic review",
                   T2="EURASIP Journal on Information Security", VL="2024", SP="26",
                   DO="10.1186/s13635-024-00171-6"),
    "butora19": dict(TY="CONF", AU=["Butora, J.", "Fridrich, J."], PY="2019",
                     TI="Detection of diversified stego sources with CNNs",
                     T2="IS&T Electronic Imaging, Media Watermarking, Security, and Forensics 2019",
                     SP="MWSF-534", DO="10.2352/ISSN.2470-1173.2019.5.MWSF-534"),
    "wang25": dict(TY="CONF", AU=["Wang, F.", "Fu, Z.", "Zhang, X.", "Li, Z.", "He, Z.", "Wang, M."], PY="2025",
                   TI="Pair-wise confidence difference-based pseudo-label selection for universal mismatched "
                      "steganalysis",
                   T2="Proceedings of the 33rd ACM International Conference on Multimedia (MM '25)", SP="8673",
                   EP="8681", PB="ACM", DO="10.1145/3746027.3755614"),
    "yu23": dict(TY="JOUR", AU=["Yu, L.", "Li, Y.", "Weng, S.", "Tian, H.", "Liu, J."], PY="2023",
                 TI="Adaptive multi-teacher softened relational knowledge distillation framework for payload "
                    "mismatch in image steganalysis",
                 T2="Journal of Visual Communication and Image Representation", VL="95", SP="103900",
                 DO="10.1016/j.jvcir.2023.103900"),
    "alaska": dict(TY="CONF", AU=["Cogranne, R.", "Giboulot, Q.", "Bas, P."], PY="2019",
                   TI="The ALASKA steganalysis challenge: A first step towards steganalysis “into the wild”",
                   T2="Proceedings of the ACM Workshop on Information Hiding and Multimedia Security (IH&MMSec '19)",
                   SP="125", EP="137", PB="ACM", DO="10.1145/3335203.3335726"),
    "cogranne15": dict(TY="JOUR", AU=["Cogranne, R.", "Fridrich, J."], PY="2015",
                       TI="Modeling and extending the ensemble classifier for steganalysis of digital images using "
                          "hypothesis testing theory",
                       T2="IEEE Transactions on Information Forensics and Security", VL="10", IS="12", SP="2627",
                       EP="2642", DO="10.1109/TIFS.2015.2470220"),
    "mode25": dict(TY="CONF", AU=["Butora, J.", "Bas, P."], PY="2025",
                   TI="MODE: Loss function for deep steganalysis at low false positive rate",
                   T2="33rd European Signal Processing Conference (EUSIPCO 2025)", CY="Palermo, Italy"),
    "boss": dict(TY="CHAP", AU=["Bas, P.", "Filler, T.", "Pevný, T."], PY="2011",
                 TI="“Break our steganographic system”: The ins and outs of organizing BOSS",
                 T2="Information Hiding, IH 2011", T3="Lecture Notes in Computer Science", VL="6958", SP="59",
                 EP="70", PB="Springer", CY="Heidelberg", DO="10.1007/978-3-642-24178-9_5"),
    "sklearn": dict(TY="JOUR", AU=["Pedregosa, F.", "et al."], PY="2011",
                    TI="Scikit-learn: Machine learning in Python", T2="Journal of Machine Learning Research",
                    VL="12", SP="2825", EP="2830"),
    "sealwatch": dict(TY="COMP", AU=["Beneš, M.", "Lorch, B."], PY="2024",
                      TI="sealwatch: Python package for image steganalysis", PB="University of Innsbruck",
                      UR="https://github.com/uibk-uncover/sealwatch"),
}


def to_ris(e):
    lines = [f"TY  - {e['TY']}"] + [f"AU  - {a}" for a in e["AU"]]
    for tag in ("PY", "TI", "T2", "T3", "VL", "IS", "SP", "EP", "PB", "CY", "DO", "UR"):
        if tag in e:
            lines.append(f"{tag}  - {e[tag]}")
    return "\n".join(lines + ["ER  - ", ""])


def order():
    """Citation order of the manuscript (first appearance)."""
    from build_manuscript import build, ROOT
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        d, _ = build(ROOT / "templates" / "lncs", Path(t) / "x.docx")
    return d.cite_order


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs" / "references.ris"
    keys = order()
    for k in keys:
        title = E[k]["TI"].replace("“", "").replace("”", "")
        assert title.split(":")[0][:30] in REFERENCES[k].replace("“", "").replace("”", ""), k
    out.write_text("\n".join(to_ris(E[k]) for k in keys), encoding="utf8")
    print("written", out, len(keys), "entries")
