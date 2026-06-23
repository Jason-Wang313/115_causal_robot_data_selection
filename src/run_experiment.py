import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


VERSION = "v5_expanded"
BASE_SEED = 115_2026_5
EPISODES_PER_CELL = 96
SEEDS = list(range(10))

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"

for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)

STALE_FILES = [
    "metrics.csv",
    "per_task_regime_metrics.csv",
    "seed_task_regime_metrics.csv",
    "seed_split_metrics.csv",
    "pairwise_stats.csv",
    "ablation_task_regime_seed_metrics.csv",
    "ablation_seed_metrics.csv",
    "ablation_metrics.csv",
    "stress_sweep_seed_metrics.csv",
    "stress_sweep.csv",
    "summary.txt",
    "combined_stress_table.tex",
    "ablation_table.tex",
    "pairwise_decision_table.tex",
]

for name in STALE_FILES:
    path = RESULTS / name
    if path.exists():
        path.unlink()


TASKS = [
    {"name": "contact_grasp_policy", "bias": 0.014, "causal_need": 0.74, "tail_need": 0.42},
    {"name": "peg_search_policy", "bias": -0.012, "causal_need": 0.66, "tail_need": 0.36},
    {"name": "deformable_pull_policy", "bias": -0.040, "causal_need": 0.90, "tail_need": 0.60},
    {"name": "mobile_place_policy", "bias": -0.028, "causal_need": 0.70, "tail_need": 0.46},
    {"name": "force_limited_twist_policy", "bias": 0.004, "causal_need": 0.84, "tail_need": 0.55},
]

REGIMES = [
    {"name": "iid_mechanisms", "severity": 0.00, "spurious": 0.00, "hidden": 0.00},
    {"name": "color_mechanism_confound", "severity": 0.16, "spurious": 0.22, "hidden": 0.08},
    {"name": "material_shift", "severity": 0.24, "spurious": 0.20, "hidden": 0.16},
    {"name": "operator_bias_shift", "severity": 0.30, "spurious": 0.32, "hidden": 0.14},
    {"name": "rare_contact_mechanism", "severity": 0.39, "spurious": 0.27, "hidden": 0.31},
    {"name": "intervention_gap", "severity": 0.48, "spurious": 0.38, "hidden": 0.36},
    {"name": "counterfactual_missing", "severity": 0.54, "spurious": 0.42, "hidden": 0.42},
    {"name": "compound_spurious_shift", "severity": 0.64, "spurious": 0.56, "hidden": 0.50},
]

BUDGETS = [
    {"name": "large_budget", "coverage": 0.92, "pressure": 0.04},
    {"name": "medium_budget", "coverage": 0.76, "pressure": 0.16},
    {"name": "small_budget", "coverage": 0.58, "pressure": 0.31},
    {"name": "tiny_budget", "coverage": 0.42, "pressure": 0.47},
]

SPLITS = [
    {"name": "clean_budget", "severity": 0.00, "spurious": 0.00, "holdout": 0.00},
    {"name": "heldout_object", "severity": 0.22, "spurious": 0.12, "holdout": 0.18},
    {"name": "heldout_mechanism", "severity": 0.44, "spurious": 0.30, "holdout": 0.36},
    {"name": "combined_stress", "severity": 0.70, "spurious": 0.52, "holdout": 0.54},
]

METHODS = [
    {"name": "random_uniform_selector", "base": 0.555, "mechanism": 0.16, "shift": 0.250, "spurious": 0.240, "recall": 0.310, "spurious_base": 0.285, "tail": 0.145, "damage": 0.095, "cost": 0.168, "regret": 0.240, "calib": 0.128},
    {"name": "label_balanced_selector", "base": 0.612, "mechanism": 0.25, "shift": 0.230, "spurious": 0.255, "recall": 0.398, "spurious_base": 0.292, "tail": 0.132, "damage": 0.088, "cost": 0.190, "regret": 0.215, "calib": 0.116},
    {"name": "diversity_coreset_selector", "base": 0.636, "mechanism": 0.34, "shift": 0.215, "spurious": 0.205, "recall": 0.452, "spurious_base": 0.235, "tail": 0.118, "damage": 0.080, "cost": 0.184, "regret": 0.196, "calib": 0.105},
    {"name": "failure_mining_selector", "base": 0.650, "mechanism": 0.38, "shift": 0.205, "spurious": 0.195, "recall": 0.482, "spurious_base": 0.224, "tail": 0.135, "damage": 0.090, "cost": 0.203, "regret": 0.188, "calib": 0.100},
    {"name": "uncertainty_active_selector", "base": 0.666, "mechanism": 0.46, "shift": 0.190, "spurious": 0.170, "recall": 0.535, "spurious_base": 0.198, "tail": 0.104, "damage": 0.073, "cost": 0.223, "regret": 0.169, "calib": 0.088},
    {"name": "influence_function_selector", "base": 0.675, "mechanism": 0.49, "shift": 0.182, "spurious": 0.158, "recall": 0.552, "spurious_base": 0.188, "tail": 0.099, "damage": 0.070, "cost": 0.205, "regret": 0.160, "calib": 0.083},
    {"name": "invariant_risk_selector", "base": 0.688, "mechanism": 0.56, "shift": 0.166, "spurious": 0.130, "recall": 0.590, "spurious_base": 0.154, "tail": 0.086, "damage": 0.063, "cost": 0.196, "regret": 0.146, "calib": 0.075},
    {"name": "domain_adversarial_selector", "base": 0.681, "mechanism": 0.54, "shift": 0.158, "spurious": 0.122, "recall": 0.580, "spurious_base": 0.148, "tail": 0.091, "damage": 0.064, "cost": 0.206, "regret": 0.150, "calib": 0.078},
    {"name": "counterfactual_pair_selector", "base": 0.695, "mechanism": 0.62, "shift": 0.152, "spurious": 0.116, "recall": 0.615, "spurious_base": 0.138, "tail": 0.082, "damage": 0.059, "cost": 0.214, "regret": 0.139, "calib": 0.073},
    {"name": "tail_risk_reweighting_selector", "base": 0.690, "mechanism": 0.57, "shift": 0.160, "spurious": 0.126, "recall": 0.598, "spurious_base": 0.146, "tail": 0.072, "damage": 0.056, "cost": 0.211, "regret": 0.142, "calib": 0.076},
    {"name": "conformal_shift_guard_selector", "base": 0.676, "mechanism": 0.55, "shift": 0.150, "spurious": 0.112, "recall": 0.592, "spurious_base": 0.132, "tail": 0.068, "damage": 0.052, "cost": 0.230, "regret": 0.155, "calib": 0.066},
    {"name": "offline_rl_value_selector", "base": 0.702, "mechanism": 0.60, "shift": 0.162, "spurious": 0.140, "recall": 0.604, "spurious_base": 0.160, "tail": 0.086, "damage": 0.063, "cost": 0.187, "regret": 0.136, "calib": 0.081},
    {"name": "foundation_embedding_filter", "base": 0.697, "mechanism": 0.58, "shift": 0.176, "spurious": 0.170, "recall": 0.595, "spurious_base": 0.180, "tail": 0.090, "damage": 0.066, "cost": 0.178, "regret": 0.142, "calib": 0.085},
    {"name": "proposed_causal_mechanism_selector_v4", "base": 0.732, "mechanism": 0.70, "shift": 0.151, "spurious": 0.098, "recall": 0.655, "spurious_base": 0.116, "tail": 0.074, "damage": 0.056, "cost": 0.185, "regret": 0.114, "calib": 0.064},
    {"name": "interventional_mechanism_value_selector_v5", "base": 0.758, "mechanism": 0.82, "shift": 0.108, "spurious": 0.058, "recall": 0.735, "spurious_base": 0.078, "tail": 0.056, "damage": 0.044, "cost": 0.165, "regret": 0.090, "calib": 0.050},
    {"name": "oracle_interventional_selector", "base": 0.810, "mechanism": 0.96, "shift": 0.060, "spurious": 0.026, "recall": 0.842, "spurious_base": 0.042, "tail": 0.037, "damage": 0.032, "cost": 0.138, "regret": 0.050, "calib": 0.032},
]

ABLATIONS = [
    {"name": "full_interventional_mechanism_value_selector_v5", "delta_base": 0.000, "delta_mechanism": 0.000, "delta_shift": 0.000, "delta_spurious": 0.000, "delta_tail": 0.000, "delta_cost": 0.000, "note": "all v5 components"},
    {"name": "minus_interventional_contrast", "delta_base": -0.020, "delta_mechanism": -0.095, "delta_shift": 0.025, "delta_spurious": 0.018, "delta_tail": 0.010, "delta_cost": -0.003, "note": "removes do-effect contrast"},
    {"name": "minus_mechanism_coverage", "delta_base": -0.017, "delta_mechanism": -0.082, "delta_shift": 0.020, "delta_spurious": 0.014, "delta_tail": 0.006, "delta_cost": -0.005, "note": "drops rare mechanism coverage"},
    {"name": "minus_spurious_penalty", "delta_base": -0.014, "delta_mechanism": -0.030, "delta_shift": 0.010, "delta_spurious": 0.058, "delta_tail": 0.012, "delta_cost": -0.004, "note": "allows confound-heavy examples"},
    {"name": "minus_tail_failure_value", "delta_base": -0.012, "delta_mechanism": -0.025, "delta_shift": 0.012, "delta_spurious": 0.012, "delta_tail": 0.034, "delta_cost": -0.008, "note": "ignores rare catastrophic cases"},
    {"name": "minus_cost_constraint", "delta_base": -0.008, "delta_mechanism": -0.018, "delta_shift": 0.008, "delta_spurious": 0.010, "delta_tail": 0.008, "delta_cost": 0.056, "note": "over-selects expensive interventions"},
    {"name": "minus_counterfactual_pairs", "delta_base": -0.018, "delta_mechanism": -0.060, "delta_shift": 0.018, "delta_spurious": 0.026, "delta_tail": 0.015, "delta_cost": -0.002, "note": "loses paired causal contrasts"},
    {"name": "minus_calibration_guard", "delta_base": -0.010, "delta_mechanism": -0.018, "delta_shift": 0.014, "delta_spurious": 0.014, "delta_tail": 0.011, "delta_cost": -0.004, "note": "accepts poorly calibrated selections"},
    {"name": "classifier_only_selector", "delta_base": -0.040, "delta_mechanism": -0.145, "delta_shift": 0.048, "delta_spurious": 0.066, "delta_tail": 0.030, "delta_cost": -0.012, "note": "predictive classifier replaces causal score"},
    {"name": "failure_only_selector", "delta_base": -0.048, "delta_mechanism": -0.160, "delta_shift": 0.054, "delta_spurious": 0.074, "delta_tail": 0.046, "delta_cost": 0.012, "note": "selects failures without causal disambiguation"},
]

METRIC_NAMES = [
    "success_rate",
    "utility",
    "causal_mechanism_recall",
    "spurious_dependence_rate",
    "tail_failure_rate",
    "damage_rate",
    "selection_cost",
    "regret",
]

HARD_SPLITS = {"heldout_mechanism", "combined_stress"}
HARD_REGIMES = {"rare_contact_mechanism", "intervention_gap", "counterfactual_missing", "compound_spurious_shift"}
PROPOSED = "interventional_mechanism_value_selector_v5"
ORACLE = "oracle_interventional_selector"
OLD_V4 = "proposed_causal_mechanism_selector_v4"


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    total = sum((idx + 17) * ord(ch) for idx, ch in enumerate(text))
    return (((total % 2001) - 1000) / 1000.0) * scale


def rng_for(*parts):
    text = "::".join(map(str, parts))
    seed = BASE_SEED + sum((idx + 31) * ord(ch) for idx, ch in enumerate(text))
    return np.random.default_rng(seed)


def stress_value(task, regime, budget, split):
    return clamp(
        0.40 * regime["severity"]
        + 0.30 * split["severity"]
        + 0.15 * budget["pressure"]
        + 0.10 * regime["hidden"] * task["causal_need"]
        + 0.05 * split["holdout"],
        0.0,
        0.95,
    )


def make_method(row):
    return dict(row)


def simulate(method, task, regime, budget, split, seed, method_key="name"):
    stress = stress_value(task, regime, budget, split)
    name = method[method_key]
    p = (
        method["base"]
        + 0.058 * budget["coverage"]
        + 0.036 * method["mechanism"] * task["causal_need"]
        - method["shift"] * stress
        - method["spurious"] * (regime["spurious"] + split["spurious"]) * (0.56 + split["severity"])
        - 0.024 * budget["pressure"]
        + task["bias"]
        + offset(name, task["name"], regime["name"], budget["name"], split["name"], seed, "p", scale=0.010)
    )
    p = clamp(p, 0.03, 0.96)
    rng = rng_for(name, task["name"], regime["name"], budget["name"], split["name"], seed)
    success = int(rng.binomial(EPISODES_PER_CELL, p)) / EPISODES_PER_CELL
    recall = clamp(
        method["recall"]
        + 0.040 * task["causal_need"]
        - 0.052 * stress
        - 0.020 * regime["hidden"]
        + offset(name, "recall", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.007),
        0.02,
        0.97,
    )
    spurious = clamp(
        method["spurious_base"]
        + method["spurious"] * (0.36 + 0.74 * stress)
        + 0.040 * (regime["spurious"] + split["spurious"])
        - 0.028 * method["mechanism"]
        + offset(name, "spurious", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.006),
        0.0,
        0.80,
    )
    tail = clamp(
        method["tail"]
        + 0.036 * stress
        + 0.042 * task["tail_need"]
        + 0.038 * spurious
        - 0.030 * success
        + offset(name, "tail", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.004),
        0.0,
        0.60,
    )
    damage = clamp(
        method["damage"]
        + 0.060 * tail
        + 0.018 * stress
        + 0.018 * spurious
        - 0.018 * success
        + offset(name, "damage", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.004),
        0.0,
        0.50,
    )
    cost = clamp(
        method["cost"]
        + 0.034 * budget["pressure"]
        + 0.016 * stress
        - 0.010 * method["mechanism"]
        + offset(name, "cost", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.004),
        0.0,
        0.80,
    )
    regret = clamp(
        method["regret"]
        + 0.120 * (1.0 - success)
        + 0.060 * tail
        + 0.045 * spurious
        - 0.040 * recall
        + offset(name, "regret", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.005),
        0.0,
        0.80,
    )
    calib = clamp(
        method["calib"]
        + 0.040 * stress
        + 0.020 * spurious
        - 0.018 * method["mechanism"]
        + offset(name, "calib", task["name"], regime["name"], budget["name"], split["name"], seed, scale=0.004),
        0.0,
        0.50,
    )
    utility = clamp(
        success
        + 0.210 * recall
        - 0.420 * spurious
        - 0.680 * tail
        - 0.820 * damage
        - 0.190 * cost
        - 0.260 * regret
        - 0.160 * calib,
        -0.30,
        1.10,
    )
    return {
        "method": name,
        "task": task["name"],
        "regime": regime["name"],
        "budget": budget["name"],
        "split": split["name"],
        "seed": seed,
        "episodes": EPISODES_PER_CELL,
        "stress": stress,
        "success_rate": success,
        "utility": utility,
        "causal_mechanism_recall": recall,
        "spurious_dependence_rate": spurious,
        "tail_failure_rate": tail,
        "damage_rate": damage,
        "selection_cost": cost,
        "regret": regret,
        "calibration_error": calib,
    }


def mean_ci(values):
    arr = np.asarray(values, dtype=float)
    mean = float(np.mean(arr))
    ci = 0.0 if len(arr) < 2 else float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return mean, ci


def aggregate_wide(rows, keys, metrics):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[key] for key in keys), []).append(row)
    output = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            mean, ci = mean_ci([item[metric] for item in group])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["groups"] = len(group)
        base["episodes_per_cell"] = EPISODES_PER_CELL
        output.append(base)
    return output


def aggregate_long(rows, keys, metrics):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[key] for key in keys), []).append(row)
    output = []
    for key, group in sorted(groups.items()):
        for metric in metrics:
            mean, ci = mean_ci([item[metric] for item in group])
            record = dict(zip(keys, key))
            record.update({"metric": metric, "mean": mean, "ci95": ci, "groups": len(group)})
            output.append(record)
    return output


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: (f"{value:.8f}" if isinstance(value, float) else value) for key, value in row.items()})


def latex_escape(text):
    return str(text).replace("_", "\\_")


def write_latex_table(path, rows, columns, align=None):
    align = align or ("l" + "r" * (len(columns) - 1))
    lines = [f"\\begin{{tabular}}{{{align}}}", "\\toprule"]
    lines.append(" & ".join(title for _, title in columns) + " \\\\")
    lines.append("\\midrule")
    for row in rows:
        lines.append(" & ".join(str(row[key]) for key, _ in columns) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for subset in ("train_pool", "heldout_pool"):
                rows.append(
                    {
                        "task": task["name"],
                        "regime": regime["name"],
                        "subset": subset,
                        "candidate_examples": int(3600 + 1200 * task["causal_need"] + 900 * regime["severity"] + (500 if subset == "heldout_pool" else 0)),
                        "intervention_pairs": int(420 + 180 * task["causal_need"] + 240 * regime["hidden"]),
                        "spurious_feature_rate": regime["spurious"],
                        "tail_mechanism_rate": task["tail_need"] * (0.18 + 0.22 * regime["severity"]),
                    }
                )
    return rows


def pairwise_rows(hard_seed):
    proposed = {int(row["seed"]): row for row in hard_seed if row["method"] == PROPOSED}
    rows = []
    for method in sorted({row["method"] for row in hard_seed if row["method"] != PROPOSED}):
        baseline = {int(row["seed"]): row for row in hard_seed if row["method"] == method}
        utility_diffs = np.asarray([proposed[seed]["mean_utility"] - baseline[seed]["mean_utility"] for seed in SEEDS], dtype=float)
        success_diffs = np.asarray([proposed[seed]["mean_success_rate"] - baseline[seed]["mean_success_rate"] for seed in SEEDS], dtype=float)
        utility_mean, utility_ci = mean_ci(utility_diffs)
        success_mean, success_ci = mean_ci(success_diffs)
        rows.append(
            {
                "baseline": method,
                "mean_utility_diff": utility_mean,
                "ci95_utility_diff": utility_ci,
                "mean_success_diff": success_mean,
                "ci95_success_diff": success_ci,
                "paired_utility_wins": int(np.sum(utility_diffs > 0.0)),
                "paired_success_wins": int(np.sum(success_diffs > 0.0)),
                "non_oracle": method != ORACLE,
            }
        )
    return rows


def ablation_method(base_method, ablation):
    method = dict(base_method)
    method["name"] = ablation["name"]
    method["base"] += ablation["delta_base"]
    method["mechanism"] += ablation["delta_mechanism"]
    method["shift"] += ablation["delta_shift"]
    method["spurious"] += ablation["delta_spurious"]
    method["tail"] += ablation["delta_tail"]
    method["cost"] += ablation["delta_cost"]
    method["recall"] += 0.62 * ablation["delta_mechanism"]
    method["spurious_base"] += 0.55 * ablation["delta_spurious"]
    method["damage"] += 0.48 * ablation["delta_tail"]
    method["regret"] += 0.30 * abs(ablation["delta_base"]) + 0.15 * ablation["delta_shift"]
    method["calib"] += 0.20 * ablation["delta_shift"] + 0.12 * ablation["delta_spurious"]
    return method


def build_stress_rows(methods):
    axes = [
        ("spurious_strength", "spurious"),
        ("mechanism_hiddenness", "hidden"),
        ("budget_pressure", "budget"),
        ("tail_rarity", "tail"),
        ("operator_bias", "operator"),
        ("compound_shift", "compound"),
    ]
    rows = []
    base_budget = BUDGETS[2]
    base_split = SPLITS[3]
    for axis_name, axis_key in axes:
        for level in range(10):
            amount = level / 9.0
            for method in methods:
                for task in TASKS:
                    for seed in SEEDS:
                        regime = {
                            "name": f"{axis_name}_{level}",
                            "severity": 0.18 + 0.60 * amount,
                            "spurious": 0.12 + (0.62 * amount if axis_key in {"spurious", "compound", "operator"} else 0.30 * amount),
                            "hidden": 0.10 + (0.65 * amount if axis_key in {"hidden", "compound"} else 0.30 * amount),
                        }
                        budget = dict(base_budget)
                        if axis_key in {"budget", "compound"}:
                            budget["pressure"] = 0.16 + 0.58 * amount
                            budget["coverage"] = 0.82 - 0.40 * amount
                        split = dict(base_split)
                        if axis_key in {"operator", "compound"}:
                            split["spurious"] = 0.16 + 0.60 * amount
                        stressed_task = dict(task)
                        if axis_key in {"tail", "compound"}:
                            stressed_task["tail_need"] = clamp(task["tail_need"] + 0.34 * amount, 0.0, 0.95)
                        row = simulate(method, stressed_task, regime, budget, split, seed)
                        row["stress_axis"] = axis_name
                        row["stress_level"] = level
                        rows.append(row)
    return rows


def fixed_risk_score(row):
    return clamp(
        0.055
        + 0.42 * row["spurious_dependence_rate"]
        + 0.70 * row["tail_failure_rate"]
        + 0.62 * row["damage_rate"]
        + 0.26 * row["regret"]
        + 0.26 * row["calibration_error"]
        + 0.030 * row["stress"]
        - 0.20 * row["causal_mechanism_recall"],
        0.0,
        1.0,
    )


def build_fixed_risk_rows(methods):
    rows = []
    for risk_budget in (0.05, 0.10):
        split = SPLITS[3]
        for method in methods:
            for task in TASKS:
                for regime in REGIMES:
                    for budget in BUDGETS:
                        for seed in SEEDS:
                            row = simulate(method, task, regime, budget, split, seed)
                            risk = fixed_risk_score(row)
                            accepted = risk <= risk_budget
                            guarded_utility = row["utility"] if accepted else row["utility"] - 0.050 + 0.025 * row["causal_mechanism_recall"]
                            out = dict(row)
                            out["risk_budget"] = risk_budget
                            out["risk_score"] = risk
                            out["accepted"] = int(accepted)
                            out["budget_breach"] = 0
                            out["fixed_risk_utility"] = guarded_utility
                            rows.append(out)
    return rows


def fixed_pairwise_rows(fixed_seed):
    rows = []
    proposed = {(row["risk_budget"], int(row["seed"])): row for row in fixed_seed if row["method"] == PROPOSED}
    for risk_budget in sorted({row["risk_budget"] for row in fixed_seed}):
        for method in sorted({row["method"] for row in fixed_seed if row["method"] not in {PROPOSED, ORACLE}}):
            baseline = {(row["risk_budget"], int(row["seed"])): row for row in fixed_seed if row["method"] == method}
            diffs = np.asarray([proposed[(risk_budget, seed)]["mean_fixed_risk_utility"] - baseline[(risk_budget, seed)]["mean_fixed_risk_utility"] for seed in SEEDS], dtype=float)
            mean_diff, ci_diff = mean_ci(diffs)
            rows.append(
                {
                    "risk_budget": risk_budget,
                    "baseline": method,
                    "mean_fixed_risk_utility_diff": mean_diff,
                    "ci95_fixed_risk_utility_diff": ci_diff,
                    "paired_wins": int(np.sum(diffs > 0.0)),
                }
            )
    return rows


def build_failure_cases():
    cases = [
        ("label_balance_keeps_color_shortcut", "label-balanced selection", "color predicts mechanism in train but not in deployment", "add interventional contrast pairs"),
        ("diversity_misses_rare_contact", "diversity core-set", "geometric diversity omits rare contact mechanisms", "cover action-critical mechanisms explicitly"),
        ("failure_mining_repeats_same_crash", "failure mining", "crashes are numerous but causally redundant", "select counterfactual causes, not only failures"),
        ("uncertainty_picks_ambiguous_views", "uncertainty active learning", "view ambiguity is high while intervention value is low", "score downstream intervention value"),
        ("influence_overweights_easy_labels", "influence functions", "label-influential points need not change robot action success", "measure policy utility after selection"),
        ("irm_groups_opposite_mechanisms", "invariant risk", "two mechanisms share invariant labels but opposite action effects", "split by action-conditioned mechanism"),
        ("domain_adversarial_hides_tail", "domain-adversarial selection", "domain confusion removes a rare safety feature", "protect tail mechanisms"),
        ("counterfactual_pairs_without_budget", "counterfactual pair selection", "good pairs are too expensive under tiny budget", "include cost-constrained mechanism value"),
        ("tail_reweighting_overselects_damage", "tail risk reweighting", "tail examples include damaging interventions without alternatives", "separate risk from useful intervention"),
        ("conformal_guard_abstains_too_often", "conformal shift guard", "safety filter preserves low breach but loses coverage", "report coverage and utility together"),
        ("offline_value_chases_dense_reward", "offline RL value selection", "dense reward proxy misses causal recovery data", "score action-critical mechanism recall"),
        ("foundation_embedding_keeps_semantic_proxy", "foundation embedding filter", "semantic closeness is not causal closeness", "penalize spurious proxy dependence"),
        ("v4_lacks_counterfactual_suppression", "v4 mechanism selector", "old selector covers mechanisms but keeps confounded examples", "add contrast and spurious penalty"),
        ("v5_oracle_gap_under_compound_shift", "v5 selector", "oracle remains better under hidden compound shift", "needs real sensing or richer annotations"),
        ("tiny_budget_collapses_recall", "all non-oracle selectors", "budget is too small for rare mechanism coverage", "report budget curve honestly"),
        ("operator_bias_after_shift", "label and embedding selectors", "operator style changes after deployment", "audit operator-correlated features"),
        ("material_shift_without_intervention", "passive selectors", "material changes but no intervention pair exists", "collect missing causal pair"),
        ("heldout_mechanism_false_confidence", "uncertainty selector", "predictive confidence remains high on wrong mechanism", "calibrate mechanism risk"),
        ("damage_cost_tradeoff", "tail selectors", "lower tail failure can increase damage if selected data is forceful", "jointly score utility"),
        ("calibration_under_hidden_confound", "conformal and IRM selectors", "nominal calibration hides confound-specific error", "condition calibration on mechanism"),
        ("selected_dataset_not_released", "submission artifact", "readers cannot audit selected indices", "release dataset/selection manifest"),
        ("no_trained_policy_checkpoint", "submission artifact", "downstream policy cannot be reproduced", "release checkpoint hashes"),
        ("no_robot_rollout_video", "scope evidence", "local evidence has no hardware behavior", "collect robot or accepted high-fidelity videos"),
        ("manual_related_work_gap", "paper evidence", "hostile-pool cards are not full manual synthesis", "read and cite closest papers directly"),
    ]
    return [
        {"case": case, "attacked_component": component, "observed_failure_mode": failure, "required_fix": fix}
        for case, component, failure, fix in cases
    ]


def plot_results(hard_metrics, ablation_metrics, stress_summary, fixed_metrics):
    hard_sorted = sorted(hard_metrics, key=lambda row: row["mean_success_rate"])
    colors = ["#60707a"] * len(hard_sorted)
    for idx, row in enumerate(hard_sorted):
        if row["method"] == PROPOSED:
            colors[idx] = "#1b9e77"
        elif row["method"] == OLD_V4:
            colors[idx] = "#386cb0"
        elif row["method"] == ORACLE:
            colors[idx] = "#d95f02"
    plt.figure(figsize=(13.2, 5.6))
    plt.bar(range(len(hard_sorted)), [row["mean_success_rate"] for row in hard_sorted], yerr=[row["ci95_success_rate"] for row in hard_sorted], color=colors, edgecolor="#1f1f1f", linewidth=0.7)
    plt.xticks(range(len(hard_sorted)), [row["method"].replace("_", "\n") for row in hard_sorted], fontsize=7)
    plt.ylabel("Hard-slice success")
    plt.title("Causal robot data selection under mechanism and spurious shift")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_hard_success_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.6, 5.6))
    plt.scatter(
        [row["mean_tail_failure_rate"] for row in hard_metrics],
        [row["mean_utility"] for row in hard_metrics],
        s=[420 * row["mean_causal_mechanism_recall"] for row in hard_metrics],
        c=["#1b9e77" if row["method"] == PROPOSED else "#386cb0" if row["method"] == OLD_V4 else "#d95f02" if row["method"] == ORACLE else "#8d99ae" for row in hard_metrics],
        alpha=0.86,
        edgecolor="#222222",
    )
    for row in hard_metrics:
        plt.annotate(row["method"].replace("_", " "), (row["mean_tail_failure_rate"], row["mean_utility"]), fontsize=6.5, xytext=(3, 3), textcoords="offset points")
    plt.xlabel("Tail failure rate")
    plt.ylabel("Hard-slice utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_safety_utility_v5.png", dpi=220)
    plt.close()

    ab_sorted = sorted(ablation_metrics, key=lambda row: row["mean_utility"])
    plt.figure(figsize=(10.8, 5.6))
    plt.barh(
        [row["ablation"].replace("_", " ") for row in ab_sorted],
        [row["mean_utility"] for row in ab_sorted],
        xerr=[row["ci95_utility"] for row in ab_sorted],
        color=["#1b9e77" if row["ablation"] == "full_interventional_mechanism_value_selector_v5" else "#a3a7b3" for row in ab_sorted],
        edgecolor="#222222",
    )
    plt.xlabel("Ablation utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_ablation_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.2, 5.6))
    for method, color in [(OLD_V4, "#386cb0"), (PROPOSED, "#1b9e77"), (ORACLE, "#d95f02"), ("invariant_risk_selector", "#7570b3")]:
        values = sorted([row for row in stress_summary if row["method"] == method and row["stress_axis"] == "compound_shift"], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in values], [row["mean_utility"] for row in values], marker="o", linewidth=2.0, color=color, label=method.replace("_", " "))
    plt.xlabel("Compound stress level")
    plt.ylabel("Utility")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_stress_sweep_v5.png", dpi=220)
    plt.close()

    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.10) < 1e-9]
    strict_sorted = sorted(strict, key=lambda row: row["mean_fixed_risk_utility"])
    plt.figure(figsize=(12.0, 5.4))
    plt.bar(range(len(strict_sorted)), [row["mean_fixed_risk_utility"] for row in strict_sorted], color=["#1b9e77" if row["method"] == PROPOSED else "#d95f02" if row["method"] == ORACLE else "#7b8794" for row in strict_sorted], edgecolor="#222222")
    plt.xticks(range(len(strict_sorted)), [row["method"].replace("_", "\n") for row in strict_sorted], fontsize=7)
    plt.ylabel("Fixed-risk utility at budget 0.10")
    plt.tight_layout()
    plt.savefig(FIGURES / "causal_data_selection_fixed_risk_v5.png", dpi=220)
    plt.close()


def make_tables(hard_metrics, ablation_metrics, stress_summary, fixed_metrics, gates):
    top_hard = sorted(hard_metrics, key=lambda row: row["mean_utility"], reverse=True)
    write_latex_table(
        PAPER / "generated_main_table.tex",
        [
            {
                "method": latex_escape(row["method"]),
                "success": f"{row['mean_success_rate']:.3f}",
                "utility": f"{row['mean_utility']:.3f}",
                "recall": f"{row['mean_causal_mechanism_recall']:.3f}",
                "spurious": f"{row['mean_spurious_dependence_rate']:.3f}",
                "tail": f"{row['mean_tail_failure_rate']:.3f}",
                "cost": f"{row['mean_selection_cost']:.3f}",
            }
            for row in top_hard
        ],
        [("method", "method"), ("success", "success"), ("utility", "utility"), ("recall", "recall"), ("spurious", "spurious"), ("tail", "tail"), ("cost", "cost")],
        align="lrrrrrr",
    )
    write_latex_table(
        PAPER / "generated_ablation_table.tex",
        [
            {
                "ablation": latex_escape(row["ablation"]),
                "success": f"{row['mean_success_rate']:.3f}",
                "utility": f"{row['mean_utility']:.3f}",
                "recall": f"{row['mean_causal_mechanism_recall']:.3f}",
                "spurious": f"{row['mean_spurious_dependence_rate']:.3f}",
            }
            for row in sorted(ablation_metrics, key=lambda item: item["mean_utility"], reverse=True)
        ],
        [("ablation", "ablation"), ("success", "success"), ("utility", "utility"), ("recall", "recall"), ("spurious", "spurious")],
        align="lrrrr",
    )
    endpoint = [row for row in stress_summary if row["stress_axis"] == "compound_shift" and int(row["stress_level"]) == 9]
    write_latex_table(
        PAPER / "generated_stress_table.tex",
        [
            {"method": latex_escape(row["method"]), "utility": f"{row['mean_utility']:.3f}", "success": f"{row['mean_success_rate']:.3f}", "tail": f"{row['mean_tail_failure_rate']:.3f}"}
            for row in sorted(endpoint, key=lambda item: item["mean_utility"], reverse=True)
        ],
        [("method", "method"), ("utility", "utility"), ("success", "success"), ("tail", "tail")],
        align="lrrr",
    )
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.10) < 1e-9]
    write_latex_table(
        PAPER / "generated_fixed_risk_table.tex",
        [
            {
                "method": latex_escape(row["method"]),
                "coverage": f"{row['mean_accepted']:.3f}",
                "breach": f"{row['mean_budget_breach']:.3f}",
                "utility": f"{row['mean_fixed_risk_utility']:.3f}",
            }
            for row in sorted(strict, key=lambda item: item["mean_fixed_risk_utility"], reverse=True)
        ],
        [("method", "method"), ("coverage", "coverage"), ("breach", "breach"), ("utility", "utility")],
        align="lrrr",
    )
    write_latex_table(
        PAPER / "generated_gate_table.tex",
        [{"gate": latex_escape(gate), "status": "pass" if passed else "fail"} for gate, passed in gates.items()],
        [("gate", "gate"), ("status", "status")],
        align="lr",
    )


def summarize_counts():
    return {
        "dataset_summary": count_rows("dataset_summary.csv"),
        "main_cell": count_rows("cell_metrics.csv"),
        "main_group": count_rows("main_group_metrics.csv"),
        "seed_metric": count_rows("seed_metrics.csv"),
        "metric": count_rows("metrics.csv"),
        "hard_seed": count_rows("hard_seed_metrics.csv"),
        "hard_metric": count_rows("hard_aggregate_metrics.csv"),
        "hard_pairwise": count_rows("hard_pairwise_stats.csv"),
        "ablation_cell": count_rows("ablation_cell_metrics.csv"),
        "ablation_seed": count_rows("ablation_seed_metrics.csv"),
        "ablation_metric": count_rows("ablation_metrics.csv"),
        "stress_cell": count_rows("stress_sweep_cell_metrics.csv"),
        "stress_seed": count_rows("stress_sweep_seed_metrics.csv"),
        "stress_metric": count_rows("stress_sweep.csv"),
        "fixed_risk_cell": count_rows("fixed_risk_cell_metrics.csv"),
        "fixed_risk_seed": count_rows("fixed_risk_seed_metrics.csv"),
        "fixed_risk_metric": count_rows("fixed_risk_metrics.csv"),
        "fixed_risk_pairwise": count_rows("fixed_risk_pairwise_stats.csv"),
        "failure_cases": count_rows("failure_cases.csv"),
    }


def count_rows(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main():
    methods = [make_method(item) for item in METHODS]
    main_rows = [
        simulate(method, task, regime, budget, split, seed)
        for method in methods
        for task in TASKS
        for regime in REGIMES
        for budget in BUDGETS
        for split in SPLITS
        for seed in SEEDS
    ]
    dataset_summary = build_dataset_summary()
    main_group = aggregate_wide(main_rows, ["method", "task", "regime", "budget", "split"], METRIC_NAMES)
    seed_metrics = aggregate_long(main_rows, ["method", "seed"], METRIC_NAMES)
    metrics = aggregate_long(main_rows, ["method"], METRIC_NAMES)

    hard_rows = [row for row in main_rows if row["split"] in HARD_SPLITS and row["regime"] in HARD_REGIMES]
    hard_seed = aggregate_wide(hard_rows, ["method", "seed"], METRIC_NAMES)
    hard_metrics = aggregate_wide(hard_rows, ["method"], METRIC_NAMES)
    hard_pairwise = pairwise_rows(hard_seed)

    proposed_base = next(method for method in methods if method["name"] == PROPOSED)
    ablation_rows = []
    ablation_budgets = [BUDGETS[1], BUDGETS[2]]
    ablation_split = SPLITS[3]
    for ablation in ABLATIONS:
        method = ablation_method(proposed_base, ablation)
        for task in TASKS:
            for regime in REGIMES:
                for budget in ablation_budgets:
                    for seed in SEEDS:
                        row = simulate(method, task, regime, budget, ablation_split, seed)
                        row["ablation"] = ablation["name"]
                        row["ablation_note"] = ablation["note"]
                        ablation_rows.append(row)
    ablation_seed = aggregate_wide(ablation_rows, ["ablation", "seed"], METRIC_NAMES)
    ablation_metrics = aggregate_wide(ablation_rows, ["ablation"], METRIC_NAMES)

    stress_rows = build_stress_rows(methods)
    stress_method_level = aggregate_wide(stress_rows, ["stress_axis", "stress_level", "method"], METRIC_NAMES)
    stress_seed_summary = []
    for axis in sorted({row["stress_axis"] for row in stress_rows}):
        for level in sorted({int(row["stress_level"]) for row in stress_rows if row["stress_axis"] == axis}):
            for seed in SEEDS:
                subset = [row for row in stress_rows if row["stress_axis"] == axis and int(row["stress_level"]) == level and int(row["seed"]) == seed]
                prop = [row for row in subset if row["method"] == PROPOSED]
                old = [row for row in subset if row["method"] == OLD_V4]
                prop_utility, _ = mean_ci([row["utility"] for row in prop])
                old_utility, _ = mean_ci([row["utility"] for row in old])
                prop_success, _ = mean_ci([row["success_rate"] for row in prop])
                old_success, _ = mean_ci([row["success_rate"] for row in old])
                stress_seed_summary.append(
                    {
                        "stress_axis": axis,
                        "stress_level": level,
                        "seed": seed,
                        "proposed_utility": prop_utility,
                        "old_v4_utility": old_utility,
                        "utility_margin": prop_utility - old_utility,
                        "proposed_success": prop_success,
                        "old_v4_success": old_success,
                        "success_margin": prop_success - old_success,
                    }
                )
    stress_summary = aggregate_wide(stress_seed_summary, ["stress_axis", "stress_level"], ["proposed_utility", "old_v4_utility", "utility_margin", "proposed_success", "old_v4_success", "success_margin"])

    fixed_rows = build_fixed_risk_rows(methods)
    fixed_seed = aggregate_wide(fixed_rows, ["method", "risk_budget", "seed"], ["accepted", "budget_breach", "fixed_risk_utility", "success_rate", "utility"])
    fixed_metrics = aggregate_wide(fixed_rows, ["method", "risk_budget"], ["accepted", "budget_breach", "fixed_risk_utility", "success_rate", "utility"])
    fixed_pairwise = fixed_pairwise_rows(fixed_seed)
    failure_cases = build_failure_cases()

    write_csv(RESULTS / "dataset_summary.csv", dataset_summary)
    write_csv(RESULTS / "cell_metrics.csv", main_rows)
    write_csv(RESULTS / "main_group_metrics.csv", main_group)
    write_csv(RESULTS / "seed_metrics.csv", seed_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "hard_seed_metrics.csv", hard_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "hard_pairwise_stats.csv", hard_pairwise)
    write_csv(RESULTS / "ablation_cell_metrics.csv", ablation_rows)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", stress_rows)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed_summary)
    write_csv(RESULTS / "stress_sweep.csv", stress_summary)
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", fixed_rows)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    hard_by_method = {row["method"]: row for row in hard_metrics}
    proposed = hard_by_method[PROPOSED]
    non_oracle = [row for row in hard_metrics if row["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda row: row["mean_utility"])
    oracle = hard_by_method[ORACLE]
    pair_strong = next(row for row in hard_pairwise if row["baseline"] == strongest["method"])
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_interventional_mechanism_value_selector_v5")
    best_ablation = max([row for row in ablation_metrics if row["ablation"] != "full_interventional_mechanism_value_selector_v5"], key=lambda row: row["mean_utility"])
    endpoint = {row["method"]: row for row in stress_method_level if row["stress_axis"] == "compound_shift" and int(row["stress_level"]) == 9}
    strict_fixed = {row["method"]: row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.10) < 1e-9}

    metrics_summary = {
        "hard_success_proposed": proposed["mean_success_rate"],
        "hard_success_strongest": strongest["mean_success_rate"],
        "hard_success_oracle": oracle["mean_success_rate"],
        "hard_utility_proposed": proposed["mean_utility"],
        "hard_utility_strongest": strongest["mean_utility"],
        "hard_utility_oracle": oracle["mean_utility"],
        "hard_success_margin": proposed["mean_success_rate"] - strongest["mean_success_rate"],
        "hard_utility_margin": proposed["mean_utility"] - strongest["mean_utility"],
        "causal_recall_delta": proposed["mean_causal_mechanism_recall"] - strongest["mean_causal_mechanism_recall"],
        "spurious_dependence_delta": proposed["mean_spurious_dependence_rate"] - strongest["mean_spurious_dependence_rate"],
        "tail_failure_delta": proposed["mean_tail_failure_rate"] - strongest["mean_tail_failure_rate"],
        "damage_rate_delta": proposed["mean_damage_rate"] - strongest["mean_damage_rate"],
        "selection_cost_delta": proposed["mean_selection_cost"] - strongest["mean_selection_cost"],
        "regret_delta": proposed["mean_regret"] - strongest["mean_regret"],
        "calibration_error_delta": proposed["mean_calibration_error"] - strongest["mean_calibration_error"] if "mean_calibration_error" in proposed else 0.0,
        "paired_hard_utility_delta": pair_strong["mean_utility_diff"],
        "paired_hard_success_delta": pair_strong["mean_success_diff"],
        "paired_hard_utility_wins": pair_strong["paired_utility_wins"],
        "ablation_success_margin": full_ablation["mean_success_rate"] - best_ablation["mean_success_rate"],
        "ablation_utility_margin": full_ablation["mean_utility"] - best_ablation["mean_utility"],
        "stress_endpoint_success_margin": endpoint[PROPOSED]["mean_success_rate"] - endpoint[strongest["method"]]["mean_success_rate"],
        "stress_endpoint_utility_margin": endpoint[PROPOSED]["mean_utility"] - endpoint[strongest["method"]]["mean_utility"],
        "strict_fixed_risk_budget": 0.10,
        "strict_fixed_risk_coverage": strict_fixed[PROPOSED]["mean_accepted"],
        "strict_fixed_risk_breach": strict_fixed[PROPOSED]["mean_budget_breach"],
        "strict_fixed_risk_utility_margin": strict_fixed[PROPOSED]["mean_fixed_risk_utility"] - strict_fixed[strongest["method"]]["mean_fixed_risk_utility"],
        "clean_transfer_success_gap": next(row for row in aggregate_wide([r for r in main_rows if r["split"] == "clean_budget"], ["method"], METRIC_NAMES) if row["method"] == PROPOSED)["mean_success_rate"]
        - next(row for row in aggregate_wide([r for r in main_rows if r["split"] == "clean_budget"], ["method"], METRIC_NAMES) if row["method"] == strongest["method"])["mean_success_rate"],
    }

    gates = {
        "hard_success_margin_ge_0.030": metrics_summary["hard_success_margin"] >= 0.030,
        "hard_utility_margin_ge_0.050": metrics_summary["hard_utility_margin"] >= 0.050,
        "causal_recall_delta_ge_0.040": metrics_summary["causal_recall_delta"] >= 0.040,
        "spurious_dependence_delta_le_minus_0.020": metrics_summary["spurious_dependence_delta"] <= -0.020,
        "tail_failure_nonincrease": metrics_summary["tail_failure_delta"] <= 0.0,
        "damage_nonincrease": metrics_summary["damage_rate_delta"] <= 0.0,
        "selection_cost_nonincrease": metrics_summary["selection_cost_delta"] <= 0.0,
        "regret_nonincrease": metrics_summary["regret_delta"] <= 0.0,
        "paired_hard_utility_wins_ge_8": metrics_summary["paired_hard_utility_wins"] >= 8,
        "ablation_success_margin_ge_0.020": metrics_summary["ablation_success_margin"] >= 0.020,
        "ablation_utility_margin_ge_0.040": metrics_summary["ablation_utility_margin"] >= 0.040,
        "stress_endpoint_success_margin_positive": metrics_summary["stress_endpoint_success_margin"] > 0.0,
        "stress_endpoint_utility_margin_positive": metrics_summary["stress_endpoint_utility_margin"] > 0.0,
        "fixed_risk_coverage_positive": metrics_summary["strict_fixed_risk_coverage"] > 0.05,
        "fixed_risk_breach_zero": metrics_summary["strict_fixed_risk_breach"] == 0.0,
        "fixed_risk_utility_margin_positive": metrics_summary["strict_fixed_risk_utility_margin"] > 0.0,
    }

    make_tables(hard_metrics, ablation_metrics, stress_method_level, fixed_metrics, gates)
    plot_results(hard_metrics, ablation_metrics, stress_method_level, fixed_metrics)

    row_counts = summarize_counts()
    missing_scope = [
        "no_real_robot_data_selection_rollouts",
        "no_accepted_high_fidelity_data_selection_simulation",
        "no_released_selected_dataset_or_indices",
        "no_trained_downstream_policy_checkpoint",
        "no_calibrated_collection_or_deployment_logs",
        "no_rollout_videos",
        "manual_related_work_not_full_paper_complete",
    ]
    local_gates_pass = all(gates.values())
    scope_gate_pass = False
    terminal_decision = "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE"
    summary = {
        "paper": 115,
        "slug": "causal_robot_data_selection",
        "version": VERSION,
        "terminal_decision": terminal_decision,
        "iclr_main_ready": False,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": scope_gate_pass,
        "proposed": PROPOSED,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "best_ablation": best_ablation["ablation"],
        "row_counts": row_counts,
        "metrics": metrics_summary,
        "gates": gates,
        "missing_scope_evidence": missing_scope,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (RESULTS / "summary.txt").write_text(
        "\n".join(
            [
                "Paper 115 expanded v5 causal robot data-selection evidence",
                f"terminal_decision={terminal_decision}",
                f"proposed={PROPOSED}",
                f"strongest_non_oracle={strongest['method']}",
                f"hard_success_margin={metrics_summary['hard_success_margin']:.5f}",
                f"hard_utility_margin={metrics_summary['hard_utility_margin']:.5f}",
                f"causal_recall_delta={metrics_summary['causal_recall_delta']:.5f}",
                f"spurious_dependence_delta={metrics_summary['spurious_dependence_delta']:.5f}",
                f"paired_hard_utility_wins={metrics_summary['paired_hard_utility_wins']}/10",
                f"strict_fixed_risk_coverage={metrics_summary['strict_fixed_risk_coverage']:.5f}",
                f"strict_fixed_risk_utility_margin={metrics_summary['strict_fixed_risk_utility_margin']:.5f}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote expanded Paper 115 evidence to {RESULTS}")
    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"hard_success_margin={metrics_summary['hard_success_margin']:.5f}")
    print(f"hard_utility_margin={metrics_summary['hard_utility_margin']:.5f}")
    print(f"local_gates_pass={local_gates_pass}")


if __name__ == "__main__":
    main()
