"""Entry point for the satellite collision decision engine."""

import random
random.seed(42)

from config import SIMULATION_STEPS, TIME_STEP
from decision_engine import (
    choose_best_action,
    evaluate_actions,
    get_baseline_evaluation,
)
from scenarios import load_default_scenario
from utils import (
    action_phrase,
    calculate_distance_improvement,
    calculate_risk_reduction_percent,
    fuel_label,
    maneuver_is_justified,
    risk_level_value,
)


def print_action_report(evaluation) -> None:
    print(f"\nAction: {evaluation.action}")
    print(f"Average closest distance: {evaluation.result.average_closest_distance:.2f}")
    print(f"Worst closest distance: {evaluation.result.worst_closest_distance:.2f}")
    print(f"Most common risk: {evaluation.result.most_common_risk}")
    print(f"Confidence: {evaluation.result.confidence}")
    print(f"Fuel cost: {evaluation.fuel_cost}")
    print(f"Risk penalty: {evaluation.risk_penalty}")
    print(f"Total score: {evaluation.score:.2f}")
    print("-" * 40)


def print_recommendation(best_evaluation, baseline_evaluation) -> None:
    baseline_distance = baseline_evaluation.result.average_closest_distance
    best_distance = best_evaluation.result.average_closest_distance

    improvement = calculate_distance_improvement(baseline_distance, best_distance)
    risk_reduction_percent = calculate_risk_reduction_percent(
        baseline_distance,
        best_distance,
    )

    baseline_risk = baseline_evaluation.result.most_common_risk
    best_risk = best_evaluation.result.most_common_risk

    improved_text = ""
    if risk_level_value(best_risk) < risk_level_value(baseline_risk):
        improved_text = " (improved)"

    justified = maneuver_is_justified(baseline_risk, best_risk, improvement)

    print("\nRECOMMENDED ACTION")
    print("------------------")
    print(f"Baseline risk (DO_NOTHING): {baseline_risk}")
    print(f"Recommended action: {action_phrase(best_evaluation.action)}")
    print(
        f"Closest distance: {baseline_distance:.2f} -> {best_distance:.2f} "
        f"(improvement: +{improvement:.2f})"
    )
    print(f"Risk level: {baseline_risk} -> {best_risk}{improved_text}")
    print(f"Separation improvement %: {risk_reduction_percent:.1f}%")
    print(f"Fuel cost: {fuel_label(best_evaluation.fuel_cost)}")
    print(f"Confidence: {best_evaluation.result.confidence}")
    print(f"Decision score: {best_evaluation.score:.2f}")

    if justified:
        print("Maneuver is justified")
    else:
        print("Maneuver may not be necessary")


def main() -> None:
    satellite_a, satellite_b = load_default_scenario()

    print("Satellite Collision Decision Engine")
    print("-----------------------------------")
    print("Running uncertainty-aware Monte Carlo evaluation...")

    evaluations = evaluate_actions(
        satellite_a,
        satellite_b,
        SIMULATION_STEPS,
        TIME_STEP,
    )

    for evaluation in evaluations:
        print_action_report(evaluation)

    best_evaluation = choose_best_action(evaluations)
    baseline_evaluation = get_baseline_evaluation(evaluations)

    print_recommendation(best_evaluation, baseline_evaluation)


if __name__ == "__main__":
    main()