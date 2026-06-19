import json
from ga_core import load_items, calculate_fitness, STOP_PRIORITY

def generate_expert_solution(items):
    # Sort items by unloading priority (E first, A last)
    # Within the same stop, larger items go first for better volume distribution
    indices = list(range(len(items)))
    indices.sort(key=lambda idx: (
        -STOP_PRIORITY[items[idx]["stop"]],
        -items[idx]["volume"]
    ))
    return indices

if __name__ == "__main__":
    items, capacity = load_items()

    expert_chromosome = generate_expert_solution(items)
    total_fit, order_score, balance_score = calculate_fitness(expert_chromosome, items, capacity)

    print("=== Expert Solution ===")
    print(f"Chromosome   : {expert_chromosome}")
    print(f"Fitness      : {total_fit:.4f}")
    print(f"Order score  : {order_score:.4f}")
    print(f"Balance score: {balance_score:.4f}")

    expert_data = {
        "chromosome": expert_chromosome,
        "fitness": total_fit,
        "order_score": order_score,
        "balance_score": balance_score
    }

    with open("expert_solution.json", "w") as f:
        json.dump(expert_data, f, indent=4)

    print("\nSaved to expert_solution.json")