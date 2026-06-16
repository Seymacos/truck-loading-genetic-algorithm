import json
import numpy as np
from scipy.stats import spearmanr, ttest_1samp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_json_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    expert_data = load_json_data("expert_solution.json")
    ga_results = load_json_data("ga_results.json")

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
    print("1. RUNTIME ANALYSIS:")
    print(f"   - Total runtime (50 runs) : {total_runtime:.4f} seconds")
    print(f"   - Average runtime per run : {avg_runtime:.4f} seconds\n")

    # 2. Spearman Rank Correlation
    rho_values = []
    for chrom in ga_chroms:
        rho, _ = spearmanr(expert_chrom, chrom)
        rho_values.append(rho)

    avg_rho = np.mean(rho_values)
    print("2. SPEARMAN RANK CORRELATION ANALYSIS:")
    print(f"   - Average Spearman rho value : {avg_rho:.4f}")
    if avg_rho > 0.8:
        print("   - Interpretation: GA solutions are strongly correlated with the expert solution.")
    elif avg_rho < 0.2:
        print("   - Interpretation: GA solutions differ significantly from the expert solution.")
    else:
        print("   - Interpretation: GA and expert solutions show moderate similarity.")
    print()

    # 3. t-Test Analysis
    t_stat, p_value = ttest_1samp(ga_fitnesses, expert_fitness)


     # 1. Fitness Distribution
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

    # 2. Runtime Distribution
    plt.figure(figsize=(6, 4))
    plt.hist(ga_runtimes, bins=10, color="#55A868", edgecolor="black")
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("Number of Runs")
    plt.title("Distribution of Runtime over 50 GA Runs")
    plt.tight_layout()
    plt.savefig("runtime_distribution.png", dpi=150)
    plt.close()

    # 3. Spearman Rho Distribution
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

    # 4. Fitness per Run
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(ga_fitnesses)), ga_fitnesses, marker="o", linestyle="-", color="#4C72B0", label="GA best fitness")
    plt.axhline(expert_fitness, color="red", linestyle="--", label=f"Expert ({expert_fitness:.3f})")
    plt.xlabel("Run Index")
    plt.ylabel("Fitness")
    plt.title("Best Fitness per Run vs Expert Solution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fitness_per_run.png", dpi=150)
    plt.close()

    print("Plots saved: fitness_distribution.png, runtime_distribution.png, spearman_distribution.png, fitness_per_run.png")
    print("3. ONE-SAMPLE t-TEST ANALYSIS:")
    print(f"   - H0 (Null Hypothesis)        : GA mean fitness == {expert_fitness:.4f} (no significant difference)")
    print(f"   - H1 (Alternative Hypothesis) : GA mean fitness != {expert_fitness:.4f} (significant difference exists)")
    print(f"   - Significance level (alpha)  : 0.05")
    print(f"   - t-statistic                 : {t_stat:.4f}")
    print(f"   - p-value                     : {p_value:.4f}")
    print(f"   - GA mean fitness             : {np.mean(ga_fitnesses):.4f}")

    if p_value < 0.05:
        print("   - Decision: H0 REJECTED (p < 0.05)")
        print("   - Interpretation: There is a statistically significant difference between GA and expert solution.")
    else:
        print("   - Decision: H0 NOT REJECTED (p >= 0.05)")
        print("   - Interpretation: No statistically significant difference between GA and expert solution.")
    print()

    # 4. Best Result
    best_run_idx = np.argmax(ga_fitnesses)
    best_run = ga_results[best_run_idx]
    print("4. BEST RESULT:")
    print(f"   - Best fitness value : {best_run['fitness']:.4f}")
    print(f"   - Run ID             : Run {best_run['run_id']}")
    print(f"   - Expert fitness     : {expert_fitness:.4f}")
    print(f"   - Difference         : {best_run['fitness'] - expert_fitness:+.4f}")
    print(f"   - Best chromosome    : {best_run['best_chromosome']}")
    print("\n====================================================")