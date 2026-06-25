"""PAGE – Tableau de Bord 100% BOA  (poids renormalisés sur 100 pts)"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar, get_risk_info
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY
from charts.radar_chart     import radar_chart
from charts.bar_chart       import weighted_bar_chart, partial_bar_chart
from charts.donut_chart     import donut_chart
from charts.gauge_chart     import gauge_chart
from charts.waterfall_chart import waterfall_chart
from components.export_buttons import render_export_buttons
from services.llm_service   import generate_analysis

st.set_page_config(
    page_title="BOA Credit Scoring | Dashboard BOA",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("resultats_boa")

# ─── GUARD ───────────────────────────────────────────────────
if st.session_state.get("boa100_final") is None:
    st.warning("⚠️ Aucun score BOA calculé. Veuillez compléter le formulaire.")
    if st.button("← Retour au formulaire BOA"):
        navigate("formulaire_boa")
    st.stop()

# ─── GRILLE A→G ──────────────────────────────────────────────
RISK_GRID = {
    "A":  {"label": "Très faible",    "decision": "Accord immédiat",                                  "color": "#0E9F6E", "icon": "✅"},
    "B":  {"label": "Faible",         "decision": "Accord favorable",                                 "color": "#16A34A", "icon": "🟢"},
    "C":  {"label": "Modéré",         "decision": "Accord avec analyse complémentaire",               "color": "#84CC16", "icon": "🟡"},
    "D":  {"label": "Modéré à élevé", "decision": "Accord sous conditions ou garanties renforcées",  "color": "#F59E0B", "icon": "🟠"},
    "E":  {"label": "Élevé",          "decision": "Analyse approfondie obligatoire",                  "color": "#F97316", "icon": "🔴"},
    "F":  {"label": "Très élevé",     "decision": "Avis risque obligatoire et garanties importantes", "color": "#DC2626", "icon": "🔴"},
    "G":  {"label": "Critique",       "decision": "Refus recommandé",                                "color": "#7F1D1D", "icon": "⛔"},
    "NC": {"label": "Non Scorable",   "decision": "Attente d'historique suffisant (min. 3 mois)",    "color": "#94A3B8", "icon": "⚠️"},
}

def classify(score):
    if score >= 90:  return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    elif score >= 50: return "E"
    elif score >= 40: return "F"
    else:             return "G"

# ─── DATA ────────────────────────────────────────────────────
final_score  = st.session_state["boa100_final"]
rows         = st.session_state.get("boa100_rows", [])
boa_inputs   = st.session_state.get("boa_inputs_100", {})
boa_scores   = st.session_state.get("boa100_scores", {})
nc_flag      = st.session_state.get("nc_flag_100", False)
categorie    = st.session_state.get("categorie", "–")
ai_cached    = st.session_state.get("boa100_ia")
ai_error     = st.session_state.get("boa100_ia_error")

if nc_flag:
    risk_class = "NC"
else:
    risk_class = classify(final_score)

risk_info  = RISK_GRID[risk_class]
decision   = risk_info["decision"]
risk_color = risk_info["color"]
risk_icon  = risk_info["icon"]

cat_icons  = {"Commerçant": "🏪", "Profession Libérale": "💼", "Personne Morale": "🏢"}
cat_colors = {"Commerçant": COLOR_PRIMARY, "Profession Libérale": "#7C3AED", "Personne Morale": "#0891B2"}
cat_color  = cat_colors.get(categorie, COLOR_PRIMARY)

# ─── RESULT HEADER ───────────────────────────────────────────
nc_badge = '&nbsp;·&nbsp; <span style="color:#F59E0B;font-weight:700">⚠️ Client NC</span>' if nc_flag else ""
bg_color = f"rgba({int(risk_color[1:3],16)},{int(risk_color[3:5],16)},{int(risk_color[5:7],16)},0.08)"

st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;
            padding:1.75rem 2rem;margin-bottom:1.5rem;
            box-shadow:0 2px 16px rgba(0,51,102,0.07)">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                flex-wrap:wrap;gap:1rem">
        <div>
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem">
                <span style="font-size:1.5rem">🏦</span>
                <div>
                    <div style="font-size:0.72rem;color:#94A3B8;font-weight:700;
                                text-transform:uppercase;letter-spacing:0.1em">
                        Rapport d'Analyse – Scoring 100% BOA
                    </div>
                    <div style="font-family:'Playfair Display',serif;color:#003366;
                                font-size:1.5rem;font-weight:700;margin-top:1px">
                        Tableau de Bord — Critères BOA Purs
                    </div>
                </div>
            </div>
            <div style="font-size:0.82rem;color:#64748B;margin-left:2.5rem">
                Catégorie : <strong style="color:{cat_color}">{categorie}</strong>
                &nbsp;·&nbsp; 9 critères BOA renormalisés sur 100 pts
                &nbsp;·&nbsp; Modèle BOA v2.0.1{nc_badge}
            </div>
        </div>
        <div style="text-align:right">
            <div style="font-size:0.72rem;color:#94A3B8;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.5rem">
                Résultat de l'évaluation
            </div>
            <div style="margin-top:0.4rem">
                <span style="background:{bg_color};color:{risk_color};
                             border:2px solid {risk_color};border-radius:12px;
                             padding:0.6rem 1.5rem;font-size:1.1rem;font-weight:800;
                             letter-spacing:0.05em">
                    {risk_icon} Classe {risk_class} — {risk_info['label']}
                </span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MODE BADGE ──────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;
            padding:0.7rem 1.25rem;margin-bottom:1.5rem;
            display:flex;gap:0.75rem;align-items:center">
    <span style="font-size:1.1rem">🏦</span>
    <div style="font-size:0.83rem;color:#92400E">
        <strong>Analyse 100% BOA :</strong> ce tableau de bord reflète uniquement
        les 9 critères comportementaux et relationnels BOA, pondérés sur 100 points
        (sans les critères spécifiques à la catégorie <em>{categorie}</em>).
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI STRIP ───────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
kpis = [
    ("Classe de risque",     f"Classe {risk_class}", risk_info["label"],                           risk_color,  risk_icon),
    ("Décision recommandée", decision,               "Recommandation BOA",                         COLOR_PRIMARY, "📋"),
    ("Statut dossier",
     "NC — Compléter" if nc_flag else "✓ Complet",
     "Ancienneté < 3 mois"  if nc_flag else "9/9 critères BOA",
     "#F59E0B" if nc_flag else "#0E9F6E",
     "⚠️" if nc_flag else "✅"),
]
for col, (label, value, sub, color, icon) in zip([k1, k2, k3], kpis):
    with col:
        st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:12px;
            padding:1.1rem 1.25rem;box-shadow:0 1px 8px rgba(0,51,102,0.06);
            border-left:4px solid {color}">
    <div style="font-size:0.7rem;color:#94A3B8;font-weight:700;text-transform:uppercase;
                letter-spacing:0.07em;margin-bottom:0.25rem">{label}</div>
    <div style="font-size:1.05rem;font-weight:700;color:{color};line-height:1.3;
                margin-bottom:0.2rem">{icon} {value}</div>
    <div style="font-size:0.74rem;color:#94A3B8">{sub}</div>
</div>
""", unsafe_allow_html=True)

# ─── RISK GRID DISPLAY ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Grille de Décision BOA</div>', unsafe_allow_html=True)
grid_cols = st.columns(7)
grid_classes = ["A","B","C","D","E","F","G"]
grid_labels  = ["Très faible","Faible","Modéré","Modéré élevé","Élevé","Très élevé","Critique"]
grid_colors  = ["#0E9F6E","#16A34A","#84CC16","#F59E0B","#F97316","#DC2626","#7F1D1D"]
for col, cls, lbl, clr in zip(grid_cols, grid_classes, grid_labels, grid_colors):
    is_active = (risk_class == cls)
    with col:
        st.markdown(f"""
<div style="text-align:center;padding:0.75rem 0.4rem;border-radius:10px;
            background:{'#FFFFFF' if not is_active else clr + '18'};
            border:{'2.5px solid ' + clr if is_active else '1px solid #E2E8F0'};
            box-shadow:{'0 4px 12px ' + clr + '33' if is_active else 'none'}">
    <div style="font-size:1.3rem;font-weight:900;color:{clr}">{cls}</div>
    <div style="font-size:0.65rem;color:#64748B;margin-top:0.2rem;line-height:1.3">{lbl}</div>
    {'<div style="margin-top:0.3rem;font-size:0.6rem;background:' + clr + ';color:#fff;border-radius:999px;padding:1px 6px;font-weight:700">← Vous</div>' if is_active else ''}
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CLASS CARD + RADAR ──────────────────────────────────────
g_col, r_col = st.columns([1, 2], gap="large")

with g_col:
    st.markdown('<div class="section-header">Classe de Risque BOA</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div style="background:{risk_color}0D;border:3px solid {risk_color}44;
            border-radius:16px;padding:2.5rem 1rem;text-align:center;margin-top:0.5rem">
    <div style="font-size:1rem;color:#64748B;font-weight:600;text-transform:uppercase;
                letter-spacing:0.1em;margin-bottom:0.5rem">Classe de Risque</div>
    <div style="font-size:5rem;font-weight:900;color:{risk_color};line-height:1">
        {risk_class}
    </div>
    <div style="font-size:1.1rem;font-weight:700;color:{risk_color};margin-top:0.5rem">
        {risk_icon} {risk_info['label']}
    </div>
    <div style="font-size:0.82rem;color:#64748B;margin-top:0.75rem;line-height:1.5;
                padding:0 0.5rem">
        {decision}
    </div>
</div>
""", unsafe_allow_html=True)

with r_col:
    st.markdown('<div class="section-header">Profil BOA — Radar des 9 Critères</div>',
                unsafe_allow_html=True)
    if rows:
        st.plotly_chart(radar_chart(rows), use_container_width=True,
                        config={"displayModeBar": False})

# ─── BAR CHARTS ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2, gap="large")
with b1:
    st.markdown('<div class="section-header">Scores Pondérés — 9 Critères BOA</div>',
                unsafe_allow_html=True)
    if rows:
        st.plotly_chart(weighted_bar_chart(rows), use_container_width=True,
                        config={"displayModeBar": False})
with b2:
    st.markdown('<div class="section-header">Scores Partiels — 9 Critères BOA</div>',
                unsafe_allow_html=True)
    if rows:
        st.plotly_chart(partial_bar_chart(rows), use_container_width=True,
                        config={"displayModeBar": False})

# ─── DONUT + WATERFALL ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
d1, d2 = st.columns(2, gap="large")
with d1:
    st.markdown('<div class="section-header">Contribution par Critère BOA</div>',
                unsafe_allow_html=True)
    if rows:
        st.plotly_chart(donut_chart(rows), use_container_width=True,
                        config={"displayModeBar": False})
with d2:
    st.markdown('<div class="section-header">Construction du Score BOA (Waterfall)</div>',
                unsafe_allow_html=True)
    if rows:
        st.plotly_chart(waterfall_chart(rows, final_score), use_container_width=True,
                        config={"displayModeBar": False})

# ─── SCORE TABLE ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Tableau Détaillé — 9 Critères BOA (100 pts)</div>',
            unsafe_allow_html=True)

header = """
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.6rem 1rem;background:#003366;
            border-radius:10px 10px 0 0;
            font-size:0.72rem;font-weight:700;color:#fff;
            text-transform:uppercase;letter-spacing:0.05em">
    <span>Critère BOA</span>
    <span style="text-align:center">Poids</span>
    <span style="text-align:center">Score /100</span>
    <span style="text-align:center">Pondéré</span>
    <span style="text-align:center">Progression</span>
</div>"""

body = ""
for i, r in enumerate(rows):
    bg  = "#FFFFFF" if i % 2 == 0 else "#FAFBFC"
    c   = ("#0E9F6E" if r["partial"] >= 80 else
           "#16A34A" if r["partial"] >= 60 else
           "#F59E0B" if r["partial"] >= 40 else "#DC2626")
    pct = min(r["partial"], 100)
    body += f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.5rem 1rem;background:{bg};
            border-left:1px solid #E2E8F0;border-right:1px solid #E2E8F0;
            border-bottom:1px solid #F1F5F9;font-size:0.8rem;align-items:center">
    <span style="color:#1E293B;font-weight:500">{r['label']}</span>
    <span style="text-align:center;color:#94A3B8">{r['poids']:.2f}%</span>
    <span style="text-align:center">
        <span style="background:{c}18;color:{c};border:1px solid {c}44;
                     border-radius:999px;padding:2px 9px;font-size:0.73rem;font-weight:700">
            {r['partial']}/100
        </span>
    </span>
    <span style="text-align:center;color:#003366;font-weight:700">{r['weighted']:.2f}</span>
    <span>
        <div style="background:#F1F5F9;border-radius:999px;height:7px;overflow:hidden">
            <div style="width:{pct}%;height:100%;background:{c};border-radius:999px"></div>
        </div>
        <div style="font-size:0.68rem;color:#94A3B8;text-align:right;margin-top:2px">{pct}%</div>
    </span>
</div>"""

footer = f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.65rem 1rem;background:#FFFBEB;
            border:1.5px solid #FDE68A;border-radius:0 0 10px 10px;
            font-size:0.85rem;font-weight:800;color:#92400E">
    <span>CLASSE FINALE BOA</span><span></span><span></span>
    <span style="text-align:center;font-size:1rem;color:{risk_color}">
        {risk_icon} Classe {risk_class}
    </span>
    <span></span>
</div>"""

st.markdown(header + body + footer, unsafe_allow_html=True)

# ─── AI ANALYSIS ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🤖 Analyse IA — Profil BOA Pur</div>',
            unsafe_allow_html=True)

ia_pending = st.session_state.get("boa100_ia_pending", False)

if ia_pending and not ai_cached and not ai_error:
    with st.spinner("🤖 Génération de l'analyse IA en cours…"):
        try:
            analysis = generate_analysis(
                categorie=categorie,
                boa_inputs=boa_inputs,
                specific_inputs={},
                boa_scores=boa_scores,
                specific_scores={},
                final_score=final_score,
                risk_class=risk_class,
                decision=decision,
                rows=rows,
            )
            st.session_state["boa100_ia"]       = analysis
            st.session_state["boa100_ia_error"] = None
            ai_cached = analysis
        except Exception as e:
            st.session_state["boa100_ia_error"] = str(e)
            ai_error = str(e)
    st.session_state["boa100_ia_pending"] = False

if ai_cached:
    st.markdown("""
<div style="background:#F8FAFF;border:1.5px solid #DBEAFE;border-radius:12px;
            padding:1.5rem 2rem;margin-top:0.75rem">
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;
                padding-bottom:0.75rem;border-bottom:1px solid #E2E8F0">
        <span style="font-size:1.2rem">🤖</span>
        <div style="font-weight:700;color:#003366;font-size:0.95rem">
            Note de Crédit — Analyse BOA Pure
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    st.markdown(
        f'<div style="color:#1E293B;font-size:0.9rem;line-height:1.7">{ai_cached}</div>',
        unsafe_allow_html=True)
else:
    if ai_error:
        st.markdown(f"""
<div style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:10px;
            padding:1rem 1.25rem;color:#991B1B;font-size:0.85rem;margin-bottom:0.75rem">
    ⚠️ Génération IA échouée : {ai_error}
</div>
""", unsafe_allow_html=True)
    col_ai_info, col_ai_btn = st.columns([3, 1])
    with col_ai_info:
        st.markdown("""
<div style="background:#F0F7FF;border:1.5px solid #BFDBFE;border-radius:10px;
            padding:1rem 1.25rem;color:#1E40AF;font-size:0.85rem">
    🤖 Cliquez pour générer une analyse IA du profil BOA pur du client.
</div>
""", unsafe_allow_html=True)
    with col_ai_btn:
        if st.button("🤖 Générer l'analyse IA", use_container_width=True, key="btn_ai_boa"):
            with st.spinner("Analyse du dossier en cours…"):
                try:
                    analysis = generate_analysis(
                        categorie=categorie,
                        boa_inputs=boa_inputs,
                        specific_inputs={},
                        boa_scores=boa_scores,
                        specific_scores={},
                        final_score=final_score,
                        risk_class=risk_class,
                        decision=decision,
                        rows=rows,
                    )
                    st.session_state["boa100_ia"]       = analysis
                    st.session_state["boa100_ia_error"] = None
                    st.rerun()
                except Exception as e:
                    st.session_state["boa100_ia_error"] = str(e)
                    st.error(f"Erreur IA : {e}")

# ─── EXPORTS ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;
            padding:1.25rem 1.75rem;margin-bottom:1rem">
    <div style="font-weight:700;color:#003366;font-size:0.95rem;margin-bottom:0.25rem">
        📥 Exports du Rapport BOA
    </div>
    <div style="font-size:0.8rem;color:#94A3B8">
        Rapport complet basé sur les 9 critères BOA renormalisés à 100 points.
    </div>
</div>
""", unsafe_allow_html=True)

render_export_buttons(
    categorie=categorie,
    final_score=final_score,
    risk_class=risk_class,
    decision=decision,
    prob_default=risk_info["label"],
    rows=rows,
    ia_analysis=ai_cached or "",
)

# ─── NAVIGATION ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_back, col_mid, col_new = st.columns([1, 1, 1])
with col_back:
    if st.button("← Modifier le formulaire BOA", use_container_width=True):
        navigate("formulaire_boa")
with col_mid:
    if st.button("📊 Voir scoring complet (BOA + Spécifiques)", use_container_width=True):
        navigate("formulaire")
with col_new:
    if st.button("🔄 Nouveau dossier", use_container_width=True):
        for key in ["boa_inputs_100","boa100_scores","boa100_final","boa100_rows",
                    "boa100_class","boa100_ia","boa100_ia_error","nc_flag_100","categorie"]:
            st.session_state.pop(key, None)
        navigate("selection")

st.markdown("""
<div style="text-align:center;margin-top:2.5rem;color:#CBD5E1;font-size:0.72rem">
    Bank of Africa – Scoring 100% Critères BOA &nbsp;·&nbsp;
    Document confidentiel – Usage interne &nbsp;·&nbsp; v2.0.1
</div>
""", unsafe_allow_html=True)