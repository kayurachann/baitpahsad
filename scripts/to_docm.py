"""Repackage a .docx as a macro-enabled .docm (same parts, macro-enabled main content type, no VBA).

This matches the structure of the authors' original Paper_Chinhthuc_2_1.docm, which also carried the
macro-enabled content type without a VBA project.

Usage: python3 to_docm.py input.docx [output.docm]
"""
import sys
import zipfile
from pathlib import Path

DOCX_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
DOCM_MAIN = "application/vnd.ms-word.document.macroEnabled.main+xml"


def convert(src: Path, dst: Path):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        names = zin.namelist()
        # [Content_Types].xml must stay the first entry of the package
        for name in ["[Content_Types].xml"] + [n for n in names if n != "[Content_Types].xml"]:
            data = zin.read(name)
            if name == "[Content_Types].xml":
                text = data.decode("utf8")
                assert DOCX_MAIN in text, "input is not a plain .docx main document"
                data = text.replace(DOCX_MAIN, DOCM_MAIN).encode("utf8")
            zout.writestr(name, data)
    return dst


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".docm")
    print("written", convert(src, dst))
