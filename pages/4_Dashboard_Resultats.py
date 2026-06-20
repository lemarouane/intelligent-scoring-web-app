"""PAGE 4 – Tableau de Bord des Résultats  (bright theme)"""
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
    page_title="BOA Credit Scoring | Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("resultats")

if st.session_state.get("final_score") is None:
    st.warning("⚠️ Aucun score calculé. Veuillez compléter le formulaire de scoring.")
    if st.button("← Retour au formulaire"):
        navigate("formulaire")
    st.stop()

# ── Data ─────────────────────────────────────────────────────
final_score = st.session_state["final_score"]
risk_class  = st.session_state["risk_class"]
categorie   = st.session_state.get("categorie", "–")
rows        = st.session_state.get("result_rows", [])
boa_inputs  = st.session_state.get("boa_inputs", {})
spec_inputs = st.session_state.get("specific_inputs", {})
boa_scores  = st.session_state.get("boa_scores", {})
spec_scores = st.session_state.get("specific_scores", {})
nc_flag     = st.session_state.get("nc_flag", False)
ai_cached   = st.session_state.get("ia_analysis")
ai_error    = st.session_state.get("ia_error")

risk_info   = get_risk_info(risk_class)
decision    = risk_info["decision"]
prob_def    = risk_info["prob_default"]
risk_color  = risk_info["color"]
risk_icon   = risk_info["icon"]

cat_icons  = {"Commerçant":"🏪","Profession Libérale":"💼","Personne Morale":"🏢"}
cat_colors = {"Commerçant":COLOR_PRIMARY,"Profession Libérale":"#7C3AED","Personne Morale":"#0891B2"}
cat_color  = cat_colors.get(categorie, COLOR_PRIMARY)

# ─── RESULT HEADER ───────────────────────────────────────────
nc_badge = '&nbsp;·&nbsp; <span style="color:#F59E0B;font-weight:700">⚠️ Client NC</span>' if nc_flag else ''
bg_color = f"rgba({int(risk_color[1:3],16)},{int(risk_color[3:5],16)},{int(risk_color[5:7],16)},0.08)"

st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:1.75rem 2rem;margin-bottom:1.5rem;box-shadow:0 2px 16px rgba(0,51,102,0.07)">
<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem">
<div>
<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem">
<span style="font-size:1.5rem">{cat_icons.get(categorie,'🏦')}</span>
<div>
<div style="font-size:0.72rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.1em">Rapport d'Analyse – Risque Crédit</div>
<div style="font-family:'Playfair Display',serif;color:#003366;font-size:1.5rem;font-weight:700;margin-top:1px">Résultats du Scoring Professionnel</div>
</div>
</div>
<div style="font-size:0.82rem;color:#64748B;margin-left:2.5rem">Catégorie : <strong style="color:{cat_color}">{categorie}</strong>&nbsp;·&nbsp;Modèle BOA v2.0.1{nc_badge}</div>
</div>
<div style="text-align:right">
<div style="font-size:0.72rem;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px">Score Final</div>
<div style="font-size:3.5rem;font-weight:800;color:{risk_color};line-height:1">{final_score:.1f}</div>
<div style="color:#94A3B8;font-size:0.82rem">/ 100 points</div>
<div style="margin-top:0.4rem">
<span style="background:{bg_color};color:{risk_color};border:1.5px solid {risk_color};border-radius:999px;padding:4px 14px;font-size:0.8rem;font-weight:700">{risk_icon} Classe {risk_class} — {risk_info['label']}</span>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

# ─── KPI STRIP ───────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Classe de risque",       f"Classe {risk_class}",  risk_info["label"],  risk_color,  risk_icon),
    ("Décision recommandée",   decision,                "Recommandation",  COLOR_PRIMARY, "📋"),
    ("Probabilité de défaut",  prob_def,                "Estimation modèle",  "#7C3AED", "📉"),
    ("Statut dossier",
     "NC — Compléter" if nc_flag else "✓ Complet",
     "Ancienneté < 3 mois" if nc_flag else "Tous critères renseignés",
     "#F59E0B" if nc_flag else "#0E9F6E",
     "⚠️" if nc_flag else "✅"),
]
for col, (label, value, sub, color, icon) in zip([k1,k2,k3,k4], kpis):
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

st.markdown("<br>", unsafe_allow_html=True)

# ─── GAUGE + RADAR ───────────────────────────────────────────
g_col, r_col = st.columns([1, 2], gap="large")

with g_col:
    st.markdown('<div class="section-header">Score Final</div>', unsafe_allow_html=True)
    st.plotly_chart(gauge_chart(final_score, risk_class),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""
<div style="background:{risk_color}0D;border:2px solid {risk_color}33;
            border-radius:12px;padding:1.1rem;text-align:center;margin-top:0.5rem">
    <div style="font-size:2rem;margin-bottom:0.3rem">{risk_icon}</div>
    <div style="font-size:1.05rem;font-weight:800;color:{risk_color}">{risk_info['label']}</div>
    <div style="font-size:0.8rem;color:#64748B;margin-top:0.25rem">{decision}</div>
</div>
""", unsafe_allow_html=True)

with r_col:
    st.markdown('<div class="section-header">Profil des Critères — Radar</div>', unsafe_allow_html=True)
    if rows:
        st.plotly_chart(radar_chart(rows), use_container_width=True, config={"displayModeBar": False})

# ─── BAR CHARTS ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2, gap="large")
with b1:
    st.markdown('<div class="section-header">Scores Pondérés par Critère</div>', unsafe_allow_html=True)
    if rows:
        st.plotly_chart(weighted_bar_chart(rows), use_container_width=True, config={"displayModeBar": False})
with b2:
    st.markdown('<div class="section-header">Scores Partiels par Critère</div>', unsafe_allow_html=True)
    if rows:
        st.plotly_chart(partial_bar_chart(rows), use_container_width=True, config={"displayModeBar": False})

# ─── DONUT + WATERFALL ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
d1, d2 = st.columns(2, gap="large")
with d1:
    st.markdown('<div class="section-header">Contribution par Critère</div>', unsafe_allow_html=True)
    if rows:
        st.plotly_chart(donut_chart(rows), use_container_width=True, config={"displayModeBar": False})
with d2:
    st.markdown('<div class="section-header">Construction du Score (Waterfall)</div>', unsafe_allow_html=True)
    if rows:
        st.plotly_chart(waterfall_chart(rows, final_score), use_container_width=True,
                        config={"displayModeBar": False})

# ─── SCORE TABLE ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Tableau Détaillé des Critères</div>', unsafe_allow_html=True)

header = """
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.6rem 1rem;background:#003366;
            border-radius:10px 10px 0 0;
            font-size:0.72rem;font-weight:700;color:#fff;
            text-transform:uppercase;letter-spacing:0.05em">
    <span>Critère</span>
    <span style="text-align:center">Poids</span>
    <span style="text-align:center">Score /100</span>
    <span style="text-align:center">Pondéré</span>
    <span style="text-align:center">Progression</span>
</div>"""

body = ""
for i, r in enumerate(rows):
    bg   = "#FFFFFF" if i % 2 == 0 else "#FAFBFC"
    c    = ("#0E9F6E" if r["partial"] >= 80 else
            "#16A34A" if r["partial"] >= 60 else
            "#F59E0B" if r["partial"] >= 40 else "#DC2626")
    pct  = min(r["partial"], 100)
    body += f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.5rem 1rem;background:{bg};
            border-left:1px solid #E2E8F0;border-right:1px solid #E2E8F0;
            border-bottom:1px solid #F1F5F9;font-size:0.8rem;align-items:center">
    <span style="color:#1E293B;font-weight:500">{r['label']}</span>
    <span style="text-align:center;color:#94A3B8">{r['poids']}%</span>
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
        <div style="font-size:0.68rem;color:#94A3B8;text-align:right;margin-top:2px">
            {pct}%
        </div>
    </span>
</div>"""

total_w = sum(r["weighted"] for r in rows)
footer  = f"""
<div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1.3fr 1.5fr;
            gap:0.4rem;padding:0.65rem 1rem;background:#FFFBEB;
            border:1.5px solid #FDE68A;border-radius:0 0 10px 10px;
            font-size:0.85rem;font-weight:800;color:#92400E">
    <span>SCORE FINAL</span><span></span><span></span>
    <span style="text-align:center;font-size:1rem;color:#003366">{total_w:.2f}</span>
    <span></span>
</div>"""

st.markdown(header + body + footer, unsafe_allow_html=True)

# ─── AI ANALYSIS ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🤖 Analyse par Intelligence Artificielle</div>',
            unsafe_allow_html=True)

ia_pending = st.session_state.get("ia_pending", False)

# If the formulaire page just navigated here for a fresh dossier,
# ia_pending is True and nothing is cached yet — generate it now,
# right here on the dashboard. The score, KPIs, and all charts above
# have already rendered by this point, so the page never looks frozen;
# only this section shows a spinner while GPT responds.
if ia_pending and not ai_cached and not ai_error:
    with st.spinner("🤖 Génération de l'analyse IA en cours… (quelques secondes)"):
        try:
            analysis = generate_analysis(
                categorie=categorie,
                boa_inputs=boa_inputs,
                specific_inputs=spec_inputs,
                boa_scores=boa_scores,
                specific_scores=spec_scores,
                final_score=final_score,
                risk_class=risk_class,
                decision=decision,
                rows=rows,
            )
            st.session_state["ia_analysis"] = analysis
            st.session_state["ia_error"] = None
            ai_cached = analysis
        except Exception as e:
            st.session_state["ia_error"] = str(e)
            ai_error = str(e)
    st.session_state["ia_pending"] = False

# If the analysis is cached (either from the block above, or from a
# previous run), display it right away, no click needed.
if ai_cached:
    st.markdown("""
<div style="background:#F8FAFF;border:1.5px solid #DBEAFE;border-radius:12px;
            padding:1.5rem 2rem;margin-top:0.75rem">
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;
                padding-bottom:0.75rem;border-bottom:1px solid #E2E8F0">
        <span style="font-size:1.2rem">🤖</span>
        <div style="font-weight:700;color:#003366;font-size:0.95rem">
            Note de Crédit
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ← Force dark color on AI markdown output
    st.markdown(
        f'<div style="color:#1E293B;font-size:0.9rem;line-height:1.7">{ai_cached}</div>',
        unsafe_allow_html=True
    )

else:
    # Fallback: only reached if the automatic generation above failed
    # (missing token, API error, timeout, etc.).
    if ai_error:
        st.markdown(f"""
<div style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:10px;
            padding:1rem 1.25rem;color:#991B1B;font-size:0.85rem;margin-bottom:0.75rem">
    ⚠️ La génération automatique de l'analyse IA a échoué : {ai_error}
</div>
""", unsafe_allow_html=True)

    col_ai_info, col_ai_btn = st.columns([3, 1])
    with col_ai_info:
        st.markdown("""
<div style="background:#F0F7FF;border:1.5px solid #BFDBFE;border-radius:10px;
            padding:1rem 1.25rem;color:#1E40AF;font-size:0.85rem">
    🤖 Cliquez sur le bouton pour générer une analyse IA complète du dossier par GPT.
    L'analyse couvre 8 sections : résumé exécutif, critères BOA, forces, faiblesses,
    appréciation du risque et décision finale.
</div>
""", unsafe_allow_html=True)
    with col_ai_btn:
        if st.button("🤖 Générer l'analyse IA", use_container_width=True):
            with st.spinner("Analyse du dossier en cours…"):
                try:
                    analysis = generate_analysis(
                        categorie=categorie,
                        boa_inputs=boa_inputs,
                        specific_inputs=spec_inputs,
                        boa_scores=boa_scores,
                        specific_scores=spec_scores,
                        final_score=final_score,
                        risk_class=risk_class,
                        decision=decision,
                        rows=rows,
                    )
                    st.session_state["ia_analysis"] = analysis
                    st.session_state["ia_error"] = None
                    st.rerun()
                except Exception as e:
                    st.session_state["ia_error"] = str(e)
                    st.error(f"Erreur IA : {e}")

# ─── EXPORTS ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;
            padding:1.25rem 1.75rem;margin-bottom:1rem">
    <div style="font-weight:700;color:#003366;font-size:0.95rem;margin-bottom:0.25rem">
        📥 Exports du Rapport
    </div>
    <div style="font-size:0.8rem;color:#94A3B8">
        Téléchargez le rapport complet avec toutes les données et l'analyse IA.
    </div>
</div>
""", unsafe_allow_html=True)

render_export_buttons(
    categorie=categorie, final_score=final_score, risk_class=risk_class,
    decision=decision, prob_default=prob_def, rows=rows, ia_analysis=ai_cached or "",
)

# ─── NAVIGATION ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_back, _, col_new = st.columns([1, 2, 1])
with col_back:
    if st.button("← Modifier le dossier", use_container_width=True):
        navigate("formulaire")
with col_new:
    if st.button("🔄 Nouveau dossier", use_container_width=True):
        for key in ["boa_inputs","specific_inputs","boa_scores","specific_scores",
                    "final_score","risk_class","result_rows","ia_analysis","ia_error",
                    "nc_flag","categorie"]:
            st.session_state.pop(key, None)
        navigate("selection")

st.markdown("""
<div style="text-align:center;margin-top:2.5rem;color:#CBD5E1;font-size:0.72rem">
    Bank of Africa – Système de Scoring Crédit Professionnel &nbsp;·&nbsp;
    Document confidentiel – Usage interne &nbsp;·&nbsp; v2.0.1
</div>
""", unsafe_allow_html=True)