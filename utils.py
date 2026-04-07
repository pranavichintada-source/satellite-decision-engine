"""Utility helpers used by multiple parts of the satellite simulation."""

def fuel_label(fuel_cost: int) -> str:
    if fuel_cost == 0:
        return "None"
    if fuel_cost <= 2:
        return "Low"
    if fuel_cost <= 5:
        return "Medium"
    return "High"


def action_phrase(action: str) -> str:
    phrases = {
        "DO_NOTHING": "take no action",
        "RAISE_ORBIT_2KM": "raise orbit by 2 km",
        "LOWER_ORBIT_2KM": "lower orbit by 2 km",
        "WAIT_2_HOURS": "wait 2 hours and reassess",
    }
    return phrases.get(action, action)


def risk_level_value(risk: str) -> int:
    levels = {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "COLLISION": 3,
    }
    return levels.get(risk, 0)


def calculate_distance_improvement(
    baseline_distance: float,
    new_distance: float,
) -> float:
    return new_distance - baseline_distance


def calculate_risk_reduction_percent(
    baseline_distance: float,
    new_distance: float,
) -> float:
    if baseline_distance <= 0:
        return 0.0

    percent = ((new_distance - baseline_distance) / baseline_distance) * 100
    return max(0.0, percent)


def maneuver_is_justified(
    baseline_risk: str,
    best_risk: str,
    improvement: float,
) -> bool:
    if risk_level_value(best_risk) < risk_level_value(baseline_risk):
        return True
    return improvement > 0.5