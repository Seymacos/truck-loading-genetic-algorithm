import time
import json
import random
from ga_core import (
    load_items, calculate_fitness, tournament_selection, 
    one_point_crossover, swap_mutation
)

# GA Hiperparametreleri (Raporda gerekçelendireceğimiz parametreler)
POP_SIZE = 40
GENERATIONS = 100
PC = 0.90  # Ödev kuralı: Crossover olasılığı
PM = 0.10  # Ödev kuralı: Mutasyon olasılığı
NUM_RUNS = 50  # Ödev kuralı: 50 bağımsız test

def run_genetic_algorithm(items, capacity, run_id):
    """ Tek bir GA simülasyonunu çalıştırır ve en iyi bireyi döndürür """
    num_elements = len(items)
    
    # 1. Başlangıç Popülasyonunu Rastgele Oluşturma
    population = []
    for _ in range(POP_SIZE):
        chrom = list(range(num_elements))
        random.shuffle(chrom)
        population.append(chrom)
        
    best_chrom_of_run = None
    best_fit_of_run = -1.0
    
    # Jenerasyon döngüsü
    for gen in range(GENERATIONS):
        # Popülasyondaki her bireyin fitness değerini hesapla
        fitnesses = [calculate_fitness(c, items, capacity)[0] for c in population]
        
        # En iyiyi takip et (Elitizm / Takip mekanizması)
        for i, fit in enumerate(fitnesses):
            if fit > best_fit_of_run:
                best_fit_of_run = fit
                best_chrom_of_run = population[i].copy()
                
        # Yeni jenerasyonu oluşturma
        new_population = []
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            
            # Crossover (P_c = 0.90 kısıtı)
            if random.random() < PC:
                child1 = one_point_crossover(parent1, parent2)
                child2 = one_point_crossover(parent2, parent1)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
                
            # Mutation (P_m = 0.10 kısıtı)
            if random.random() < PM:
                child1 = swap_mutation(child1)
            if random.random() < PM:
                child2 = swap_mutation(child2)
                
            new_population.extend([child1, child2])
            
        population = new_population[:POP_SIZE]
        
    return best_chrom_of_run, best_fit_of_run

if __name__ == "__main__":
    items, capacity = load_items()
    
    results = []
    print(f"=== Genetik Algoritma {NUM_RUNS} Kez Bağımsız Olarak Koşturuluyor ===")
    
    # 50 bağımsız testi başlatan ana döngü
    for r in range(1, NUM_RUNS + 1):
        # Her run'ın farklı bir seed ile başlamasını garanti altına alıyoruz
        random.seed(r * 100) 
        
        start_time = time.time()
        best_chrom, best_fitness = run_genetic_algorithm(items, capacity, r)
        end_time = time.time()
        
        runtime = end_time - start_time
        
        # Her bir run sonucunu kaydediyoruz
        results.append({
            "run_id": r,
            "best_chromosome": best_chrom,
            "fitness": round(best_fitness, 4),
            "runtime": round(runtime, 4)
        })
        
        if r % 10 == 0:
            print(f"Run {r:2d}/{NUM_RUNS} tamamlandı... (En İyi Fitness: {best_fitness:.4f})")
            
    # Sonuçları istatistiksel analiz adımında okumak üzere kaydedelim
    with open("ga_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n=== TÜM DENEYLER TAMAMLANDI VE 'ga_results.json' DOSYASINA KAYDEDİLDİ ===")