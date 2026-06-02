#!/usr/bin/env python3
"""Generuje sformatowany plik .docx z case-study-ai-logistyka.md.

Formatowanie zgodne z wymaganiami pracy:
- czcionka: Times New Roman 12
- interlinia: 1.5
- tekst wyjustowany
- marginesy: 2.5 cm
- numeracja stron (w stopce)

Użycie:
    pip install python-docx
    python build_docx.py            # czyta case-study-ai-logistyka.md
    python build_docx.py plik.md out.docx
"""
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Cm, RGBColor

FONT_NAME = "Times New Roman"
FONT_SIZE = 12


def set_base_style(document):
    """Czcionka, rozmiar, interlinia 1.5 i justowanie dla stylu Normal."""
    style = document.styles["Normal"]
    style.font.name = FONT_NAME
    style.font.size = Pt(FONT_SIZE)
    # zapewnij czcionkę także dla znaków wschodnioazjatyckich/complex
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), FONT_NAME)
    rfonts.set(qn("w:hAnsi"), FONT_NAME)
    rfonts.set(qn("w:cs"), FONT_NAME)
    pf = style.paragraph_format
    pf.line_spacing = 1.5
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_after = Pt(6)


def set_margins(document):
    for section in document.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)


def add_page_numbers(document):
    """Wstawia pole numeru strony wyśrodkowane w stopce."""
    for section in document.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        fld_begin = OxmlElement("w:fldChar")
        fld_begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = "PAGE"
        fld_end = OxmlElement("w:fldChar")
        fld_end.set(qn("w:fldCharType"), "end")
        run._r.append(fld_begin)
        run._r.append(instr)
        run._r.append(fld_end)


def add_runs_with_bold(paragraph, text):
    """Dodaje tekst do akapitu, interpretując **pogrubienie**."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not part:
            continue
        run = paragraph.add_run(part)
        if i % 2 == 1:  # fragmenty pomiędzy ** **
            run.bold = True


def render_table(document, rows):
    """rows: lista list komórek (już bez znaków |)."""
    if not rows:
        return
    # pomiń wiersz separatora markdown (|---|---|)
    body = [r for r in rows if not re.match(r"^\s*:?-{2,}", r[0])]
    if not body:
        return
    cols = max(len(r) for r in body)
    table = document.add_table(rows=0, cols=cols)
    table.style = "Light Grid Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(body):
        cells = table.add_row().cells
        for c_idx in range(cols):
            txt = row[c_idx] if c_idx < len(row) else ""
            cell_p = cells[c_idx].paragraphs[0]
            cell_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs_with_bold(cell_p, txt.strip())
            if r_idx == 0:  # nagłówek tabeli pogrubiony
                for run in cell_p.runs:
                    run.bold = True


def parse_markdown(document, lines):
    i = 0
    in_code = False
    code_buffer = []
    table_buffer = []

    def flush_table():
        if table_buffer:
            render_table(document, list(table_buffer))
            table_buffer.clear()

    def flush_code():
        if code_buffer:
            p = document.add_paragraph()
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run("\n".join(code_buffer))
            run.font.name = "Courier New"
            run.font.size = Pt(9)
            code_buffer.clear()

    while i < len(lines):
        raw = lines[i].rstrip("\n")
        stripped = raw.strip()

        # bloki kodu ```
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_table()
                in_code = True
            i += 1
            continue
        if in_code:
            code_buffer.append(raw)
            i += 1
            continue

        # tabele markdown
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            table_buffer.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # pusta linia
        if not stripped:
            i += 1
            continue

        # linia pozioma
        if re.match(r"^-{3,}$", stripped):
            i += 1
            continue

        # nagłówki
        if stripped.startswith("# "):
            h = document.add_heading(level=0)
            add_runs_with_bold(h, stripped[2:])
            i += 1
            continue
        if stripped.startswith("## "):
            h = document.add_heading(level=1)
            add_runs_with_bold(h, stripped[3:])
            i += 1
            continue
        if stripped.startswith("### "):
            h = document.add_heading(level=2)
            add_runs_with_bold(h, stripped[4:])
            i += 1
            continue

        # cytat / nota
        if stripped.startswith(">"):
            text = stripped.lstrip(">").strip()
            p = document.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.75)
            r0 = p.add_run("")
            add_runs_with_bold(p, text)
            for run in p.runs:
                run.italic = True
                run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue

        # listy punktowane / numerowane
        m_bullet = re.match(r"^[-*]\s+(.*)", stripped)
        m_num = re.match(r"^\d+\.\s+(.*)", stripped)
        if m_bullet:
            p = document.add_paragraph(style="List Bullet")
            add_runs_with_bold(p, m_bullet.group(1))
            i += 1
            continue
        if m_num:
            p = document.add_paragraph(style="List Number")
            add_runs_with_bold(p, m_num.group(1))
            i += 1
            continue

        # zwykły akapit
        p = document.add_paragraph()
        add_runs_with_bold(p, stripped)
        i += 1

    flush_table()
    flush_code()


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "case-study-ai-logistyka.md"
    out = sys.argv[2] if len(sys.argv) > 2 else "case-study-ai-logistyka.docx"

    with open(src, encoding="utf-8") as f:
        lines = f.readlines()

    document = Document()
    set_base_style(document)
    set_margins(document)
    add_page_numbers(document)
    parse_markdown(document, lines)
    document.save(out)
    print(f"Zapisano: {out}")


if __name__ == "__main__":
    main()
