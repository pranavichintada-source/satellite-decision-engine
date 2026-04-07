# Satellite Collision Decision Engine 🚀

An uncertainty-aware decision engine that recommends optimal satellite maneuvers to minimize collision risk while balancing fuel cost and mission impact.

---

## What this project does

Instead of just detecting collisions, this system answers a more important question:

> **What should we do about it?**

Given two satellites on a potential collision path, the system:

- simulates their motion over time
- detects how close they get
- evaluates multiple possible actions
- runs uncertainty-aware simulations (Monte Carlo)
- scores each action based on safety, fuel, and risk
- recommends the best decision

---

## Key Features

- **2D orbital simulation** (simplified physics)
- **Collision risk classification**:
  - LOW, MEDIUM, HIGH, COLLISION
- **Multiple action evaluation**:
  - DO_NOTHING
  - RAISE_ORBIT
  - LOWER_ORBIT
- **Monte Carlo uncertainty modeling**
  - random perturbations in position and velocity
  - multiple simulation runs per action
- **Decision optimization**
  - balances safety, fuel cost, and risk penalty
  - considers both average and worst-case outcomes
- **Baseline comparison**
  - compares recommended action vs doing nothing
- **Human-readable output**
  - explains why a maneuver is justified

---

## Example Output


Baseline risk (DO_NOTHING): HIGH
Recommended action: raise orbit

Closest distance: 2.80 -> 6.93 (improvement: +4.14)
Risk level: HIGH -> MEDIUM (improved)
Separation improvement %: 148.0%

Fuel cost: Low
Confidence: High
Decision score: 43.12

Maneuver is justified


---

## Project Structure


satellite-decision-engine/
├── main.py # Entry point
├── models.py # Data models
├── simulator.py # Physics + Monte Carlo simulation
├── decision_engine.py # Action evaluation + scoring
├── scenarios.py # Test scenarios
├── config.py # Tunable parameters
└── utils.py # Helper functions


---

## How it works

1. Load a scenario with two satellites  
2. Simulate their motion over time  
3. Detect closest approach distance  
4. Generate possible actions  
5. For each action:
   - run multiple simulations with uncertainty
   - measure average and worst-case outcomes  
6. Score each action:
   - maximize safety
   - minimize fuel usage
   - reduce risk  
7. Compare against baseline (DO_NOTHING)  
8. Recommend the best action  

---

## Assumptions (Prototype)

This is a simplified model:

- 2D motion instead of real orbital mechanics  
- basic velocity adjustments for maneuvers  
- simplified fuel model  
- simplified risk thresholds  
- no real satellite data yet  

These choices keep the system understandable and extensible.

---

## Future Improvements

- Real orbital mechanics using `sgp4` / `skyfield`
- Real satellite data (TLE from CelesTrak)
- Multi-satellite conflict scenarios
- Graphical visualization / dashboard
- ML-based action ranking
- Time-based decision planning

---

## How to run

```bash
python main.py

---

## 📖 Citation and Attribution

If you use this project in research, presentations, or derivative work, please reference this repository.

This project was developed as a proof-of-concept for uncertainty-aware decision optimization in satellite collision avoidance.

For questions, feedback, or collaboration ideas, feel free to open an issue or reach out.

Last updated: April 2026