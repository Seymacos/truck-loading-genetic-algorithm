import json
import random

def generate_and_save_dataset(num_items=50, filename="items.json"):
    # Tekrarlanabilirlik için random seed sabitleyelim (Ödev kuralı)
    random.seed(42) 
    
    stops = ["A", "B", "C", "D", "E"]
    items = []
    
    for i in range(num_items):
        # Ödevdeki limitler: maks 60x60x90 cm (Metre cinsinden yapalım: 0.6x0.6x0.9)
        height = round(random.uniform(0.15, 0.60), 2)
        width = round(random.uniform(0.15, 0.60), 2)
        depth = round(random.uniform(0.20, 0.90), 2)
        
        volume = round(height * width * depth, 4)
        stop = random.choice(stops)
        
        items.append({
            "id": i,
            "height": height,
            "width": width,
            "depth": depth,
            "volume": volume,
            "stop": stop
        })
        
    # Veri paketini hazırlayalım (Kamyon kapasitesi: 65 m3)
    dataset = {
        "truck_capacity_m3": 65.0,
        "items": items
    }
    
    with open(filename, "w") as f:
        json.dump(dataset, f, indent=4)
        
    print(f"=== {filename} başarıyla oluşturuldu ve sabitlendi! ===")

if __name__ == "__main__":
    generate_and_save_dataset()