# ============================================================
# BOA INTELLIGENT CREDIT SCORING – CALCULATION ENGINE
# ============================================================

import numpy as np


# ─── BOA COMMON CRITERIA ────────────────────────────────────

def score_age(age: int) -> int:
    if 30 <= age <= 55:  return 100
    if 25 <= age <= 29:  return 80
    if 56 <= age <= 60:  return 70
    if 18 <= age <= 24:  return 50
    if 61 <= age <= 65:  return 30
    return 0

def score_incidents_cheques(n: int) -> int:
    if n == 0:   return 100
    if n == 1:   return 80
    if n == 2:   return 60
    if n == 3:   return 40
    return 20

def score_impayes(n: int) -> int:
    if n == 0:   return 100
    if n == 1:   return 80
    if n == 2:   return 60
    if n == 3:   return 40
    return 20

CREDIT_BUREAU_OPTIONS = [
    "Aucun endettement",
    "Endettement faible",
    "Endettement modéré",
    "Endettement élevé",
    "Endettement très élevé",
]

def score_credit_bureau(level: str) -> int:
    mapping = {
        "Aucun endettement":    100,
        "Endettement faible":    80,
        "Endettement modéré":    60,
        "Endettement élevé":     40,
        "Endettement très élevé": 20,
    }
    return mapping.get(level, 0)

CONTENTIEUX_OPTIONS = ["Aucun", "Clôturé", "En cours"]

def score_contentieux(status: str) -> int:
    mapping = {"Aucun": 100, "Clôturé": 70, "En cours": 20}
    return mapping.get(status, 0)

COMPTE_GELE_OPTIONS = ["Jamais", "Gelé dans le passé", "Actuellement gelé"]

def score_compte_gele(status: str) -> int:
    mapping = {"Jamais": 100, "Gelé dans le passé": 50, "Actuellement gelé": 0}
    return mapping.get(status, 0)

def score_mouvements(mouvement_crediteur: float, montant_credit: float) -> tuple[int, float]:
    """Returns (score, ratio)"""
    if montant_credit <= 0:
        return 0, 0.0
    ratio = mouvement_crediteur / montant_credit
    if ratio > 10:   score = 100
    elif ratio >= 5: score = 80
    elif ratio >= 3: score = 60
    elif ratio >= 1: score = 40
    else:            score = 20
    return score, ratio

def score_rme(rme: float, mensualite: float) -> tuple[int, float]:
    if mensualite <= 0:
        return 0, 0.0
    ratio = rme / mensualite
    if ratio > 5:         score = 100
    elif ratio > 3:       score = 80
    elif ratio > 2:       score = 60
    elif ratio > 1:       score = 20
    else:                 score = 0
    return score, ratio

ANCIENNETE_OPTIONS = [
    "Moins de 3 mois",
    "3 mois à 1 an",
    "1 à 3 ans",
    "Plus de 3 ans",
]

def score_anciennete(level: str) -> tuple[int, bool]:
    """Returns (score, is_nc)"""
    if level == "Moins de 3 mois":
        return 0, True        # NC
    mapping = {
        "3 mois à 1 an": 60,
        "1 à 3 ans":      80,
        "Plus de 3 ans": 100,
    }
    return mapping.get(level, 0), False


# ─── COMMERÇANT CRITERIA ────────────────────────────────────

TRANSACTIONS_OPTIONS = [
    "Très régulière",
    "Régulière",
    "Moyennement régulière",
    "Irrégulière",
    "Très irrégulière",
]

def score_transactions_digitales(level: str) -> int:
    mapping = {
        "Très régulière":         100,
        "Régulière":               80,
        "Moyennement régulière":   60,
        "Irrégulière":             40,
        "Très irrégulière":        20,
    }
    return mapping.get(level, 0)

def score_solde_moyen(solde: float, mensualite: float):
    if mensualite <= 0:
        return 20, 0.0
    ratio = solde / mensualite
    if ratio >= 2:      score = 100
    elif ratio >= 1.5:  score = 80
    elif ratio >= 1.0:  score = 60
    elif ratio >= 0.5:  score = 40
    else:               score = 20
    return score, ratio

ANCIENNETE_COMMERCE_OPTIONS = [
    "Moins d'1 an",
    "1 à 3 ans",
    "3 à 5 ans",
    "5 à 10 ans",
    "Plus de 10 ans",
]

def score_anciennete_commerce(level: str) -> int:
    mapping = {
        "Moins d'1 an": 20,
        "1 à 3 ans":    40,
        "3 à 5 ans":    60,
        "5 à 10 ans":   80,
        "Plus de 10 ans": 100,
    }
    return mapping.get(level, 0)


# ─── PROFESSION LIBÉRALE CRITERIA ───────────────────────────

def score_stabilite_revenus(revenues: list[float]) -> tuple[int, float, float, float]:
    """Returns (score, cv_pct, mean, std)"""
    arr = np.array([r for r in revenues if r > 0], dtype=float)
    if len(arr) < 2:
        return 0, 0.0, 0.0, 0.0
    mean = float(np.mean(arr))
    std  = float(np.std(arr))
    cv   = (std / mean * 100) if mean > 0 else 999.0
    if cv < 10:    score = 100
    elif cv < 20:  score = 80
    elif cv < 30:  score = 60
    elif cv < 50:  score = 40
    else:          score = 20
    return score, cv, mean, std

ANCIENNETE_EXERCICE_OPTIONS = [
    "Moins de 2 ans",
    "2 à 4 ans",
    "4 à 7 ans",
    "7 à 10 ans",
    "Plus de 10 ans",
]

def score_anciennete_exercice(level: str) -> int:
    mapping = {
        "Moins de 2 ans": 20,
        "2 à 4 ans":      40,
        "4 à 7 ans":      60,
        "7 à 10 ans":     80,
        "Plus de 10 ans": 100,
    }
    return mapping.get(level, 0)
    
def score_regularite_honoraires(mois: int) -> int:
    if mois == 12:   return 100
    if mois >= 10:   return 80
    if mois >= 8:    return 60
    if mois >= 6:    return 40
    return 20


# ─── PERSONNE MORALE CRITERIA ───────────────────────────────

def score_rentabilite(ebit: float, total_actif: float) -> tuple[int, float]:
    """Returns (score, ratio_pct)"""
    if total_actif <= 0:
        return 0, 0.0
    ratio = (ebit / total_actif) * 100
    if ratio > 15:   score = 100
    elif ratio >= 10: score = 80
    elif ratio >= 5:  score = 60
    elif ratio >= 0:  score = 40
    else:             score = 20
    return score, ratio

def score_endettement(dettes: float, fonds_propres: float) -> tuple[int, float]:
    """Returns (score, ratio)"""
    if fonds_propres <= 0:
        return 20, 999.0
    ratio = dettes / fonds_propres
    if ratio < 1:    score = 100
    elif ratio <= 2: score = 80
    elif ratio <= 4: score = 60
    elif ratio <= 6: score = 40
    else:            score = 20
    return score, ratio

def score_croissance_ca(ca_n: float, ca_n1: float) -> tuple[int, float]:
    """Returns (score, taux_pct)"""
    if ca_n1 <= 0:
        return 0, 0.0
    taux = ((ca_n - ca_n1) / ca_n1) * 100
    if taux > 20:    score = 100
    elif taux >= 10: score = 80
    elif taux >= 0:  score = 60
    elif taux >= -10: score = 40
    else:            score = 20
    return score, taux


# ─── WEIGHTED SCORE ─────────────────────────────────────────

def weighted_score(partial: int, weight: int) -> float:
    return (partial * weight) / 100


# ─── FINAL SCORE ────────────────────────────────────────────

def compute_final_score(scores: dict, weights: dict) -> float:
    total = 0.0
    for key, partial in scores.items():
        w = weights.get(key, 0)
        total += weighted_score(partial, w)
    return round(total, 2)


# ─── RISK CLASS ─────────────────────────────────────────────

def get_risk_class(score: float) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    return "D"