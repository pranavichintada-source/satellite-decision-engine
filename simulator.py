"""Simulation engine for moving objects and risk detection."""

import random
from collections import Counter

from config import (
    MONTE_CARLO_RUNS,
    POSITION_NOISE,
    RISK_THRESHOLDS,
    VELOCITY_NOISE,
)
from models import MonteCarloResult, SimulationResult, SpaceObject


def calculate_distance(obj1: SpaceObject, obj2: SpaceObject) -> float:
    return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5


def classify_risk(distance: float) -> str:
    if distance <= RISK_THRESHOLDS["COLLISION"]:
        return "COLLISION"
    if distance <= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    if distance <= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"


def simulate(
    obj1: SpaceObject,
    obj2: SpaceObject,
    steps: int,
    time_step: float,
) -> SimulationResult:
    satellite_a = obj1.copy()
    satellite_b = obj2.copy()

    closest_distance = float("inf")
    closest_step = 0
    highest_risk = "LOW"

    risk_priority = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "COLLISION": 4,
    }

    for step in range(steps):
        distance = calculate_distance(satellite_a, satellite_b)
        risk = classify_risk(distance)

        if distance < closest_distance:
            closest_distance = distance
            closest_step = step + 1

        if risk_priority[risk] > risk_priority[highest_risk]:
            highest_risk = risk

        satellite_a.update_position(time_step)
        satellite_b.update_position(time_step)

    return SimulationResult(
        closest_distance=closest_distance,
        closest_step=closest_step,
        highest_risk=highest_risk,
        details={},
    )


def perturb_object(space_object: SpaceObject) -> SpaceObject:
    perturbed = space_object.copy()
    perturbed.x += random.uniform(-POSITION_NOISE, POSITION_NOISE)
    perturbed.y += random.uniform(-POSITION_NOISE, POSITION_NOISE)
    perturbed.vx += random.uniform(-VELOCITY_NOISE, VELOCITY_NOISE)
    perturbed.vy += random.uniform(-VELOCITY_NOISE, VELOCITY_NOISE)
    return perturbed


def confidence_from_counts(risk_counts: dict[str, int], total_runs: int) -> str:
    most_common_count = max(risk_counts.values())
    consistency = most_common_count / total_runs

    if consistency >= 0.8:
        return "High"
    if consistency >= 0.6:
        return "Medium"
    return "Low"


def simulate_monte_carlo(
    obj1: SpaceObject,
    obj2: SpaceObject,
    steps: int,
    time_step: float,
    runs: int = MONTE_CARLO_RUNS,
) -> MonteCarloResult:
    closest_distances: list[float] = []
    risks: list[str] = []

    for _ in range(runs):
        perturbed_a = perturb_object(obj1)
        perturbed_b = perturb_object(obj2)

        result = simulate(perturbed_a, perturbed_b, steps, time_step)
        closest_distances.append(result.closest_distance)
        risks.append(result.highest_risk)

    average_closest_distance = sum(closest_distances) / len(closest_distances)
    worst_closest_distance = min(closest_distances)

    risk_counts = dict(Counter(risks))
    most_common_risk = max(risk_counts, key=risk_counts.get)
    confidence = confidence_from_counts(risk_counts, runs)

    return MonteCarloResult(
        average_closest_distance=average_closest_distance,
        worst_closest_distance=worst_closest_distance,
        most_common_risk=most_common_risk,
        confidence=confidence,
        risk_counts=risk_counts,
    )