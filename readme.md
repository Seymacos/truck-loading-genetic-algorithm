# Truck Loading Problem with Genetic Algorithm
Evolutionary Computation — Final
ŞEYMA COŞTUR
---

## What this project does

A truck with 65 m³ capacity visits five stops in order: A → B → C → D → E.
Items need to be loaded in reverse so that whatever gets unloaded first is
always closest to the door — this is the LIFO constraint. If it's violated,
the driver has to move other cargo out of the way at each stop, which defeats
the whole point. This project uses a Genetic Algorithm to find loading
arrangements that respect this constraint as much as possible.

---

## Files

- `dataset.py` — creates the item dataset
- `ga_core.py` — fitness function, crossover, mutation, selection
- `expert_solution.py` — builds a hand-crafted reference solution
- `ga_simulation.py` — runs the GA 50 times
- `statistical_analysis.py` — computes stats and saves plots

---

## Setup

```bash
pip install numpy scipy matplotlib
```

---

## How to run

```bash
python dataset.py           # run this only once
python expert_solution.py
python ga_simulation.py     # takes ~10 seconds
python statistical_analysis.py
```

Results go into `ga_results.json` and the plots are saved as PNG files.

---

## GA settings

- Population: 40
- Generations: 100
- Crossover rate: 0.90
- Mutation rate: 0.10
- Elitism: top 2 individuals carried over each generation
- Selection: tournament (k=3)
- Runs: 50 independent runs, each starting with a different random seed

---

## Results

The GA averaged a fitness of 0.955 across 50 runs, compared to 0.904 for the
expert solution. The best run reached 0.979. Each run took about 0.195 seconds.
A one-sample t-test confirmed that the difference between the GA and the expert
solution is statistically significant (p < 0.05), so the GA's better performance
is not just luck.