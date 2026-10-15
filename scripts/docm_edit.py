"""Sửa chữ trong document.xml của file .docm mà không đụng style, trường EndNote hay SEQ/REF.

Các thao tác:
  - van_ban(p): chữ hiển thị của đoạn (bỏ mã trường, giữ kết quả trường);
  - thay(p, cu, moi): thay một đoạn chữ nằm hoàn toàn trong các run thường (ngoài trường) của đoạn;
  - chen_sau(p, moc, cac_phan): chèn run mới ngay sau đoạn chữ `moc`, mỗi phần (chữ, tô_vàng) chép định dạng
    của run chứa `moc`;
  - xoa_truong(p, k): xóa trường EndNote cấp ngoài thứ k (tính từ 0) của đoạn, kể cả kết quả hiển thị;
  - doan_moi_sau(p, mau, cac_phan): thêm đoạn mới sau p, chép pPr của đoạn mẫu `mau`.
"""
import copy

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def _runs_thuong(p):
    """Các phần tử w:t nằm trong run thường (không thuộc trường nào) của đoạn, theo thứ tự."""
    out, sau = [], []
    for el in p.iter():
        if el.tag == W + "fldChar":
            t = el.get(W + "fldCharType")
            if t == "begin":
                sau.append("instr")
            elif t == "separate" and sau:
                sau[-1] = "result"
            elif t == "end" and sau:
                sau.pop()
        elif el.tag == W + "t" and not sau:
            out.append(el)
    return out


def van_ban(p):
    out, sau = [], []
    for el in p.iter():
        if el.tag == W + "fldChar":
            t = el.get(W + "fldCharType")
            if t == "begin":
                sau.append("instr")
            elif t == "separate" and sau:
                sau[-1] = "result"
            elif t == "end" and sau:
                sau.pop()
        elif all(x == "result" for x in sau):
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag == W + "tab":
                out.append("\t")
    return "".join(out)


def _dat(t, chu):
    t.text = chu
    t.set(XML_SPACE, "preserve")


def thay(p, cu, moi):
    """Thay `cu` (phải nằm trọn trong các w:t thường liên tiếp) bằng `moi`. Báo lỗi nếu không thấy đúng 1 lần."""
    ts = _runs_thuong(p)
    chu = "".join(t.text or "" for t in ts)
    n = chu.count(cu)
    if n != 1:
        raise ValueError(f"tìm thấy {n} lần: {cu[:60]!r}")
    a = chu.index(cu)
    b = a + len(cu)
    vt = 0
    dau = None
    for t in ts:
        s = t.text or ""
        lo, hi = vt, vt + len(s)
        if hi > a and lo < b:
            giu_truoc = s[: max(0, a - lo)]
            giu_sau = s[max(0, b - lo):] if b < hi else ""
            if dau is None:
                _dat(t, giu_truoc + moi + giu_sau)
                dau = t
            else:
                _dat(t, giu_sau)
        elif dau is None and lo == a == hi and not cu:
            pass
        vt = hi
    if dau is None:
        raise ValueError("không xác định được run cần thay")


def _run_chua(p, moc):
    ts = _runs_thuong(p)
    chu = "".join(t.text or "" for t in ts)
    if chu.count(moc) != 1:
        raise ValueError(f"mốc xuất hiện {chu.count(moc)} lần: {moc[:60]!r}")
    het = chu.index(moc) + len(moc)
    vt = 0
    for t in ts:
        s = t.text or ""
        if vt < het <= vt + len(s):
            return t, het - vt
        vt += len(s)
    raise ValueError("không thấy run chứa mốc")


def _run_moi(r_mau, chu, vang=False, dam=False):
    r = etree.Element(W + "r")
    rpr = r_mau.find(W + "rPr")
    if rpr is not None:
        rpr = copy.deepcopy(rpr)
        for tag in ("highlight",):
            for x in rpr.findall(W + tag):
                rpr.remove(x)
        r.append(rpr)
    else:
        rpr = None
    if vang or dam:
        if rpr is None:
            rpr = etree.SubElement(r, W + "rPr")
        if dam:
            b = etree.SubElement(rpr, W + "b")
        if vang:
            h = etree.SubElement(rpr, W + "highlight")
            h.set(W + "val", "yellow")
    t = etree.SubElement(r, W + "t")
    _dat(t, chu)
    return r


def chen_sau(p, moc, cac_phan):
    """Chèn các run mới ngay sau `moc`. cac_phan: danh sách (chữ, tô_vàng)."""
    t, cat = _run_chua(p, moc)
    r = t.getparent()
    s = t.text or ""
    _dat(t, s[:cat])
    sau = s[cat:]
    vi_tri = r
    for chu, vang in cac_phan:
        moi = _run_moi(r, chu, vang)
        vi_tri.addnext(moi)
        vi_tri = moi
    if sau:
        con = _run_moi(r, sau)
        vi_tri.addnext(con)


def xoa_truong(p, k):
    """Xóa trường cấp ngoài thứ k của đoạn: mọi run từ fldChar begin đến fldChar end (cùng cấp)."""
    runs = [r for r in p if r.tag == W + "r"]
    muc = 0
    dem = -1
    bat_dau = None
    for r in runs:
        fc = r.find(W + "fldChar")
        if fc is not None:
            t = fc.get(W + "fldCharType")
            if t == "begin":
                if muc == 0:
                    dem += 1
                    if dem == k:
                        bat_dau = r
                muc += 1
            elif t == "end":
                muc -= 1
                if muc == 0 and dem == k and bat_dau is not None:
                    xoa, dang = [], False
                    for x in list(p):
                        if x is bat_dau:
                            dang = True
                        if dang:
                            xoa.append(x)
                        if x is r:
                            break
                    for x in xoa:
                        p.remove(x)
                    return
    raise ValueError(f"không có trường thứ {k}")


def doan_moi_sau(p, mau, cac_phan):
    """Thêm đoạn mới ngay sau p; pPr chép từ đoạn mẫu; định dạng run chép từ run chữ đầu tiên của đoạn mẫu."""
    moi = etree.Element(W + "p")
    ppr = mau.find(W + "pPr")
    if ppr is not None:
        moi.append(copy.deepcopy(ppr))
    r_mau = next(r for r in mau.iter(W + "r") if r.find(W + "t") is not None)
    for phan in cac_phan:
        chu, vang, dam = (phan + (False,))[:3] if len(phan) == 2 else phan
        moi.append(_run_moi(r_mau, chu, vang, dam))
    p.addnext(moi)
    return moi
