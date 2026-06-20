# ============================================================
# BOA INTELLIGENT CREDIT SCORING – CONSTANTS
# ============================================================

APP_NAME = "Système Intelligent de Scoring de Crédit Professionnel"
APP_SUBTITLE = "Bank of Africa – Département Risque Crédit"
APP_VERSION = "2.0.1"

# ─── COLOR PALETTE ──────────────────────────────────────────
COLOR_PRIMARY   = "#003366"
COLOR_SECONDARY = "#D4AF37"
COLOR_BG        = "#F5F7FA"
COLOR_SUCCESS   = "#0E9F6E"
COLOR_DANGER    = "#DC2626"
COLOR_WARNING   = "#F59E0B"
COLOR_DARK      = "#1E293B"
COLOR_LIGHT     = "#FFFFFF"
COLOR_GRAY      = "#64748B"
COLOR_GRAY_LIGHT= "#E2E8F0"

# ─── CLIENT CATEGORIES ──────────────────────────────────────
CATEGORIES = {
    "Commerçant": {
        "icon": "🏪",
        "description": "Commerçant individuel, artisan ou exploitant d'un fonds de commerce.",
        "criteria_label": "Critères Commerce",
    },
    "Profession Libérale": {
        "icon": "💼",
        "description": "Médecin, avocat, architecte, expert-comptable ou toute profession réglementée.",
        "criteria_label": "Critères Profession Libérale",
    },
    "Personne Morale": {
        "icon": "🏢",
        "description": "Société commerciale, SARL, SA, SAS ou tout autre entité morale.",
        "criteria_label": "Critères Entreprise",
    },
}

# ─── BOA COMMON WEIGHTS ─────────────────────────────────────
BOA_WEIGHTS = {
    "age":              3,
    "incidents_cheques":8,
    "impayes":         12,
    "credit_bureau":   15,
    "contentieux":      8,
    "compte_gele":      5,
    "mouvements":       8,
    "rme":              7,
    "anciennete":       4,
}
BOA_TOTAL_WEIGHT = sum(BOA_WEIGHTS.values())   # 70

# ─── SPECIFIC WEIGHTS BY CATEGORY ──────────────────────────
SPECIFIC_WEIGHTS = {
    "Commerçant": {
        "transactions_digitales": 15,
        "solde_moyen":            10,
        "anciennete_commerce":     5,
    },
    "Profession Libérale": {
        "stabilite_revenus":  15,
        "anciennete_exercice":  5,
        "regularite_honoraires":10,
    },
    "Personne Morale": {
        "rentabilite":  12,
        "endettement":  10,
        "croissance_ca":  8,
    },
}

# ─── RISK CLASSES ──────────────────────────────────────────
RISK_CLASSES = {
    "A": {
        "min": 80,
        "max": 100,
        "label": "Risque Faible",
        "decision": "Accord Favorable",
        "color": COLOR_SUCCESS,
        "prob_default": "< 5 %",
        "icon": "✅",
    },
    "B": {
        "min": 65,
        "max": 79,
        "label": "Risque Modéré",
        "decision": "Accord sous Conditions",
        "color": "#16A34A",
        "prob_default": "5 – 15 %",
        "icon": "⚠️",
    },
    "C": {
        "min": 50,
        "max": 64,
        "label": "Risque Élevé",
        "decision": "Analyse Approfondie Requise",
        "color": COLOR_WARNING,
        "prob_default": "15 – 35 %",
        "icon": "🔶",
    },
    "D": {
        "min": 0,
        "max": 49,
        "label": "Risque Très Élevé",
        "decision": "Refus ou Révision du Dossier",
        "color": COLOR_DANGER,
        "prob_default": "> 35 %",
        "icon": "❌",
    },
}

# ─── LABELS FOR DISPLAY ────────────────────────────────────
CRITERIA_LABELS = {
    # BOA common
    "age":               "Âge du client",
    "incidents_cheques": "Incidents de chèques",
    "impayes":           "Impayés",
    "credit_bureau":     "Crédit Bureau",
    "contentieux":       "Contentieux",
    "compte_gele":       "Compte gelé",
    "mouvements":        "Mouvements du compte",
    "rme":               "Revenu Mensuel Estimé (RME)",
    "anciennete":        "Ancienneté bancaire",
    # Commerçant
    "transactions_digitales": "Transactions digitales",
    "solde_moyen":            "Solde moyen créditeur",
    "anciennete_commerce":    "Ancienneté du fonds de commerce",
    # Profession Libérale
    "stabilite_revenus":      "Stabilité des revenus",
    "anciennete_exercice":    "Ancienneté d'exercice",
    "regularite_honoraires":  "Régularité des honoraires",
    # Personne Morale
    "rentabilite":   "Rentabilité (EBIT / Total Actif)",
    "endettement":   "Endettement (Dettes / Fonds Propres)",
    "croissance_ca": "Croissance du Chiffre d'Affaires",
}