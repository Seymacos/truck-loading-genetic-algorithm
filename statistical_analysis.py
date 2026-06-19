import json
import numpy as np
from scipy.stats import spearmanr, ttest_1samp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    expert_data = load_json("expert_solution.json")
    ga_results = load_json("ga_results.json")
    convergence_data = load_json("convergence.json")

    expert_chrom = expert_data["chromosome"]
    expert_fitness = expert_data["fitness"]

    ga_fitnesses = [run["fitness"] for run in ga_results]
    ga_runtimes = [run["runtime"] for run in ga_results]
    ga_chroms = [run["best_chromosome"] for run in ga_results]

    print("====================================================")
    print("   SECTION 2: STATISTICAL ANALYSIS RESULTS")
    print("====================================================\n")

    # 1. Runtime Analysis
    avg_runtime = np.mean(ga_runtimes)
    total_runtime = np.sum(ga_runtimes)
    std_runtime = np.std(ga_runtimes, ddof=1)
    print("1. RUNTIME ANALYSIS:")
    print(f"   - Total runtime (50 runs)    : {total_runtime:.4f} seconds")
    print(f"   - Average runtime per run    : {avg_runtime:.4f} seconds")
    print(f"   - Std deviation              : {std_runtime:.4f} seconds")
    print(f"   - Min / Max                  : {min(ga_runtimes):.4f}s / {max(ga_runtimes):.4f}s\n")

    # 2. Spearman Rank Correlation
    rho_values = []
    for chrom in ga_chroms:
        rho, _ = spearmanr(expert_chrom, chrom)
        rho_values.append(rho)

    avg_rho = np.mean(rho_values)
    std_rho = np.std(rho_values, ddof=1)
    print("2. SPEARMAN RANK CORRELATION ANALYSIS:")
    print(f"   - Average Spearman rho       : {avg_rho:.4f}")
    print(f"   - Std deviation              : {std_rho:.4f}")
    print(f"   - Min / Max rho              : {min(rho_values):.4f} / {max(rho_values):.4f}")
    if avg_rho > 0.8:
        print("   - Interpretation: GA solutions closely follow the same ordering as the expert solution.")
    elif avg_rho > 0.2:
        print("   - Interpretation: GA and expert solutions share some structural similarity in item ordering.")
    else:
        print("   - Interpretation: GA explores very different orderings than the expert solution,")
        print("     yet still achieves comparable fitness. This suggests multiple valid solutions exist.")
    print()

    # 3. t-Test Analysis
    t_stat, p_value = ttest_1samp(ga_fitnesses, expert_fitness)
    print("3. ONE-SAMPLE t-TEST ANALYSIS:")
    print(f"   - H0 (Null Hypothesis)       : GA mean fitness == {expert_fitness:.4f}")
    print(f"   - H1 (Alternative Hypothesis): GA mean fitness != {expert_fitness:.4f}")
    print(f"   - Significance level (alpha) : 0.05")
    print(f"   - GA mean fitness            : {np.mean(ga_fitnesses):.4f}")
    print(f"   - t-statistic                : {t_stat:.4f}")
    print(f"   - p-value                    : {p_value:.4f}")
    if p_value < 0.05:
        print("   - Decision: H0 REJECTED (p < 0.05)")
        print("   - Interpretation: The GA's average performance is statistically different")
        print("     from the expert solution, meaning the difference is not due to chance.")
    else:
        print("   - Decision: H0 NOT REJECTED (p >= 0.05)")
        print("   - Interpretation: No statistically significant difference between")
        print("     GA results and the expert solution.")
    print()

    # 4. Best Result
    best_run_idx = np.argmax(ga_fitnesses)
    best_run = ga_results[best_run_idx]
    print("4. BEST RESULT:")
    print(f"   - Best fitness value         : {best_run['fitness']:.4f}")
    print(f"   - Run ID                     : Run {best_run['run_id']}")
    print(f"   - Expert fitness             : {expert_fitness:.4f}")
    print(f"   - Difference                 : {best_run['fitness'] - expert_fitness:+.4f}")
    print(f"   - Best chromosome            : {best_run['best_chromosome']}")
    print("\n====================================================\n")

    # --- PLOTS ---

    # Plot 1: Fitness Distribution
    plt.figure(figsize=(6, 4))
    plt.hist(ga_fitnesses, bins=10, color="#4C72B0", edgecolor="black")
    plt.axvline(expert_fitness, color="red", linestyle="--", label=f"Expert ({expert_fitness:.3f})")
    plt.xlabel("Fitness")
    plt.ylabel("Number of Runs")
    plt.title("Distribution of Best Fitness over 50 GA Runs")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fitness_distribution.png", dpi=150)
    plt.close()

    # Plot 2: Runtime Distribution
    plt.figure(figsize=(6, 4))
    plt.hist(ga_runtimes, bins=10, color="#55A868", edgecolor="black")
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("Number of Runs")
    plt.title("Distribution of Runtime over 50 GA Runs")
    plt.tight_layout()
    plt.savefig("runtime_distribution.png", dpi=150)
    plt.close()

    # Plot 3: Spearman Rho Distribution
    plt.figure(figsize=(6, 4))
    plt.hist(rho_values, bins=10, color="#C44E52", edgecolor="black")
    plt.axvline(avg_rho, color="black", linestyle="--", label=f"Mean rho ({avg_rho:.3f})")
    plt.xlabel("Spearman rho")
    plt.ylabel("Number of Runs")
    plt.title("Spearman Rank Correlation with Expert Solution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("spearman_distribution.png", dpi=150)
    plt.close()

    # Plot 4: Fitness per Run
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(ga_fitnesses)), ga_fitnesses, marker="o", linestyle="-",
             color="#4C72B0", label="GA best fitness")
    plt.axhline(expert_fitness, color="red", linestyle="--", label=f"Expert ({expert_fitness:.3f})")
    plt.xlabel("Run Index")
    plt.ylabel("Fitness")
    plt.title("Best Fitness per Run vs Expert Solution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fitness_per_run.png", dpi=150)
    plt.close()

    # Plot 5: Convergence (average fitness across generations)
    avg_convergence = np.mean(convergence_data, axis=0)
    plt.figure(figsize=(8, 4))
    plt.plot(range(GENERATIONS := len(avg_convergence)), avg_convergence,
             color="#4C72B0", linewidth=2, label="Average best fitness")
    plt.axhline(expert_fitness, color="red", linestyle="--", label=f"Expert ({expert_fitness:.3f})")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Average Convergence over 50 Runs")
    plt.legend()
    plt.tight_layout()
    plt.savefig("convergence.png", dpi=150)
    plt.close()

    print("Plots saved: fitness_distribution.png, runtime_distribution.png,")
    print("             spearman_distribution.png, fitness_per_run.png, convergence.png")