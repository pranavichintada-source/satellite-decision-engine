"""Decision engine for scoring and recommending satellite actions."""

from typing import List

from config import FUEL_COSTS, RISK_PENALTIES, SCORING_WEIGHTS
from models import ActionEvaluation, MonteCarloResult, SpaceObject
from simulator import simulate_monte_carlo


def generate_actions() -> List[str]:
    return [
        "DO_NOTHING",
        "RAISE_ORBIT_2KM",
        "LOWER_ORBIT_2KM",
        "WAIT_2_HOURS",
    ]


def apply_action(space_object: SpaceObject, action: str) -> SpaceObject:
    modified_object = space_object.copy()

    if action == "RAISE_ORBIT_2KM":
        modified_object.vy += 1
    elif action == "LOWER_ORBIT_2KM":
        modified_object.vy -= 1
    elif action == "WAIT_2_HOURS":
        modified_object.x += modified_object.vx * 2
        modified_object.y += modified_object.vy * 2

    return modified_object


def get_fuel_cost(action: str) -> int:
    return FUEL_COSTS.get(action, 0)


def get_risk_penalty(risk: str) -> int:
    return RISK_PENALTIES.get(risk, 0)


def score_action(action: str, monte_carlo_result: MonteCarloResult) -> float:
    average_safety_score = (
        monte_carlo_result.average_closest_distance
        * SCORING_WEIGHTS["average_safety"]
    )
    worst_case_score = (
        monte_carlo_result.worst_closest_distance
        * SCORING_WEIGHTS["worst_case_safety"]
    )
    fuel_cost = get_fuel_cost(action)
    risk_penalty = get_risk_penalty(monte_carlo_result.most_common_risk)

    return (
        average_safety_score
        + worst_case_score
        + SCORING_WEIGHTS["fuel"] * fuel_cost
        + SCORING_WEIGHTS["risk_penalty"] * risk_penalty
    )


def evaluate_actions(
    satellite_a: SpaceObject,
    satellite_b: SpaceObject,
    steps: int,
    time_step: float,
) -> List[ActionEvaluation]:
    evaluations: List[ActionEvaluation] = []

    for action in generate_actions():
        test_satellite_a = apply_action(satellite_a, action)
        monte_carlo_result = simulate_monte_carlo(
            test_satellite_a,
            satellite_b,
            steps,
            time_step,
        )

        fuel_cost = get_fuel_cost(action)
        risk_penalty = get_risk_penalty(monte_carlo_result.most_common_risk)
        score = score_action(action, monte_carlo_result)

        evaluations.append(
            ActionEvaluation(
                action=action,
                score=score,
                fuel_cost=fuel_cost,
                risk_penalty=risk_penalty,
                result=monte_carlo_result,
            )
        )

    return evaluations


def choose_best_action(evaluations: List[ActionEvaluation]) -> ActionEvaluation:
    if not evaluations:
        raise ValueError("No actions were evaluated.")
    return max(evaluations, key=lambda evaluation: evaluation.score)


def get_baseline_evaluation(
    evaluations: List[ActionEvaluation],
) -> ActionEvaluation:
    for evaluation in evaluations:
        if evaluation.action == "DO_NOTHING":
            return evaluation
    raise ValueError("Baseline DO_NOTHING evaluation not found.")