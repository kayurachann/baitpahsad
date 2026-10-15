"""So các con số giữa bản mới (gốc) và bản viết lại theo format bản cũ.

    python3 check_numbers.py <goc.docx> <content/de_an.json>

In ra: số có trong bản gốc nhưng không còn trong bản viết lại (kèm ngữ cảnh gốc) và số mới xuất hiện
trong bản viết lại (kèm ngữ cảnh). Bỏ qua phần bìa, mục lục, và các URL.
"""
import json
import re
import sys
from collections import Counter

from extract_index import build_index

NUM = re.compile(r"(?<![\w/])[−-]?\d+(?:[.,]\d+)*(?:%|°C)?")
URL = re.compile(r"https?://\S+")


def norm(tok):
    return tok.replace("−", "-").rstrip(".,")


def numbers(text):
    text = URL.sub(" ", text.replace("​", ""))
    return [norm(m.group()) for m in NUM.finditer(text)]


def block_texts(sections):
    for sec in sections:
        for b in sec:
            parts = [b.get("lead", ""), b.get("text", "")]
            parts += b.get("header", []) or []
            for row in b.get("rows", []) or []:
                parts += row
            parts += b.get("items", []) or []
            for p in parts:
                if p:
                    yield p.replace("**", "")


def main():
    units = build_index(sys.argv[1])
    start = next(i for i, u in enumerate(units) if u["style"].startswith("Heading") and u["text"].strip() == "MỞ ĐẦU")
    src_texts = [u["text"] for u in units[start:]]
    new_texts = list(block_texts(json.loads(open(sys.argv[2], encoding="utf8").read())["sections"]))

    src = Counter(n for t in src_texts for n in numbers(t))
    new = Counter(n for t in new_texts for n in numbers(t))

    def ctx(texts, n, k=2):
        out = []
        for t in texts:
            if n in numbers(t):
                out.append(t if len(t) < 140 else t[:140] + "…")
            if len(out) >= k:
                break
        return " ‖ ".join(out)

    missing = sorted(n for n in src if n not in new)
    added = sorted(n for n in new if n not in src)
    print(f"Số khác nhau trong bản gốc: {len(src)}; trong bản viết lại: {len(new)}")
    print(f"\n== Có trong bản gốc, không còn trong bản viết lại ({len(missing)}) ==")
    for n in missing:
        print(f"  {n:>12}  ×{src[n]}  | {ctx(src_texts, n)}")
    print(f"\n== Mới trong bản viết lại ({len(added)}) ==")
    for n in added:
        print(f"  {n:>12}  ×{new[n]}  | {ctx(new_texts, n)}")


if __name__ == "__main__":
    main()
