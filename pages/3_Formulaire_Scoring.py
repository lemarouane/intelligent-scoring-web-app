"""PAGE 3 – Formulaire de Scoring  (bright theme, calcul temps réel, layout compact 2-3 cols)"""
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

cat_icons  = {"Commerçant": "🏪", "Profession Libérale": "💼", "Personne Morale": "🏢"}
cat_colors = {"Commerçant": COLOR_PRIMARY, "Profession Libérale": "#7C3AED", "Personne Morale": "#0891B2"}
cat_color  = cat_colors.get(categorie, COLOR_PRIMARY)

# ─── HELPERS ─────────────────────────────────────────────────
def badge(label: str, partial: int, weight) -> str:
    c  = score_color(partial)
    ws = weighted_score(partial, weight) if isinstance(weight, int) else round(partial * weight / 100, 2)
    return (
        f'<span style="background:{c}18;color:{c};border:1.5px solid {c}44;'
        f'border-radius:6px;padding:2px 10px;font-size:0.76rem;font-weight:700">'
        f'{partial}/100</span>'
        f'<span style="color:#64748B;font-size:0.73rem;margin-left:0.35rem">'
        f'→ <strong style="color:{COLOR_PRIMARY}">{ws:.2f} pts</strong></span>'
    )

def field_wrap(num, title, pct, color=None):
    color = color or COLOR_PRIMARY
    return f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
        padding:0.9rem 1rem;margin-bottom:0.6rem;box-shadow:0 1px 4px rgba(0,51,102,0.04)">
        <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.5rem">
            <span style="font-weight:700;color:#1E293B;font-size:0.82rem">{num}. {title}</span>
            <span style="background:{color}12;color:{color};border:1px solid {color}30;
                         border-radius:999px;padding:1px 7px;font-size:0.67rem;font-weight:700">{pct}</span>
        </div>"""

# ─── PAGE HEADER ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;
            padding:1rem 1.5rem;margin-bottom:1rem;
            box-shadow:0 1px 8px rgba(0,51,102,0.06);
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.75rem">
    <div style="display:flex;align-items:center;gap:0.65rem">
        <span style="font-size:1.6rem">{cat_icons.get(categorie,'📋')}</span>
        <div>
            <div style="font-family:'Playfair Display',serif;color:{COLOR_PRIMARY};
                        font-size:1.2rem;font-weight:700">Formulaire de Scoring</div>
            <div style="color:#64748B;font-size:0.79rem">
                Profil : <strong style="color:{cat_color}">{categorie}</strong>
                &nbsp;·&nbsp; Calcul pondéré en temps réel
            </div>
        </div>
    </div>
    <div style="display:flex;gap:0.4rem">
        <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;
                    padding:0.35rem 0.8rem;font-size:0.75rem;color:{COLOR_PRIMARY};font-weight:600">
            Section A — BOA <span style="opacity:0.6">70%</span>
        </div>
        <div style="background:{cat_color}10;border:1px solid {cat_color}30;border-radius:8px;
                    padding:0.35rem 0.8rem;font-size:0.75rem;color:{cat_color};font-weight:600">
            Section B — Spécifiques <span style="opacity:0.6">30%</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SECTION A – CRITÈRES BOA (layout compact : 3 colonnes)
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:linear-gradient(90deg,{COLOR_PRIMARY},#004488);
            border-radius:10px;padding:0.6rem 1.1rem;margin-bottom:0.85rem">
    <span style="color:#fff;font-weight:700;font-size:0.92rem">Section A — Critères BOA Communs</span>
    <span style="color:rgba(255,255,255,0.6);font-size:0.79rem;margin-left:0.6rem">Poids total : 70 points</span>
</div>
""", unsafe_allow_html=True)

col_form, col_live = st.columns([3, 2], gap="large")

with col_form:

    # ── ROW 1 : Âge | Incidents | Impayés ────────────────────
    r1a, r1b, r1c = st.columns(3, gap="small")

    with r1a:
        st.markdown(field_wrap(1, "Âge", "3%"), unsafe_allow_html=True)
        age = st.number_input("Âge (ans)", min_value=18, max_value=80,
                              value=int(boa_inputs.get("age", 35)), key="f_age", label_visibility="collapsed")
        s_age = score_age(age)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">Âge : <strong>{age} ans</strong> &nbsp; {badge("", s_age, BOA_WEIGHTS["age"])}</div>', unsafe_allow_html=True)
        boa_inputs["age"] = age
        boa_rows.append({"label": CRITERIA_LABELS["age"], "poids": BOA_WEIGHTS["age"],
                         "partial": s_age, "weighted": weighted_score(s_age, BOA_WEIGHTS["age"])})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1b:
        st.markdown(field_wrap(2, "Incidents chèques", "8%"), unsafe_allow_html=True)
        inc = st.number_input("Incidents", min_value=0, max_value=20,
                              value=int(boa_inputs.get("incidents_cheques", 0)), key="f_inc", label_visibility="collapsed")
        s_inc = score_incidents_cheques(inc)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">Nb : <strong>{inc}</strong> &nbsp; {badge("", s_inc, BOA_WEIGHTS["incidents_cheques"])}</div>', unsafe_allow_html=True)
        boa_inputs["incidents_cheques"] = inc
        boa_rows.append({"label": CRITERIA_LABELS["incidents_cheques"], "poids": BOA_WEIGHTS["incidents_cheques"],
                         "partial": s_inc, "weighted": weighted_score(s_inc, BOA_WEIGHTS["incidents_cheques"])})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1c:
        st.markdown(field_wrap(3, "Impayés", "12%"), unsafe_allow_html=True)
        imp = st.number_input("Impayés", min_value=0, max_value=20,
                              value=int(boa_inputs.get("impayes", 0)), key="f_imp", label_visibility="collapsed")
        s_imp = score_impayes(imp)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">Nb : <strong>{imp}</strong> &nbsp; {badge("", s_imp, BOA_WEIGHTS["impayes"])}</div>', unsafe_allow_html=True)
        boa_inputs["impayes"] = imp
        boa_rows.append({"label": CRITERIA_LABELS["impayes"], "poids": BOA_WEIGHTS["impayes"],
                         "partial": s_imp, "weighted": weighted_score(s_imp, BOA_WEIGHTS["impayes"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 2 : Crédit Bureau | Contentieux | Compte gelé ────
    r2a, r2b, r2c = st.columns(3, gap="small")

    with r2a:
        st.markdown(field_wrap(4, "Crédit Bureau", "15%"), unsafe_allow_html=True)
        cb = st.selectbox("CB", CREDIT_BUREAU_OPTIONS,
                          index=CREDIT_BUREAU_OPTIONS.index(boa_inputs.get("credit_bureau", CREDIT_BUREAU_OPTIONS[0])),
                          key="f_cb", label_visibility="collapsed")
        s_cb = score_credit_bureau(cb)
        st.markdown(badge("", s_cb, BOA_WEIGHTS["credit_bureau"]), unsafe_allow_html=True)
        boa_inputs["credit_bureau"] = cb
        boa_rows.append({"label": CRITERIA_LABELS["credit_bureau"], "poids": BOA_WEIGHTS["credit_bureau"],
                         "partial": s_cb, "weighted": weighted_score(s_cb, BOA_WEIGHTS["credit_bureau"])})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2b:
        st.markdown(field_wrap(5, "Contentieux", "8%"), unsafe_allow_html=True)
        cont = st.selectbox("Cont", CONTENTIEUX_OPTIONS,
                            index=CONTENTIEUX_OPTIONS.index(boa_inputs.get("contentieux", CONTENTIEUX_OPTIONS[0])),
                            key="f_cont", label_visibility="collapsed")
        s_cont = score_contentieux(cont)
        st.markdown(badge("", s_cont, BOA_WEIGHTS["contentieux"]), unsafe_allow_html=True)
        boa_inputs["contentieux"] = cont
        boa_rows.append({"label": CRITERIA_LABELS["contentieux"], "poids": BOA_WEIGHTS["contentieux"],
                         "partial": s_cont, "weighted": weighted_score(s_cont, BOA_WEIGHTS["contentieux"])})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2c:
        st.markdown(field_wrap(6, "Compte gelé", "5%"), unsafe_allow_html=True)
        gel = st.selectbox("Gel", COMPTE_GELE_OPTIONS,
                           index=COMPTE_GELE_OPTIONS.index(boa_inputs.get("compte_gele", COMPTE_GELE_OPTIONS[0])),
                           key="f_gel", label_visibility="collapsed")
        s_gel = score_compte_gele(gel)
        st.markdown(badge("", s_gel, BOA_WEIGHTS["compte_gele"]), unsafe_allow_html=True)
        boa_inputs["compte_gele"] = gel
        boa_rows.append({"label": CRITERIA_LABELS["compte_gele"], "poids": BOA_WEIGHTS["compte_gele"],
                         "partial": s_gel, "weighted": weighted_score(s_gel, BOA_WEIGHTS["compte_gele"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 3 : Mouvements (2 champs) ─────────────────────────
    st.markdown(field_wrap(7, "Mouvements du compte", "8%"), unsafe_allow_html=True)
    m1, m2 = st.columns(2, gap="small")
    with m1:
        mvt = st.number_input("Mvt créditeurs annuels (MAD)", min_value=0.0,
                              value=float(boa_inputs.get("mouvement_crediteur", 500000.0)),
                              step=10000.0, key="f_mvt", format="%.0f")
    with m2:
        mc = st.number_input("Montant crédit demandé (MAD)", min_value=1.0,
                             value=float(boa_inputs.get("montant_credit", 100000.0)),
                             step=10000.0, key="f_mc", format="%.0f")
    s_mvt, r_mvt = score_mouvements(mvt, mc)
    st.markdown(
        f'<div style="font-size:0.75rem;color:#64748B;margin-top:0.25rem">'
        f'Ratio MVT/Crédit : <strong style="color:{COLOR_PRIMARY}">{r_mvt:.2f}x</strong>'
        f'&nbsp;&nbsp; {badge("", s_mvt, BOA_WEIGHTS["mouvements"])}</div>',
        unsafe_allow_html=True)
    boa_inputs["mouvement_crediteur"] = mvt
    boa_inputs["montant_credit"]      = mc
    boa_rows.append({"label": CRITERIA_LABELS["mouvements"], "poids": BOA_WEIGHTS["mouvements"],
                     "partial": s_mvt, "weighted": weighted_score(s_mvt, BOA_WEIGHTS["mouvements"])})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 4 : RME | Ancienneté ──────────────────────────────
    r4a, r4b = st.columns(2, gap="small")

    with r4a:
        st.markdown(field_wrap(8, "RME", "7%"), unsafe_allow_html=True)
        rme_c1, rme_c2 = st.columns(2, gap="small")
        with rme_c1:
            rme = st.number_input("RME (MAD/mois)", min_value=0.0,
                                  value=float(boa_inputs.get("rme", 30000.0)),
                                  step=1000.0, key="f_rme", format="%.0f")
        with rme_c2:
            mens = st.number_input("Mensualité (MAD)", min_value=1.0,
                                   value=float(boa_inputs.get("mensualite", 5000.0)),
                                   step=500.0, key="f_mens", format="%.0f")
        s_rme, r_rme = score_rme(rme, mens)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
            f'Ratio : <strong style="color:{COLOR_PRIMARY}">{r_rme:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge("", s_rme, BOA_WEIGHTS["rme"])}</div>',
            unsafe_allow_html=True)
        boa_inputs["rme"]        = rme
        boa_inputs["mensualite"] = mens
        boa_rows.append({"label": CRITERIA_LABELS["rme"], "poids": BOA_WEIGHTS["rme"],
                         "partial": s_rme, "weighted": weighted_score(s_rme, BOA_WEIGHTS["rme"])})
        st.markdown("</div>", unsafe_allow_html=True)

    with r4b:
        st.markdown(field_wrap(9, "Ancienneté bancaire", "4%"), unsafe_allow_html=True)
        anc = st.selectbox("Ancienneté", ANCIENNETE_OPTIONS,
                           index=ANCIENNETE_OPTIONS.index(boa_inputs.get("anciennete", ANCIENNETE_OPTIONS[2])),
                           key="f_anc", label_visibility="collapsed")
        s_anc, nc = score_anciennete(anc)
        if nc:
            nc_flag = True
            st.markdown(
                '<div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:6px;'
                'padding:4px 8px;font-size:0.72rem;color:#92400E;margin-top:0.3rem">'
                '⚠️ Client NC — Ancienneté &lt; 3 mois</div>', unsafe_allow_html=True)
        else:
            st.markdown(badge("", s_anc, BOA_WEIGHTS["anciennete"]), unsafe_allow_html=True)
        boa_inputs["anciennete"] = anc
        if not nc:
            boa_rows.append({"label": CRITERIA_LABELS["anciennete"], "poids": BOA_WEIGHTS["anciennete"],
                             "partial": s_anc, "weighted": weighted_score(s_anc, BOA_WEIGHTS["anciennete"])})
        st.markdown("</div>", unsafe_allow_html=True)

# ── Live score panel A ────────────────────────────────────────
with col_live:
    boa_total = sum(r["weighted"] for r in boa_rows)
    st.markdown(f"""
<div style="position:sticky;top:80px">
    <div style="background:{COLOR_PRIMARY};color:#fff;border-radius:10px 10px 0 0;
                padding:0.6rem 1rem;font-weight:700;font-size:0.85rem">
        📊 Scores en temps réel – Section A
    </div>
""", unsafe_allow_html=True)
    render_score_table(boa_rows, boa_total)
    st.markdown(f"""
    <div style="background:#F0F7FF;border:1.5px solid #BFDBFE;border-radius:0 0 10px 10px;
                padding:0.75rem 1rem;text-align:center;margin-top:-2px">
        <div style="font-size:0.7rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:0.15rem">Sous-total Section A</div>
        <div style="font-size:2rem;font-weight:800;color:{COLOR_PRIMARY};line-height:1">
            {boa_total:.2f}
        </div>
        <div style="font-size:0.72rem;color:#94A3B8">sur 70 points</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state["boa_inputs"] = boa_inputs
st.session_state["nc_flag"]    = nc_flag

# ═══════════════════════════════════════════════════════════════
# SECTION B – CRITÈRES SPÉCIFIQUES (layout compact aussi)
# ═══════════════════════════════════════════════════════════════
specific_rows   = []
specific_inputs = st.session_state.get("specific_inputs", {})
spec_weights    = SPECIFIC_WEIGHTS.get(categorie, {})

st.markdown(f"""
<div style="background:linear-gradient(90deg,{cat_color},{cat_color}cc);
            border-radius:10px;padding:0.6rem 1.1rem;margin:1.2rem 0 0.85rem">
    <span style="color:#fff;font-weight:700;font-size:0.92rem">
        Section B — Critères Spécifiques : {cat_icons.get(categorie,'')} {categorie}
    </span>
    <span style="color:rgba(255,255,255,0.6);font-size:0.79rem;margin-left:0.6rem">Poids total : 30 points</span>
</div>
""", unsafe_allow_html=True)

col_b_form, col_b_live = st.columns([3, 2], gap="large")

with col_b_form:

    # ── COMMERÇANT ───────────────────────────────────────────
    if categorie == "Commerçant":
        sb1, sb2 = st.columns(2, gap="small")

        with sb1:
            st.markdown(field_wrap(1, "Transactions digitales", "15%", cat_color), unsafe_allow_html=True)
            trans = st.selectbox("Trans", TRANSACTIONS_OPTIONS,
                                 index=TRANSACTIONS_OPTIONS.index(
                                     specific_inputs.get("transactions_digitales", TRANSACTIONS_OPTIONS[1])),
                                 key="f_trans", label_visibility="collapsed")
            s_trans = score_transactions_digitales(trans)
            st.markdown(badge("", s_trans, spec_weights["transactions_digitales"]), unsafe_allow_html=True)
            specific_inputs["transactions_digitales"] = trans
            specific_rows.append({"label": CRITERIA_LABELS["transactions_digitales"],
                                   "poids": spec_weights["transactions_digitales"],
                                   "partial": s_trans,
                                   "weighted": weighted_score(s_trans, spec_weights["transactions_digitales"])})
            st.markdown("</div>", unsafe_allow_html=True)

        with sb2:
            st.markdown(field_wrap(3, "Ancienneté fonds commerce", "5%", cat_color), unsafe_allow_html=True)
            anc_comm = st.selectbox("AncComm", ANCIENNETE_COMMERCE_OPTIONS,
                                    index=ANCIENNETE_COMMERCE_OPTIONS.index(
                                        specific_inputs.get("anciennete_commerce", ANCIENNETE_COMMERCE_OPTIONS[2])),
                                    key="f_anc_comm", label_visibility="collapsed")
            s_anc_comm = score_anciennete_commerce(anc_comm)
            st.markdown(badge("", s_anc_comm, spec_weights["anciennete_commerce"]), unsafe_allow_html=True)
            specific_inputs["anciennete_commerce"] = anc_comm
            specific_rows.append({"label": CRITERIA_LABELS["anciennete_commerce"],
                                   "poids": spec_weights["anciennete_commerce"],
                                   "partial": s_anc_comm,
                                   "weighted": weighted_score(s_anc_comm, spec_weights["anciennete_commerce"])})
            st.markdown("</div>", unsafe_allow_html=True)

        # Solde moyen seul (2 inputs internes)

        st.markdown(field_wrap(2, "Solde moyen créditeur", "10%", cat_color), unsafe_allow_html=True)
        sc1, sc2 = st.columns(2, gap="small")
        with sc1:
            solde = st.number_input("Solde moyen (MAD)", min_value=0.0,
                                    value=float(specific_inputs.get("solde_moyen", 50000.0)),
                                    step=5000.0, key="f_solde", format="%.0f")
        with sc2:
            mensualite_ref = float(boa_inputs.get("mensualite", 5000.0))
            st.number_input("Mensualité réf. (MAD)", value=mensualite_ref, disabled=True,
                            key="f_solde_ref", format="%.0f")
        s_solde, r_solde = score_solde_moyen(solde, mensualite_ref)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
            f'Ratio Solde/Mensualité : <strong style="color:{cat_color}">{r_solde:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge("", s_solde, spec_weights["solde_moyen"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["solde_moyen"] = solde
        specific_rows.append({"label": CRITERIA_LABELS["solde_moyen"],
                               "poids": spec_weights["solde_moyen"],
                               "partial": s_solde,
                               "weighted": weighted_score(s_solde, spec_weights["solde_moyen"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PROFESSION LIBÉRALE ──────────────────────────────────
    elif categorie == "Profession Libérale":

        # Ancienneté + Régularité côte à côte
        pl1, pl2 = st.columns(2, gap="small")
        with pl1:
            st.markdown(field_wrap(2, "Ancienneté d'exercice", "5%", cat_color), unsafe_allow_html=True)
            anc_ex = st.selectbox("AncEx", ANCIENNETE_EXERCICE_OPTIONS,
                                  index=ANCIENNETE_EXERCICE_OPTIONS.index(
                                      specific_inputs.get("anciennete_exercice", ANCIENNETE_EXERCICE_OPTIONS[2])),
                                  key="f_anc_ex", label_visibility="collapsed")
            s_anc_ex = score_anciennete_exercice(anc_ex)
            st.markdown(badge("", s_anc_ex, spec_weights["anciennete_exercice"]), unsafe_allow_html=True)
            specific_inputs["anciennete_exercice"] = anc_ex
            specific_rows.append({"label": CRITERIA_LABELS["anciennete_exercice"],
                                   "poids": spec_weights["anciennete_exercice"],
                                   "partial": s_anc_ex,
                                   "weighted": weighted_score(s_anc_ex, spec_weights["anciennete_exercice"])})
            st.markdown("</div>", unsafe_allow_html=True)

        with pl2:
            st.markdown(field_wrap(3, "Régularité honoraires", "10%", cat_color), unsafe_allow_html=True)
            reg_hon = st.slider("Mois honoraires (sur 12)", 0, 12,
                                int(specific_inputs.get("regularite_honoraires", 12)), key="f_reg_hon")
            s_reg_hon = score_regularite_honoraires(reg_hon)
            st.markdown(badge("", s_reg_hon, spec_weights["regularite_honoraires"]), unsafe_allow_html=True)
            specific_inputs["regularite_honoraires"] = reg_hon
            specific_rows.append({"label": CRITERIA_LABELS["regularite_honoraires"],
                                   "poids": spec_weights["regularite_honoraires"],
                                   "partial": s_reg_hon,
                                   "weighted": weighted_score(s_reg_hon, spec_weights["regularite_honoraires"])})
            st.markdown("</div>", unsafe_allow_html=True)

        # Stabilité des revenus — 12 champs en 4 colonnes
        st.markdown(field_wrap(1, "Stabilité des revenus (12 mois)", "15%", cat_color), unsafe_allow_html=True)
        st.caption("Revenus mensuels (MAD)")
        rev_defaults = specific_inputs.get("revenues", [30000.0] * 12)
        revenues = []
        months   = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]
        rcols    = st.columns(4)
        for i in range(12):
            with rcols[i % 4]:
                v = st.number_input(months[i], min_value=0.0,
                                    value=float(rev_defaults[i]) if i < len(rev_defaults) else 30000.0,
                                    step=1000.0, key=f"f_rev_{i}", format="%.0f")
                revenues.append(v)
        s_stab, cv, mean_r, _ = score_stabilite_revenus(revenues)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.3rem">'
            f'CV : <strong style="color:{cat_color}">{cv:.1f}%</strong> · '
            f'Moy : <strong style="color:{cat_color}">{mean_r:,.0f} MAD</strong>'
            f'&nbsp;&nbsp; {badge("", s_stab, spec_weights["stabilite_revenus"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["revenues"] = revenues
        specific_rows.append({"label": CRITERIA_LABELS["stabilite_revenus"],
                               "poids": spec_weights["stabilite_revenus"],
                               "partial": s_stab,
                               "weighted": weighted_score(s_stab, spec_weights["stabilite_revenus"])})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PERSONNE MORALE ──────────────────────────────────────
    elif categorie == "Personne Morale":

        # Rentabilité
        st.markdown(field_wrap(1, "Rentabilité  (EBIT / Total Actif)", "12%", cat_color), unsafe_allow_html=True)
        pm1, pm2 = st.columns(2, gap="small")
        with pm1:
            ebit = st.number_input("EBIT (MAD)", value=float(specific_inputs.get("ebit", 500000.0)),
                                   step=50000.0, key="f_ebit", format="%.0f")
        with pm2:
            actif = st.number_input("Total Actif (MAD)", min_value=1.0,
                                    value=float(specific_inputs.get("total_actif", 3000000.0)),
                                    step=100000.0, key="f_actif", format="%.0f")
        s_rent, r_rent = score_rentabilite(ebit, actif)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
            f'Rentabilité : <strong style="color:{cat_color}">{r_rent:.1f}%</strong>'
            f'&nbsp;&nbsp; {badge("", s_rent, spec_weights["rentabilite"])}</div>',
            unsafe_allow_html=True)
        specific_inputs["ebit"]        = ebit
        specific_inputs["total_actif"] = actif
        specific_rows.append({"label": CRITERIA_LABELS["rentabilite"],
                               "poids": spec_weights["rentabilite"],
                               "partial": s_rent,
                               "weighted": weighted_score(s_rent, spec_weights["rentabilite"])})
        st.markdown("</div>", unsafe_allow_html=True)

        # Endettement + Croissance côte à côte
        pm_r2a, pm_r2b = st.columns(2, gap="small")

        with pm_r2a:
            st.markdown(field_wrap(2, "Endettement  (D / FP)", "10%", cat_color), unsafe_allow_html=True)
            det1, det2 = st.columns(2, gap="small")
            with det1:
                dettes = st.number_input("Dettes (MAD)", min_value=0.0,
                                         value=float(specific_inputs.get("dettes", 1000000.0)),
                                         step=100000.0, key="f_dettes", format="%.0f")
            with det2:
                fp = st.number_input("Fonds propres (MAD)", min_value=1.0,
                                     value=float(specific_inputs.get("fonds_propres", 2000000.0)),
                                     step=100000.0, key="f_fp", format="%.0f")
            s_end, r_end = score_endettement(dettes, fp)
            st.markdown(
                f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
                f'D/FP : <strong style="color:{cat_color}">{r_end:.2f}x</strong>'
                f'&nbsp;&nbsp; {badge("", s_end, spec_weights["endettement"])}</div>',
                unsafe_allow_html=True)
            specific_inputs["dettes"]        = dettes
            specific_inputs["fonds_propres"] = fp
            specific_rows.append({"label": CRITERIA_LABELS["endettement"],
                                   "poids": spec_weights["endettement"],
                                   "partial": s_end,
                                   "weighted": weighted_score(s_end, spec_weights["endettement"])})
            st.markdown("</div>", unsafe_allow_html=True)

        with pm_r2b:
            st.markdown(field_wrap(3, "Croissance CA", "8%", cat_color), unsafe_allow_html=True)
            ca1, ca2 = st.columns(2, gap="small")
            with ca1:
                ca_n = st.number_input("CA N (MAD)", min_value=0.0,
                                       value=float(specific_inputs.get("ca_n", 5000000.0)),
                                       step=100000.0, key="f_ca_n", format="%.0f")
            with ca2:
                ca_n1 = st.number_input("CA N-1 (MAD)", min_value=1.0,
                                        value=float(specific_inputs.get("ca_n1", 4500000.0)),
                                        step=100000.0, key="f_ca_n1", format="%.0f")
            s_ca, r_ca = score_croissance_ca(ca_n, ca_n1)
            st.markdown(
                f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
                f'Croissance : <strong style="color:{cat_color}">{r_ca:.1f}%</strong>'
                f'&nbsp;&nbsp; {badge("", s_ca, spec_weights["croissance_ca"])}</div>',
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
                padding:0.6rem 1rem;font-weight:700;font-size:0.85rem">
        📊 Scores en temps réel – Section B
    </div>
""", unsafe_allow_html=True)
    render_score_table(specific_rows, spec_total)
    st.markdown(f"""
    <div style="background:{cat_color}0D;border:1.5px solid {cat_color}33;
                border-radius:0 0 10px 10px;padding:0.75rem 1rem;text-align:center;margin-top:-2px">
        <div style="font-size:0.7rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:0.15rem">Sous-total Section B</div>
        <div style="font-size:2rem;font-weight:800;color:{cat_color};line-height:1">
            {spec_total:.2f}
        </div>
        <div style="font-size:0.72rem;color:#94A3B8">sur 30 points</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state["specific_inputs"] = specific_inputs

# ─── GRAND TOTAL BANNER ──────────────────────────────────────
grand_total = boa_total + spec_total
st.markdown("<br>", unsafe_allow_html=True)

if grand_total >= 90:   prov_class, prov_color = "A", "#0E9F6E"
elif grand_total >= 80: prov_class, prov_color = "B", "#16A34A"
elif grand_total >= 70: prov_class, prov_color = "C", "#84CC16"
elif grand_total >= 60: prov_class, prov_color = "D", "#F59E0B"
elif grand_total >= 50: prov_class, prov_color = "E", "#F97316"
elif grand_total >= 40: prov_class, prov_color = "F", "#DC2626"
else:                   prov_class, prov_color = "G", "#7F1D1D"

st.markdown(f"""
<div style="background:#FFFFFF;border:2px solid {prov_color}44;border-radius:14px;
            padding:1.25rem 1.75rem;box-shadow:0 2px 16px {prov_color}18;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
    <div>
        <div style="font-size:0.72rem;color:#94A3B8;text-transform:uppercase;
                    letter-spacing:0.08em;font-weight:600">Évaluation provisoire</div>
        <div style="font-size:0.82rem;color:#64748B;margin-top:0.2rem">
            Section A ({boa_total:.2f} pts) + Section B ({spec_total:.2f} pts)
        </div>
        <div style="margin-top:0.5rem">
            <span style="background:{prov_color}15;color:{prov_color};border:1.5px solid {prov_color}44;
                         border-radius:999px;padding:4px 14px;font-size:0.82rem;font-weight:700">
                Classe provisoire {prov_class}
            </span>
        </div>
    </div>
    <div style="text-align:center">
        <div style="font-size:4rem;font-weight:900;color:{prov_color};line-height:1">{prov_class}</div>
        <div style="color:#94A3B8;font-size:0.75rem">classe provisoire</div>
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
        st.session_state["ia_analysis"]     = None
        st.session_state["ia_error"]        = None
        st.session_state["ia_pending"]      = True
        navigate("resultats")