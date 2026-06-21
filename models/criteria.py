# ============================================================
# BOA INTELLIGENT CREDIT SCORING – CRITERIA MODELS
# ============================================================
"""
Structured representation of every scoring criterion used by the
engine. This complements utils/constants.py (raw weight/label maps)
by exposing a typed, iterable object that pages/components can use
to render forms and tables without hard-coding key names everywhere.
"""

# ============================================================
# comment : import des bibliothèques dataclasses et field
# ============================================================
from dataclasses import dataclass, field
# comment : import des poids et labels des critères
from utils.constants import BOA_WEIGHTS, SPECIFIC_WEIGHTS, CRITERIA_LABELS


@dataclass
class Criterion:
    key: str
    label: str
    weight: int
    category: str = "BOA"          # "BOA" | "Commerçant" | "Profession Libérale" | "Personne Morale"
    partial_score: int | None = None
    weighted_score: float | None = None
    raw_value: object = None
    is_nc: bool = False

    def compute_weighted(self) -> float:
        if self.partial_score is None:
            return 0.0
        self.weighted_score = round((self.partial_score * self.weight) / 100, 2)
        return self.weighted_score


@dataclass
class CriteriaSet:
    """A full collection of criteria for a given client category."""
    categorie: str
    criteria: list[Criterion] = field(default_factory=list)

    @property
    def total_weight(self) -> int:
        return sum(c.weight for c in self.criteria)

    @property
    def total_weighted_score(self) -> float:
        return round(sum((c.weighted_score or 0.0) for c in self.criteria), 2)

    def get(self, key: str) -> Criterion | None:
        return next((c for c in self.criteria if c.key == key), None)

    def update_score(self, key: str, partial_score: int):
        c = self.get(key)
        if c:
            c.partial_score = partial_score
            c.compute_weighted()

    def as_rows(self) -> list[dict]:
        return [
            {
                "key": c.key,
                "label": c.label,
                "poids": c.weight,
                "partial": c.partial_score,
                "weighted": c.weighted_score,
            }
            for c in self.criteria
        ]


# comment : fonction qui permet de construire les critères BOA
def build_boa_criteria_set() -> CriteriaSet:
    """BOA common criteria (70%), unweighted by category."""
    criteria = [
        Criterion(key=k, label=CRITERIA_LABELS.get(k, k), weight=w, category="BOA")
        for k, w in BOA_WEIGHTS.items()
    ]
    return CriteriaSet(categorie="BOA", criteria=criteria)


# comment : fonction qui permet de construire les critères spécifiques
def build_specific_criteria_set(categorie: str) -> CriteriaSet:
    """Category-specific criteria (30%) for the chosen client category."""
    weights = SPECIFIC_WEIGHTS.get(categorie, {})
    criteria = [
        Criterion(key=k, label=CRITERIA_LABELS.get(k, k), weight=w, category=categorie)
        for k, w in weights.items()
    ]
    return CriteriaSet(categorie=categorie, criteria=criteria)


# comment : fonction qui permet de construire l'ensemble des critères
def build_full_criteria_set(categorie: str) -> CriteriaSet:
    """Merged BOA + specific criteria set (100%) for a given category."""
    boa = build_boa_criteria_set()
    spec = build_specific_criteria_set(categorie)
    merged = CriteriaSet(categorie=categorie, criteria=boa.criteria + spec.criteria)
    return merged