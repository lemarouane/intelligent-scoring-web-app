"""PAGE – Formulaire Scoring 100% BOA  (poids renormalisés · layout compact 2-3 cols)"""
import streamlit as st
from utils.helpers import inject_global_css, init_session_state, navigate, topbar, score_color
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY, CRITERIA_LABELS
from utils.calculations import (
    score_age, score_incidents_cheques, score_impayes,
    score_credit_bureau, score_contentieux, score_compte_gele,
    score_mouvements, score_rme, score_anciennete,
    weighted_score,
    CREDIT_BUREAU_OPTIONS, CONTENTIEUX_OPTIONS, COMPTE_GELE_OPTIONS, ANCIENNETE_OPTIONS,
)
from components.score_table import render_score_table

st.set_page_config(
    page_title="BOA Credit Scoring | 100% BOA",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_global_css()
topbar("formulaire_boa")

# ─── POIDS BOA RENORMALISÉS SUR 100 ─────────────────────────
BOA_WEIGHTS_100 = {
    "age":               4.29,
    "incidents_cheques": 11.43,
    "impayes":           17.14,
    "credit_bureau":     21.43,
    "contentieux":       11.43,
    "compte_gele":        7.14,
    "mouvements":        11.43,
    "rme":               10.0,
    "anciennete":         5.71,
}

if not st.session_state.get("categorie"):
    st.warning("⚠️ Veuillez d'abord sélectionner une catégorie de client.")
    if st.button("← Aller à la sélection"):
        navigate("selection")
    st.stop()

categorie  = st.session_state["categorie"]
boa_inputs = st.session_state.get("boa_inputs_100", {})
nc_flag    = False
rows       = []

cat_icons  = {"Commerçant": "🏪", "Profession Libérale": "💼", "Personne Morale": "🏢"}
cat_colors = {"Commerçant": COLOR_PRIMARY, "Profession Libérale": "#7C3AED", "Personne Morale": "#0891B2"}
cat_color  = cat_colors.get(categorie, COLOR_PRIMARY)

# ─── HELPERS ─────────────────────────────────────────────────
def badge(partial: int, weight: float) -> str:
    from utils.helpers import score_color
    c  = score_color(partial)
    ws = round(partial * weight / 100, 2)
    return (
        f'<span style="background:{c}18;color:{c};border:1.5px solid {c}44;'
        f'border-radius:6px;padding:2px 10px;font-size:0.76rem;font-weight:700">'
        f'{partial}/100</span>'
        f'<span style="color:#64748B;font-size:0.73rem;margin-left:0.35rem">'
        f'→ <strong style="color:{COLOR_PRIMARY}">{ws:.2f} pts</strong></span>'
    )

def field_wrap(num, title, pct):
    return f"""<div style="background:#FFFFFF;border:1px solid #E8EDF4;border-radius:10px;
        padding:0.9rem 1rem;margin-bottom:0.6rem;box-shadow:0 1px 4px rgba(0,51,102,0.04)">
        <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.5rem">
            <span style="font-weight:700;color:#1E293B;font-size:0.82rem">{num}. {title}</span>
            <span style="background:{COLOR_PRIMARY}12;color:{COLOR_PRIMARY};border:1px solid {COLOR_PRIMARY}30;
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
                        font-size:1.2rem;font-weight:700">Scoring 100% Critères BOA</div>
            <div style="color:#64748B;font-size:0.79rem">
                Profil : <strong style="color:{cat_color}">{categorie}</strong>
                &nbsp;·&nbsp; Poids BOA renormalisés sur 100 pts
            </div>
        </div>
    </div>
    <div style="background:#EFF6FF;border:1.5px solid #BFDBFE;border-radius:8px;
                padding:0.4rem 0.9rem;font-size:0.79rem;color:{COLOR_PRIMARY};font-weight:700">
        🏦 9 Critères BOA — 100 points
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:10px;
            padding:0.7rem 1rem;margin-bottom:1rem;display:flex;gap:0.6rem;align-items:flex-start">
    <span style="font-size:1rem">ℹ️</span>
    <div style="font-size:0.8rem;color:#92400E;line-height:1.5">
        <strong>Mode analyse pure BOA :</strong> 9 critères comportementaux pondérés à 100%
        — sans critères spécifiques à la catégorie <em>{categorie}</em>.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── SECTION BOA ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(90deg,{COLOR_PRIMARY},#004488);
            border-radius:10px;padding:0.6rem 1.1rem;margin-bottom:0.85rem">
    <span style="color:#fff;font-weight:700;font-size:0.92rem">Critères BOA Communs — Pondération 100%</span>
    <span style="color:rgba(255,255,255,0.6);font-size:0.79rem;margin-left:0.6rem">9 critères · 100 points</span>
</div>
""", unsafe_allow_html=True)

col_form, col_live = st.columns([3, 2], gap="large")

with col_form:

    # ── ROW 1 : Âge | Incidents | Impayés ────────────────────
    r1a, r1b, r1c = st.columns(3, gap="small")

    with r1a:
        st.markdown(field_wrap(1, "Âge", "4.29%"), unsafe_allow_html=True)
        age = st.number_input("Âge (ans)", min_value=18, max_value=80,
                              value=int(boa_inputs.get("age", 35)), key="fb_age", label_visibility="collapsed")
        s = score_age(age)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">{age} ans &nbsp; {badge(s, BOA_WEIGHTS_100["age"])}</div>', unsafe_allow_html=True)
        boa_inputs["age"] = age
        rows.append({"label": CRITERIA_LABELS["age"], "poids": BOA_WEIGHTS_100["age"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["age"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1b:
        st.markdown(field_wrap(2, "Incidents chèques", "11.43%"), unsafe_allow_html=True)
        inc = st.number_input("Incidents", min_value=0, max_value=20,
                              value=int(boa_inputs.get("incidents_cheques", 0)), key="fb_inc", label_visibility="collapsed")
        s = score_incidents_cheques(inc)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">Nb : {inc} &nbsp; {badge(s, BOA_WEIGHTS_100["incidents_cheques"])}</div>', unsafe_allow_html=True)
        boa_inputs["incidents_cheques"] = inc
        rows.append({"label": CRITERIA_LABELS["incidents_cheques"], "poids": BOA_WEIGHTS_100["incidents_cheques"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["incidents_cheques"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1c:
        st.markdown(field_wrap(3, "Impayés", "17.14%"), unsafe_allow_html=True)
        imp = st.number_input("Impayés", min_value=0, max_value=20,
                              value=int(boa_inputs.get("impayes", 0)), key="fb_imp", label_visibility="collapsed")
        s = score_impayes(imp)
        st.markdown(f'<div style="font-size:0.72rem;color:#64748B">Nb : {imp} &nbsp; {badge(s, BOA_WEIGHTS_100["impayes"])}</div>', unsafe_allow_html=True)
        boa_inputs["impayes"] = imp
        rows.append({"label": CRITERIA_LABELS["impayes"], "poids": BOA_WEIGHTS_100["impayes"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["impayes"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 2 : Crédit Bureau | Contentieux | Compte gelé ────
    r2a, r2b, r2c = st.columns(3, gap="small")

    with r2a:
        st.markdown(field_wrap(4, "Crédit Bureau", "21.43%"), unsafe_allow_html=True)
        cb = st.selectbox("CB", CREDIT_BUREAU_OPTIONS,
                          index=CREDIT_BUREAU_OPTIONS.index(boa_inputs.get("credit_bureau", CREDIT_BUREAU_OPTIONS[0])),
                          key="fb_cb", label_visibility="collapsed")
        s = score_credit_bureau(cb)
        st.markdown(badge(s, BOA_WEIGHTS_100["credit_bureau"]), unsafe_allow_html=True)
        boa_inputs["credit_bureau"] = cb
        rows.append({"label": CRITERIA_LABELS["credit_bureau"], "poids": BOA_WEIGHTS_100["credit_bureau"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["credit_bureau"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2b:
        st.markdown(field_wrap(5, "Contentieux", "11.43%"), unsafe_allow_html=True)
        cont = st.selectbox("Cont", CONTENTIEUX_OPTIONS,
                            index=CONTENTIEUX_OPTIONS.index(boa_inputs.get("contentieux", CONTENTIEUX_OPTIONS[0])),
                            key="fb_cont", label_visibility="collapsed")
        s = score_contentieux(cont)
        st.markdown(badge(s, BOA_WEIGHTS_100["contentieux"]), unsafe_allow_html=True)
        boa_inputs["contentieux"] = cont
        rows.append({"label": CRITERIA_LABELS["contentieux"], "poids": BOA_WEIGHTS_100["contentieux"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["contentieux"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2c:
        st.markdown(field_wrap(6, "Compte gelé", "7.14%"), unsafe_allow_html=True)
        gel = st.selectbox("Gel", COMPTE_GELE_OPTIONS,
                           index=COMPTE_GELE_OPTIONS.index(boa_inputs.get("compte_gele", COMPTE_GELE_OPTIONS[0])),
                           key="fb_gel", label_visibility="collapsed")
        s = score_compte_gele(gel)
        st.markdown(badge(s, BOA_WEIGHTS_100["compte_gele"]), unsafe_allow_html=True)
        boa_inputs["compte_gele"] = gel
        rows.append({"label": CRITERIA_LABELS["compte_gele"], "poids": BOA_WEIGHTS_100["compte_gele"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["compte_gele"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 3 : Mouvements ───────────────────────────────────
    st.markdown(field_wrap(7, "Mouvements du compte", "11.43%"), unsafe_allow_html=True)
    m1, m2 = st.columns(2, gap="small")
    with m1:
        mvt = st.number_input("Mvt créditeurs annuels (MAD)", min_value=0.0,
                              value=float(boa_inputs.get("mouvement_crediteur", 500000.0)),
                              step=10000.0, key="fb_mvt", format="%.0f")
    with m2:
        mc = st.number_input("Montant crédit demandé (MAD)", min_value=1.0,
                             value=float(boa_inputs.get("montant_credit", 100000.0)),
                             step=10000.0, key="fb_mc", format="%.0f")
    s, r_mvt = score_mouvements(mvt, mc)
    st.markdown(
        f'<div style="font-size:0.75rem;color:#64748B;margin-top:0.25rem">'
        f'Ratio : <strong style="color:{COLOR_PRIMARY}">{r_mvt:.2f}x</strong>'
        f'&nbsp;&nbsp; {badge(s, BOA_WEIGHTS_100["mouvements"])}</div>',
        unsafe_allow_html=True)
    boa_inputs["mouvement_crediteur"] = mvt
    boa_inputs["montant_credit"]      = mc
    rows.append({"label": CRITERIA_LABELS["mouvements"], "poids": BOA_WEIGHTS_100["mouvements"],
                 "partial": s, "weighted": round(s * BOA_WEIGHTS_100["mouvements"] / 100, 2)})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── ROW 4 : RME | Ancienneté ─────────────────────────────
    r4a, r4b = st.columns(2, gap="small")

    with r4a:
        st.markdown(field_wrap(8, "RME", "10.00%"), unsafe_allow_html=True)
        rme_c1, rme_c2 = st.columns(2, gap="small")
        with rme_c1:
            rme = st.number_input("RME (MAD/mois)", min_value=0.0,
                                  value=float(boa_inputs.get("rme", 30000.0)),
                                  step=1000.0, key="fb_rme", format="%.0f")
        with rme_c2:
            mens = st.number_input("Mensualité (MAD)", min_value=1.0,
                                   value=float(boa_inputs.get("mensualite", 5000.0)),
                                   step=500.0, key="fb_mens", format="%.0f")
        s, r_rme = score_rme(rme, mens)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#64748B;margin-top:0.2rem">'
            f'Ratio : <strong style="color:{COLOR_PRIMARY}">{r_rme:.2f}x</strong>'
            f'&nbsp;&nbsp; {badge(s, BOA_WEIGHTS_100["rme"])}</div>',
            unsafe_allow_html=True)
        boa_inputs["rme"]        = rme
        boa_inputs["mensualite"] = mens
        rows.append({"label": CRITERIA_LABELS["rme"], "poids": BOA_WEIGHTS_100["rme"],
                     "partial": s, "weighted": round(s * BOA_WEIGHTS_100["rme"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

    with r4b:
        st.markdown(field_wrap(9, "Ancienneté bancaire", "5.71%"), unsafe_allow_html=True)
        anc = st.selectbox("Ancienneté", ANCIENNETE_OPTIONS,
                           index=ANCIENNETE_OPTIONS.index(boa_inputs.get("anciennete", ANCIENNETE_OPTIONS[2])),
                           key="fb_anc", label_visibility="collapsed")
        s, nc = score_anciennete(anc)
        if nc:
            nc_flag = True
            st.markdown(
                '<div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:6px;'
                'padding:4px 8px;font-size:0.72rem;color:#92400E;margin-top:0.3rem">'
                '⚠️ Client NC — Ancienneté &lt; 3 mois</div>', unsafe_allow_html=True)
        else:
            st.markdown(badge(s, BOA_WEIGHTS_100["anciennete"]), unsafe_allow_html=True)
        boa_inputs["anciennete"] = anc
        if not nc:
            rows.append({"label": CRITERIA_LABELS["anciennete"], "poids": BOA_WEIGHTS_100["anciennete"],
                         "partial": s, "weighted": round(s * BOA_WEIGHTS_100["anciennete"] / 100, 2)})
        st.markdown("</div>", unsafe_allow_html=True)

# ─── LIVE SCORE PANEL ────────────────────────────────────────
with col_live:
    total = round(sum(r["weighted"] for r in rows), 2)
    st.markdown(f"""
<div style="position:sticky;top:80px">
    <div style="background:{COLOR_PRIMARY};color:#fff;border-radius:10px 10px 0 0;
                padding:0.6rem 1rem;font-weight:700;font-size:0.85rem">
        📊 Scores en temps réel — 100% BOA
    </div>
""", unsafe_allow_html=True)
    render_score_table(rows, total)
    st.markdown(f"""
    <div style="background:#F0F7FF;border:1.5px solid #BFDBFE;border-radius:0 0 10px 10px;
                padding:0.75rem 1rem;text-align:center;margin-top:-2px">
        <div style="font-size:0.7rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:0.15rem">Score Total BOA</div>
        <div style="font-size:2rem;font-weight:800;color:{COLOR_PRIMARY};line-height:1">
            {total:.2f}
        </div>
        <div style="font-size:0.72rem;color:#94A3B8">sur 100 points</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state["boa_inputs_100"] = boa_inputs
st.session_state["nc_flag_100"]    = nc_flag

# ─── GRAND TOTAL BANNER ──────────────────────────────────────
grand_total = round(sum(r["weighted"] for r in rows), 2)

if grand_total >= 90:   prov_class, prov_color = "A", "#0E9F6E"
elif grand_total >= 80: prov_class, prov_color = "B", "#16A34A"
elif grand_total >= 70: prov_class, prov_color = "C", "#84CC16"
elif grand_total >= 60: prov_class, prov_color = "D", "#F59E0B"
elif grand_total >= 50: prov_class, prov_color = "E", "#F97316"
elif grand_total >= 40: prov_class, prov_color = "F", "#DC2626"
else:                   prov_class, prov_color = "G", "#7F1D1D"

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:#FFFFFF;border:2px solid {prov_color}44;border-radius:14px;
            padding:1.25rem 1.75rem;box-shadow:0 2px 16px {prov_color}18;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
    <div>
        <div style="font-size:0.72rem;color:#94A3B8;text-transform:uppercase;
                    letter-spacing:0.08em;font-weight:600">Évaluation BOA provisoire</div>
        <div style="font-size:0.82rem;color:#64748B;margin-top:0.2rem">
            9 critères BOA renormalisés — 100 points
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
    if st.button("🎯 Voir le Dashboard BOA", use_container_width=True):
        st.session_state["boa100_scores"]     = {r["label"]: r["partial"] for r in rows}
        st.session_state["boa100_final"]      = grand_total
        st.session_state["boa100_rows"]       = rows
        st.session_state["boa100_class"]      = prov_class
        st.session_state["boa100_ia"]         = None
        st.session_state["boa100_ia_error"]   = None
        st.session_state["boa100_ia_pending"] = True
        navigate("resultats_boa")