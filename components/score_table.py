# ============================================================
# BOA INTELLIGENT CREDIT SCORING – SCORE TABLE COMPONENT
# ============================================================

# comment : import des bibliothèques streamlit et des helpers
import streamlit as st
# comment : import de la fonction score_color
from utils.helpers import score_color

# comment : fonction qui permet de rendre une ligne du tableau de score 
def _row_html(label: str, poids, partial, weighted, bg: str) -> str:
    #condition si le score partiel est None
    if partial is None:
        badge = '<span style="color:#94A3B8;font-size:0.78rem">—</span>'
        weighted_display = "—"
    #sinon le score partiel est non Null
    else:
        color = score_color(partial)
        badge = (
            f'<span style="background:{color};color:#fff;border-radius:999px;'
            f'padding:2px 8px;font-size:0.75rem;font-weight:600">{partial}/100</span>'
        )
        weighted_display = f"{weighted:.2f}"
    
    return f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1fr 1fr;gap:0.5rem;padding:0.5rem 1rem;background:{bg};border-bottom:1px solid #E2E8F0;font-size:0.82rem;align-items:center">
<span style="color:#1E293B;font-weight:500">{label}</span>
<span style="text-align:center;color:#64748B">{poids}%</span>
<span style="text-align:center">{badge}</span>
<span style="text-align:center;color:#003366;font-weight:600">{weighted_display}</span>
</div>
""".strip()

# comment : fonction qui permet de rendre le tableau de score
def render_score_table(rows: list[dict], total: float = None):
    header_html = """
<div style="display:grid;grid-template-columns:3fr 1fr 1fr 1fr;gap:0.5rem;padding:0.5rem 1rem;background:#003366;border-radius:8px 8px 0 0;font-size:0.78rem;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:0.04em">
<span>Critère</span>
<span style="text-align:center">Poids</span>
<span style="text-align:center">Score</span>
<span style="text-align:center">Pondéré</span>
</div>
""".strip()

    body_parts = []
    for i, r in enumerate(rows):
        bg = "#F8FAFC" if i % 2 == 0 else "#FFFFFF"
        body_parts.append(
            _row_html(r["label"], r["poids"], r.get("partial"), r.get("weighted"), bg)
        )
    body_html = "\n".join(body_parts)

    footer_html = ""
    if total is not None:
        footer_html = f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1fr 1fr;gap:0.5rem;padding:0.6rem 1rem;background:#EFF6FF;border-radius:0 0 8px 8px;border-top:2px solid #003366;font-size:0.85rem;font-weight:700;color:#003366">
<span>TOTAL EN COURS</span>
<span></span>
<span></span>
<span style="text-align:center">{total:.2f}</span>
</div>
""".strip()

    full_html = f"""
<div style="border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,51,102,0.07)">
{header_html}
{body_html}
{footer_html}
</div>
""".strip()

    st.markdown(full_html, unsafe_allow_html=True)