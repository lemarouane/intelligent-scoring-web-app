# ============================================================
# BOA INTELLIGENT CREDIT SCORING – PDF EXPORT
# ============================================================

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

BLUE    = colors.HexColor("#003366")
GOLD    = colors.HexColor("#D4AF37")
GREEN   = colors.HexColor("#0E9F6E")
RED_C   = colors.HexColor("#DC2626")
GRAY    = colors.HexColor("#64748B")
LIGHT   = colors.HexColor("#F5F7FA")


def _styles():
    ss = getSampleStyleSheet()
    extra = {
        "TitleMain": ParagraphStyle(
            "TitleMain", parent=ss["Title"],
            fontSize=18, textColor=BLUE, spaceAfter=4,
        ),
        "SubTitle": ParagraphStyle(
            "SubTitle", parent=ss["Normal"],
            fontSize=10, textColor=GOLD, spaceAfter=12, alignment=TA_CENTER,
        ),
        "SectionHead": ParagraphStyle(
            "SectionHead", parent=ss["Heading2"],
            fontSize=12, textColor=BLUE, spaceBefore=12, spaceAfter=4,
            borderPad=4,
        ),
        "BodyText": ParagraphStyle(
            "BodyText", parent=ss["Normal"],
            fontSize=9, leading=14, textColor=colors.black, spaceAfter=4,
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader", parent=ss["Normal"],
            fontSize=8, textColor=colors.white, fontName="Helvetica-Bold",
        ),
        "Footer": ParagraphStyle(
            "Footer", parent=ss["Normal"],
            fontSize=7, textColor=GRAY, alignment=TA_CENTER,
        ),
    }
    for name, style in extra.items():
        try:
            ss.add(style)
        except KeyError:
            pass  # style with this name already exists in the base sheet
    return ss

def generate_pdf(
    categorie: str,
    final_score: float,
    risk_class: str,
    decision: str,
    prob_default: str,
    rows: list,
    ia_analysis: str = "",
) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    s = _styles()
    story = []

    # ── Header
    story.append(Paragraph("BANK OF AFRICA", s["TitleMain"]))
    story.append(Paragraph(
        "Système Intelligent de Scoring de Crédit Professionnel", s["SubTitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD))
    story.append(Spacer(1, 0.4*cm))

    # ── Meta
    meta = [
        ["Date d'analyse :", datetime.now().strftime("%d/%m/%Y %H:%M")],
        ["Catégorie client :", categorie],
        ["Score Final :", f"{final_score:.2f} / 100"],
        ["Classe de risque :", f"Classe {risk_class}"],
        ["Décision :", decision],
        
    ]
    t = Table(meta, colWidths=[5*cm, 10*cm])
    t.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,0), (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",   (0,0), (0,-1),  BLUE),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT, colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.25, colors.HexColor("#E2E8F0")),
        ("PADDING",     (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    # ── Score table
    story.append(Paragraph("Détail des critères de scoring", s["SectionHead"]))
    header = ["Critère", "Poids (%)", "Score Partiel", "Score Pondéré"]
    data   = [header] + [
        [r["label"], f"{r['poids']}%", f"{r['partial']}/100", f"{r['weighted']}"]
        for r in rows
    ]
    st2 = Table(data, colWidths=[7*cm, 2.5*cm, 3*cm, 3*cm])
    st2.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), BLUE),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT, colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.25, colors.HexColor("#E2E8F0")),
        ("PADDING",     (0,0), (-1,-1), 5),
    ]))
    story.append(st2)
    story.append(Spacer(1, 0.5*cm))

    # ── IA Analysis
    if ia_analysis:
        story.append(Paragraph("Analyse Intelligence Artificielle", s["SectionHead"]))
        for line in ia_analysis.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.2*cm))
                continue
            if line.startswith("**") and line.endswith("**"):
                line = f"<b>{line[2:-2]}</b>"
            elif line.startswith("#"):
                line = f"<b>{line.lstrip('#').strip()}</b>"
            story.append(Paragraph(line, s["BodyText"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    story.append(Paragraph(
        "Document confidentiel – Usage interne – Bank of Africa © 2026",
        s["Footer"],
    ))

    doc.build(story)
    return buffer.getvalue()