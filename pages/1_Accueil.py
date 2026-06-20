"""PAGE 1 – Accueil"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY

st.set_page_config(
    page_title="BOA Credit Scoring | Accueil",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
inject_global_css()
topbar("accueil")

# ─── HERO (light) ────────────────────────────────────────────
st.markdown(f"""
<div style="
background: linear-gradient(135deg, #FFFFFF 0%, #F5F7FA 60%, #EEF2F8 100%);
border: 1px solid #E2E8F0;
border-radius: 16px;
padding: 4rem 3rem;
margin-bottom: 2rem;
position: relative;
overflow: hidden;
box-shadow: 0 8px 32px rgba(0,51,102,0.08);
">
<div style="position:absolute;top:-60px;right:-60px;width:300px;height:300px;border-radius:50%;background:rgba(212,175,55,0.08)"></div>
<div style="position:absolute;bottom:-80px;left:-40px;width:250px;height:250px;border-radius:50%;background:rgba(0,51,102,0.04)"></div>
<div style="position:relative;z-index:2">
<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem">
<span style="font-size:2.5rem">🏦</span>
<div>
<div style="color:{COLOR_SECONDARY};font-size:0.8rem;text-transform:uppercase;letter-spacing:0.15em;font-weight:700">Bank of Africa</div>
<div style="color:#64748B;font-size:0.75rem">Département Risque Crédit</div>
</div>
</div>
<h1 style="color:{COLOR_PRIMARY};font-family:'Playfair Display',serif;font-size:2.6rem;font-weight:700;line-height:1.2;margin-bottom:1rem">
Système Intelligent de<br>
<span style="color:{COLOR_SECONDARY}">Scoring de Crédit Professionnel</span>
</h1>
<p style="color:#475569;font-size:1.05rem;max-width:640px;line-height:1.7;margin-bottom:2rem">
Évaluez le risque de crédit des clients professionnels avec précision.
Une solution bancaire combinant les critères BOA traditionnels
et une intelligence artificielle avancée.
</p>
<div style="display:flex;gap:1rem;flex-wrap:wrap">
<div style="background:rgba(212,175,55,0.12);border:1px solid rgba(212,175,55,0.4);border-radius:8px;padding:0.6rem 1rem;color:#8a6d1f;font-size:0.85rem;font-weight:600">
✦ Scoring en temps réel
</div>
<div style="background:rgba(0,51,102,0.06);border:1px solid rgba(0,51,102,0.15);border-radius:8px;padding:0.6rem 1rem;color:{COLOR_PRIMARY};font-size:0.85rem">
🤖 Analyse IA intégrée
</div>
<div style="background:rgba(0,51,102,0.06);border:1px solid rgba(0,51,102,0.15);border-radius:8px;padding:0.6rem 1rem;color:{COLOR_PRIMARY};font-size:0.85rem">
📊 Tableaux de bord bancaires
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI STRIP ───────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("9", "Critères BOA", "analysés automatiquement", COLOR_PRIMARY),
    ("3", "Profils clients", "Commerçant · Prof. Libérale · Personne Morale", COLOR_SECONDARY),
    ("6", "Visualisations", "Radar, Gauge, Waterfall…", "#0E9F6E"),
    ("100", "Score maximal", "Grille de décision A/B/C/D", "#7C3AED"),
]
for col, (val, label, sub, color) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(f"""
<div class="boa-card" style="text-align:center;border-top:3px solid {color}">
<div style="font-size:2.2rem;font-weight:800;color:{color}">{val}</div>
<div style="font-weight:600;color:#1E293B;font-size:0.9rem">{label}</div>
<div style="font-size:0.78rem;color:#64748B;margin-top:0.2rem">{sub}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ABOUT THE THESIS ────────────────────────────────────────
col_l, col_r = st.columns([3, 2])

with col_l:
    st.markdown('<div class="section-header">À propos de ce projet</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="boa-card">
<p style="color:#1E293B;line-height:1.8;font-size:0.92rem">
Cette application constitue l'implémentation pratique d'un
<strong>mémoire de Master Finance</strong> réalisé au sein de
<strong>Bank of Africa</strong>. Elle modélise un système de scoring
crédit à deux niveaux :
</p>

<div style="display:flex;gap:1.5rem;margin:1.2rem 0">
<div style="text-align:center;padding:1rem;background:#F5F7FA;border-radius:10px;flex:1">
<div style="font-size:2rem;font-weight:800;color:#003366">70%</div>
<div style="font-size:0.82rem;color:#64748B;margin-top:0.3rem">
Critères BOA communs<br><em>9 indicateurs bancaires</em>
</div>
</div>

<div style="text-align:center;padding:1rem;background:#FFF8E7;border-radius:10px;flex:1">
<div style="font-size:2rem;font-weight:800;color:#D4AF37">30%</div>
<div style="font-size:0.82rem;color:#64748B;margin-top:0.3rem">
Critères spécifiques<br><em>Par catégorie professionnelle</em>
</div>
</div>
</div>


<div style="margin-top:1.2rem;padding-top:1rem;border-top:1px solid #E2E8F0">
<p style="margin:0;color:#475569;font-size:0.82rem;line-height:1.6">
<strong>Développé par Oumayma Beioued</strong> dans le cadre de son
mémoire de Master Finance réalisé au sein de <strong>Bank of Africa</strong>,
avec pour objectif l'optimisation et l'automatisation du processus
de scoring crédit à travers des méthodes quantitatives et l'intelligence artificielle.
</p>
</div>

</div>
""", unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="section-header">Fonctionnalités clés</div>', unsafe_allow_html=True)
    
    features = [
        ("📋", "Formulaire dynamique", "Adapté à chaque catégorie de client"),
        ("⚡", "Calcul temps réel", "Scores mis à jour instantanément"),
        ("🧠", "Analyse IA", "Note de crédit professionnelle"),
        ("📊", "6 visualisations", "Radar, Gauge, Waterfall, Donut…"),
        ("📥", "Exports multiples", "PDF · Word · Excel"),
        ("🛡️", "Sécurisé", "Données locales, aucun stockage externe"),
    ]
    for icon, title, desc in features:
        st.markdown(f"""
<div style="display:flex;gap:0.8rem;align-items:flex-start;padding:0.65rem 0;border-bottom:1px solid #F0F4F8">
<span style="font-size:1.3rem;min-width:2rem">{icon}</span>
<div>
<div style="font-weight:600;color:#1E293B;font-size:0.88rem">{title}</div>
<div style="font-size:0.78rem;color:#64748B">{desc}</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── PROCESS STEPS ───────────────────────────────────────────
st.markdown('<div class="section-header">Processus d\'évaluation</div>', unsafe_allow_html=True)
steps = [
    ("1", "Sélection du profil", "Commerçant, Profession Libérale ou Personne Morale", COLOR_PRIMARY),
    ("2", "Saisie des données", "Informations bancaires et financières du client", "#004488"),
    ("3", "Scoring automatique", "Calcul pondéré en temps réel sur 100 points", "#0055AA"),
    ("4", "Analyse IA", "Note de crédit argumentée par intelligence artificielle", "#D4AF37"),
    ("5", "Décision & Export", "Recommandation et export du rapport", "#0E9F6E"),
]
cols = st.columns(5)
for col, (num, title, desc, color) in zip(cols, steps):
    with col:
        st.markdown(f"""
<div style="text-align:center;padding:1.25rem 0.75rem;background:#FFFFFF;border-radius:12px;box-shadow:0 2px 12px rgba(0,51,102,0.07);border-top:3px solid {color};height:100%">
<div style="width:2.5rem;height:2.5rem;border-radius:50%;background:{color};color:#fff;font-weight:800;font-size:1.1rem;display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem">
{num}
</div>
<div style="font-weight:700;color:{color};font-size:0.85rem;margin-bottom:0.4rem">{title}</div>
<div style="font-size:0.75rem;color:#64748B;line-height:1.5">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ─── CTA ─────────────────────────────────────────────────────
_, cta_col, _ = st.columns([2, 1, 2])
with cta_col:
    if st.button("🚀 Commencer l'évaluation", use_container_width=True):
        navigate("selection")

st.markdown("""
<div style="text-align:center;margin-top:2rem;color:#94A3B8;font-size:0.78rem">
Bank of Africa – Département Risque Crédit &nbsp;|&nbsp;
Usage interne confidentiel &nbsp;|&nbsp; v2.0.1
</div>
""", unsafe_allow_html=True)