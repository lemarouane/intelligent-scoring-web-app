# ============================================================
# BOA INTELLIGENT CREDIT SCORING – REPORT GENERATOR
# ============================================================
"""
Builds the structured dossier (client category, raw inputs, partial
scores, weighted scores, final score, risk class, decision) that is
sent to services/llm_service.py, and assembles the AI's sectioned
response into a clean report object used by the dashboard and the
export services (PDF / Word / Excel).
"""

from datetime import datetime
from utils.constants import RISK_CLASSES


# ─── SECTIONS EXPECTED FROM THE AI ──────────────────────────
REPORT_SECTIONS = [
    "Résumé Exécutif",
    "Analyse des Critères BOA",
    "Analyse des Critères Spécifiques",
    "Forces du Dossier",
    "Faiblesses du Dossier",
    "Appréciation du Risque",
    "Recommandation",
    "Décision Finale",
]


def build_dossier_payload(
    categorie: str,
    boa_inputs: dict,
    specific_inputs: dict,
    score_summary: dict,
) -> dict:
    """
    Assembles everything the LLM needs to produce a grounded,
    professional credit analysis. This is the single source of
    truth passed to services/llm_service.py.
    """
    final_score = score_summary.get("final", 0)
    risk_class  = _risk_class_from_score(final_score)
    risk_info   = RISK_CLASSES.get(risk_class, RISK_CLASSES["D"])

    rows = score_summary.get("rows", [])

    return {
        "generated_at":  datetime.now().strftime("%d/%m/%Y %H:%M"),
        "categorie":     categorie,
        "boa_inputs":    boa_inputs,
        "specific_inputs": specific_inputs,
        "criteres": [
            {
                "label":    r["label"],
                "poids":    r["poids"],
                "score_partiel":  r["partial"],
                "score_pondere":  r["weighted"],
            }
            for r in rows
        ],
        "score_final":   final_score,
        "classe_risque": risk_class,
        "libelle_risque": risk_info["label"],
        "probabilite_defaut": risk_info["prob_default"],
        "decision_recommandee": risk_info["decision"],
    }


def _risk_class_from_score(score: float) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    return "D"


# ─── PARSING THE AI RESPONSE INTO SECTIONS ──────────────────

def parse_ai_sections(raw_text: str) -> dict:
    """
    Splits the AI's free-text markdown response into the 8 expected
    sections, matching on heading text (numbered or not, '##' or
    plain). Falls back gracefully if a section is missing.
    """
    sections = {name: "" for name in REPORT_SECTIONS}
    if not raw_text:
        return sections

    lines = raw_text.splitlines()
    current = None
    buffer: list[str] = []

    def flush():
        if current and buffer:
            sections[current] = "\n".join(buffer).strip()

    for line in lines:
        stripped = line.strip().lstrip("#").strip()

        matched_section = None
        for name in REPORT_SECTIONS:
            if name.lower() in stripped.lower():
                matched_section = name
                break

        if matched_section:
            flush()
            current = matched_section
            buffer = []
        elif current:
            buffer.append(line)

    flush()
    return sections


def build_report_object(dossier_payload: dict, ai_raw_text: str) -> dict:
    """
    Final report object combining the quantitative dossier with the
    AI's qualitative analysis, ready for the dashboard and exporters.
    """
    return {
        "dossier": dossier_payload,
        "sections": parse_ai_sections(ai_raw_text),
        "raw_analysis": ai_raw_text,
    }