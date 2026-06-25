"""PAGE 2-BOA – Sélection de la catégorie (mode 100% BOA)"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY

st.set_page_config(
    page_title="BOA Credit Scoring | Sélection – Mode BOA",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("selection_boa")

# ─── MODE BADGE ──────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;
            padding:0.65rem 1.25rem;margin-bottom:1.25rem;
            display:flex;gap:0.75rem;align-items:center">
    <span style="font-size:1.1rem">🏦</span>
    <div style="font-size:0.83rem;color:#92400E">
        <strong>Mode Scoring 100% BOA :</strong> le formulaire utilisera uniquement
        les 9 critères comportementaux BOA, renormalisés sur 100 points.
        La catégorie choisie ne change pas les critères, mais reste associée au dossier.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── PAGE HEADER ─────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0 2rem">
    <div style="display:inline-block;background:#FFFBEB;border:1px solid #FDE68A;
                border-radius:999px;padding:4px 16px;color:#92400E;
                font-size:0.75rem;font-weight:700;letter-spacing:0.08em;margin-bottom:0.75rem">
        SCORING 100% BOA — ÉTAPE 1 SUR 2
    </div>
    <h2 style="font-family:'Playfair Display',serif;color:{COLOR_PRIMARY};
               font-size:2rem;margin:0 0 0.6rem;font-weight:700">
        Sélection du Profil Client
    </h2>
    <p style="color:#64748B;font-size:0.95rem;max-width:520px;margin:0 auto;line-height:1.6">
        Sélectionnez la catégorie du client. Dans ce mode, tous les profils
        utilisent les mêmes 9 critères BOA — aucun critère spécifique n'est ajouté.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── CATEGORY CARDS ──────────────────────────────────────────
card_details = {
    "Commerçant": {
        "icon": "🏪",
        "color": COLOR_PRIMARY,
        "bg":    "#EFF6FF",
        "border":"#BFDBFE",
        "desc": "Commerçant individuel, artisan ou exploitant d'un fonds de commerce enregistré.",
    },
    "Profession Libérale": {
        "icon": "💼",
        "color": "#7C3AED",
        "bg":    "#F5F3FF",
        "border":"#DDD6FE",
        "desc": "Médecin, avocat, architecte, expert-comptable ou toute profession réglementée.",
    },
    "Personne Morale": {
        "icon": "🏢",
        "color": "#0891B2",
        "bg":    "#F0FDFF",
        "border":"#A5F3FC",
        "desc": "Société commerciale : SARL, SA, SAS ou toute autre entité juridique.",
    },
}

selected = st.session_state.get("categorie")
cat_cols = st.columns(3, gap="large")

for col, (cat_name, d) in zip(cat_cols, card_details.items()):
    with col:
        is_sel  = selected == cat_name
        border  = f"2.5px solid {d['color']}" if is_sel else f"1.5px solid {d['border']}"
        bg      = d["bg"] if is_sel else "#FFFFFF"
        shadow  = f"0 6px 24px {d['color']}22" if is_sel else "0 1px 8px rgba(0,51,102,0.06)"

        badge   = (f'<div style="background:{d["color"]};color:#fff;border-radius:999px;'
                   f'padding:3px 12px;font-size:0.72rem;font-weight:700;display:inline-block;'
                   f'margin-top:0.75rem">✓ Sélectionné</div>') if is_sel else ""

        # BOA-mode: show the 9 shared BOA criteria instead of category-specific ones
        boa_note = """
<div style="margin-top:0.75rem;padding:0.6rem 0.75rem;background:rgba(255,251,235,0.8);
            border:1px solid #FDE68A;border-radius:8px">
    <div style="font-size:0.72rem;font-weight:700;color:#92400E;
                text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.3rem">
        🏦 9 critères BOA communs
    </div>
    <div style="font-size:0.75rem;color:#64748B;line-height:1.5">
        Ancienneté · Incidents · Impayés · Bureau · Garanties ·
        Domiciliation · Engagement · Secteur · Relation
    </div>
</div>"""

        st.markdown(f"""
<div style="background:{bg};border-radius:14px;padding:1.75rem 1.5rem;
            border:{border};box-shadow:{shadow};
            transition:all 0.2s;min-height:300px">
    <div style="font-size:2.5rem;margin-bottom:0.75rem">{d['icon']}</div>
    <div style="font-size:1.05rem;font-weight:800;color:{d['color']};
                margin-bottom:0.35rem">{cat_name}</div>
    <p style="font-size:0.8rem;color:#64748B;line-height:1.6;margin-bottom:0.75rem">
        {d['desc']}
    </p>
    {boa_note}
    {badge}
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        label = "✓ Sélectionné" if is_sel else f"Choisir – {cat_name}"
        if st.button(label, key=f"cat_boa_{cat_name}", use_container_width=True):
            st.session_state["categorie"] = cat_name
            st.rerun()

# ─── CONFIRM BAR ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.get("categorie"):
    cat = st.session_state["categorie"]
    d   = card_details[cat]
    st.markdown(f"""
<div style="background:{d['bg']};border:1.5px solid {d['border']};border-radius:10px;
            padding:1rem 1.5rem;display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
    <span style="font-size:1.6rem">{d['icon']}</span>
    <div>
        <div style="font-weight:700;color:{d['color']};font-size:0.9rem">
            Profil sélectionné : {cat}
        </div>
        <div style="color:#64748B;font-size:0.8rem">
            Mode 100% BOA · 9 critères communs renormalisés sur 100 pts
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    col_back, _, col_next = st.columns([1, 2, 1])
    with col_back:
        if st.button("← Retour Accueil", use_container_width=True, key="back_accueil_boa"):
            navigate("accueil")
    with col_next:
        # ── KEY DIFFERENCE: routes to formulaire_boa, not formulaire ──
        if st.button("Continuer → Formulaire BOA pur", use_container_width=True, key="next_boa"):
            navigate("formulaire_boa")
else:
    st.markdown("""
<div style="text-align:center;color:#CBD5E1;font-size:0.85rem;padding:1rem">
    ⬆️&nbsp; Sélectionnez une catégorie pour continuer
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:2.5rem;color:#CBD5E1;font-size:0.72rem">
    Bank of Africa – Scoring 100% Critères BOA &nbsp;·&nbsp;
    Document confidentiel – Usage interne &nbsp;·&nbsp; v2.0.1
</div>
""", unsafe_allow_html=True)