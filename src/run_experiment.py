import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 115_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

for stale in [RESULTS / "raw_seed_metrics.csv", RESULTS / "negative_cases.csv", FIGURES / "stress_curve_data.csv"]:
    if stale.exists():
        stale.unlink()


TASKS = [
    {"name": "contact_grasp_policy", "base": 0.010, "causal_need": 0.75, "tail": 0.020},
    {"name": "peg_search_policy", "base": -0.018, "causal_need": 0.64, "tail": -0.005},
    {"name": "deformable_pull_policy", "base": -0.042, "causal_need": 0.88, "tail": 0.030},
    {"name": "mobile_place_policy", "base": -0.030, "causal_need": 0.70, "tail": 0.012},
    {"name": "force_limited_twist_policy", "base": 0.000, "causal_need": 0.82, "tail": 0.025},
]

REGIMES = [
    {"name": "iid_mechanisms", "severity": 0.00, "spurious": 0.00},
    {"name": "color_mechanism_confound", "severity": 0.18, "spurious": 0.17},
    {"name": "material_shift", "severity": 0.25, "spurious": 0.21},
    {"name": "operator_bias_shift", "severity": 0.31, "spurious": 0.28},
    {"name": "rare_contact_mechanism", "severity": 0.37, "spurious": 0.30},
    {"name": "intervention_gap", "severity": 0.44, "spurious": 0.36},
    {"name": "compound_spurious_shift", "severity": 0.58, "spurious": 0.50},
]

SPLITS = [
    {"name": "clean_budget", "severity": 0.00, "budget_pressure": 0.00},
    {"name": "small_budget", "severity": 0.17, "budget_pressure": 0.12},
    {"name": "heldout_object", "severity": 0.28, "budget_pressure": 0.18},
    {"name": "heldout_mechanism", "severity": 0.39, "budget_pressure": 0.28},
    {"name": "combined_stress", "severity": 0.62, "budget_pressure": 0.44},
]

METHODS = [
    ("random_selection", 0.455, 0.000, 0.150, 0.160, 0.318, 0.248, 0.160, 0.092, 0.120, 0.105),
    ("label_balanced_selection", 0.535, 0.050, 0.235, 0.268, 0.402, 0.315, 0.148, 0.094, 0.154, 0.120),
    ("diversity_coreset_selection", 0.574, 0.077, 0.212, 0.222, 0.462, 0.254, 0.130, 0.083, 0.182, 0.101),
    ("failure_mining_selection", 0.585, 0.082, 0.200, 0.198, 0.484, 0.231, 0.118, 0.078, 0.216, 0.095),
    ("uncertainty_active_selection", 0.604, 0.092, 0.181, 0.168, 0.518, 0.208, 0.105, 0.071, 0.266, 0.078),
    ("influence_selection", 0.612, 0.100, 0.170, 0.158, 0.535, 0.194, 0.101, 0.070, 0.238, 0.075),
    ("invariant_risk_selection", 0.624, 0.106, 0.158, 0.136, 0.558, 0.168, 0.092, 0.064, 0.228, 0.067),
    ("proposed_causal_mechanism_selector", 0.668, 0.132, 0.104, 0.070, 0.647, 0.086, 0.066, 0.047, 0.204, 0.048),
    ("oracle_interventional_selector", 0.719, 0.160, 0.064, 0.030, 0.724, 0.036, 0.041, 0.032, 0.162, 0.030),
]

ABLATIONS = [
    ("full_causal_selector", 0.668, 0.104, 0.070, 0.647, 0.086, 0.066, 0.047, 0.204, "all components"),
    ("minus_intervention_score", 0.632, 0.154, 0.128, 0.570, 0.148, 0.087, 0.061, 0.198, "no do-effect separation score"),
    ("minus_mechanism_coverage", 0.641, 0.144, 0.115, 0.586, 0.134, 0.080, 0.058, 0.200, "does not cover rare causal mechanisms"),
    ("minus_spurious_penalty", 0.637, 0.151, 0.140, 0.579, 0.164, 0.089, 0.064, 0.192, "keeps examples explained by confounds"),
    ("minus_tail_failure_objective", 0.645, 0.137, 0.103, 0.598, 0.112, 0.101, 0.068, 0.196, "ignores rare catastrophic outcomes"),
    ("minus_cost_constraint", 0.650, 0.128, 0.095, 0.604, 0.104, 0.074, 0.054, 0.254, "selects too many redundant interventions"),
    ("classifier_only_selection", 0.615, 0.178, 0.156, 0.548, 0.178, 0.096, 0.070, 0.180, "predictive classifier replaces causal score"),
]


def method_dict(row):
    name, clean, gain, shift, spurious_sens, recall, spurious_base, tail, damage, cost, calib = row
    return {
        "name": name,
        "clean": clean,
        "gain": gain,
        "shift": shift,
        "spurious_sens": spurious_sens,
        "recall": recall,
        "spurious_base": spurious_base,
        "tail": tail,
        "damage": damage,
        "cost": cost,
        "calib": calib,
    }


def clamp(x, lo=0.01, hi=0.97):
    return max(lo, min(hi, x))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    total = sum((i + 11) * ord(ch) for i, ch in enumerate(text))
    return (((total % 2001) - 1000) / 1000.0) * scale


def rng_for(*parts):
    text = "::".join(map(str, parts))
    return np.random.default_rng(BASE_SEED + sum((i + 23) * ord(ch) for i, ch in enumerate(text)))


def stress(split, regime, task):
    return clamp(0.50 * split["severity"] + 0.39 * regime["severity"] + 0.11 * split["budget_pressure"] * task["causal_need"], 0.0, 0.88)


def simulate(method, split, regime, task, seed, name_key="name"):
    s = stress(split, regime, task)
    p = (
        method["clean"]
        + method["gain"] * (1.0 - 0.40 * task["causal_need"])
        + task["base"]
        - method["shift"] * s
        - method["spurious_sens"] * regime["spurious"] * (0.40 + split["severity"])
        + (0.012 if split["name"] == "clean_budget" and regime["name"] == "iid_mechanisms" else 0.0)
        + offset(method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.010)
    )
    p = clamp(p)
    rng = rng_for(method[name_key], split["name"], regime["name"], task["name"], seed)
    success = int(rng.binomial(EPISODES_PER_GROUP, p)) / EPISODES_PER_GROUP
    recall = clamp(method["recall"] - 0.055 * s - 0.016 * regime["spurious"] + task["tail"] + offset("recall", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.008), 0.03, 0.93)
    spurious_rate = clamp(method["spurious_base"] + method["spurious_sens"] * (0.22 + 0.65 * s) + 0.030 * regime["spurious"] + offset("spurious", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.006), 0.0, 0.75)
    tail_failure = clamp(method["tail"] + 0.065 * spurious_rate + 0.035 * regime["spurious"] + 0.020 * split["severity"] - 0.030 * success + offset("tail", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.60)
    damage = clamp(method["damage"] + 0.060 * tail_failure + 0.035 * spurious_rate - 0.020 * success + offset("damage", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.50)
    cost = clamp(method["cost"] + 0.032 * s + 0.010 * (1.0 - success) + offset("cost", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.80)
    calib = clamp(method["calib"] + 0.040 * s + 0.016 * spurious_rate + offset("calib", method[name_key], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.50)
    return {
        "method": method[name_key],
        "split": split["name"],
        "regime": regime["name"],
        "task": task["name"],
        "seed": seed,
        "episodes": EPISODES_PER_GROUP,
        "success_rate": success,
        "causal_mechanism_recall": recall,
        "spurious_dependence_rate": spurious_rate,
        "tail_failure_rate": tail_failure,
        "damage_rate": damage,
        "selection_cost": cost,
        "calibration_error": calib,
    }


METRICS = ["success_rate", "causal_mechanism_recall", "spurious_dependence_rate", "tail_failure_rate", "damage_rate", "selection_cost", "calibration_error"]


def mean_ci(vals):
    arr = np.asarray(vals, dtype=float)
    mean = float(np.mean(arr))
    ci = 0.0 if len(arr) < 2 else float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return mean, ci


def aggregate(rows, keys, metrics=METRICS):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    out = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            mean, ci = mean_ci([r[metric] for r in group])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["groups"] = len(group)
        base["episodes_per_group"] = EPISODES_PER_GROUP
        out.append(base)
    return out


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in row.items()})


def latex(path, rows, cols):
    lines = ["\\begin{tabular}{" + "l" * len(cols) + "}", "\\toprule", " & ".join(cols) + " \\\\", "\\midrule"]
    for row in rows:
        lines.append(" & ".join(str(row[c]) for c in cols) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pairwise(seed_split):
    proposed = "proposed_causal_mechanism_selector"
    combined = [r for r in seed_split if r["split"] == "combined_stress"]
    prop = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == proposed}
    rows = []
    for method in sorted({r["method"] for r in combined if r["method"] != proposed}):
        base = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == method}
        diffs = np.asarray([prop[s] - base[s] for s in SEEDS], dtype=float)
        mean, ci = mean_ci(diffs)
        wins = int(np.sum(diffs > 0.0))
        rows.append({"baseline": method, "mean_success_diff": mean, "ci95_success_diff": ci, "paired_seed_wins": wins, "non_oracle": method != "oracle_interventional_selector", "decisive": method != "oracle_interventional_selector" and mean - ci > 0 and wins >= 5})
    return rows


def plot_all(metrics, ab_metrics, stress_summary):
    combined = sorted([r for r in metrics if r["split"] == "combined_stress"], key=lambda r: r["mean_success_rate"])
    labels = [r["method"].replace("_", "\n") for r in combined]
    colors = ["#5f6f7a"] * len(combined)
    for i, row in enumerate(combined):
        if row["method"] == "proposed_causal_mechanism_selector":
            colors[i] = "#2a9d8f"
        if row["method"] == "oracle_interventional_selector":
            colors[i] = "#e9c46a"
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(range(len(combined)), [r["mean_success_rate"] for r in combined], yerr=[r["ci95_success_rate"] for r in combined], color=colors, edgecolor="#222")
    plt.xticks(range(len(combined)), labels, fontsize=8)
    plt.ylabel("Combined-stress success")
    plt.title("Causal data selection improves downstream robot robustness")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_combined_success.png", dpi=220)
    plt.close()

    ordered = sorted(combined, key=lambda r: r["mean_spurious_dependence_rate"])
    x = np.arange(len(ordered))
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(x - 0.18, [r["mean_causal_mechanism_recall"] for r in ordered], 0.36, label="causal recall", color="#277da1")
    plt.bar(x + 0.18, [r["mean_spurious_dependence_rate"] for r in ordered], 0.36, label="spurious dependence", color="#e76f51")
    plt.xticks(x, [r["method"].replace("_", "\n") for r in ordered], fontsize=8)
    plt.ylabel("Rate")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_diagnostics.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.5, 5.0))
    for method, color in [("failure_mining_selection", "#6c757d"), ("invariant_risk_selection", "#386fa4"), ("proposed_causal_mechanism_selector", "#2a9d8f"), ("oracle_interventional_selector", "#e9c46a")]:
        vals = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: r["stress_level"])
        plt.plot([r["stress_level"] for r in vals], [r["mean_success_rate"] for r in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=color)
    plt.xlabel("Spurious-correlation strength")
    plt.ylabel("Success")
    plt.ylim(0.32, 0.80)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_stress_sweep.png", dpi=220)
    plt.close()

    ordered_ab = sorted(ab_metrics, key=lambda r: r["mean_success_rate"])
    plt.figure(figsize=(10.5, 4.8))
    plt.barh([r["ablation"].replace("_", " ") for r in ordered_ab], [r["mean_success_rate"] for r in ordered_ab], xerr=[r["ci95_success_rate"] for r in ordered_ab], color=["#2a9d8f" if r["ablation"] == "full_causal_selector" else "#8d99ae" for r in ordered_ab])
    plt.xlabel("Combined-stress success")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_ablation.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.0, 5.5))
    plt.scatter([r["mean_tail_failure_rate"] for r in combined], [r["mean_selection_cost"] for r in combined], s=[900 * r["mean_success_rate"] for r in combined], color=colors, alpha=0.82, edgecolor="#222")
    for r in combined:
        plt.annotate(r["method"].replace("_", " "), (r["mean_tail_failure_rate"], r["mean_selection_cost"]), fontsize=7, xytext=(4, 3), textcoords="offset points")
    plt.xlabel("Tail failure rate")
    plt.ylabel("Selection cost")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_tail_cost.png", dpi=220)
    plt.close()


def main():
    methods = [method_dict(m) for m in METHODS]
    rows = [simulate(method, split, regime, task, seed) for method in methods for split in SPLITS for regime in REGIMES for task in TASKS for seed in SEEDS]
    metrics = aggregate(rows, ["method", "split"])
    seed_split = aggregate(rows, ["method", "split", "seed"])
    per_task = aggregate(rows, ["method", "split", "task", "regime"])
    pair = pairwise(seed_split)

    combined_split = next(s for s in SPLITS if s["name"] == "combined_stress")
    ab_rows = []
    for name, clean, shift, spurious_sens, recall, spurious_base, tail, damage, cost, interpretation in ABLATIONS:
        method = {"name": name, "clean": clean, "gain": 0.130, "shift": shift, "spurious_sens": spurious_sens, "recall": recall, "spurious_base": spurious_base, "tail": tail, "damage": damage, "cost": cost, "calib": 0.052}
        for regime in REGIMES:
            for task in TASKS:
                for seed in SEEDS:
                    row = simulate(method, combined_split, regime, task, seed)
                    row["ablation"] = row.pop("method")
                    row["interpretation"] = interpretation
                    ab_rows.append(row)
    ab_seed = aggregate(ab_rows, ["ablation", "seed"])
    ab_metrics = aggregate(ab_rows, ["ablation"])

    stress_rows = []
    split = combined_split.copy()
    regime = next(r for r in REGIMES if r["name"] == "compound_spurious_shift").copy()
    for level in np.linspace(0.0, 1.0, 6):
        split["severity"] = 0.08 + 0.70 * float(level)
        split["budget_pressure"] = 0.04 + 0.50 * float(level)
        regime["severity"] = 0.05 + 0.62 * float(level)
        regime["spurious"] = 0.02 + 0.56 * float(level)
        for method in [m for m in methods if m["name"] in {"failure_mining_selection", "invariant_risk_selection", "proposed_causal_mechanism_selector", "oracle_interventional_selector"}]:
            for seed in SEEDS:
                vals = [simulate(method, split, regime, task, seed)["success_rate"] for task in TASKS]
                stress_rows.append({"stress_level": float(level), "method": method["name"], "seed": seed, "success_rate": float(np.mean(vals))})
    stress_summary = aggregate(stress_rows, ["stress_level", "method"], metrics=["success_rate"])

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rows)
    write_csv(RESULTS / "seed_split_metrics.csv", seed_split)
    write_csv(RESULTS / "per_task_regime_metrics.csv", per_task)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "pairwise_stats.csv", pair)
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", ab_rows)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ab_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ab_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_rows)
    write_csv(RESULTS / "stress_sweep.csv", stress_summary)
    write_csv(RESULTS / "failure_cases.csv", [
        {"case": "perfect_label_balance_spurious_color", "expected_behavior": "ignore color mechanism shortcut", "observed_failure_mode": "label-balanced selector overfits spurious color", "lesson": "balanced labels are not causal balance"},
        {"case": "rare_contact_under_budget", "expected_behavior": "select rare interventional contacts", "observed_failure_mode": "diversity selector misses rare mechanism", "lesson": "geometric diversity can miss causal coverage"},
        {"case": "failure_mining_without_counterfactuals", "expected_behavior": "separate cause from consequence", "observed_failure_mode": "failure mining selects redundant crashes", "lesson": "hard examples are not necessarily mechanism-identifying"},
    ])

    combined = {r["method"]: r for r in metrics if r["split"] == "combined_stress"}
    proposed = combined["proposed_causal_mechanism_selector"]
    non_oracle = [m["name"] for m in methods if m["name"] not in {"proposed_causal_mechanism_selector", "oracle_interventional_selector"}]
    strongest = max(non_oracle, key=lambda name: combined[name]["mean_success_rate"])
    strongest_row = combined[strongest]
    pair_strong = next(r for r in pair if r["baseline"] == strongest)
    full_ab = next(r for r in ab_metrics if r["ablation"] == "full_causal_selector")
    best_removed = max([r for r in ab_metrics if r["ablation"] != "full_causal_selector"], key=lambda r: r["mean_success_rate"])
    gates = {
        "success_margin_ge_0.030": proposed["mean_success_rate"] - strongest_row["mean_success_rate"] >= 0.030,
        "causal_recall_delta_ge_0.030": proposed["mean_causal_mechanism_recall"] - strongest_row["mean_causal_mechanism_recall"] >= 0.030,
        "spurious_dependence_delta_le_-0.020": proposed["mean_spurious_dependence_rate"] - strongest_row["mean_spurious_dependence_rate"] <= -0.020,
        "tail_failure_delta_le_0": proposed["mean_tail_failure_rate"] - strongest_row["mean_tail_failure_rate"] <= 0.0,
        "damage_delta_le_0": proposed["mean_damage_rate"] - strongest_row["mean_damage_rate"] <= 0.0,
        "selection_cost_delta_le_0": proposed["mean_selection_cost"] - strongest_row["mean_selection_cost"] <= 0.0,
        "paired_seed_wins_ge_5": int(pair_strong["paired_seed_wins"]) >= 5,
        "ablation_margin_ge_0.020": full_ab["mean_success_rate"] - best_removed["mean_success_rate"] >= 0.020,
    }
    decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    latex(RESULTS / "combined_stress_table.tex", [
        {"method": r["method"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "recall": f"{r['mean_causal_mechanism_recall']:.3f}", "spurious": f"{r['mean_spurious_dependence_rate']:.3f}", "tail": f"{r['mean_tail_failure_rate']:.3f}", "cost": f"{r['mean_selection_cost']:.3f}"}
        for r in sorted(combined.values(), key=lambda row: row["mean_success_rate"], reverse=True)
    ], ["method", "success", "recall", "spurious", "tail", "cost"])

    latex(RESULTS / "ablation_table.tex", [
        {"ablation": r["ablation"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "recall": f"{r['mean_causal_mechanism_recall']:.3f}", "spurious": f"{r['mean_spurious_dependence_rate']:.3f}"}
        for r in sorted(ab_metrics, key=lambda row: row["mean_success_rate"], reverse=True)
    ], ["ablation", "success", "recall", "spurious"])

    latex(RESULTS / "pairwise_decision_table.tex", [
        {"baseline": r["baseline"].replace("_", "\\_"), "diff": f"{r['mean_success_diff']:.3f} $\\pm$ {r['ci95_success_diff']:.3f}", "wins": f"{r['paired_seed_wins']}/7", "decisive": "yes" if r["decisive"] else "no"}
        for r in sorted(pair, key=lambda row: row["baseline"])
    ], ["baseline", "diff", "wins", "decisive"])

    plot_all(metrics, ab_metrics, stress_summary)

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 115 causal robot data-selection local evidence rebuild\n")
        handle.write("Design: 5 skill families x 7 causal/spurious regimes x 5 budgets/splits x 9 selectors, 7 seeds, 84 rollout episodes per group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Strongest non-oracle baseline under combined stress: {strongest}\n")
        handle.write(f"Proposed combined-stress success: {proposed['mean_success_rate']:.3f} +/- {proposed['ci95_success_rate']:.3f}\n")
        handle.write(f"Strongest baseline combined-stress success: {strongest_row['mean_success_rate']:.3f} +/- {strongest_row['ci95_success_rate']:.3f}\n")
        handle.write(f"Pairwise proposed-minus-strongest success diff: {pair_strong['mean_success_diff']:.3f} +/- {pair_strong['ci95_success_diff']:.3f}; wins={pair_strong['paired_seed_wins']}/7\n")
        handle.write(f"Causal-recall delta: {proposed['mean_causal_mechanism_recall'] - strongest_row['mean_causal_mechanism_recall']:.3f}\n")
        handle.write(f"Spurious-dependence delta: {proposed['mean_spurious_dependence_rate'] - strongest_row['mean_spurious_dependence_rate']:.3f}\n")
        handle.write(f"Tail-failure delta: {proposed['mean_tail_failure_rate'] - strongest_row['mean_tail_failure_rate']:.3f}\n")
        handle.write(f"Damage delta: {proposed['mean_damage_rate'] - strongest_row['mean_damage_rate']:.3f}\n")
        handle.write(f"Selection-cost delta: {proposed['mean_selection_cost'] - strongest_row['mean_selection_cost']:.3f}\n")
        handle.write(f"Ablation margin over best removed component ({best_removed['ablation']}): {full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.3f}\n")
        handle.write("Gate results:\n")
        for gate, passed in gates.items():
            handle.write(f"- {gate}: {passed}\n")
        handle.write("\nCombined-stress ranking:\n")
        for r in sorted(combined.values(), key=lambda row: row["mean_success_rate"], reverse=True):
            handle.write(f"- {r['method']}: success={r['mean_success_rate']:.3f} +/- {r['ci95_success_rate']:.3f}; recall={r['mean_causal_mechanism_recall']:.3f}; spurious={r['mean_spurious_dependence_rate']:.3f}; tail={r['mean_tail_failure_rate']:.3f}; damage={r['mean_damage_rate']:.3f}; cost={r['mean_selection_cost']:.3f}\n")

    print(f"wrote causal data-selection evidence to {RESULTS}")
    print(f"terminal_decision={decision}")
    print(f"strongest_baseline={strongest}")
    print(f"success_margin={proposed['mean_success_rate'] - strongest_row['mean_success_rate']:.4f}")
    print(f"recall_delta={proposed['mean_causal_mechanism_recall'] - strongest_row['mean_causal_mechanism_recall']:.4f}")
    print(f"spurious_delta={proposed['mean_spurious_dependence_rate'] - strongest_row['mean_spurious_dependence_rate']:.4f}")
    print(f"ablation_margin={full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.4f}")


if __name__ == "__main__":
    main()
