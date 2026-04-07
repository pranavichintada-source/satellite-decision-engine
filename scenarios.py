"""Scenario definitions for the satellite simulation project.

This file stores example setups of objects and initial states. It keeps
scenario details separate from simulation and decision logic.
"""

from models import SpaceObject


def load_default_scenario() -> tuple[SpaceObject, SpaceObject]:
    satellite_a = SpaceObject("Satellite A", 0.0, 0.0, 2.0, 1.0)
    satellite_b = SpaceObject("Satellite B", 20.0, 10.0, -1.0, -1.0)
    return satellite_a, satellite_b