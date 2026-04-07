"""Data models for the satellite simulation system."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SpaceObject:
    name: str
    x: float
    y: float
    vx: float
    vy: float

    def update_position(self, time_step: float) -> None:
        self.x += self.vx * time_step
        self.y += self.vy * time_step

    def copy(self) -> "SpaceObject":
        return SpaceObject(self.name, self.x, self.y, self.vx, self.vy)

    def __str__(self) -> str:
        return (
            f"{self.name}: position=({self.x:.2f}, {self.y:.2f}), "
            f"velocity=({self.vx:.2f}, {self.vy:.2f})"
        )


@dataclass
class SimulationResult:
    closest_distance: float
    closest_step: int
    highest_risk: str
    details: Dict[str, Any]


@dataclass
class MonteCarloResult:
    average_closest_distance: float
    worst_closest_distance: float
    most_common_risk: str
    confidence: str
    risk_counts: Dict[str, int]


@dataclass
class ActionEvaluation:
    action: str
    score: float
    fuel_cost: int
    risk_penalty: int
    result: MonteCarloResult