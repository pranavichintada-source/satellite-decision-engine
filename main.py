"""Entry point for the satellite collision decision engine."""

import random

from config import FUEL_COSTS, RISK_PENALTIES, SIMULATION_STEPS, TIME_STEP
from data_loader import load_satellites
from decision_engine import (
    choose_best_action,
    evaluate_actions,
    get_baseline_evaluation,
)
from real_orbits import (
    apply_real_action,
    compute_positions,
    create_controlled_conjunction,
)
from scenarios import load_default_scenario
from simulator import simulate_real_positions
from utils import (
    action_phrase,
    calculate_distance_improvement,
    calculate_risk_reduction_percent,
    fuel_label,
    maneuver_is_justified,
    risk_level_value,
)

random.seed(42)


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
    separation_improvement_percent = calculate_risk_reduction_percent(
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
    print(f"Separation improvement %: {separation_improvement_percent:.1f}%")
    print(f"Fuel cost: {fuel_label(best_evaluation.fuel_cost)}")
    print(f"Confidence: {best_evaluation.result.confidence}")
    print(f"Decision score: {best_evaluation.score:.2f}")

    if justified:
        print("Maneuver is justified")
    else:
        print("Maneuver may not be necessary")


def run_synthetic_demo() -> None:
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


def score_real_result(action: str, closest_distance: float, risk: str) -> float:
    safety_score = closest_distance * 5
    fuel_penalty = FUEL_COSTS.get(action, 0)
    risk_penalty = RISK_PENALTIES.get(risk, 0)
    return safety_score - fuel_penalty - risk_penalty


def run_real_data_demo() -> None:
    print("Real Satellite Data Demo")
    print("------------------------")

    satellites = load_satellites()
    if len(satellites) < 2:
        print("Not enough satellites loaded.")
        return

    sat_a = satellites[0]
    sat_b = satellites[1]

    print(f"Satellite A: {sat_a.name}")
    print(f"Satellite B: {sat_b.name}")

    positions = compute_positions([sat_a, sat_b], minutes=180)
    positions_a = positions[sat_a.name]
    positions_b = positions[sat_b.name]

    positions_b = create_controlled_conjunction(
        positions_a,
        positions_b,
        target_step=30,
        offset=(0.4, 0.4),
    )

    actions = [
        "DO_NOTHING",
        "RAISE_ORBIT_2KM",
        "LOWER_ORBIT_2KM",
        "WAIT_2_HOURS",
    ]

    real_results = []

    for action in actions:
        action_positions_a = positions_a[:]
        action_positions_b = apply_real_action(positions_b, action)

        if action == "WAIT_2_HOURS":
            if len(action_positions_a) > 120 and len(action_positions_b) > 120:
                action_positions_a = action_positions_a[120:]
                action_positions_b = action_positions_b[: len(action_positions_a)]
        else:
            action_positions_b = action_positions_b[: len(action_positions_a)]

        result = simulate_real_positions(action_positions_a, action_positions_b)
        score = score_real_result(action, result.closest_distance, result.highest_risk)

        real_results.append(
            {
                "action": action,
                "result": result,
                "score": score,
                "fuel_cost": FUEL_COSTS.get(action, 0),
            }
        )

    real_results.sort(key=lambda item: item["score"], reverse=True)

    best = real_results[0]
    alternative = real_results[1]
    baseline = next(item for item in real_results if item["action"] == "DO_NOTHING")

    baseline_distance = baseline["result"].closest_distance
    best_distance = best["result"].closest_distance

    improved_text = ""
    if risk_level_value(best["result"].highest_risk) < risk_level_value(
        baseline["result"].highest_risk
    ):
        improved_text = " (improved)"

    print("\nControlled conjunction scenario created for demo.")
    print(f"Baseline risk score: {baseline['result'].highest_risk}")
    print(f"Recommended action: {action_phrase(best['action'])}")
    print(f"Alternative: {action_phrase(alternative['action'])}")
    print(
        f"Closest distance increased from {baseline_distance:.2f} "
        f"to {best_distance:.2f}"
    )
    print(
        f"Risk level: {baseline['result'].highest_risk} -> "
        f"{best['result'].highest_risk}{improved_text}"
    )
    print(f"Fuel cost: {fuel_label(best['fuel_cost'])}")
    print("Confidence: Medium")
    print("Why this matters:")
    print("- Prevents expensive satellite loss")
    print("- Reduces unnecessary fuel use")
    print("- Makes space operations more scalable")


def main() -> None:
    run_synthetic_demo()
    print("\n" + "=" * 50 + "\n")
    run_real_data_demo()


if __name__ == "__main__":
    main()