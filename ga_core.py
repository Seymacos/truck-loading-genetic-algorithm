import json
import random

# Unloading order is A -> B -> C -> D -> E, so items going to E
# should be loaded first (placed deepest) and A items loaded last (near the door)
STOP_PRIORITY = {"E": 5, "D": 4, "C": 3, "B": 2, "A": 1}

def load_items(path="items.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data["items"], data["truck_capacity_m3"]

def calculate_fitness(chromosome, items, capacity=65.0):
    total_volume = 0.0
    loaded_items_count = 0

    # Load items in chromosome order, stop when truck is full
    for item_idx in chromosome:
        item = items[item_idx]
        if total_volume + item["volume"] <= capacity:
            total_volume += item["volume"]
            loaded_items_count += 1
        else:
            break

    # Check all pairs, not just adjacent ones.
    # Item at position i is deeper in the truck than item at position j (i < j),
    # so it should have equal or higher unloading priority (loaded later = unloaded later).
    lifo_violations = 0
    for i in range(loaded_items_count):
        for j in range(i + 1, loaded_items_count):
            stop_i = items[chromosome[i]]["stop"]
            stop_j = items[chromosome[j]]["stop"]
            if STOP_PRIORITY[stop_i] < STOP_PRIORITY[stop_j]:
                lifo_violations += 1

    max_violations = max(1, loaded_items_count * (loaded_items_count - 1) // 2)
    order_score = 1.0 - (lifo_violations / max_violations)

    # Split loaded items into 5 zones and measure how evenly volume is distributed
    if loaded_items_count == 0:
        balance_score = 0.0
    else:
        zone_size    = loaded_items_count / 5
        zone_volumes = [0.0] * 5
        for i in range(loaded_items_count):
            zone = min(int(i / zone_size), 4) if zone_size > 0 else 0
            zone_volumes[zone] += items[chromosome[i]]["volume"]

        mean_vol = sum(zone_volumes) / 5
        if mean_vol == 0:
            balance_score = 1.0
        else:
            std_dev       = (sum((v - mean_vol) ** 2 for v in zone_volumes) / 5) ** 0.5
            balance_score = max(0.0, 1.0 - (std_dev / mean_vol))

    # Order compliance is weighted higher since it is the primary constraint
    total_fitness = (order_score * 0.7) + (balance_score * 0.3)

    return total_fitness, order_score, balance_score


def tournament_selection(population, fitnesses, k=3):
    # Pick k random individuals and return the best one
    contenders = random.sample(range(len(population)), k)
    best = max(contenders, key=lambda i: fitnesses[i])
    return population[best]

def one_point_crossover(parent1, parent2):
    # Take a prefix from parent1, fill the rest from parent2 in order
    cut   = random.randint(1, len(parent1) - 2)
    child = parent1[:cut]
    for item in parent2:
        if item not in child:
            child.append(item)
    return child

def swap_mutation(chromosome):
    # Swap two randomly chosen positions
    mutated    = chromosome.copy()
    i, j       = random.sample(range(len(mutated)), 2)
    mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated