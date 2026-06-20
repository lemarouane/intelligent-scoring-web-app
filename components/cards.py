# ============================================================
# BOA INTELLIGENT CREDIT SCORING – CARDS COMPONENT
# ============================================================

import streamlit as st
from utils.constants import CATEGORIES, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_GRAY


def render_category_card(categorie: str, key_suffix: str = "") -> bool:
    """
    Renders one professional category card (Page 2: Commerçant,
    Profession Libérale, Personne Morale) with hover animation.
    Returns True if the card's button was clicked this run.
    """
    info = CATEGORIES.get(categorie, {})
    icon = info.get("icon", "🏦")
    desc = info.get("description", "")

    st.markdown(
        f"""
        <div class="boa-cat-card">
            <div class="boa-cat-icon">{icon}</div>
            <div class="boa-cat-title">{categorie}</div>
            <div class="boa-cat-desc">{desc}</div>
        </div>
        <style>
        .boa-cat-card {{
            background:#FFFFFF;
            border:1px solid rgba(0,51,102,0.08);
            border-radius:14px;
            padding:1.75rem 1.5rem;
            text-align:center;
            box-shadow:0 4px 18px rgba(0,51,102,0.07);
            transition:transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            height:210px;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
        }}
        .boa-cat-card:hover {{
            transform:translateY(-6px);
            box-shadow:0 14px 36px rgba(0,51,102,0.18);
            border-color:{COLOR_SECONDARY};
        }}
        .boa-cat-icon {{ font-size:2.6rem; margin-bottom:0.6rem; }}
        .boa-cat-title {{
            color:{COLOR_PRIMARY}; font-weight:700; font-size:1.05rem; margin-bottom:0.5rem;
        }}
        .boa-cat-desc {{ color:{COLOR_GRAY}; font-size:0.82rem; line-height:1.4; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return st.button(
        f"Sélectionner {categorie}",
        key=f"select_cat_{key_suffix or categorie}",
        use_container_width=True,
    )


def render_metric_card(label: str, value: str, sub: str = "", color: str = COLOR_PRIMARY):
    """Small KPI card used on the dashboard and home page."""
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color}">{value}</div>
            {f'<div class="metric-sub">{sub}</div>' if sub else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(icon: str, title: str, description: str):
    """Feature highlight card used on the Accueil page."""
    st.markdown(
        f"""
        <div class="boa-card" style="text-align:center;height:100%">
            <div style="font-size:2rem;margin-bottom:0.5rem">{icon}</div>
            <div style="color:{COLOR_PRIMARY};font-weight:700;font-size:1rem;margin-bottom:0.4rem">
                {title}
            </div>
            <div style="color:{COLOR_GRAY};font-size:0.85rem;line-height:1.5">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_criterion_row(label: str, poids: int, partial, weighted):
    """
    Single-row display for a scoring criterion: label / weight /
    partial score / weighted score — used as a fallback to the full
    components/score_table.py when rendering inline within a form.
    """
    partial_display  = "—" if partial is None else f"{partial}/100"
    weighted_display = "—" if weighted is None else f"{weighted:.2f}"

    c1, c2, c3, c4 = st.columns([3, 1, 1.2, 1.2])
    with c1:
        st.markdown(f"**{label}**")
    with c2:
        st.markdown(f"<span style='color:{COLOR_GRAY}'>{poids}%</span>", unsafe_allow_html=True)
    with c3:
        st.markdown(partial_display)
    with c4:
        st.markdown(f"**{weighted_display}**")