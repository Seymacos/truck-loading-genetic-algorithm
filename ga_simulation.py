import time
import json
import random
from ga_core import (
    load_items, calculate_fitness, tournament_selection,
    one_point_crossover, swap_mutation
)

POP_SIZE = 40
GENERATIONS = 100
PC = 0.90
PM = 0.10
NUM_RUNS = 50
ELITE_SIZE = 2  # keep the best 2 individuals each generation

def run_genetic_algorithm(items, capacity):
    n = len(items)

    # start with a random population
    population = []
    for _ in range(POP_SIZE):
        chrom = list(range(n))
        random.shuffle(chrom)
        population.append(chrom)

    best_chrom = None
    best_fitness = -1.0
    convergence = []  # best fitness at each generation

    for gen in range(GENERATIONS):
        fitnesses = [calculate_fitness(c, items, capacity)[0] for c in population]

        # track the best solution seen so far
        for i, fit in enumerate(fitnesses):
            if fit > best_fitness:
                best_fitness = fit
                best_chrom = population[i].copy()

        convergence.append(best_fitness)

        # sort by fitness so we can apply elitism easily
        sorted_indices = sorted(range(POP_SIZE), key=lambda i: fitnesses[i], reverse=True)
        elites = [population[i].copy() for i in sorted_indices[:ELITE_SIZE]]

        # build next generation
        new_population = elites[:]
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            if random.random() < PC:
                child1 = one_point_crossover(parent1, parent2)
                child2 = one_point_crossover(parent2, parent1)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < PM:
                child1 = swap_mutation(child1)
            if random.random() < PM:
                child2 = swap_mutation(child2)

            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    return best_chrom, best_fitness, convergence


if __name__ == "__main__":
    items, capacity = load_items()

    results = []
    all_convergence = []

    print(f"Running GA {NUM_RUNS} times independently...")

    for r in range(1, NUM_RUNS + 1):
        random.seed(r * 100)

        start = time.time()
        best_chrom, best_fit, convergence = run_genetic_algorithm(items, capacity)
        elapsed = time.time() - start

        results.append({
            "run_id": r,
            "best_chromosome": best_chrom,
            "fitness": round(best_fit, 4),
            "runtime": round(elapsed, 4)
        })
        all_convergence.append(convergence)

        if r % 10 == 0:
            print(f"  Run {r:2d}/{NUM_RUNS} done  (best fitness: {best_fit:.4f})")

    with open("ga_results.json", "w") as f:
        json.dump(results, f, indent=4)

    with open("convergence.json", "w") as f:
        json.dump(all_convergence, f)

    print("\nAll runs complete. Results saved to ga_results.json and convergence.json")