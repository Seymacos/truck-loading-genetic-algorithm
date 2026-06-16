import json
from ga_core import load_items, calculate_fitness, STOP_PRIORITY

def generate_expert_solution(items):
    """
    Deterministik sezgisel yaklaşım kullanarak ideal bir kromozom üretir.
    Önce durak önceliğine göre büyükten küçüğe (E->D->C->B->A),
    sonra kendi içinde hacme göre büyükten küçüğe sıralar.
    """
    indices = list(range(len(items)))
    
    # Sıralama anahtarı: 
    # 1. Eleman: STOP_PRIORITY değerinin negatifi (Örn: E için -5, A için -1 olur. Küçük olan önce gelir, yani E başa geçer)
    # 2. Eleman: Hacmin negatifi (Büyük hacimler başa gelir)
    indices.sort(
        key=lambda idx: (
            -STOP_PRIORITY[items[idx]["stop"]],
            -items[idx]["volume"]
        )
    )
    return indices

if __name__ == "__main__":
    # 1. Veriyi yükle
    items, capacity = load_items()
    
    # 2. Expert çözümü üret
    expert_chromosome = generate_expert_solution(items)
    
    # 3. Kalitesini (fitness) hesapla
    total_fit, order_score, balance_score = calculate_fitness(expert_chromosome, items, capacity)
    
    print("=== EXPERT SOLUTION BAŞARIYLA ÜRETİLDİ ===")
    print(f"Expert Kromozomu (Yükleme Sırası): {expert_chromosome}\n")
    print(f"Toplam Fitness : {total_fit:.4f}")
    print(f"LIFO Skoru     : {order_score:.4f} (1.0000 kusursuz demektir)")
    print(f"Doluluk Skoru  : {balance_score:.4f}")
    
    # İleride istatistiksel analizde (t-test ve Spearman) kullanmak için diske kaydedelim
    expert_data = {
        "chromosome": expert_chromosome,
        "fitness": total_fit,
        "order_score": order_score,
        "balance_score": balance_score
    }
    
    with open("expert_solution.json", "w") as f:
        json.dump(expert_data, f, indent=4)
    print("\n'expert_solution.json' dosyası kaydedildi!")