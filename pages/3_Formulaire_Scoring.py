"""PAGE 3 – Formulaire de Scoring  (bright theme, calcul temps réel)"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar, score_color
from utils.constants import (
    COLOR_PRIMARY, COLOR_SECONDARY, BOA_WEIGHTS, SPECIFIC_WEIGHTS, CRITERIA_LABELS, RISK_CLASSES,
)
from utils.calculations import (
    score_age, score_incidents_cheques, score_impayes,
    score_credit_bureau, score_contentieux, score_compte_gele,
    score_mouvements, score_rme, score_anciennete,
    score_transactions_digitales, score_solde_moyen, score_anciennete_commerce,
    score_stabilite_revenus, score_anciennete_exercice, score_regularite_honoraires,
    score_rentabilite, score_endettement, score_croissance_ca,
    weighted_score,
    CREDIT_BUREAU_OPTIONS, CONTENTIEUX_OPTIONS, COMPTE_GELE_OPTIONS,
    ANCIENNETE_OPTIONS, TRANSACTIONS_OPTIONS, ANCIENNETE_COMMERCE_OPTIONS,
    ANCIENNETE_EXERCICE_OPTIONS,
)
from components.score_table import render_score_table
from services.llm_service import generate_analysis

st.set_page_config(
    page_title="BOA Credit Scoring | Formulaire",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("formulaire")

if not st.session_state.get("categorie"):
    st.warning("⚠️ Veuillez d'abord sélectionner une catégorie de client.")
    if st.button("← Aller à la sélection"):
        navigate("selection")
    st.stop()

categorie  = st.session_state["categorie"]
boa_inputs = st.session_state.get("boa_inputs", {})
nc_flag    = False
boa_rows   = []

# ── helper badge — label lives INSIDE the colored pill ───────
def badge(label: str, partial: int, weight: int) -> str:
    c  = score_color(partial)
    ws = weighted_score(partial, weight)
    return (
        f'<span style="background:{c}18;color:{c};border:1.5px solid {c}44;'
        f'border-radius:6px;padding:3px 12px;font-size:0.78rem;font-weight:700">'
        f'{label} {partial}/100</span>'
        f'<span style="color:#64748B;font-size:0.75rem;margin-left:0.4rem">'
        f'→ <strong style="color:{COLOR_PRIMARY}">{ws:.2f} pts</strong></span>'
    )

# ─── PAGE HEADER ─────────────────────────────────────────────
cat_icons = {"Commerçant": "🏪", "Profession Libérale": "💼", "Personne Morale": "🏢"}
cat_colors= {"Commerçant": COLOR_PRIMARY, "Profession Libérale": "#7C3AED", "Personne Morale": "#0891B2"}
cat_color = cat_colors.get(categorie, COLOR_PRIMARY)

st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;
            padding:1.25rem 1.75rem;margin-bottom:1.5rem;
            box-shadow:0 1px 8px rgba(0,51,102,0.06);
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
    <div style="display:flex;align-items:center;gap:0.75rem">
        <span style="font-size:1.8rem">{cat_icons.get(categorie,'📋')}</span>
        <div>
            <div style="font-family:'Playfair Display',serif;color:{COLOR_PRIMARY};
                        font-size:1.3rem;font-weight:700">Formulaire de Scoring</div>
            <div style="color:#64748B;font-size:0.82rem">
                Profil : <strong style="color:{cat_color}">{categorie}</strong>
                &nbsp;·&nbsp; Calcul pondéré en temps réel
            </div>
        </div>
    </div>
    <div style="display:flex;gap:0.5rem">
        <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;
                    padding:0.4rem 0.9rem;font-size:0.78rem;color:{COLOR_PRIMARY};font-weight:600">
            Section A — Critères BOA <span style="opacity:0.6">70%</span>
        </div>
        <div style="background:{cat_color}10;border:1px solid {cat_color}30;border-radius:8px;
                    padding:0.4rem 0.9rem;font-size:0.78rem;color:{cat_color};font-weight:600">
            Section B — Spécifiques <span style="opacity:0.6">30%</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SECTION A – CRITÈRES BOA COMMUNS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:linear-gradient(90deg,{COLOR_PRIMARY},#004488);
            border-radius:10px;padding:0.7rem 1.25rem;margin-bottom:1rem">
    <span style="color:#fff;font-weight:700;font-size:0.95rem">
        Section A — Critères BOA Communs
    </span>
    <span style="color:rgba(255,255,255,0.6);font-size:0.82rem;margin-left:0.75rem">
        Poids total : 70 points
    </span>
</div>
""", unsafe_allow_html=True)

col_form, col_live = st.columns([3, 2], gap="large")

with col_form:

    # 1. Âge
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">1. Âge du client</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">3%</span>
            </div>""", unsafe_allow_html=True)
        age = st.number_input("Âge (années)", min_value=18, max_value=80,
                              value=int(boa_inputs.get("age", 35)), key="f_age")
        s_age = score_age(age)
        st.markdown(badge("Score", s_age, BOA_WEIGHTS['age']), unsafe_allow_html=True)
        boa_inputs["age"] = age
        boa_rows.append({"label": CRITERIA_LABELS["age"], "poids": BOA_WEIGHTS["age"],
                         "partial": s_age, "weighted": weighted_score(s_age, BOA_WEIGHTS["age"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Incidents
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">2. Incidents de chèques</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">8%</span>
            </div>""", unsafe_allow_html=True)
        inc = st.number_input("Nombre d'incidents", min_value=0, max_value=20,
                              value=int(boa_inputs.get("incidents_cheques", 0)), key="f_inc")
        s_inc = score_incidents_cheques(inc)
        st.markdown(badge("Score", s_inc, BOA_WEIGHTS['incidents_cheques']), unsafe_allow_html=True)
        boa_inputs["incidents_cheques"] = inc
        boa_rows.append({"label": CRITERIA_LABELS["incidents_cheques"],
                         "poids": BOA_WEIGHTS["incidents_cheques"],
                         "partial": s_inc,
                         "weighted": weighted_score(s_inc, BOA_WEIGHTS["incidents_cheques"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Impayés
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">3. Impayés</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">12%</span>
            </div>""", unsafe_allow_html=True)
        imp = st.number_input("Nombre d'impayés", min_value=0, max_value=20,
                              value=int(boa_inputs.get("impayes", 0)), key="f_imp")
        s_imp = score_impayes(imp)
        st.markdown(badge("Score", s_imp, BOA_WEIGHTS['impayes']), unsafe_allow_html=True)
        boa_inputs["impayes"] = imp
        boa_rows.append({"label": CRITERIA_LABELS["impayes"], "poids": BOA_WEIGHTS["impayes"],
                         "partial": s_imp, "weighted": weighted_score(s_imp, BOA_WEIGHTS["impayes"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Crédit Bureau
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">4. Crédit Bureau</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">15%</span>
            </div>""", unsafe_allow_html=True)
        cb = st.selectbox("Niveau d'endettement", CREDIT_BUREAU_OPTIONS,
                          index=CREDIT_BUREAU_OPTIONS.index(
                              boa_inputs.get("credit_bureau", CREDIT_BUREAU_OPTIONS[0])), key="f_cb")
        s_cb = score_credit_bureau(cb)
        st.markdown(badge("Score", s_cb, BOA_WEIGHTS['credit_bureau']), unsafe_allow_html=True)
        boa_inputs["credit_bureau"] = cb
        boa_rows.append({"label": CRITERIA_LABELS["credit_bureau"],
                         "poids": BOA_WEIGHTS["credit_bureau"],
                         "partial": s_cb,
                         "weighted": weighted_score(s_cb, BOA_WEIGHTS["credit_bureau"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. Contentieux
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">5. Contentieux</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">8%</span>
            </div>""", unsafe_allow_html=True)
        cont = st.selectbox("Statut contentieux", CONTENTIEUX_OPTIONS,
                            index=CONTENTIEUX_OPTIONS.index(
                                boa_inputs.get("contentieux", CONTENTIEUX_OPTIONS[0])), key="f_cont")
        s_cont = score_contentieux(cont)
        st.markdown(badge("Score", s_cont, BOA_WEIGHTS['contentieux']), unsafe_allow_html=True)
        boa_inputs["contentieux"] = cont
        boa_rows.append({"label": CRITERIA_LABELS["contentieux"],
                         "poids": BOA_WEIGHTS["contentieux"],
                         "partial": s_cont,
                         "weighted": weighted_score(s_cont, BOA_WEIGHTS["contentieux"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 6. Compte gelé
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">6. Compte gelé</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">5%</span>
            </div>""", unsafe_allow_html=True)
        gel = st.selectbox("Statut du compte", COMPTE_GELE_OPTIONS,
                           index=COMPTE_GELE_OPTIONS.index(
                               boa_inputs.get("compte_gele", COMPTE_GELE_OPTIONS[0])), key="f_gel")
        s_gel = score_compte_gele(gel)
        st.markdown(badge("Score", s_gel, BOA_WEIGHTS['compte_gele']), unsafe_allow_html=True)
        boa_inputs["compte_gele"] = gel
        boa_rows.append({"label": CRITERIA_LABELS["compte_gele"],
                         "poids": BOA_WEIGHTS["compte_gele"],
                         "partial": s_gel,
                         "weighted": weighted_score(s_gel, BOA_WEIGHTS["compte_gele"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 7. Mouvements
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">7. Mouvements du compte</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">8%</span>
            </div>""", unsafe_allow_html=True)
        c71, c72 = st.columns(2)
        with c71:
            mvt = st.number_input("Mouvements créditeurs annuels (MAD)", min_value=0.0,
                                  value=float(boa_inputs.get("mouvement_crediteur", 500000.0)),
                                  step=10000.0, key="f_mvt", format="%.0f")
        with c72:
            mc = st.number_input("Montant du crédit demandé (MAD)", min_value=1.0,
                                 value=float(boa_inputs.get("montant_credit", 100000.0)),
                                 step=10000.0, key="f_mc", format="%.0f")
        s_mvt, r_mvt = score_mouvements(mvt, mc)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Ratio MVT/Crédit : <strong style="color:{COLOR_PRIMARY}">{r_mvt:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_mvt, BOA_WEIGHTS["mouvements"])}</div>',
            unsafe_allow_html=True)
        boa_inputs["mouvement_crediteur"] = mvt
        boa_inputs["montant_credit"]      = mc
        boa_rows.append({"label": CRITERIA_LABELS["mouvements"],
                         "poids": BOA_WEIGHTS["mouvements"],
                         "partial": s_mvt,
                         "weighted": weighted_score(s_mvt, BOA_WEIGHTS["mouvements"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 8. RME
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">8. Revenu Mensuel Estimé (RME)</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">7%</span>
            </div>""", unsafe_allow_html=True)
        c81, c82 = st.columns(2)
        with c81:
            rme = st.number_input("RME (MAD / mois)", min_value=0.0,
                                  value=float(boa_inputs.get("rme", 30000.0)),
                                  step=1000.0, key="f_rme", format="%.0f")
        with c82:
            mens = st.number_input("Mensualité estimée (MAD)", min_value=1.0,
                                   value=float(boa_inputs.get("mensualite", 5000.0)),
                                   step=500.0, key="f_mens", format="%.0f")
        s_rme, r_rme = score_rme(rme, mens)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Ratio RME/Mensualité : <strong style="color:{COLOR_PRIMARY}">{r_rme:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_rme, BOA_WEIGHTS["rme"])}</div>',
            unsafe_allow_html=True)
        boa_inputs["rme"]        = rme
        boa_inputs["mensualite"] = mens
        boa_rows.append({"label": CRITERIA_LABELS["rme"], "poids": BOA_WEIGHTS["rme"],
                         "partial": s_rme, "weighted": weighted_score(s_rme, BOA_WEIGHTS["rme"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # 9. Ancienneté
    with st.container():
        st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
            padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
                <span style="font-weight:700;color:#1E293B;font-size:0.88rem">9. Ancienneté bancaire</span>
                <span style="background:#EFF6FF;color:{COLOR_PRIMARY};border-radius:999px;
                             padding:2px 8px;font-size:0.7rem;font-weight:700">4%</span>
            </div>""", unsafe_allow_html=True)
        anc = st.selectbox("Ancienneté", ANCIENNETE_OPTIONS,
                           index=ANCIENNETE_OPTIONS.index(
                               boa_inputs.get("anciennete", ANCIENNETE_OPTIONS[2])), key="f_anc")
        s_anc, nc = score_anciennete(anc)
        if nc:
            nc_flag = True
            st.markdown(
                '<div class="nc-alert">⚠️ Client NC – Analyse complémentaire requise. '
                'Ancienneté inférieure à 3 mois.</div>', unsafe_allow_html=True)
        else:
            st.markdown(badge("Score", s_anc, BOA_WEIGHTS['anciennete']), unsafe_allow_html=True)
        boa_inputs["anciennete"] = anc
        if not nc:
            boa_rows.append({"label": CRITERIA_LABELS["anciennete"],
                             "poids": BOA_WEIGHTS["anciennete"],
                             "partial": s_anc,
                             "weighted": weighted_score(s_anc, BOA_WEIGHTS["anciennete"])})
        st.markdown("</div>", unsafe_allow_html=True)

# ── Live score panel A
with col_live:
    boa_total = sum(r["weighted"] for r in boa_rows)
    st.markdown(f"""
<div style="position:sticky;top:80px">
    <div style="background:{COLOR_PRIMARY};color:#fff;border-radius:10px 10px 0 0;
                padding:0.65rem 1rem;font-weight:700;font-size:0.88rem">
        📊 Scores en temps réel – Section A
    </div>
""", unsafe_allow_html=True)
    render_score_table(boa_rows, boa_total)
    st.markdown(f"""
    <div style="background:#F0F7FF;border:1.5px solid #BFDBFE;border-radius:0 0 10px 10px;
                padding:0.85rem 1rem;text-align:center;margin-top:-2px">
        <div style="font-size:0.72rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:0.2rem">Sous-total Section A</div>
        <div style="font-size:2.2rem;font-weight:800;color:{COLOR_PRIMARY};line-height:1">
            {boa_total:.2f}
        </div>
        <div style="font-size:0.75rem;color:#94A3B8">sur 70 points</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state["boa_inputs"] = boa_inputs
st.session_state["nc_flag"]    = nc_flag

# ═══════════════════════════════════════════════════════════════
# SECTION B – CRITÈRES SPÉCIFIQUES
# ═══════════════════════════════════════════════════════════════
specific_rows   = []
specific_inputs = st.session_state.get("specific_inputs", {})
spec_weights    = SPECIFIC_WEIGHTS.get(categorie, {})

st.markdown(f"""
<div style="background:linear-gradient(90deg,{cat_color},{cat_color}cc);
            border-radius:10px;padding:0.7rem 1.25rem;margin:1.5rem 0 1rem">
    <span style="color:#fff;font-weight:700;font-size:0.95rem">
        Section B — Critères Spécifiques : {cat_icons.get(categorie,'')} {categorie}
    </span>
    <span style="color:rgba(255,255,255,0.6);font-size:0.82rem;margin-left:0.75rem">
        Poids total : 30 points
    </span>
</div>
""", unsafe_allow_html=True)

col_b_form, col_b_live = st.columns([3, 2], gap="large")

def spec_card(num, title, pct, color):
    return f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
        padding:1.1rem 1.25rem;margin-bottom:0.75rem;box-shadow:0 1px 6px rgba(0,51,102,0.05)">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem">
            <span style="font-weight:700;color:#1E293B;font-size:0.88rem">{num}. {title}</span>
            <span style="background:{color}15;color:{color};border:1.5px solid {color}33;
                         border-radius:999px;padding:2px 8px;font-size:0.7rem;font-weight:700">
                {pct}%
            </span>
        </div>"""

with col_b_form:

    # ── COMMERÇANT ───────────────────────────────────────────
    if categorie == "Commerçant":
        st.markdown(spec_card(1,"Transactions digitales",15,cat_color), unsafe_allow_html=True)
        trans = st.selectbox("Régularité des transactions", TRANSACTIONS_OPTIONS,
                             index=TRANSACTIONS_OPTIONS.index(
                                 specific_inputs.get("transactions_digitales", TRANSACTIONS_OPTIONS[1])),
                             key="f_trans")
        s_trans = score_transactions_digitales(trans)
        st.markdown(badge("Score", s_trans, spec_weights['transactions_digitales']), unsafe_allow_html=True)
        specific_inputs["transactions_digitales"] = trans
        specific_rows.append({"label": CRITERIA_LABELS["transactions_digitales"],
                               "poids": spec_weights["transactions_digitales"],
                               "partial": s_trans,
                               "weighted": weighted_score(s_trans, spec_weights["transactions_digitales"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(2,"Solde moyen créditeur",10,cat_color), unsafe_allow_html=True)
        solde = st.number_input("Solde moyen créditeur (MAD)", min_value=0.0,
                                value=float(specific_inputs.get("solde_moyen", 50000.0)),
                                step=5000.0, key="f_solde", format="%.0f")
        montant_ref = float(boa_inputs.get("montant_credit", 100000.0))
        s_solde, r_solde = score_solde_moyen(solde, montant_ref)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Ratio : <strong style="color:{cat_color}">{r_solde:.1f}%</strong> du crédit'
            f'&nbsp;&nbsp; {badge("Score", s_solde, spec_weights["solde_moyen"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["solde_moyen"]    = solde
        specific_inputs["montant_credit"] = montant_ref
        specific_rows.append({"label": CRITERIA_LABELS["solde_moyen"],
                               "poids": spec_weights["solde_moyen"],
                               "partial": s_solde,
                               "weighted": weighted_score(s_solde, spec_weights["solde_moyen"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(3,"Ancienneté du fonds de commerce",5,cat_color), unsafe_allow_html=True)
        anc_comm = st.selectbox("Ancienneté", ANCIENNETE_COMMERCE_OPTIONS,
                                index=ANCIENNETE_COMMERCE_OPTIONS.index(
                                    specific_inputs.get("anciennete_commerce", ANCIENNETE_COMMERCE_OPTIONS[2])),
                                key="f_anc_comm")
        s_anc_comm = score_anciennete_commerce(anc_comm)
        st.markdown(badge("Score", s_anc_comm, spec_weights['anciennete_commerce']), unsafe_allow_html=True)
        specific_inputs["anciennete_commerce"] = anc_comm
        specific_rows.append({"label": CRITERIA_LABELS["anciennete_commerce"],
                               "poids": spec_weights["anciennete_commerce"],
                               "partial": s_anc_comm,
                               "weighted": weighted_score(s_anc_comm, spec_weights["anciennete_commerce"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PROFESSION LIBÉRALE ──────────────────────────────────
    elif categorie == "Profession Libérale":
        st.markdown(spec_card(1,"Stabilité des revenus",15,cat_color), unsafe_allow_html=True)
        st.caption("Saisissez les 12 revenus mensuels (MAD)")
        rev_defaults = specific_inputs.get("revenues", [30000.0]*12)
        revenues, months = [], ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]
        rcols = st.columns(4)
        for i in range(12):
            with rcols[i % 4]:
                v = st.number_input(months[i], min_value=0.0,
                                    value=float(rev_defaults[i]) if i < len(rev_defaults) else 30000.0,
                                    step=1000.0, key=f"f_rev_{i}", format="%.0f")
                revenues.append(v)
        s_stab, cv, mean_r, _ = score_stabilite_revenus(revenues)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'CV : <strong style="color:{cat_color}">{cv:.1f}%</strong> · '
            f'Moyenne : <strong style="color:{cat_color}">{mean_r:,.0f} MAD</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_stab, spec_weights["stabilite_revenus"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["revenues"] = revenues
        specific_rows.append({"label": CRITERIA_LABELS["stabilite_revenus"],
                               "poids": spec_weights["stabilite_revenus"],
                               "partial": s_stab,
                               "weighted": weighted_score(s_stab, spec_weights["stabilite_revenus"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(2,"Ancienneté d'exercice",5,cat_color), unsafe_allow_html=True)
        anc_ex = st.selectbox("Durée d'exercice", ANCIENNETE_EXERCICE_OPTIONS,
                              index=ANCIENNETE_EXERCICE_OPTIONS.index(
                                  specific_inputs.get("anciennete_exercice", ANCIENNETE_EXERCICE_OPTIONS[2])),
                              key="f_anc_ex")
        s_anc_ex = score_anciennete_exercice(anc_ex)
        st.markdown(badge("Score", s_anc_ex, spec_weights['anciennete_exercice']), unsafe_allow_html=True)
        specific_inputs["anciennete_exercice"] = anc_ex
        specific_rows.append({"label": CRITERIA_LABELS["anciennete_exercice"],
                               "poids": spec_weights["anciennete_exercice"],
                               "partial": s_anc_ex,
                               "weighted": weighted_score(s_anc_ex, spec_weights["anciennete_exercice"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(3,"Régularité des honoraires",10,cat_color), unsafe_allow_html=True)
        reg_hon = st.slider("Mois avec honoraires perçus (sur 12)", 0, 12,
                            int(specific_inputs.get("regularite_honoraires", 12)), key="f_reg_hon")
        s_reg_hon = score_regularite_honoraires(reg_hon)
        st.markdown(badge("Score", s_reg_hon, spec_weights['regularite_honoraires']), unsafe_allow_html=True)
        specific_inputs["regularite_honoraires"] = reg_hon
        specific_rows.append({"label": CRITERIA_LABELS["regularite_honoraires"],
                               "poids": spec_weights["regularite_honoraires"],
                               "partial": s_reg_hon,
                               "weighted": weighted_score(s_reg_hon, spec_weights["regularite_honoraires"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PERSONNE MORALE ──────────────────────────────────────
    elif categorie == "Personne Morale":
        st.markdown(spec_card(1,"Rentabilité  (EBIT / Total Actif)",12,cat_color), unsafe_allow_html=True)
        pm1, pm2 = st.columns(2)
        with pm1:
            ebit = st.number_input("EBIT (MAD)", value=float(specific_inputs.get("ebit", 500000.0)),
                                   step=50000.0, key="f_ebit", format="%.0f")
        with pm2:
            actif = st.number_input("Total Actif (MAD)", min_value=1.0,
                                    value=float(specific_inputs.get("total_actif", 3000000.0)),
                                    step=100000.0, key="f_actif", format="%.0f")
        s_rent, r_rent = score_rentabilite(ebit, actif)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Rentabilité : <strong style="color:{cat_color}">{r_rent:.1f}%</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_rent, spec_weights["rentabilite"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["ebit"]        = ebit
        specific_inputs["total_actif"] = actif
        specific_rows.append({"label": CRITERIA_LABELS["rentabilite"],
                               "poids": spec_weights["rentabilite"],
                               "partial": s_rent,
                               "weighted": weighted_score(s_rent, spec_weights["rentabilite"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(2,"Endettement  (Dettes / Fonds Propres)",10,cat_color), unsafe_allow_html=True)
        pm3, pm4 = st.columns(2)
        with pm3:
            dettes = st.number_input("Dettes Totales (MAD)", min_value=0.0,
                                     value=float(specific_inputs.get("dettes", 1000000.0)),
                                     step=100000.0, key="f_dettes", format="%.0f")
        with pm4:
            fp = st.number_input("Fonds Propres (MAD)", min_value=1.0,
                                 value=float(specific_inputs.get("fonds_propres", 2000000.0)),
                                 step=100000.0, key="f_fp", format="%.0f")
        s_end, r_end = score_endettement(dettes, fp)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Ratio D/FP : <strong style="color:{cat_color}">{r_end:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_end, spec_weights["endettement"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["dettes"]        = dettes
        specific_inputs["fonds_propres"] = fp
        specific_rows.append({"label": CRITERIA_LABELS["endettement"],
                               "poids": spec_weights["endettement"],
                               "partial": s_end,
                               "weighted": weighted_score(s_end, spec_weights["endettement"])})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(spec_card(3,"Croissance du Chiffre d'Affaires",8,cat_color), unsafe_allow_html=True)
        pm5, pm6 = st.columns(2)
        with pm5:
            ca_n = st.number_input("CA Année N (MAD)", min_value=0.0,
                                   value=float(specific_inputs.get("ca_n", 5000000.0)),
                                   step=100000.0, key="f_ca_n", format="%.0f")
        with pm6:
            ca_n1 = st.number_input("CA Année N-1 (MAD)", min_value=1.0,
                                    value=float(specific_inputs.get("ca_n1", 4500000.0)),
                                    step=100000.0, key="f_ca_n1", format="%.0f")
        s_ca, r_ca = score_croissance_ca(ca_n, ca_n1)
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748B;margin-top:0.3rem">'
            f'Formule : ((CA_N − CA_N₋₁) / CA_N₋₁) × 100 = '
            f'<strong style="color:{cat_color}">{r_ca:.1f}%</strong>'
            f'&nbsp;&nbsp; {badge("Score", s_ca, spec_weights["croissance_ca"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["ca_n"]  = ca_n
        specific_inputs["ca_n1"] = ca_n1
        specific_rows.append({"label": CRITERIA_LABELS["croissance_ca"],
                               "poids": spec_weights["croissance_ca"],
                               "partial": s_ca,
                               "weighted": weighted_score(s_ca, spec_weights["croissance_ca"])})
        st.markdown("</div>", unsafe_allow_html=True)

with col_b_live:
    spec_total = sum(r["weighted"] for r in specific_rows)
    st.markdown(f"""
<div style="position:sticky;top:80px">
    <div style="background:{cat_color};color:#fff;border-radius:10px 10px 0 0;
                padding:0.65rem 1rem;font-weight:700;font-size:0.88rem">
        📊 Scores en temps réel – Section B
    </div>
""", unsafe_allow_html=True)
    render_score_table(specific_rows, spec_total)
    st.markdown(f"""
    <div style="background:{cat_color}0D;border:1.5px solid {cat_color}33;
                border-radius:0 0 10px 10px;padding:0.85rem 1rem;text-align:center;margin-top:-2px">
        <div style="font-size:0.72rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:0.2rem">Sous-total Section B</div>
        <div style="font-size:2.2rem;font-weight:800;color:{cat_color};line-height:1">
            {spec_total:.2f}
        </div>
        <div style="font-size:0.75rem;color:#94A3B8">sur 30 points</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state["specific_inputs"] = specific_inputs

# ─── GRAND TOTAL ─────────────────────────────────────────────
grand_total = boa_total + spec_total
st.markdown("<br>", unsafe_allow_html=True)

if grand_total >= 80:   prov_class, prov_color = "A", "#0E9F6E"
elif grand_total >= 65: prov_class, prov_color = "B", "#16A34A"
elif grand_total >= 50: prov_class, prov_color = "C", "#F59E0B"
else:                   prov_class, prov_color = "D", "#DC2626"

st.markdown(f"""
<div style="background:#FFFFFF;border:2px solid {prov_color}44;border-radius:14px;
            padding:1.5rem 2rem;box-shadow:0 2px 16px {prov_color}18;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
    <div>
        <div style="font-size:0.75rem;color:#94A3B8;text-transform:uppercase;
                    letter-spacing:0.08em;font-weight:600">Score provisoire total</div>
        <div style="font-size:0.85rem;color:#64748B;margin-top:0.2rem">
            Section A ({boa_total:.2f} pts) + Section B ({spec_total:.2f} pts)
        </div>
        <div style="margin-top:0.5rem">
            <span style="background:{prov_color}15;color:{prov_color};border:1.5px solid {prov_color}44;
                         border-radius:999px;padding:4px 14px;font-size:0.82rem;font-weight:700">
                Classe provisoire {prov_class}
            </span>
        </div>
    </div>
    <div style="text-align:right">
        <div style="font-size:3.5rem;font-weight:800;color:{prov_color};line-height:1">
            {grand_total:.2f}
        </div>
        <div style="color:#94A3B8;font-size:0.85rem">/ 100</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col_back, _, col_calc = st.columns([1, 2, 1])
with col_back:
    if st.button("← Modifier la catégorie", use_container_width=True):
        navigate("selection")
with col_calc:
    if st.button("🎯 Calculer le Score Final & Voir le Dashboard", use_container_width=True):
        all_rows = boa_rows + specific_rows
        st.session_state["boa_scores"]      = {r["label"]: r["partial"] for r in boa_rows}
        st.session_state["specific_scores"] = {r["label"]: r["partial"] for r in specific_rows}
        st.session_state["final_score"]     = round(grand_total, 2)
        st.session_state["result_rows"]     = all_rows
        st.session_state["risk_class"]      = prov_class

        # Clear any previous analysis/error so the dashboard knows to
        # auto-trigger a fresh one for this dossier. We do NOT call the
        # AI here — calling it before navigating froze the button while
        # the page sat blank waiting on the network. The dashboard page
        # generates it on its own first load instead, where there's a
        # visible spinner and the rest of the page (scores, charts) is
        # already on screen while it works.
        st.session_state["ia_analysis"]  = None
        st.session_state["ia_error"]     = None
        st.session_state["ia_pending"]   = True

        navigate("resultats")