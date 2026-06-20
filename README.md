# 🏦 BOA – Système Intelligent de Scoring de Crédit Professionnel

> Implémentation pratique d'un mémoire de Master Finance – Bank of Africa  
> Département Risque Crédit | v2.0.1

---

## 📋 Description

Application Streamlit professionnelle d'évaluation du risque de crédit pour les clients professionnels de Bank of Africa.

Le modèle repose sur deux composantes :
- **70 %** – Critères BOA communs (9 indicateurs bancaires)
- **30 %** – Critères spécifiques par catégorie (Commerçant, Profession Libérale, Personne Morale)

---

## 🚀 Installation

```bash
# 1. Cloner / copier le projet
cd BOA_Scoring_Intelligent

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API
cp .env.example .env
# Éditez .env et ajoutez votre GITHUB_TOKEN
```

---

## ⚙️ Configuration

Créez un fichier `.env` à la racine :

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Obtenez votre token sur : https://github.com/settings/tokens  
Le modèle utilisé est `openai/gpt-4o-mini` via GitHub Models.

---

## ▶️ Lancement

```bash
streamlit run app.py
```

---

## 🗂️ Structure du projet

```
BOA_Scoring_Intelligent/
├── app.py                      # Point d'entrée principal
├── pages/
│   ├── 1_Accueil.py            # Page d'accueil hero
│   ├── 2_Selection_Client.py   # Sélection du profil client
│   ├── 3_Formulaire_Scoring.py # Formulaire dynamique + calcul temps réel
│   └── 4_Dashboard_Resultats.py# Dashboard + graphiques + IA + exports
├── components/
│   ├── score_table.py          # Tableau de scores inline
│   └── export_buttons.py       # Boutons d'export PDF/Word/Excel
├── services/
│   ├── scoring_engine.py       # Pipeline de scoring
│   ├── llm_service.py          # Appel GitHub Models GPT
│   ├── pdf_export.py           # Export PDF ReportLab
│   ├── word_export.py          # Export Word python-docx
│   └── excel_export.py         # Export Excel openpyxl
├── utils/
│   ├── constants.py            # Poids, couleurs, classes
│   ├── calculations.py         # Toutes les formules de scoring
│   ├── helpers.py              # CSS, navigation, session state
│   └── risk_classes.py         # Grille de décision A/B/C/D
├── charts/
│   ├── radar_chart.py
│   ├── bar_chart.py
│   ├── donut_chart.py
│   ├── gauge_chart.py
│   └── waterfall_chart.py
├── models/
│   ├── client.py
│   └── score_result.py
├── prompts/
│   └── system_prompt.txt
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📊 Grille de décision

| Classe | Score    | Risque        | Décision                      |
|--------|----------|---------------|-------------------------------|
| A      | ≥ 80     | Faible        | Accord favorable              |
| B      | 65 – 79  | Modéré        | Accord sous conditions        |
| C      | 50 – 64  | Élevé         | Analyse approfondie requise   |
| D      | < 50     | Très élevé    | Refus ou révision du dossier  |

---

## 🔒 Sécurité

- La clé API est lue depuis `.env` et jamais codée en dur
- Aucune donnée client n'est stockée externement
- Le fichier `.env` est dans `.gitignore`

---

## 📄 Exports disponibles

- **PDF** – Rapport complet avec mise en page bancaire (ReportLab)
- **Word** – Document éditable avec tableaux formatés (python-docx)
- **Excel** – Classeur multi-onglets avec données et analyse IA (openpyxl)

---

*Bank of Africa – Usage interne confidentiel – © 2025*