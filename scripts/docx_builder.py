"""Minimal WordprocessingML writer that fills the Springer LNCS template used by PaperID 581.

Only the template's styles, numbering and page setup are reused; its body text, charts,
VBA project and EndNote data are discarded.

Inline markup understood by ``runs()``:
  **bold**  *italic*  ^{superscript}  _{subscript}
  [[text]]            highlighted placeholder that must be filled from the code base
  {tab:key} {fig:key} cross-reference (Word REF field to the caption number)
  \\cite{a,b}         numbered citation, numbered by first appearance
"""
import re
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

W_NS = ("xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" "
        "xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\" "
        "mc:Ignorable=\"w14\"")

DOCX_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
EMU_PER_IN = 914400


def prepare_template(src_unzipped: Path, dst: Path):
    """Copy the LNCS template package and strip everything that belongs to the source paper."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src_unzipped, dst)
    w = dst / "word"
    for p in [w / "vbaProject.bin", w / "vbaData.xml", w / "_rels" / "vbaProject.bin.rels"]:
        p.unlink(missing_ok=True)
    for d in [w / "charts", w / "embeddings", w / "media"]:
        shutil.rmtree(d, ignore_errors=True)
    (w / "media").mkdir()

    ct = (dst / "[Content_Types].xml").read_text(encoding="utf8")
    ct = ct.replace("application/vnd.ms-word.document.macroEnabled.main+xml", DOCX_MAIN)
    ct = re.sub(r'<Default Extension="(bin|xlsx)"[^>]*/>', "", ct)
    ct = re.sub(r'<Override PartName="/word/(vbaData\.xml|charts/[^"]+)"[^>]*/>', "", ct)
    if 'Extension="png"' not in ct:
        ct = ct.replace("<Default Extension=\"rels\"",
                        "<Default Extension=\"png\" ContentType=\"image/png\"/><Default Extension=\"rels\"")
    (dst / "[Content_Types].xml").write_text(ct, encoding="utf8")

    rels = (w / "_rels" / "document.xml.rels").read_text(encoding="utf8")
    rels = re.sub(r'<Relationship Id="rId\d+" Type="[^"]+/(vbaProject|chart|hyperlink)"[^>]*/>', "", rels)
    (w / "_rels" / "document.xml.rels").write_text(rels, encoding="utf8")

    st = (w / "settings.xml").read_text(encoding="utf8")
    st = re.sub(r"<w:docVars>.*?</w:docVars>", "", st, flags=re.S)
    st = re.sub(r"<w:attachedTemplate[^>]*/>", "", st)
    (w / "settings.xml").write_text(st, encoding="utf8")

    for f in ["core.xml", "app.xml"]:
        p = dst / "docProps" / f
        txt = p.read_text(encoding="utf8")
        txt = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title></dc:title>", txt)
        txt = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator></dc:creator>", txt)
        txt = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "<cp:lastModifiedBy></cp:lastModifiedBy>", txt)
        p.write_text(txt, encoding="utf8")


class Doc:
    def __init__(self, template_dir: Path, ref_order=None):
        self.dir = template_dir
        self.body = []
        self.bm_id = 100
        self.rid = 900
        self.rels = []
        self.media = 0
        self.labels = {}      # key -> (kind, number)
        self.counters = {"Table": 0, "Figure": 0}
        self.cite_order = list(ref_order or [])
        self.after_heading = True
        self.placeholders = []

    # ------------------------------------------------------------------ labels
    def reserve(self, kind, key):
        self.counters[kind] += 1
        self.labels[key] = (kind, self.counters[kind])

    def _bm(self, key):
        return "_Ref" + re.sub(r"[^A-Za-z0-9]", "", key)[:30]

    # ------------------------------------------------------------------ runs
    @staticmethod
    def rpr(b=False, i=False, sup=False, sub=False, size=None, hl=False, font=None, color=None, extra=""):
        x = ""
        if font:
            x += f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
        if b:
            x += "<w:b/><w:bCs/>"
        if i:
            x += "<w:i/><w:iCs/>"
        if color:
            x += f'<w:color w:val="{color}"/>'
        if size:
            x += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        if hl:
            x += '<w:highlight w:val="yellow"/>'
        if sup:
            x += '<w:vertAlign w:val="superscript"/>'
        if sub:
            x += '<w:vertAlign w:val="subscript"/>'
        x += extra
        return f"<w:rPr>{x}</w:rPr>" if x else ""

    @staticmethod
    def t(text):
        return f'<w:t xml:space="preserve">{escape(text)}</w:t>'

    def cite(self, keys):
        nums = []
        for k in keys:
            k = k.strip()
            if k not in self.cite_order:
                self.cite_order.append(k)
            nums.append(self.cite_order.index(k) + 1)
        nums = sorted(set(nums))
        parts, start, prev = [], nums[0], nums[0]
        for n in nums[1:] + [None]:
            if n is not None and n == prev + 1:
                prev = n
                continue
            if prev - start >= 2:
                parts.append(f"{start}–{prev}")
            elif prev - start == 1:
                parts += [str(start), str(prev)]
            else:
                parts.append(str(start))
            if n is not None:
                start = prev = n
        return "[" + ", ".join(parts) + "]"

    TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|\^\{.+?\}|_\{.+?\}|\[\[.+?\]\]|\{(?:tab|fig):[\w-]+\}"
                       r"|\\cite\{[^}]+\})")

    def runs(self, text, size=None, b=False, i=False, font=None):
        out = []
        for part in self.TOKEN.split(text):
            if not part:
                continue
            if part.startswith("**") and part.endswith("**"):
                out.append(self.runs(part[2:-2], size=size, b=True, i=i, font=font))
            elif part.startswith("*") and part.endswith("*") and len(part) > 2:
                out.append(self.runs(part[1:-1], size=size, b=b, i=True, font=font))
            elif part.startswith("^{"):
                out.append(f"<w:r>{self.rpr(b, i, sup=True, size=size, font=font)}{self.t(part[2:-1])}</w:r>")
            elif part.startswith("_{"):
                out.append(f"<w:r>{self.rpr(b, i, sub=True, size=size, font=font)}{self.t(part[2:-1])}</w:r>")
            elif part.startswith("[["):
                self.placeholders.append(part[2:-2])
                out.append(f"<w:r>{self.rpr(b, i, size=size, hl=True, font=font)}{self.t('[' + part[2:-2] + ']')}</w:r>")
            elif part.startswith("{tab:") or part.startswith("{fig:"):
                key = part[1:-1]
                kind, num = self.labels[key]
                word = "Table" if kind == "Table" else "Fig."
                out.append(f"<w:r>{self.rpr(b, i, size=size, font=font)}{self.t(word + chr(160))}</w:r>")
                out.append(f'<w:fldSimple w:instr=" REF {self._bm(key)} \\h \\* MERGEFORMAT ">'
                           f"<w:r>{self.rpr(b, i, size=size, font=font)}{self.t(str(num))}</w:r></w:fldSimple>")
            elif part.startswith("\\cite{"):
                out.append(f"<w:r>{self.rpr(b, i, size=size, font=font)}{self.t(self.cite(part[6:-1].split(',')))}</w:r>")
            else:
                out.append(f"<w:r>{self.rpr(b, i, size=size, font=font)}{self.t(part)}</w:r>")
        return "".join(out)

    # ------------------------------------------------------------------ blocks
    def para(self, xml_runs, style=None, ppr_extra=""):
        ps = f'<w:pStyle w:val="{style}"/>' if style else ""
        self.body.append(f"<w:p><w:pPr>{ps}{ppr_extra}</w:pPr>{xml_runs}</w:p>")

    def p(self, text, style=None, ppr_extra=""):
        if style is None:
            style = "p1a" if self.after_heading else None
        self.para(self.runs(text), style, ppr_extra)
        self.after_heading = False

    def h1(self, text):
        self.para(self.runs(text), "heading1")
        self.after_heading = True

    def h2(self, text):
        self.para(self.runs(text), "heading2")
        self.after_heading = True

    def runin(self, head, text):
        """Paragraph that opens with a bold run-in heading (LNCS \\paragraph style)."""
        self.para(self.runs(f"**{head}** ") + self.runs(text), "p1a",
                  '<w:spacing w:before="120"/>')
        self.after_heading = False

    def bullets(self, items):
        for it in items:
            self.para(self.runs(it), "bulletitem", '<w:spacing w:before="40" w:after="40"/>')
        self.after_heading = True

    def numbered(self, items):
        for it in items:
            self.para(self.runs(it), "numitem", '<w:spacing w:before="40" w:after="40"/>')
        self.after_heading = True

    def caption(self, kind, key, text):
        if key not in self.labels:
            self.reserve(kind, key)
        num = self.labels[key][1]
        self.bm_id += 1
        label = "Table" if kind == "Table" else "Fig."
        seq = "Table" if kind == "Table" else "Figure"
        num_xml = (f'<w:r>{self.rpr(b=True)}{self.t(label + " ")}</w:r>'
                   f'<w:bookmarkStart w:id="{self.bm_id}" w:name="{self._bm(key)}"/>'
                   f'<w:fldSimple w:instr=" SEQ {seq} \\* ARABIC "><w:r>{self.rpr(b=True)}{self.t(str(num))}</w:r>'
                   f'</w:fldSimple><w:bookmarkEnd w:id="{self.bm_id}"/>'
                   f'<w:r>{self.rpr(b=True)}{self.t(". ")}</w:r>')
        style = "tablecaption" if kind == "Table" else "figurecaption"
        extra = '<w:jc w:val="both"/>' if len(text) > 90 else ""
        self.para(num_xml + self.runs(text), style, extra)

    def table(self, key, caption, widths, header, rows, size=17, aligns=None, note=None,
              header_rows=None, group_rules=(), bold_cols=()):
        """Booktabs-style table. ``header`` is a list of rows; cells may be (text, span)."""
        self.caption("Table", key, caption)
        total = sum(widths)
        aligns = aligns or ["left"] + ["center"] * (len(widths) - 1)
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        tblpr = (f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:jc w:val="center"/>'
                 '<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                 '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/></w:tblBorders>'
                 '<w:tblLayout w:type="fixed"/>'
                 '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="57" w:type="dxa"/>'
                 '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
                 '<w:tblLook w:val="0000"/></w:tblPr>')

        def cell(content, width, align, bottom=False, top_rule=False, bold=False, span=1, keep=True):
            borders = ""
            if bottom or top_rule:
                borders = "<w:tcBorders>"
                if top_rule:
                    borders += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                if bottom:
                    borders += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                borders += "</w:tcBorders>"
            gs = f'<w:gridSpan w:val="{span}"/>' if span > 1 else ""
            tcpr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{gs}{borders}<w:vAlign w:val="center"/></w:tcPr>'
            paras = []
            for line in str(content).split("\n"):
                kn = "<w:keepNext/>" if keep else ""
                paras.append(f'<w:p><w:pPr>{kn}<w:spacing w:before="10" w:after="10" w:line="216" w:lineRule="auto"/>'
                             f'<w:ind w:firstLine="0"/><w:jc w:val="{align}"/></w:pPr>'
                             f'{self.runs(line, size=size, b=bold)}</w:p>')
            return f"<w:tc>{tcpr}{''.join(paras)}</w:tc>"

        def row(cells, header=False, last_header=False, rule_above=False, keep=True):
            if isinstance(cells, dict):  # full-width group label row
                txt = cells["group"]
                tcpr = (f'<w:tcPr><w:tcW w:w="{total}" w:type="dxa"/><w:gridSpan w:val="{len(widths)}"/>'
                        + ('<w:tcBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>'
                           if rule_above else '') + '</w:tcPr>')
                para = (f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="30" w:after="10" w:line="216" w:lineRule="auto"/>'
                        f'<w:ind w:firstLine="0"/><w:jc w:val="left"/></w:pPr>{self.runs(txt, size=size, i=True)}</w:p>')
                return f"<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc>{tcpr}{para}</w:tc></w:tr>"
            xml, col = [], 0
            for c in cells:
                text, span = (c if isinstance(c, tuple) else (c, 1))
                width = sum(widths[col:col + span])
                align = "center" if span > 1 else aligns[col]
                # in multi-row headers, underline spanning group labels
                bottom = last_header or (header and span > 1)
                xml.append(cell(text, width, align, bottom=bottom, top_rule=rule_above, bold=header, span=span,
                                keep=keep))
                col += span
            trpr = '<w:trPr><w:cantSplit/>' + ('<w:tblHeader/>' if header else '') + '</w:trPr>'
            return f"<w:tr>{trpr}{''.join(xml)}</w:tr>"

        trs = []
        for k, hr in enumerate(header):
            trs.append(row(hr, header=True, last_header=(k == len(header) - 1)))
        for k, r in enumerate(rows):
            trs.append(row(r, rule_above=(k in group_rules), keep=(k < len(rows) - 1)))
        self.body.append(f"<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>")
        if note:
            self.para(self.runs(note, size=16), None,
                      '<w:spacing w:before="40" w:after="200" w:line="200" w:lineRule="atLeast"/>'
                      '<w:ind w:firstLine="0"/><w:jc w:val="both"/>')
        else:
            self.para("", None, '<w:spacing w:before="0" w:after="0" w:line="120" w:lineRule="exact"/>')
        self.after_heading = True

    def figure(self, key, png: Path, width_in, caption, height_in=None):
        from PIL import Image
        self.media += 1
        self.rid += 1
        rid = f"rId{self.rid}"
        name = f"image{self.media}.png"
        shutil.copy(png, self.dir / "word" / "media" / name)
        self.rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                         f'relationships/image" Target="media/{name}"/>')
        w, h = Image.open(png).size
        if height_in is None:
            height_in = width_in * h / w
        cx, cy = int(width_in * EMU_PER_IN), int(height_in * EMU_PER_IN)
        drawing = (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
                   f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{self.media}" name="Figure {self.media}"/>'
                   f'<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                   f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                   f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{self.media}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
                   f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                   f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                   f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData>'
                   f'</a:graphic></wp:inline></w:drawing></w:r>')
        self.para(drawing, "image", '<w:keepNext/><w:spacing w:before="160" w:after="60"/>')
        self.caption("Figure", key, caption)
        self.after_heading = True

    def equation(self, omml, number):
        xml = (f'<w:r><w:tab/></w:r><m:oMath>{omml}</m:oMath>'
               f'<w:r><w:tab/></w:r><w:r>{self.t(f"({number})")}</w:r>')
        self.para(xml, "equation", '<w:spacing w:before="80" w:after="80"/>')

    def raw(self, xml):
        self.body.append(xml)

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ------------------------------------------------------------------ output
    def save(self, out_path: Path, sect_pr: str):
        doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document {W_NS}><w:body>'
               + "".join(self.body) + sect_pr + "</w:body></w:document>")
        (self.dir / "word" / "document.xml").write_text(doc, encoding="utf8")
        rels_p = self.dir / "word" / "_rels" / "document.xml.rels"
        rels = rels_p.read_text(encoding="utf8")
        rels = rels.replace("</Relationships>", "".join(self.rels) + "</Relationships>")
        rels_p.write_text(rels, encoding="utf8")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.exists():
            out_path.unlink()
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            ct = self.dir / "[Content_Types].xml"
            z.write(ct, "[Content_Types].xml")
            for f in sorted(self.dir.rglob("*")):
                if f.is_file() and f != ct:
                    z.write(f, f.relative_to(self.dir).as_posix())


# ---------------------------------------------------------------------- OMML helpers
def mr(text, plain=False):
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ""
    return f'<m:r>{sty}<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr><m:t xml:space="preserve">{escape(text)}</m:t></m:r>'


def mfrac(num, den):
    return f"<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>"


def msub(base, sub):
    return f"<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>"


def msubsup(base, sub, sup):
    return f"<m:sSubSup><m:e>{base}</m:e><m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>"


def mparen(inner, beg="(", end=")"):
    return (f'<m:d><m:dPr><m:begChr m:val="{escape(beg)}"/><m:endChr m:val="{escape(end)}"/></m:dPr>'
            f"<m:e>{inner}</m:e></m:d>")


def msum(sub, sup, body):
    return (f'<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
            f"<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>")
