# Satellite Collision Decision Engine 🚀

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![Project Type](https://img.shields.io/badge/Type-Simulation%20%7C%20AI-orange)

An uncertainty-aware decision engine that recommends optimal satellite maneuvers to minimize collision risk while balancing fuel cost and mission impact.

---

## ⚡ What this project does

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

##  Key Features

- **2D orbital simulation (prototype engine)**  
- **Collision risk classification**
  - LOW, MEDIUM, HIGH, COLLISION  
- **Action evaluation**
  - DO_NOTHING  
  - RAISE_ORBIT_2KM  
  - LOWER_ORBIT_2KM  
  - WAIT_2_HOURS  
- **Monte Carlo uncertainty modeling**
  - randomized perturbations in position and velocity  
  - multiple simulation runs per action  
- **Decision optimization**
  - balances safety, fuel cost, and risk penalty  
  - considers both average and worst-case outcomes  
- **Baseline comparison**
  - compares recommended action vs doing nothing  
- **Human-readable output**
  - explains why a maneuver is justified  

---

## 🌍 Real-Data Demo 

This project now includes a **real orbital data demo**:

- Uses real satellite data from **CelesTrak**
- Propagates orbits using **Skyfield + SGP4**
- Selects real satellites and simulates their trajectories over time
- Creates a **controlled conjunction scenario** for demonstration
- Evaluates actions on real trajectories
- Outputs a recommended action + alternative

This bridges the gap between:
- prototype simulation ✔  
- real-world orbital data ✔  

---

## 📊 Example Output

### Synthetic Decision Engine

```text
Baseline risk (DO_NOTHING): HIGH
Recommended action: raise orbit by 2 km

Closest distance: 3.13 -> 7.04 (improvement: +3.91)
Risk level: HIGH -> MEDIUM (improved)

Fuel cost: Medium
Confidence: High
Decision score: 41.81

Maneuver is justified
Real-Data Scenario
Baseline risk score: COLLISION
Recommended action: wait 2 hours and reassess
Alternative: raise orbit by 2 km

Closest distance increased from 0.57 to 30.11
Risk level: COLLISION -> LOW

Fuel cost: None
Confidence: Medium


---


🧱 Project Structure
satellite-decision-engine/
├── main.py                # Entry point
├── models.py              # Data models
├── simulator.py           # Simulation + Monte Carlo
├── decision_engine.py     # Action evaluation + scoring
├── real_orbits.py         # Real satellite propagation (Skyfield)
├── data_loader.py         # CelesTrak data ingestion
├── scenarios.py           # Synthetic scenarios
├── config.py              # Tunable parameters
└── utils.py               # Helper functions


---


🧪 How it works
Load a scenario (synthetic or real)
Simulate satellite motion
Detect closest approach
Generate possible actions
For each action:
simulate outcomes
evaluate safety + cost
Score actions
Compare against baseline
Recommend optimal decision


---


⚠️ Assumptions (Prototype)
Simplified 2D motion for synthetic simulation
Basic maneuver modeling (velocity adjustments)
Simplified fuel and risk models
Controlled conjunction scenarios for demo purposes
🔮 Future Improvements
Full orbital mechanics integration
Multi-satellite conflict handling
Real-time data ingestion pipelines
Dashboard visualization
Machine learning–based action ranking
Mission-level optimization over time


---


🚀 How to run
python main.py


---


📖 Citation and Attribution

If you use this project in research, presentations, or derivative work, please reference this repository.

This project was developed as a proof-of-concept for uncertainty-aware decision optimization in satellite collision avoidance.

For questions or collaboration, feel free to open an issue.

Last updated: April 2026