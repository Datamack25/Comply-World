# -*- coding: utf-8 -*-
"""Exports PDF (ReportLab), Word (python-docx) et Excel (openpyxl) aux couleurs du cabinet."""
import io
from datetime import date

import pandas as pd

from .config import ROOT, BRAND, FOOTER_LINE, DISCLAIMER, COLORS

FONT_DIR = ROOT / "assets" / "fonts"


# ============================================================================ PDF
def _register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    try:
        pdfmetrics.getFont("CW")
        return "CW", "CW-Bold"
    except KeyError:
        pass
    try:
        pdfmetrics.registerFont(TTFont("CW", str(FONT_DIR / "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("CW-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
        return "CW", "CW-Bold"
    except Exception:
        return "Helvetica", "Helvetica-Bold"


def to_pdf(title: str, subtitle: str, meta: dict, sections: list[tuple], landscape_mode: bool = True) -> bytes:
    """sections : liste de (titre, contenu) où contenu est un DataFrame, une chaîne ou une liste de chaînes."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak)

    f, fb = _register_fonts()
    navy, copper = colors.HexColor(COLORS["navy"]), colors.HexColor(COLORS["copper"])
    size = landscape(A4) if landscape_mode else A4
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=size, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=24 * mm, bottomMargin=18 * mm,
                            title=title, author=BRAND)
    st_h1 = ParagraphStyle("h1", fontName=fb, fontSize=17, leading=21, textColor=navy, spaceAfter=4)
    st_sub = ParagraphStyle("sub", fontName=f, fontSize=10, leading=13, textColor=colors.HexColor(COLORS["muted"]), spaceAfter=8)
    st_h2 = ParagraphStyle("h2", fontName=fb, fontSize=12, leading=15, textColor=navy, spaceBefore=10, spaceAfter=5)
    st_p = ParagraphStyle("p", fontName=f, fontSize=9, leading=12, textColor=colors.HexColor(COLORS["ink"]))
    st_cell = ParagraphStyle("cell", fontName=f, fontSize=7.2, leading=9)
    st_head = ParagraphStyle("head", fontName=fb, fontSize=7.4, leading=9, textColor=colors.white)

    def esc(x):
        s = "" if (x is None or (isinstance(x, float) and pd.isna(x))) else str(x)
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    story = [Paragraph(esc(title), st_h1), Paragraph(esc(subtitle), st_sub)]
    if meta:
        mt = Table([[Paragraph(f"<b>{esc(k)}</b>", st_p), Paragraph(esc(v), st_p)] for k, v in meta.items()],
                   colWidths=[50 * mm, size[0] - 28 * mm - 50 * mm])
        mt.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1EBE4")),
                                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor(COLORS["line"])),
                                ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story += [mt, Spacer(1, 6)]

    avail = size[0] - 28 * mm
    for i, (h, content) in enumerate(sections):
        if h == "__pagebreak__":
            story.append(PageBreak())
            continue
        story.append(Paragraph(esc(h), st_h2))
        if isinstance(content, pd.DataFrame):
            d = content.copy()
            if d.empty:
                story.append(Paragraph("Aucune donnée.", st_p))
                continue
            lens = [min(60.0, max(5.0, float(d[c].astype(str).str.len().mean()), len(str(c)) * 0.9)) for c in d.columns]
            widths = [avail * l / sum(lens) for l in lens]
            mn = 19 * mm
            small = [i for i, w in enumerate(widths) if w < mn]
            if small:
                rest = avail - mn * len(small)
                big = sum(lens[i] for i in range(len(lens)) if i not in small)
                widths = [mn if i in small else rest * lens[i] / big for i in range(len(lens))]
            data = [[Paragraph(esc(c), st_head) for c in d.columns]]
            def cell(v):
                sv = esc(v)
                if sv.startswith("http"):
                    return Paragraph(f'<link href="{sv}" color="#B8743A"><u>Lien officiel</u></link>', st_cell)
                return Paragraph(sv, st_cell)
            for _, row in d.iterrows():
                data.append([cell(v) for v in row.values])
            t = Table(data, colWidths=widths, repeatRows=1)
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), navy),
                                   ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F7FA")]),
                                   ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor(COLORS["line"])),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
            story.append(t)
        elif isinstance(content, dict) and "flow" in content:
            steps = content["flow"]
            st_fn = ParagraphStyle("fn", fontName=fb, fontSize=6.8, leading=8, textColor=copper)
            st_ft = ParagraphStyle("ft", fontName=fb, fontSize=8.6, leading=10.5, textColor=navy)
            st_fa = ParagraphStyle("fa", fontName=fb, fontSize=7.2, leading=9, textColor=colors.HexColor(COLORS["navy2"]))
            st_fd = ParagraphStyle("fd", fontName=f, fontSize=7, leading=8.8, textColor=colors.HexColor(COLORS["muted"]))
            st_arrow = ParagraphStyle("ar", fontName=fb, fontSize=14, leading=16, textColor=copper, alignment=1)
            row, widths = [], []
            n = len(steps)
            box_w = (avail - (n - 1) * 7 * mm) / n
            for i, (e, a, dsc) in enumerate(steps, 1):
                if i > 1:
                    row.append(Paragraph("→", st_arrow)); widths.append(7 * mm)
                row.append([Paragraph(f"ÉTAPE {i}", st_fn), Paragraph(esc(e), st_ft), Paragraph(esc(a), st_fa), Paragraph(esc(dsc), st_fd)])
                widths.append(box_w)
            t = Table([row], colWidths=widths)
            style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
            for k in range(0, len(row), 2):
                style += [("BOX", (k, 0), (k, 0), 0.5, colors.HexColor(COLORS["line"])),
                          ("LINEABOVE", (k, 0), (k, 0), 2.2, navy), ("VALIGN", (k, 0), (k, 0), "TOP"),
                          ("BACKGROUND", (k, 0), (k, 0), colors.white)]
            t.setStyle(TableStyle(style))
            story.append(t)
        elif isinstance(content, (list, tuple)):
            for line in content:
                story.append(Paragraph("• " + esc(line), st_p))
        else:
            story.append(Paragraph(esc(content), st_p))

    def deco(canvas, doc_):
        w, hgt = size
        canvas.saveState()
        canvas.setFillColor(navy)
        canvas.rect(0, hgt - 15 * mm, w, 15 * mm, fill=1, stroke=0)
        canvas.setFillColor(copper)
        canvas.rect(0, hgt - 15.8 * mm, w, 0.8 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont(fb, 11)
        canvas.drawString(14 * mm, hgt - 9.5 * mm, BRAND.upper())
        canvas.setFont(f, 8)
        canvas.drawRightString(w - 14 * mm, hgt - 9.5 * mm, f"Document généré le {date.today().strftime('%d/%m/%Y')}")
        canvas.setFillColor(colors.HexColor(COLORS["muted"]))
        canvas.setFont(f, 6.6)
        canvas.drawString(14 * mm, 10 * mm, FOOTER_LINE)
        canvas.drawString(14 * mm, 6.5 * mm, DISCLAIMER[:190] + ("…" if len(DISCLAIMER) > 190 else ""))
        canvas.drawRightString(w - 14 * mm, 10 * mm, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=deco, onLaterPages=deco)
    return buf.getvalue()


# ============================================================================ WORD
def to_docx(title: str, subtitle: str, meta: dict, sections: list[tuple]) -> bytes:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.shared import Pt, RGBColor, Cm
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def shade(cell, hex_):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_.lstrip("#"))
        tcPr.append(shd)

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(1.6))
    style = doc.styles["Normal"]
    style.font.name = "Calibri"; style.font.size = Pt(9.5)
    navy = RGBColor.from_string(COLORS["navy"].lstrip("#"))

    hp = sec.header.paragraphs[0]
    r = hp.add_run(BRAND.upper()); r.bold = True; r.font.color.rgb = navy; r.font.size = Pt(9)
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run(FOOTER_LINE + "\n" + DISCLAIMER); fr.font.size = Pt(7); fr.font.color.rgb = RGBColor(0x5B, 0x64, 0x78)

    h = doc.add_heading(title, level=0)
    for run in h.runs:
        run.font.color.rgb = navy
    p = doc.add_paragraph(subtitle); p.runs[0].italic = True
    if meta:
        t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"
        for k, v in meta.items():
            c = t.add_row().cells
            c[0].text, c[1].text = str(k), str(v)
            shade(c[0], "#F1EBE4")
    for hd, content in sections:
        if hd == "__pagebreak__":
            doc.add_page_break(); continue
        hh = doc.add_heading(hd, level=2)
        for run in hh.runs:
            run.font.color.rgb = navy
        if isinstance(content, pd.DataFrame):
            d = content.fillna("")
            t = doc.add_table(rows=1, cols=len(d.columns)); t.style = "Table Grid"
            for i, c in enumerate(d.columns):
                cell = t.rows[0].cells[i]; cell.text = str(c); shade(cell, COLORS["navy"])
                for rr in cell.paragraphs[0].runs:
                    rr.font.bold = True; rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); rr.font.size = Pt(8)
            for _, row in d.iterrows():
                cells = t.add_row().cells
                for i, v in enumerate(row.values):
                    cells[i].text = str(v)
                    for rr in cells[i].paragraphs[0].runs:
                        rr.font.size = Pt(8)
        elif isinstance(content, dict) and "flow" in content:
            steps = content["flow"]
            t = doc.add_table(rows=1, cols=len(steps)); t.style = "Table Grid"
            for i, (e, a, dsc) in enumerate(steps):
                c = t.rows[0].cells[i]
                c.text = ""
                p0 = c.paragraphs[0]; r0 = p0.add_run(f"Étape {i + 1}" + (" →" if i < len(steps) - 1 else "")); r0.font.size = Pt(7); r0.bold = True
                r0.font.color.rgb = RGBColor.from_string(COLORS["copper"].lstrip("#"))
                p1 = c.add_paragraph(); r1 = p1.add_run(e); r1.bold = True; r1.font.size = Pt(9); r1.font.color.rgb = navy
                p2 = c.add_paragraph(); r2 = p2.add_run(a); r2.font.size = Pt(8); r2.bold = True
                p3 = c.add_paragraph(); r3 = p3.add_run(dsc); r3.font.size = Pt(8)
        elif isinstance(content, (list, tuple)):
            for line in content:
                doc.add_paragraph(str(line), style="List Bullet")
        else:
            doc.add_paragraph(str(content))
    out = io.BytesIO(); doc.save(out)
    return out.getvalue()


# ============================================================================ EXCEL
def to_xlsx(sheets: dict) -> bytes:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as xw:
        for name, df in sheets.items():
            sname = name[:31]
            df.to_excel(xw, sheet_name=sname, index=False)
            ws = xw.sheets[sname]
            for c in ws[1]:
                c.font = Font(bold=True, color="FFFFFF")
                c.fill = PatternFill("solid", fgColor=COLORS["navy"].lstrip("#"))
                c.alignment = Alignment(wrap_text=True, vertical="top")
            for i, col in enumerate(df.columns, 1):
                width = min(60, max(10, int(df[col].astype(str).str.len().quantile(0.9) if len(df) else 10) + 2, len(str(col)) + 2))
                ws.column_dimensions[get_column_letter(i)].width = width
                for cell in ws[get_column_letter(i)][1:]:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
            ws.freeze_panes = "A2"
    return out.getvalue()


def to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")
