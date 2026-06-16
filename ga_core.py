import json
import random

STOP_PRIORITY = {"E": 5, "D": 4, "C": 3, "B": 2, "A": 1}

def load_items(path="items.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data["items"], data["truck_capacity_m3"]

def calculate_fitness(chromosome, items, capacity=65.0):
    total_volume = 0.0
    lifo_violations = 0
    loaded_items_count = 0

    # 1. Kapasite kontrolü ve yükleme
    for item_idx in chromosome:
        item = items[item_idx]
        if total_volume + item["volume"] <= capacity:
            total_volume += item["volume"]
            loaded_items_count += 1
        else:
            break

    # 2. LIFO (sıra) kontrolü
    for i in range(loaded_items_count - 1):
        current_stop = items[chromosome[i]]["stop"]
        next_stop = items[chromosome[i+1]]["stop"]
        if STOP_PRIORITY[current_stop] < STOP_PRIORITY[next_stop]:
            lifo_violations += 1

    max_possible_violations = max(1, loaded_items_count - 1)
    order_score = 1.0 - (lifo_violations / max_possible_violations)

    # 3. Bölge dengesi (YENİ balance_score)
    # Yüklenen eşyaları 5 eşit bölgeye böl, her bölgedeki hacim ne kadar dengeli?
    if loaded_items_count == 0:
        balance_score = 0.0
    else:
        zone_size = loaded_items_count / 5
        zone_volumes = [0.0] * 5
        for i in range(loaded_items_count):
            zone = min(int(i / zone_size), 4) if zone_size > 0 else 0
            zone_volumes[zone] += items[chromosome[i]]["volume"]
        mean_vol = sum(zone_volumes) / 5
        if mean_vol == 0:
            balance_score = 1.0
        else:
            std_dev = (sum((v - mean_vol)**2 for v in zone_volumes) / 5) ** 0.5
            balance_score = max(0.0, 1.0 - (std_dev / mean_vol))

    # 4. Toplam fitness
    total_fitness = (order_score * 0.7) + (balance_score * 0.3)

    return total_fitness, order_score, balance_score


def tournament_selection(population, fitnesses, k=3):
    selected_indices = random.sample(range(len(population)), k)
    best_idx = max(selected_indices, key=lambda idx: fitnesses[idx])
    return population[best_idx]

def one_point_crossover(parent1, parent2):
    cut = random.randint(1, len(parent1) - 2)
    child = parent1[:cut]
    for item in parent2:
        if item not in child:
            child.append(item)
    return child

def swap_mutation(chromosome):
    mutated = chromosome.copy()
    idx1, idx2 = random.sample(range(len(mutated)), 2)
    mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated