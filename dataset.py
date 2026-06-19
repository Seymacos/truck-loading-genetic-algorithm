import json
import random

def generate_and_save_dataset(num_items=30, filename="items.json"):
    # Fix the random seed so the dataset stays the same across all experiments
    random.seed(42)

    stops = ["A", "B", "C", "D", "E"]
    items = []

    for i in range(num_items):
        # Item dimensions are capped at 60x60x90 cm as stated in the assignment
        height = round(random.uniform(0.15, 0.60), 2)
        width  = round(random.uniform(0.15, 0.60), 2)
        depth  = round(random.uniform(0.20, 0.90), 2)

        volume = round(height * width * depth, 4)
        stop   = random.choice(stops)

        items.append({
            "id": i,
            "height": height,
            "width": width,
            "depth": depth,
            "volume": volume,
            "stop": stop
        })

    dataset = {
        "truck_capacity_m3": 65.0,
        "items": items
    }

    with open(filename, "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"Dataset saved to {filename} ({num_items} items, seed=42)")

if __name__ == "__main__":
    generate_and_save_dataset()