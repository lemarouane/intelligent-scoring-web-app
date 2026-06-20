"""
BOA Intelligent Credit Scoring  –  Entry point
Run with:  streamlit run app.py
"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state
from utils.constants import APP_VERSION

st.set_page_config(
    page_title="BOA | Scoring de Crédit Professionnel",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": f"BOA Credit Scoring v{APP_VERSION} – Bank of Africa © 2025",
        "Report a bug": None,
        "Get help": None,
    },
)

init_session_state()
inject_global_css()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    # ── Brand header
    st.markdown(
        """
        <div style="padding:1.5rem 0 1rem;border-bottom:1px solid #E2E8F0;margin-bottom:1.25rem">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.25rem">
                <span style="font-size:1.8rem">🏦</span>
                <div>
                    <div style="color:#003366 !important;font-weight:800;font-size:0.95rem;
                                letter-spacing:0.04em">BANK OF AFRICA</div>
                    <div style="color:#94A3B8 !important;font-size:0.68rem;margin-top:1px">
                        Département Risque Crédit
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Navigation links
    st.markdown(
        '<p style="color:#94A3B8 !important;font-size:0.68rem;font-weight:700;'
        'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Navigation</p>',
        unsafe_allow_html=True,
    )

    nav_items = [
        ("pages/1_Accueil.py",             "🏠", "Accueil"),
        ("pages/2_Selection_Client.py",    "👤", "Sélection du client"),
        ("pages/3_Formulaire_Scoring.py",  "📋", "Formulaire de scoring"),
        ("pages/4_Dashboard_Resultats.py", "📊", "Dashboard résultats"),
    ]
    for path, icon, label in nav_items:
        if st.button(f"{icon}  {label}", key=f"sb_{path}", use_container_width=True):
            st.switch_page(path)

    st.markdown('<div style="border-top:1px solid #E2E8F0;margin:1.25rem 0"></div>',
                unsafe_allow_html=True)

    # ── Progress tracker
    st.markdown(
        '<p style="color:#94A3B8 !important;font-size:0.68rem;font-weight:700;'
        'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">État du dossier</p>',
        unsafe_allow_html=True,
    )

    categorie = st.session_state.get("categorie")
    final     = st.session_state.get("final_score")
    checks = [
        ("Catégorie sélectionnée", categorie is not None),
        ("Données saisies",        bool(st.session_state.get("boa_inputs"))),
        ("Score calculé",          final is not None),
        ("Analyse IA générée",     bool(st.session_state.get("ia_analysis"))),
    ]
    for label, done in checks:
        icon  = "✅" if done else "○"
        color = "#0E9F6E" if done else "#CBD5E1"
        st.markdown(
            f'<div style="font-size:0.78rem;color:{color} !important;padding:0.2rem 0;'
            f'display:flex;align-items:center;gap:0.4rem">'
            f'<span>{icon}</span><span style="color:{"#374151" if done else "#94A3B8"} !important">'
            f'{label}</span></div>',
            unsafe_allow_html=True,
        )

    # ── Active profile chip
    if categorie:
        cat_icons = {"Commerçant": "🏪", "Profession Libérale": "💼", "Personne Morale": "🏢"}
        st.markdown(
            f"""
            <div style="margin-top:1rem;background:#EFF6FF;border:1px solid #BFDBFE;
                        border-radius:8px;padding:0.6rem 0.8rem">
                <div style="color:#94A3B8 !important;font-size:0.66rem;font-weight:700;
                            text-transform:uppercase;letter-spacing:0.08em">Profil actif</div>
                <div style="color:#003366 !important;font-weight:700;font-size:0.85rem;margin-top:2px">
                    {cat_icons.get(categorie, "")} {categorie}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Score chip
    if final is not None:
        rc = st.session_state.get("risk_class", "–")
        rc_colors = {"A": "#0E9F6E", "B": "#16A34A", "C": "#F59E0B", "D": "#DC2626"}
        rc_color  = rc_colors.get(rc, "#003366")
        st.markdown(
            f"""
            <div style="margin-top:0.6rem;background:{rc_color}10;border:1.5px solid {rc_color}44;
                        border-radius:8px;padding:0.6rem 0.8rem;text-align:center">
                <div style="color:#94A3B8 !important;font-size:0.66rem;font-weight:700;
                            text-transform:uppercase;letter-spacing:0.08em">Score final</div>
                <div style="font-size:1.8rem;font-weight:800;color:{rc_color} !important;
                            line-height:1.1">{final:.1f}</div>
                <div style="color:#64748B !important;font-size:0.72rem">Classe {rc} · /100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="margin-top:2rem;color:#CBD5E1 !important;font-size:0.65rem;text-align:center">'
        f'v{APP_VERSION} · Usage interne confidentiel</div>',
        unsafe_allow_html=True,
    )

# ── Route to home page ───────────────────────────────────────
st.switch_page("pages/1_Accueil.py")