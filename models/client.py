
# ============================================================
# comment : import des bibliothèques dataclasses et Optional
# ============================================================
from dataclasses import dataclass, field
from typing import Optional


# comment : classe qui permet de stocker les informations du client
@dataclass
class ClientProfile:
    nom: str = ""
    prenom: str = ""
    categorie: str = ""
    montant_credit: float = 0.0
    objet_credit: str = ""
    duree_mois: int = 12

    boa_inputs: dict = field(default_factory=dict)
    specific_inputs: dict = field(default_factory=dict)

    boa_scores: dict = field(default_factory=dict)
    specific_scores: dict = field(default_factory=dict)

    final_score: Optional[float] = None
    risk_class: Optional[str] = None
    nc_flag: bool = False
    ia_analysis: Optional[str] = None