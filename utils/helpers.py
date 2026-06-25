# ============================================================
# BOA INTELLIGENT CREDIT SCORING – HELPERS  (bright theme)
# ============================================================

import streamlit as st
from utils.constants import RISK_CLASSES, COLOR_PRIMARY, COLOR_SECONDARY


def format_score(score: float) -> str:
    return f"{score:.1f} / 100"


def get_risk_info(risk_class: str) -> dict:
    return RISK_CLASSES.get(risk_class, RISK_CLASSES["D"])


def score_color(score: int) -> str:
    if score >= 80: return "#0E9F6E"
    if score >= 60: return "#16A34A"
    if score >= 40: return "#F59E0B"
    return "#DC2626"


def init_session_state():
    defaults = {
        "categorie":        None,
        "boa_scores":       {},
        "boa_inputs":       {},
        "specific_scores":  {},
        "specific_inputs":  {},
        "final_score":      None,
        "risk_class":       None,
        "ia_analysis":      None,
        "nc_flag":          False,
        "result_rows":      [],
        # ── BOA-100 mode keys ──────────────────────────────
        "boa_inputs_100":   {},
        "boa100_scores":    {},
        "boa100_rows":      [],
        "boa100_final":     None,
        "boa100_class":     None,
        "boa100_ia":        None,
        "boa100_ia_error":  None,
        "boa100_ia_pending": False,
        "nc_flag_100":      False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Routing table ─────────────────────────────────────────────
PAGE_PATHS = {
    # Standard flow
    "accueil":        "pages/1_Accueil.py",
    "selection":      "pages/2_Selection_Client.py",
    "formulaire":     "pages/3_Formulaire_Scoring.py",
    "resultats":      "pages/4_Dashboard_Resultats.py",
    # BOA-100 flow
    "selection_boa":  "pages/5_Selection_BOA.py",
    "formulaire_boa": "pages/6_Formulaire_BOA.py",
    "resultats_boa":  "pages/7_Dashboard_BOA.py",
}


def navigate(page: str):
    path = PAGE_PATHS.get(page)
    if path:
        st.switch_page(path)


def inject_global_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

        /* ── Reset ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ── Force light background everywhere ── */
        .stApp, .main, [data-testid="stAppViewContainer"] {
            background-color: #F8FAFC !important;
        }

        /* ── Sidebar: navy left strip ── */
        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 2px 0 12px rgba(0,51,102,0.06) !important;
        }
        section[data-testid="stSidebar"] * {
            color: #1E293B !important;
        }
        section[data-testid="stSidebar"] .sidebar-brand-title {
            color: #003366 !important;
        }
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: #475569 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 0.5rem 0.75rem !important;
            transition: background 0.15s !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #F1F5F9 !important;
            color: #003366 !important;
            transform: none !important;
        }

        /* ── Main container ── */
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        /* ── Topbar / navbar ── */
        .boa-topbar {
            background: #FFFFFF;
            border-bottom: 2px solid #E2E8F0;
            padding: 0.85rem 2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 2px 12px rgba(0,51,102,0.06);
            position: sticky;
            top: 0;
            z-index: 999;
        }
        .boa-topbar-logo {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .boa-topbar-title {
            color: #003366;
            font-family: 'Playfair Display', serif;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }
        .boa-topbar-sub {
            color: #94A3B8;
            font-size: 0.72rem;
            margin-top: 1px;
        }
        .boa-topbar-divider {
            width: 1px;
            height: 32px;
            background: #E2E8F0;
            margin: 0 0.75rem;
        }
        .boa-nav-link {
            font-size: 0.82rem;
            font-weight: 500;
            color: #64748B;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            transition: all 0.15s;
            text-decoration: none;
            white-space: nowrap;
        }
        .boa-nav-link.active {
            background: #EFF6FF;
            color: #003366;
            font-weight: 700;
        }
        .boa-nav-link.active-boa {
            background: #FFFBEB;
            color: #92400E;
            font-weight: 700;
        }
        .boa-nav-dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #D4AF37;
            margin-right: 5px;
            vertical-align: middle;
        }

        /* ── Section header ── */
        .section-header {
            font-family: 'Playfair Display', serif;
            color: #003366;
            font-size: 1.25rem;
            font-weight: 700;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #D4AF37;
            margin-bottom: 1.25rem;
        }

        /* ── Cards ── */
        .boa-card {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 1.5rem 1.75rem;
            box-shadow: 0 1px 8px rgba(0,51,102,0.07);
            border: 1px solid #E8EDF4;
            transition: box-shadow 0.2s, transform 0.15s;
            margin-bottom: 1rem;
        }
        .boa-card:hover {
            box-shadow: 0 6px 24px rgba(0,51,102,0.11);
            transform: translateY(-1px);
        }

        /* ── Metric card ── */
        .metric-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 8px rgba(0,51,102,0.07);
            border-left: 4px solid #003366;
            margin-bottom: 0.75rem;
        }
        .metric-label {
            font-size: 0.72rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.07em;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #003366;
            line-height: 1.2;
            margin-top: 0.15rem;
        }
        .metric-sub {
            font-size: 0.78rem;
            color: #64748B;
            margin-top: 0.15rem;
        }

        /* ── Streamlit native buttons ── */
        div[data-testid="stMainBlockContainer"] .stButton > button {
            background: #003366 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 0.55rem 1.4rem !important;
            transition: all 0.18s !important;
            box-shadow: 0 2px 8px rgba(0,51,102,0.18) !important;
        }
        div[data-testid="stMainBlockContainer"] .stButton > button:hover {
            background: #004488 !important;
            box-shadow: 0 4px 16px rgba(0,51,102,0.28) !important;
            transform: translateY(-1px) !important;
        }

        /* ── Input labels ── */
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label,
        div[data-testid="stTextInput"] label {
            font-weight: 600;
            color: #374151 !important;
            font-size: 0.85rem;
        }

        /* ── Inputs themselves ── */
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInput"] input {
            background: #F8FAFC !important;
            border: 1.5px solid #E2E8F0 !important;
            border-radius: 8px !important;
            color: #1E293B !important;
        }
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stTextInput"] input:focus {
            border-color: #003366 !important;
            box-shadow: 0 0 0 3px rgba(0,51,102,0.08) !important;
        }

        /* ── NC alert ── */
        .nc-alert {
            background: #FFFBEB;
            border: 1.5px solid #F59E0B;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #92400E;
            font-size: 0.84rem;
        }

        /* ── AI section ── */
        .ai-section {
            background: #F0F7FF;
            border: 1.5px solid #BFDBFE;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin-top: 1.5rem;
        }

        /* ── Dividers ── */
        hr {
            border: none;
            border-top: 1px solid #E8EDF4;
            margin: 1rem 0;
        }

        /* ── Streamlit chrome ── */
        #MainMenu { visibility: hidden; }
        footer    { visibility: hidden; }
        header    { visibility: hidden; }

        /* ── Download buttons ── */
        div[data-testid="stDownloadButton"] > button {
            background: #F1F5F9 !important;
            color: #003366 !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background: #E2E8F0 !important;
            border-color: #003366 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── BOA-100 pages — used to detect which topbar mode to render
_BOA_PAGES = {"selection_boa", "formulaire_boa", "resultats_boa"}


def topbar(current_page: str = ""):
    """
    White sticky navbar. Shows standard nav for the normal flow,
    and a BOA-mode variant (amber tint) when inside the BOA-100 flow.
    """
    is_boa_mode = current_page in _BOA_PAGES

    if is_boa_mode:
        # ── BOA-100 flow navbar ──────────────────────────────
        pages = [
            ("🏠", "Accueil",         "accueil"),
            ("👤", "Sélection BOA",   "selection_boa"),
            ("📋", "Formulaire BOA",  "formulaire_boa"),
            ("📊", "Résultats BOA",   "resultats_boa"),
        ]
        mode_badge = (
            '<span style="background:#FFFBEB;color:#92400E;border-radius:999px;'
            'padding:3px 10px;font-size:0.72rem;font-weight:700;border:1px solid #FDE68A;'
            'margin-left:0.5rem">🏦 Mode 100% BOA</span>'
        )
    else:
        # ── Standard flow navbar ─────────────────────────────
        pages = [
            ("🏠", "Accueil",    "accueil"),
            ("👤", "Sélection",  "selection"),
            ("📋", "Formulaire", "formulaire"),
            ("📊", "Résultats",  "resultats"),
        ]
        mode_badge = ""

    nav_items = ""
    for icon, label, key in pages:
        if key == current_page:
            css_cls = "active-boa" if is_boa_mode else "active"
            dot     = '<span class="boa-nav-dot"></span>'
        else:
            css_cls = ""
            dot     = ""
        nav_items += (
            f'<span class="boa-nav-link {css_cls}">'
            f'{dot}{icon} {label}</span>'
        )

    badge_html = ""
    cat = st.session_state.get("categorie")
    if cat:
        badge_html = (
            f'<span style="background:#EFF6FF;color:#003366;border-radius:999px;'
            f'padding:3px 12px;font-size:0.75rem;font-weight:700;border:1px solid #BFDBFE">'
            f'{cat}</span>'
        )

    # Show the correct score depending on which flow we're in
    if is_boa_mode:
        score     = st.session_state.get("boa100_final")
        risk_cls  = st.session_state.get("boa100_class", "")
    else:
        score     = st.session_state.get("final_score")
        risk_cls  = st.session_state.get("risk_class", "")

    score_html = ""
    if score is not None:
        rc_colors = {"A": "#0E9F6E", "B": "#16A34A", "C": "#F59E0B", "D": "#DC2626"}
        sc = rc_colors.get(risk_cls, "#003366")
        score_html = (
            f'<span style="background:{sc}18;color:{sc};border-radius:999px;'
            f'padding:3px 12px;font-size:0.75rem;font-weight:700;border:1px solid {sc}44">'
            f'Score {score:.1f} · Classe {risk_cls}</span>'
        )

 