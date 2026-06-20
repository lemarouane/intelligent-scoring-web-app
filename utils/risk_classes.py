from utils.constants import RISK_CLASSES


def get_class(score: float) -> str:
    for cls, info in RISK_CLASSES.items():
        if info["min"] <= score <= info["max"]:
            return cls
    return "D"


def get_class_info(score: float) -> dict:
    cls = get_class(score)
    return {"class": cls, **RISK_CLASSES[cls]}


def get_prob_default(risk_class: str) -> str:
    return RISK_CLASSES.get(risk_class, RISK_CLASSES["D"])["prob_default"]