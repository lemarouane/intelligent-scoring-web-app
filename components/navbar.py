# ============================================================
# BOA INTELLIGENT CREDIT SCORING – NAVBAR COMPONENT
# ============================================================

import streamlit as st
from utils.helpers import topbar, navigate
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY


def render_navbar(current_page: str = ""):
    """Thin wrapper around helpers.topbar for use inside page files."""
    topbar(current_page)


def render_step_indicator(current_step: int):
    """
    Horizontal 4-step progress indicator shown under the topbar on
    the workflow pages (Sélection → Formulaire → Résultats).
    """
    steps = ["Accueil", "Sélection Client", "Formulaire Scoring", "Dashboard Résultats"]

    cols = st.columns(len(steps))
    for i, (col, label) in enumerate(zip(cols, steps), start=1):
        is_done    = i < current_step
        is_current = i == current_step
        if is_done:
            color, icon = COLOR_SECONDARY, "✓"
        elif is_current:
            color, icon = COLOR_PRIMARY, str(i)
        else:
            color, icon = "#CBD5E1", str(i)

        with col:
            st.markdown(
                f"""
                <div style="text-align:center;padding:0.4rem 0">
                    <div style="
                        width:32px;height:32px;border-radius:50%;
                        background:{color};color:#fff;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 0.3rem;font-weight:700;font-size:0.85rem;
                    ">{icon}</div>
                    <div style="font-size:0.72rem;color:{'#1E293B' if is_current else '#94A3B8'};
                                font-weight:{'600' if is_current else '400'}">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_breadcrumb(items: list[str]):
    """Simple breadcrumb trail, e.g. ['Accueil', 'Commerçant', 'Scoring']."""
    trail = " &nbsp;›&nbsp; ".join(
        f'<span style="color:{COLOR_SECONDARY if i == len(items)-1 else "#64748B"};'
        f'font-weight:{"600" if i == len(items)-1 else "400"}">{item}</span>'
        for i, item in enumerate(items)
    )
    st.markdown(
        f'<div style="font-size:0.8rem;margin-bottom:1rem">{trail}</div>',
        unsafe_allow_html=True,
    )