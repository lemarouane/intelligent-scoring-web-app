# ============================================================
# BOA INTELLIGENT CREDIT SCORING – SCORING ENGINE
# ============================================================

from utils.calculations import (
    score_age, score_incidents_cheques, score_impayes,
    score_credit_bureau, score_contentieux, score_compte_gele,
    score_mouvements, score_rme, score_anciennete,
    score_transactions_digitales, score_solde_moyen, score_anciennete_commerce,
    score_stabilite_revenus, score_anciennete_exercice, score_regularite_honoraires,
    score_rentabilite, score_endettement, score_croissance_ca,
    weighted_score, compute_final_score,
)
from utils.constants import BOA_WEIGHTS, SPECIFIC_WEIGHTS, CRITERIA_LABELS


def build_boa_scores(inputs: dict) -> dict:
    """
    Returns dict of {key: partial_score} for all BOA criteria
    from the raw inputs dict stored in session state.
    """
    scores = {}

    if "age" in inputs:
        scores["age"] = score_age(int(inputs["age"]))

    if "incidents_cheques" in inputs:
        scores["incidents_cheques"] = score_incidents_cheques(int(inputs["incidents_cheques"]))

    if "impayes" in inputs:
        scores["impayes"] = score_impayes(int(inputs["impayes"]))

    if "credit_bureau" in inputs:
        scores["credit_bureau"] = score_credit_bureau(inputs["credit_bureau"])

    if "contentieux" in inputs:
        scores["contentieux"] = score_contentieux(inputs["contentieux"])

    if "compte_gele" in inputs:
        scores["compte_gele"] = score_compte_gele(inputs["compte_gele"])

    if "mouvement_crediteur" in inputs and "montant_credit" in inputs:
        s, _ = score_mouvements(
            float(inputs["mouvement_crediteur"]),
            float(inputs["montant_credit"]),
        )
        scores["mouvements"] = s

    if "rme" in inputs and "mensualite" in inputs:
        s, _ = score_rme(float(inputs["rme"]), float(inputs["mensualite"]))
        scores["rme"] = s

    if "anciennete" in inputs:
        s, _ = score_anciennete(inputs["anciennete"])
        scores["anciennete"] = s

    return scores


def build_specific_scores(categorie: str, inputs: dict) -> dict:
    scores = {}

    if categorie == "Commerçant":
        if "transactions_digitales" in inputs:
            scores["transactions_digitales"] = score_transactions_digitales(
                inputs["transactions_digitales"]
            )
        if "solde_moyen" in inputs and "montant_credit" in inputs:
            s, _ = score_solde_moyen(
                float(inputs["solde_moyen"]), float(inputs["montant_credit"])
            )
            scores["solde_moyen"] = s
        if "anciennete_commerce" in inputs:
            scores["anciennete_commerce"] = score_anciennete_commerce(
                inputs["anciennete_commerce"]
            )

    elif categorie == "Profession Libérale":
        revenues = inputs.get("revenues", [])
        if revenues:
            s, _, _, _ = score_stabilite_revenus(revenues)
            scores["stabilite_revenus"] = s
        if "anciennete_exercice" in inputs:
            scores["anciennete_exercice"] = score_anciennete_exercice(
                inputs["anciennete_exercice"]
            )
        if "regularite_honoraires" in inputs:
            scores["regularite_honoraires"] = score_regularite_honoraires(
                int(inputs["regularite_honoraires"])
            )

    elif categorie == "Personne Morale":
        if "ebit" in inputs and "total_actif" in inputs:
            s, _ = score_rentabilite(
                float(inputs["ebit"]), float(inputs["total_actif"])
            )
            scores["rentabilite"] = s
        if "dettes" in inputs and "fonds_propres" in inputs:
            s, _ = score_endettement(
                float(inputs["dettes"]), float(inputs["fonds_propres"])
            )
            scores["endettement"] = s
        if "ca_n" in inputs and "ca_n1" in inputs:
            s, _ = score_croissance_ca(
                float(inputs["ca_n"]), float(inputs["ca_n1"])
            )
            scores["croissance_ca"] = s

    return scores


def compute_score_summary(
    categorie: str,
    boa_inputs: dict,
    specific_inputs: dict,
) -> dict:
    """
    Full pipeline: inputs → partial scores → weighted scores → final score.
    Returns a rich summary dict ready for the dashboard.
    """
    boa_scores     = build_boa_scores(boa_inputs)
    specific_scores = build_specific_scores(categorie, specific_inputs)

    spec_weights   = SPECIFIC_WEIGHTS.get(categorie, {})
    all_weights    = {**BOA_WEIGHTS, **spec_weights}
    all_scores     = {**boa_scores, **specific_scores}

    final = compute_final_score(all_scores, all_weights)

    rows = []
    for key, partial in all_scores.items():
        w  = all_weights.get(key, 0)
        ws = weighted_score(partial, w)
        rows.append({
            "key":     key,
            "label":   CRITERIA_LABELS.get(key, key),
            "poids":   w,
            "partial": partial,
            "weighted":round(ws, 2),
        })

    return {
        "boa_scores":      boa_scores,
        "specific_scores": specific_scores,
        "final":           final,
        "rows":            rows,
    }