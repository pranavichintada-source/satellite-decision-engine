"""Configuration values and constants for the simulation project."""

TIME_STEP = 1.0
SIMULATION_STEPS = 10

RISK_THRESHOLDS = {
    "COLLISION": 1.0,
    "HIGH": 5.0,
    "MEDIUM": 10.0,
}

RISK_PENALTIES = {
    "LOW": 0,
    "MEDIUM": 15,
    "HIGH": 40,
    "COLLISION": 100,
}

FUEL_COSTS = {
    "DO_NOTHING": 0,
    "RAISE_ORBIT_2KM": 3,
    "LOWER_ORBIT_2KM": 3,
    "WAIT_2_HOURS": 0,
}

SCORING_WEIGHTS = {
    "average_safety": 4.0,
    "worst_case_safety": 6.0,
    "fuel": -1.0,
    "risk_penalty": -1.0,
}

MONTE_CARLO_RUNS = 50
POSITION_NOISE = 0.5
VELOCITY_NOISE = 0.2