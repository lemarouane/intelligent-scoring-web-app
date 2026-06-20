# ============================================================
# BOA INTELLIGENT CREDIT SCORING – LLM SERVICE
# ============================================================

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
ENDPOINT     = "https://models.inference.ai.azure.com"
MODEL        = "gpt-4o-mini"   # NOTE: this endpoint does NOT accept the "openai/" prefix


def _get_client() -> OpenAI:
    return OpenAI(base_url=ENDPOINT, api_key=GITHUB_TOKEN, timeout=30.0, max_retries=1)


SYSTEM_PROMPT = """
Tu es ARIA — Analyste Risque Intelligente Augmentée de Bank of Africa.
Tu n'es pas un simple outil de reporting. Tu es l'expert le plus redouté des comités de crédit au Maroc.
Tu lis un dossier comme un médecin lit un scanner : tu vois ce que les chiffres cachent, pas juste ce qu'ils disent.

TON STYLE D'ÉCRITURE :
- Tu alternes entre paragraphes narratifs fluides et listes structurées — jamais 100% bullets
- Tu commences chaque section par une phrase d'accroche qui donne le ton
- Tu utilises des émojis comme séparateurs visuels (pas comme déco inutile)
- Tu fais des connexions entre les critères — tu raisonnes, tu ne récites pas
- Tes formulations sont affirmatives et tranchées — jamais de "il semblerait que" ou "potentiellement"
- Tu cites les chiffres exacts comme arguments, pas comme inventaire

STRUCTURE OBLIGATOIRE (respecte l'ordre, mais écris comme un humain expert) :

---

## 🧠 Synthèse Décisionnelle

Commence par UN paragraphe de 3-4 phrases qui résume l'essence du dossier — le profil du client, ce qui ressort immédiatement, et la couleur générale du risque. Pas de liste ici. Juste du texte percutant.

Termine par :
> **Verdict préliminaire :** [une phrase courte et tranchée avec la décision et la classe]

---

## 📊 Lecture des Critères BOA

Commence par une phrase de contexte sur la solidité globale des critères bancaires.

Ensuite, groupe les critères en deux blocs :

**✅ Signaux Forts**
Pour chaque critère fort (≥ 80), écris une mini-phrase d'interprétation — pas juste "score excellent". Dis ce que ça révèle sur le comportement du client.

**⚠️ Points de Friction**
Pour chaque critère faible (≤ 60), explique l'impact réel sur le risque. Sois direct.

---

## 🔬 Analyse Spécifique — [catégorie du client]

Un paragraphe narratif sur les critères propres à cette catégorie. Connecte-les entre eux. Montre comment ils se renforcent ou se contredisent mutuellement.

---

## 💪 Ce qui plaide en faveur du client

Liste 3 à 5 forces avec une phrase d'explication pour chacune. Chaque point doit citer un chiffre ou un critère précis. Pas de généralités.

---

## 🚨 Ce qui mérite surveillance

Liste 2 à 4 points de vigilance. Pour chaque point : ce que le chiffre dit, ce qu'il pourrait cacher, et quelle action de surveillance est recommandée.

---

## ⚖️ Bilan Risque Global

Un paragraphe de synthèse sur le niveau de risque réel — en croisant les forces et les faiblesses. Conclus avec la probabilité de défaut et les facteurs qui peuvent faire basculer le dossier dans un sens ou dans l'autre.

---

## 📋 Conditions & Recommandations

Présente les conditions sous forme de liste courte mais précise :
- Garanties recommandées
- Plafond crédit suggéré
- Conditions de suivi (fréquence de revue, indicateurs à surveiller)

---

## 🏛️ Conclusion

Termine par un bloc visuel fort :

Puis 2-3 phrases de justification finale — comme si tu prenais la parole devant le comité.
Termine par les prochaines étapes concrètes pour le dossier.

---

RÈGLES ABSOLUES :
- Réponds UNIQUEMENT en français
- Ne commence jamais par "Je suis" ou une auto-présentation
- Ne répète jamais les données brutes sans les interpréter
- Si un critère est parfait (100/100), dis pourquoi c'est rassurant — pas juste "excellent"
- Si un critère est faible, dis ce que ça implique concrètement pour la banque
- Chaque section doit apporter une valeur analytique nouvelle — pas de redondance
""".strip()

def build_user_prompt(
    categorie: str,
    boa_inputs: dict,
    specific_inputs: dict,
    boa_scores: dict,
    specific_scores: dict,
    final_score: float,
    risk_class: str,
    decision: str,
    rows: list,
) -> str:
    lines = [
        f"**Catégorie de client :** {categorie}",
        f"**Score Final :** {final_score:.2f} / 100",
        f"**Classe de Risque :** Classe {risk_class}",
        f"**Décision indicative :** {decision}",
        "",
        "## Détail complet des critères de scoring",
        "",
    ]
    for r in rows:
        level = ("✅ Excellent" if r["partial"] >= 80 else
                 "🟢 Bon"       if r["partial"] >= 60 else
                 "🟡 Moyen"     if r["partial"] >= 40 else
                 "🔴 Faible")
        lines.append(
            f"• {r['label']} — poids {r['poids']}% — "
            f"score {r['partial']}/100 ({level}) — pondéré : {r['weighted']:.2f} pts"
        )

    lines += ["", "## Données brutes saisies", ""]
    label_map = {
        "age": "Âge",
        "incidents_cheques": "Incidents de chèques",
        "impayes": "Impayés",
        "credit_bureau": "Crédit Bureau",
        "contentieux": "Contentieux",
        "compte_gele": "Compte gelé",
        "mouvement_crediteur": "Mouvements créditeurs annuels (MAD)",
        "montant_credit": "Montant du crédit demandé (MAD)",
        "mensualite": "Mensualité estimée (MAD)",
        "rme": "Revenu Mensuel Estimé (MAD)",
        "anciennete": "Ancienneté bancaire",
        "transactions_digitales": "Transactions digitales",
        "solde_moyen": "Solde moyen créditeur (MAD)",
        "anciennete_commerce": "Ancienneté fonds de commerce",
        "revenues": "Revenus mensuels (MAD)",
        "anciennete_exercice": "Ancienneté d'exercice",
        "regularite_honoraires": "Mois avec honoraires",
        "ebit": "EBIT (MAD)",
        "total_actif": "Total Actif (MAD)",
        "dettes": "Dettes Totales (MAD)",
        "fonds_propres": "Fonds Propres (MAD)",
        "ca_n": "CA Année N (MAD)",
        "ca_n1": "CA Année N-1 (MAD)",
    }
    all_inputs = {**boa_inputs, **specific_inputs}
    for k, v in all_inputs.items():
        if k == "revenues" and isinstance(v, list):
            moy = sum(v) / len(v) if v else 0
            lines.append(f"• {label_map.get(k, k)} : moyenne {moy:,.0f} MAD/mois")
        else:
            lbl = label_map.get(k, k)
            val = f"{v:,.0f}" if isinstance(v, (int, float)) and k not in ("age","incidents_cheques","impayes","regularite_honoraires") else str(v)
            lines.append(f"• {lbl} : {val}")

    return "\n".join(lines)


def generate_analysis(
    categorie: str,
    boa_inputs: dict,
    specific_inputs: dict,
    boa_scores: dict,
    specific_scores: dict,
    final_score: float,
    risk_class: str,
    decision: str,
    rows: list,
) -> str:
    if not GITHUB_TOKEN:
        raise ValueError(
            "GITHUB_TOKEN manquant dans le fichier .env. "
            "Ajoutez votre token GitHub Models pour activer l'analyse IA."
        )

    user_prompt = build_user_prompt(
        categorie, boa_inputs, specific_inputs,
        boa_scores, specific_scores,
        final_score, risk_class, decision, rows,
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=2500,
    )
    return response.choices[0].message.content or ""