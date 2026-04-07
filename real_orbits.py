from datetime import datetime, timedelta, timezone

import numpy as np
from skyfield.api import load


def compute_positions(satellites, minutes=180):
    ts = load.timescale()

    start = datetime.now(timezone.utc)
    datetimes = [start + timedelta(minutes=i) for i in range(minutes)]
    times = ts.from_datetimes(datetimes)

    positions = {}

    for sat in satellites:
        geocentric = sat.at(times)
        subpoint = geocentric.subpoint()

        lat = subpoint.latitude.degrees
        lon = subpoint.longitude.degrees

        positions[sat.name] = list(zip(lat, lon))

    return positions


def compute_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def create_controlled_conjunction(
    positions_a: list[tuple[float, float]],
    positions_b: list[tuple[float, float]],
    target_step: int = 30,
    offset: tuple[float, float] = (0.4, 0.4),
) -> list[tuple[float, float]]:
    """
    Shift the second satellite's track so that near target_step it passes
    close to the first satellite. This creates a fake-but-realistic demo scenario.
    """
    if target_step >= len(positions_a) or target_step >= len(positions_b):
        return positions_b

    ax, ay = positions_a[target_step]
    bx, by = positions_b[target_step]

    shift_x = (ax + offset[0]) - bx
    shift_y = (ay + offset[1]) - by

    shifted_positions = []
    for x, y in positions_b:
        shifted_positions.append((x + shift_x, y + shift_y))

    return shifted_positions


def apply_real_action(
    positions: list[tuple[float, float]],
    action: str,
) -> list[tuple[float, float]]:
    if action == "DO_NOTHING":
        return positions[:]

    if action == "RAISE_ORBIT_2KM":
        return [(lat + 0.8, lon) for lat, lon in positions]

    if action == "LOWER_ORBIT_2KM":
        return [(lat - 0.8, lon) for lat, lon in positions]

    if action == "WAIT_2_HOURS":
        if len(positions) <= 120:
            return positions[:]
        return positions[120:]

    return positions[:]