#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 gesp_downloads/一级/Python 下的所有 PDF 提取文字、重新排版为干净可编辑的 Word (.docx)

思路: 用 PyMuPDF 按阅读顺序抽取文字，去掉 PDF 的错位版式，
      再按"正文 / 代码块 / 题目编号"结构化重排成 Word。
      （注: 此为文字版，PDF 里的图片/流程图不会被带入，如需原版图文请用"页面转图嵌入"方案。）

依赖:
    pip install pymupdf python-docx
用法:
    cd /Users/sean/gespWorkSpace/gesp
    python3 pdf_to_word.py
输出:
    gesp_downloads/一级/Python/docx/<原名>.docx
"""
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ 缺少依赖 PyMuPDF，请执行: python3 -m pip install pymupdf")
    sys.exit(1)
try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("❌ 缺少依赖 python-docx，请执行: python3 -m pip install python-docx")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "gesp_downloads" / "一级" / "Python"
OUT_DIR = SRC_DIR / "docx"

CJK_FONT = "宋体"           # 正文中文
CODE_FONT = "Courier New"   # 代码等宽

# 代码关键字/特征，用于判定某段文字是否为代码
CODE_HINTS = re.compile(
    r'(def |class |import |from \w+ import|print\(|for \w+ in|while |'
    r'if \w+|elif |else:|return |==|!=|>=|<=|->|//|#|^\s{2,}\S)'
)
# 题目编号：一、 1. 2) (3) 等
QUESTION_HEAD = re.compile(r'^\s*([一二三四五六七八九十]+、|\d+[.)\、])')


def is_code_block(text: str) -> bool:
    if not text.strip():
        return False
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    if CODE_HINTS.search(text) and (len(lines) >= 2 or any(l.startswith((" ", "\t")) for l in lines)):
        return True
    # 多行且普遍带前导空格 => 多半是代码/缩进内容
    indented = sum(1 for l in lines if l.startswith((" ", "\t")))
    if len(lines) >= 3 and indented >= max(2, len(lines) // 2):
        return True
    return False


def _set_run_font(run, name, size=None, bold=False):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:eastAsia'), name)
    rfonts.set(qn('w:ascii'), name)
    rfonts.set(qn('w:hAnsi'), name)
    if size:
        run.font.size = Pt(size)
    run.font.bold = bold


def _shade(paragraph, fill="F2F2F2"):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def add_code(text, doc):
    for line in text.splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Inches(0.15)
        _shade(p, "F2F2F2")
        run = p.add_run(line if line else " ")
        _set_run_font(run, CODE_FONT, size=9.5)


def set_default_font(doc, name, size):
    style = doc.styles['Normal']
    style.font.name = name
    style.font.size = Pt(size)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:eastAsia'), name)


def convert_one(pdf_path, docx_path):
    doc = Document()
    set_default_font(doc, CJK_FONT, 11)

    src = fitz.open(str(pdf_path))
    n_pages = len(src)
    buf = []

    def flush():
        if not buf:
            return
        chunk = "\n".join(buf)
        if is_code_block(chunk):
            add_code(chunk, doc)
        else:
            for ln in buf:
                ln = ln.rstrip()
                if not ln:
                    continue
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(ln)
                _set_run_font(run, CJK_FONT, 11)
                if QUESTION_HEAD.match(ln):
                    run.font.bold = True
        buf.clear()

    for pi, page in enumerate(src):
        # sort=True: 按阅读顺序输出，兼容性更好的多栏/双栏排版
        text = page.get_text("text", sort=True)
        for ln in text.splitlines():
            if ln.strip() == "":
                flush()
            else:
                buf.append(ln)
        flush()
        if pi < n_pages - 1:
            doc.add_page_break()
    doc.save(str(docx_path))
    src.close()


def main():
    if not SRC_DIR.exists():
        print(f"❌ 目录不存在: {SRC_DIR}（请先下载 PDF）")
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(SRC_DIR.glob("*.pdf"))
    if not pdfs:
        print("⚠️ 未在", SRC_DIR, "下找到任何 PDF")
        sys.exit(0)

    print(f"🔄 找到 {len(pdfs)} 个 PDF，开始提取文字生成 Word\n")
    ok, fail = 0, 0
    for i, pdf in enumerate(pdfs, 1):
        docx = OUT_DIR / (pdf.stem + ".docx")
        try:
            print(f"[{i}/{len(pdfs)}] {pdf.name} ...")
            convert_one(pdf, docx)
            kb = docx.stat().st_size / 1024
            print(f"   ✅ -> {docx.name} ({kb:.1f} KB)")
            ok += 1
        except Exception as e:
            print(f"   ❌ 失败: {pdf.name} - {e}")
            fail += 1
    print(f"\n🎉 完成：成功 {ok} 个，失败 {fail} 个\n📂 输出目录: {OUT_DIR}")


if __name__ == "__main__":
    main()
