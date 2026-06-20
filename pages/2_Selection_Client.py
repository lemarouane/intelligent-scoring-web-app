"""PAGE 2 – Sélection de la catégorie de client  (bright theme)"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY

st.set_page_config(
    page_title="BOA Credit Scoring | Sélection",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("selection")

# ─── PAGE HEADER ─────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0 2rem">
    <div style="display:inline-block;background:#EFF6FF;border:1px solid #BFDBFE;
                border-radius:999px;padding:4px 16px;color:{COLOR_PRIMARY};
                font-size:0.75rem;font-weight:700;letter-spacing:0.08em;margin-bottom:0.75rem">
        ÉTAPE 1 SUR 3
    </div>
    <h2 style="font-family:'Playfair Display',serif;color:{COLOR_PRIMARY};
               font-size:2rem;margin:0 0 0.6rem;font-weight:700">
        Sélection du Profil Client
    </h2>
    <p style="color:#64748B;font-size:0.95rem;max-width:520px;margin:0 auto;line-height:1.6">
        Sélectionnez la catégorie correspondant au client afin d'adapter
        les critères de scoring spécifiques.
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
        "criteria": [
            "Transactions digitales (15%)",
            "Solde moyen créditeur (10%)",
            "Ancienneté fonds de commerce (5%)",
        ],
        "desc": "Commerçant individuel, artisan ou exploitant d'un fonds de commerce enregistré.",
    },
    "Profession Libérale": {
        "icon": "💼",
        "color": "#7C3AED",
        "bg":    "#F5F3FF",
        "border":"#DDD6FE",
        "criteria": [
            "Stabilité des revenus (15%)",
            "Ancienneté d'exercice (5%)",
            "Régularité des honoraires (10%)",
        ],
        "desc": "Médecin, avocat, architecte, expert-comptable ou toute profession réglementée.",
    },
    "Personne Morale": {
        "icon": "🏢",
        "color": "#0891B2",
        "bg":    "#F0FDFF",
        "border":"#A5F3FC",
        "criteria": [
            "Rentabilité EBIT / Actif (12%)",
            "Endettement Dettes / FP (10%)",
            "Croissance du CA (8%)",
        ],
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

        criteria_html = "".join(
            f'<li style="font-size:0.78rem;color:#64748B;padding:3px 0;'
            f'border-bottom:1px solid #F1F5F9">{c}</li>'
            for c in d["criteria"]
        )

        st.markdown(f"""
<div style="background:{bg};border-radius:14px;padding:1.75rem 1.5rem;
            border:{border};box-shadow:{shadow};
            transition:all 0.2s;min-height:320px">
    <div style="font-size:2.5rem;margin-bottom:0.75rem">{d['icon']}</div>
    <div style="font-size:1.05rem;font-weight:800;color:{d['color']};
                margin-bottom:0.35rem">{cat_name}</div>
    <p style="font-size:0.8rem;color:#64748B;line-height:1.6;margin-bottom:0.9rem">
        {d['desc']}
    </p>
    <div style="font-size:0.72rem;font-weight:700;color:#94A3B8;
                text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem">
        Critères spécifiques
    </div>
    <ul style="margin:0;padding-left:1.1rem">{criteria_html}</ul>
    {badge}
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        label = f"✓ Sélectionné" if is_sel else f"Choisir – {cat_name}"
        if st.button(label, key=f"cat_{cat_name}", use_container_width=True):
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
        <div style="color:#64748B;font-size:0.8rem">{d['desc']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    col_back, _, col_next = st.columns([1, 2, 1])
    with col_back:
        if st.button("← Retour Accueil", use_container_width=True):
            navigate("accueil")
    with col_next:
        if st.button("Continuer →  Formulaire de scoring", use_container_width=True):
            navigate("formulaire")
else:
    st.markdown("""
<div style="text-align:center;color:#CBD5E1;font-size:0.85rem;padding:1rem">
    ⬆️&nbsp; Sélectionnez une catégorie pour continuer
</div>
""", unsafe_allow_html=True)
