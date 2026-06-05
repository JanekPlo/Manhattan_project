#!/usr/bin/env python3
"""Generuje sformatowany plik .docx ze sprawozdania w formacie Markdown.

Obsługuje: nagłówki (#, ##, ###), akapity z pogrubieniem (**...**), listy
punktowane i numerowane, tabele Markdown (| ... |) oraz bloki kodu (```).

Formatowanie pracy:
- czcionka tekstu: Times New Roman 12, interlinia 1.5, justowanie
- marginesy 2.5 cm, numeracja stron w stopce
- kod: Consolas 10

Użycie:
    pip install python-docx
    python3 build_docx.py            # sprawozdanie.md -> sprawozdanie.docx
"""
import os
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Cm, RGBColor

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "sprawozdanie.md")
OUT = os.path.join(BASE, "sprawozdanie.docx")


def set_cell_bg(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def add_page_numbers(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fldChar1 = OxmlElement("w:fldChar"); fldChar1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar"); fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1); run._r.append(instr); run._r.append(fldChar2)


def add_runs_with_bold(paragraph, text):
    """Dodaje tekst, interpretując **pogrubienie** oraz `kod`."""
    parts = re.split(r"(\*\*.+?\*\*|`.+?`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = paragraph.add_run(part[2:-2]); r.bold = True
        elif part.startswith("`") and part.endswith("`"):
            r = paragraph.add_run(part[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(10)
        else:
            paragraph.add_run(part)


def style_normal(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    pf = st.paragraph_format
    pf.line_spacing = 1.5
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_after = Pt(6)


def _center(doc, text, size=12, bold=False, italic=False, before=0, after=0, caps=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text.upper() if caps else text)
    r.font.name = "Times New Roman"; r.font.size = Pt(size)
    r.bold = bold; r.italic = italic
    return p


def add_title_page(doc):
    """Strona tytułowa z miejscami do uzupełnienia (……)."""
    _center(doc, "……………………………………………………………", size=12, before=0, after=2)
    _center(doc, "(nazwa uczelni / wydziału)", size=10, italic=True, after=30)

    _center(doc, "Informatyka w zarządzaniu", size=14, after=2)
    _center(doc, "57 MC – FIR", size=11, italic=True, after=70)

    _center(doc, "SPRAWOZDANIE Z PROJEKTU", size=13, bold=True, after=10)
    _center(doc, "Projekt i implementacja relacyjnej bazy danych "
                 "systemu obsługi zamówień firmy usługowej "
                 "oraz jej odtworzenie w aplikacji no-code (Knack.com)",
            size=17, bold=True, after=80)

    _center(doc, "Autor: ………………………………………………", size=12, after=6)
    _center(doc, "Nr indeksu: ……………………        Grupa: ……………………", size=12, after=6)
    _center(doc, "Kierunek / tryb studiów: ………………………………", size=12, after=40)

    _center(doc, "Prowadzący: ………………………………………………", size=12, after=80)

    _center(doc, "………………………………, rok akademicki 2025/2026", size=12, after=2)
    _center(doc, "(miejscowość)", size=10, italic=True)

    # twardy podział strony – treść zaczyna się na nowej stronie
    doc.add_page_break()


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    out = sys.argv[2] if len(sys.argv) > 2 else OUT
    with open(src, encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(2.5)
        s.different_first_page_header_footer = True   # bez numeru na stronie tytułowej
        add_page_numbers(s)
    style_normal(doc)
    add_title_page(doc)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # blok kodu
        if line.strip().startswith("```"):
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.left_indent = Cm(0.5)
            r = p.add_run("\n".join(code))
            r.font.name = "Consolas"; r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            continue

        # tabela Markdown
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            tbl = doc.add_table(rows=1, cols=len(header))
            tbl.style = "Table Grid"
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for j, h in enumerate(header):
                cell = tbl.rows[0].cells[j]
                cell.paragraphs[0].text = ""
                run = cell.paragraphs[0].add_run(h.replace("**", "")); run.bold = True
                run.font.size = Pt(10); run.font.name = "Times New Roman"
                set_cell_bg(cell, "D9E2F3")
            for row in rows:
                cells = tbl.add_row().cells
                for j in range(len(header)):
                    val = row[j] if j < len(row) else ""
                    cells[j].paragraphs[0].text = ""
                    add_runs_with_bold(cells[j].paragraphs[0], val)
                    for rn in cells[j].paragraphs[0].runs:
                        rn.font.size = Pt(10); rn.font.name = "Times New Roman"
            doc.add_paragraph()
            continue

        # nagłówki
        if line.startswith("### "):
            h = doc.add_heading(level=3); add_runs_with_bold(h, line[4:])
        elif line.startswith("## "):
            h = doc.add_heading(level=2); add_runs_with_bold(h, line[3:])
        elif line.startswith("# "):
            h = doc.add_heading(level=1); add_runs_with_bold(h, line[2:])
        elif line.strip() == "---":
            pass
        elif re.match(r"^\s*[-*] ", line):
            p = doc.add_paragraph(style="List Bullet")
            add_runs_with_bold(p, re.sub(r"^\s*[-*] ", "", line))
        elif re.match(r"^\s*\d+\. ", line):
            p = doc.add_paragraph(style="List Number")
            add_runs_with_bold(p, re.sub(r"^\s*\d+\. ", "", line))
        elif line.startswith("> "):
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8)
            add_runs_with_bold(p, line[2:]);
            for rn in p.runs: rn.italic = True
        elif line.strip() == "":
            pass
        else:
            p = doc.add_paragraph(); add_runs_with_bold(p, line)
        i += 1

    doc.save(out)
    print(f"Zapisano: {out}")


if __name__ == "__main__":
    main()
