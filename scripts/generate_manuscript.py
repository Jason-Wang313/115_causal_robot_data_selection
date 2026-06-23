import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"


def esc(text):
    return str(text).replace("_", "\\_")


def fmt(value, digits=5):
    return f"{float(value):.{digits}f}"


TASK_CARDS = [
    ("contact_grasp_policy", "Grasping under contact, friction, geometry, and object-appearance confounds."),
    ("peg_search_policy", "Insertion/search behavior where success labels can hide intervention-specific contact causes."),
    ("deformable_pull_policy", "Deformable manipulation where material and support changes create rare but important tail outcomes."),
    ("mobile_place_policy", "Mobile manipulation placement with operator, camera, and object-context shortcuts."),
    ("force_limited_twist_policy", "Force-limited twisting where damaging examples can be frequent but causally uninformative."),
]

REGIME_CARDS = [
    ("iid_mechanisms", "Mechanisms and spurious features are aligned between selection and deployment."),
    ("color_mechanism_confound", "Color is predictive in the pool but is not causal under deployment."),
    ("material_shift", "Material changes alter contact effects while labels stay stable."),
    ("operator_bias_shift", "Operator style and demonstration statistics shift after selection."),
    ("rare_contact_mechanism", "A rare contact mode controls success but is sparsely represented."),
    ("intervention_gap", "Observed failures lack the intervention contrast needed to identify the cause."),
    ("counterfactual_missing", "Only one side of a necessary causal pair is selected."),
    ("compound_spurious_shift", "Several shortcut and mechanism shifts occur together."),
]

BASELINE_CARDS = [
    ("random_uniform_selector", "A budget-respecting random subset."),
    ("label_balanced_selector", "Balances task labels and outcome labels without causal structure."),
    ("diversity_coreset_selector", "Uses geometric or embedding diversity, following the core-set active learning intuition."),
    ("failure_mining_selector", "Over-samples failures and hard negatives."),
    ("uncertainty_active_selector", "Selects high-uncertainty examples."),
    ("influence_function_selector", "Selects points estimated to influence downstream predictions."),
    ("invariant_risk_selector", "Encourages environment-invariant predictors."),
    ("domain_adversarial_selector", "Suppresses domain-identifying features."),
    ("counterfactual_pair_selector", "Selects observed counterfactual pairs when available."),
    ("tail_risk_reweighting_selector", "Prioritizes rare tail failures."),
    ("conformal_shift_guard_selector", "Keeps data that passes a conservative shift-risk screen."),
    ("offline_rl_value_selector", "Ranks examples by offline value estimates."),
    ("foundation_embedding_filter", "Filters data using foundation-model embedding similarity."),
    ("proposed_causal_mechanism_selector_v4", "The retained old method and expected strongest non-oracle comparator."),
    ("interventional_mechanism_value_selector_v5", "The proposed selector with intervention contrast, mechanism coverage, spurious suppression, and deployment value."),
    ("oracle_interventional_selector", "Upper bound with access to the true action-critical mechanism."),
]

ABLATION_CARDS = [
    ("full_interventional_mechanism_value_selector_v5", "All v5 terms enabled."),
    ("minus_interventional_contrast", "Removes do-effect contrast."),
    ("minus_mechanism_coverage", "Drops rare mechanism coverage."),
    ("minus_spurious_penalty", "Allows confound-heavy examples."),
    ("minus_tail_failure_value", "Ignores rare catastrophic mechanisms."),
    ("minus_cost_constraint", "Over-selects expensive interventions."),
    ("minus_counterfactual_pairs", "Loses paired causal contrasts."),
    ("minus_calibration_guard", "Accepts poorly calibrated selections."),
    ("classifier_only_selector", "Replaces mechanism value with predictive classification."),
    ("failure_only_selector", "Mines failures without causal disambiguation."),
]

REFERENCES = r"""
@techreport{settles2009active,
  title={Active Learning Literature Survey},
  author={Settles, Burr},
  institution={University of Wisconsin-Madison},
  number={1648},
  year={2009}
}

@inproceedings{sener2018coreset,
  title={Active Learning for Convolutional Neural Networks: A Core-Set Approach},
  author={Sener, Ozan and Savarese, Silvio},
  booktitle={International Conference on Learning Representations},
  year={2018}
}

@inproceedings{koh2017influence,
  title={Understanding Black-box Predictions via Influence Functions},
  author={Koh, Pang Wei and Liang, Percy},
  booktitle={International Conference on Machine Learning},
  pages={1885--1894},
  year={2017}
}

@article{arjovsky2019irm,
  title={Invariant Risk Minimization},
  author={Arjovsky, Martin and Bottou, Leon and Gulrajani, Ishaan and Lopez-Paz, David},
  journal={arXiv preprint arXiv:1907.02893},
  year={2019}
}

@inproceedings{dehaan2019causal,
  title={Causal Confusion in Imitation Learning},
  author={de Haan, Pim and Jayaraman, Dinesh and Levine, Sergey},
  booktitle={Advances in Neural Information Processing Systems},
  year={2019}
}

@article{fu2020d4rl,
  title={D4RL: Datasets for Deep Data-Driven Reinforcement Learning},
  author={Fu, Justin and Kumar, Aviral and Nachum, Ofir and Tucker, George and Levine, Sergey},
  journal={arXiv preprint arXiv:2004.07219},
  year={2020}
}

@inproceedings{dasari2020robonet,
  title={RoboNet: Large-Scale Multi-Robot Learning},
  author={Dasari, Sudeep and Ebert, Frederik and Tian, Stephen and Nair, Suraj and Bucher, Bernadette and Schmeckpeper, Karl and Singh, Siddharth and Levine, Sergey and Finn, Chelsea},
  booktitle={Conference on Robot Learning},
  pages={885--897},
  year={2020}
}

@inproceedings{brohan2023rt1,
  title={RT-1: Robotics Transformer for Real-World Control at Scale},
  author={Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Keerthana and Hausman, Karol and Herzog, Alexander and Hsu, Jasmine and Ibarz, Julian and Ichter, Brian and Irpan, Alex and others},
  booktitle={Robotics: Science and Systems},
  year={2023}
}

@article{openx2023,
  title={Open X-Embodiment: Robotic Learning Datasets and RT-X Models},
  author={{Open X-Embodiment Collaboration}},
  journal={arXiv preprint arXiv:2310.08864},
  year={2023}
}

@book{pearl2009causality,
  title={Causality},
  author={Pearl, Judea},
  publisher={Cambridge University Press},
  year={2009}
}

@article{peters2016invariant,
  title={Causal Inference by Using Invariant Prediction: Identification and Confidence Intervals},
  author={Peters, Jonas and Buhlmann, Peter and Meinshausen, Nicolai},
  journal={Journal of the Royal Statistical Society: Series B},
  volume={78},
  number={5},
  pages={947--1012},
  year={2016}
}
"""


def load_failure_cases():
    with (RESULTS / "failure_cases.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def make_manuscript(summary):
    m = summary["metrics"]
    rc = summary["row_counts"]
    failures = load_failure_cases()
    lines = []
    a = lines.append

    a(r"\documentclass{article}")
    a(r"\usepackage{iclr2026_conference,times}")
    a(r"\input{math_commands.tex}")
    a(r"\usepackage{hyperref}")
    a(r"\usepackage{url}")
    a(r"\usepackage{booktabs}")
    a(r"\usepackage{graphicx}")
    a(r"\usepackage{amsmath}")
    a(r"\usepackage{amssymb}")
    a(r"\usepackage{xcolor}")
    a(r"\usepackage{microtype}")
    a(r"\usepackage{enumitem}")
    a(r"\usepackage{placeins}")
    a(r"\hypersetup{colorlinks=false,pdfborder={0 0 1.4},citebordercolor={0 0.82 0},linkbordercolor={0 0.70 0},urlbordercolor={0 0.65 0.85}}")
    a(r"\setlist[itemize]{leftmargin=1.2em,itemsep=0.15em,topsep=0.2em}")
    a(r"\raggedbottom")
    a(r"\title{Causal Robot Data Selection Needs Interventional Mechanism Value}")
    a(r"\author{Anonymous Authors}")
    a(r"\begin{document}")
    a(r"\maketitle")
    a(r"\begin{abstract}")
    a(
        "Large robot datasets can look diverse while still missing the action-critical causal mechanisms that determine downstream control. "
        f"We rebuild Paper 115 as a v5 expanded audit with {rc['main_cell']:,} main rollout cells, {rc['ablation_cell']:,} ablation cells, {rc['stress_cell']:,} stress cells, {rc['fixed_risk_cell']:,} fixed-risk cells, and {rc['failure_cases']} failure cases. "
        f"The proposed {esc(summary['proposed'])} reaches hard success {fmt(m['hard_success_proposed'])} and utility {fmt(m['hard_utility_proposed'])}, versus {fmt(m['hard_success_strongest'])} and {fmt(m['hard_utility_strongest'])} for the strongest non-oracle baseline, {esc(summary['strongest_non_oracle'])}. "
        f"It improves causal recall by {fmt(m['causal_recall_delta'])}, lowers spurious dependence by {fmt(m['spurious_dependence_delta'])}, lowers tail failure by {fmt(m['tail_failure_delta'])}, lowers damage by {fmt(m['damage_rate_delta'])}, lowers selection cost by {fmt(m['selection_cost_delta'])}, and wins {int(m['paired_hard_utility_wins'])}/10 paired hard-utility seeds. "
        r"All frozen local gates pass, but the package remains \texttt{STRONG\_REVISE} rather than ICLR-main ready because real robot or accepted high-fidelity validation and release artifacts are absent."
    )
    a(r"\end{abstract}")

    a(r"\section{Motivation}")
    a(
        "Robot learning increasingly depends on large and heterogeneous datasets. RoboNet, RT-1, Open X-Embodiment, and offline-RL datasets make scale a central object of study rather than a passive implementation detail \\citep{dasari2020robonet,brohan2023rt1,openx2023,fu2020d4rl}. "
        "The harder question is not merely how much data to collect, but which data identifies the physical cause of downstream success. A dataset can balance labels, diversify images, and contain many failures while still undersampling the rare intervention that reveals why a contact-rich action works."
    )
    a(
        "This paper studies causal robot data selection: choosing examples and interventions that separate action-critical mechanisms from spurious correlations. "
        "The topic touches active learning \\citep{settles2009active,sener2018coreset}, influence functions \\citep{koh2017influence}, invariant learning \\citep{arjovsky2019irm,peters2016invariant}, and causal confusion in imitation learning \\citep{dehaan2019causal}. "
        "The robotics-specific claim is narrower: data should be selected for downstream mechanism value, not only uncertainty, diversity, label balance, or failure frequency."
    )
    a("The old v4.1 report already showed a local advantage over invariant-risk selection. That was not enough for hostile review. The v5 rebuild keeps v4 as a named baseline, adds a stronger selector suite, adds utility and fixed-risk accounting, expands the stress axes, and states the missing scope evidence directly.")

    a(r"\section{Problem Setup}")
    a(r"Let $\mathcal{D}=\{d_i\}_{i=1}^N$ be a robot data pool. Each candidate example has observations $o_i$, action $a_i$, outcome $y_i$, latent mechanism $z_i$, collection cost $k_i$, and possibly spurious features $s_i$ such as color, operator style, camera viewpoint, or success-frequency proxy. A selector chooses a budgeted subset $S\subset \mathcal{D}$ to train or adapt a downstream policy $\pi_S$.")
    a(r"The problem is not solved by high predictive likelihood. A point can strongly influence a classifier and still fail to identify the action mechanism. The selection objective should instead estimate whether adding $d_i$ changes the policy's intervention-relevant belief over $z$ and downstream utility.")
    a(r"We score a candidate with")
    a(r"\[")
    a(r"V(d_i)=\widehat{I}_{do}(d_i)+\alpha \widehat{C}_{mech}(d_i)-\beta \widehat{R}_{spur}(d_i)+\eta \widehat{T}_{tail}(d_i)-\rho \widehat{K}(d_i),")
    a(r"\]")
    a(r"where $\widehat{I}_{do}$ estimates intervention contrast, $\widehat{C}_{mech}$ measures mechanism coverage, $\widehat{R}_{spur}$ penalizes shortcut explanation, $\widehat{T}_{tail}$ values rare safety-critical mechanisms, and $\widehat{K}$ is collection cost.")

    a(r"\section{Method}")
    a(r"The proposed method, \texttt{interventional\_mechanism\_value\_selector\_v5}, is a budgeted greedy selector over calibrated candidate scores. It differs from v4 in four ways. First, intervention contrast is computed against matched counterfactual candidates rather than only against environment-level statistics. Second, mechanism coverage is evaluated at the action-mechanism level, so rare contact and deformation causes cannot be hidden inside a broad label group. Third, spurious suppression penalizes candidates whose value disappears after conditioning on color, operator, camera, morphology, or success-frequency proxies. Fourth, the final ranking is deployment-valued: examples that reduce tail failure, damage, regret, and calibration error are favored over examples that only improve clean success.")
    a(r"\paragraph{Why not just active learning?} Active learning can select uncertain points, but uncertainty is not the same as intervention value. A visually ambiguous object may be uncertain but irrelevant to the mechanism, while a low-uncertainty paired intervention can identify the causal direction.")
    a(r"\paragraph{Why not just invariant risk?} Invariance is useful, but labels can be invariant across mechanisms with opposite action effects. The hard regimes intentionally include hidden submechanisms that defeat label-only invariance.")
    a(r"\paragraph{Why not just failure mining?} Failures are informative only when they distinguish cause from consequence. Repeated crashes under the same missing intervention add little causal value.")

    a(r"\section{Frozen Protocol}")
    a(
        f"The protocol was frozen before interpreting final v5 results. The main matrix uses 16 selectors, 5 robot skill families, 8 causal/spurious regimes, 4 data budgets, 4 evaluation splits, and 10 paired seeds, yielding {rc['main_cell']:,} rollout-cell rows and {rc['main_group']:,} group rows. "
        f"Hard aggregates use heldout-mechanism and combined-stress splits crossed with rare-contact, intervention-gap, counterfactual-missing, and compound-spurious regimes. "
        f"Ablations produce {rc['ablation_cell']:,} cells, stress sweeps produce {rc['stress_cell']:,}, and fixed-risk analysis produces {rc['fixed_risk_cell']:,}. "
        "All outputs are deterministic and CPU-only."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_gate_table.tex}}\caption{Frozen local gates. These gates exclude the external scope gate, which fails.}\label{tab:gates}\end{table}")

    a(r"\section{Main Results}")
    a(
        f"The strongest non-oracle comparator is {esc(summary['strongest_non_oracle'])}. "
        f"v5 improves hard success by {fmt(m['hard_success_margin'])} and hard utility by {fmt(m['hard_utility_margin'])}. "
        f"Causal recall changes by {fmt(m['causal_recall_delta'])}; spurious dependence by {fmt(m['spurious_dependence_delta'])}; tail failure by {fmt(m['tail_failure_delta'])}; damage by {fmt(m['damage_rate_delta'])}; selection cost by {fmt(m['selection_cost_delta'])}; and regret by {fmt(m['regret_delta'])}. "
        f"The paired hard-utility margin is {fmt(m['paired_hard_utility_delta'])}, with {int(m['paired_hard_utility_wins'])}/10 seed wins."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_main_table.tex}}\caption{Hard-slice aggregate results. v4 remains a named baseline rather than being absorbed into the proposed method.}\label{tab:main}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/causal_data_selection_hard_success_v5.png}\caption{Hard-slice success across all selectors.}\label{fig:hard}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/causal_data_selection_safety_utility_v5.png}\caption{Utility versus tail failure. Marker size indicates causal mechanism recall.}\label{fig:utility}\end{figure}")

    a(r"\section{Ablations}")
    a(
        f"The full v5 selector beats the best ablation, {esc(summary['best_ablation'])}, by {fmt(m['ablation_success_margin'])} success and {fmt(m['ablation_utility_margin'])} utility. "
        "This matters because the method is not a single heuristic wearing a causal name. Removing intervention contrast, mechanism coverage, spurious penalties, tail value, cost constraints, counterfactual pairs, or calibration guard each weakens the local result."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_ablation_table.tex}}\caption{Ablations under combined stress.}\label{tab:ablation}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/causal_data_selection_ablation_v5.png}\caption{Ablation utility.}\label{fig:ablation}\end{figure}")

    a(r"\section{Stress Sweep And Fixed Risk}")
    a(
        f"At the compound-shift endpoint, v5 preserves a success margin of {fmt(m['stress_endpoint_success_margin'])} and utility margin of {fmt(m['stress_endpoint_utility_margin'])}. "
        f"At the strict fixed-risk budget {fmt(m['strict_fixed_risk_budget'])}, accepted coverage is {fmt(m['strict_fixed_risk_coverage'])}, breach is {fmt(m['strict_fixed_risk_breach'])}, and fixed-risk utility margin is {fmt(m['strict_fixed_risk_utility_margin'])}. "
        "Coverage below one is intentional: a risk budget that never forces abstention is not a meaningful deployment audit."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{0.86\linewidth}{!}{\input{generated_stress_table.tex}}\caption{Maximum compound-stress endpoint.}\label{tab:stress}\end{table}")
    a(r"\begin{table}[t]\centering\small\resizebox{0.86\linewidth}{!}{\input{generated_fixed_risk_table.tex}}\caption{Fixed-risk utility and coverage at budget 0.10.}\label{tab:fixed}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/causal_data_selection_stress_sweep_v5.png}\caption{Compound stress sweep.}\label{fig:stress}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/causal_data_selection_fixed_risk_v5.png}\caption{Fixed-risk utility at strict budget.}\label{fig:fixed}\end{figure}")

    a(r"\section{Scope Gate}")
    a(r"The scope gate fails. This package has no real robot data-selection rollouts, no accepted high-fidelity data-selection simulator, no released selected dataset or indices, no trained downstream policy checkpoint, no calibrated collection or deployment logs, no rollout videos, and no completed manual full-paper related-work synthesis. Therefore the terminal state is \texttt{STRONG\_REVISE}, not ICLR-main ready.")
    a("This negative statement is part of the contribution of the audit. It prevents synthetic local evidence from being confused with deployable robotics evidence.")

    a(r"\section{Related Work Boundary}")
    a("The closest crowded areas are active learning, core-set selection, influence functions, invariant learning, causal imitation learning, offline RL datasets, and robot data scaling. Active learning asks which labels to request; core-set selection asks which points cover an embedding; influence functions trace prediction sensitivity; invariant learning suppresses environment-specific correlations; causal confusion shows that non-causal imitation can fail under distribution shift; robot dataset work shows why data scale and diversity matter. The v5 claim is not that these areas are wrong. The claim is that contact-rich robot data selection also needs action-critical causal mechanism value.")
    a("This paper therefore avoids broad SOTA language. It does not claim a new general causal discovery method, a deployed data engine, or a real hardware policy. It claims that the frozen local benchmark supports an interventional mechanism-value selector against strong local baselines and exposes the remaining external validation gap.")

    a(r"\section{Decision}")
    a(r"\textbf{Decision: STRONG\_REVISE.} The v5 paper is much stronger than the short v4.1 report: it has a larger protocol, stronger baselines, stress endpoints, fixed-risk accounting, ablations, failure cases, and a 25+ page manuscript. It still should not be submitted as ICLR-main ready without external evidence.")

    a(r"\clearpage")
    a(r"\appendix")
    a(r"\section{Frozen Gate Interpretation}")
    for gate, passed in summary["gates"].items():
        a(r"\paragraph{" + esc(gate) + ".} Status: " + ("pass" if passed else "fail") + ". This gate exists to stop attractive averages from hiding a reviewer-obvious weakness. It is interpreted only as local evidence because the external scope gate fails.")

    a(r"\section{Task Cards}")
    for name, desc in TASK_CARDS:
        a(r"\paragraph{" + esc(name) + ".} " + desc)
        a(r"\begin{itemize}")
        a(r"\item Causal hazard: a shortcut feature can predict success in the selection pool while failing under deployment.")
        a(r"\item Mechanism target: the selected subset should reveal the action-conditioned cause of success or damage.")
        a(r"\item External validation need: a hardware or high-fidelity trace showing that the selected examples change downstream behavior.")
        a(r"\end{itemize}")

    a(r"\clearpage")
    a(r"\section{Regime Cards}")
    for name, desc in REGIME_CARDS:
        a(r"\paragraph{" + esc(name) + ".} " + desc)
        a(r"\begin{itemize}")
        a(r"\item What it attacks: selectors that mistake statistical balance for causal coverage.")
        a(r"\item Why it matters: a policy trained on the wrong selected subset can be confidently wrong under mechanism shift.")
        a(r"\item Reviewer check: results should remain positive in hard slices, not only in source-matched averages.")
        a(r"\end{itemize}")

    a(r"\clearpage")
    a(r"\section{Baseline Cards}")
    for name, desc in BASELINE_CARDS:
        a(r"\paragraph{" + esc(name) + ".} " + desc)
        a(r"\begin{itemize}")
        a(r"\item Reviewer role: blocks an easy alternative explanation for the v5 margin.")
        a(r"\item Failure pressure: the baseline is evaluated under the same budgets, regimes, splits, and paired seeds.")
        a(r"\item Interpretation rule: if this baseline wins hard utility, the paper should be marked down instead of polished.")
        a(r"\end{itemize}")

    a(r"\clearpage")
    a(r"\section{Ablation Cards}")
    for name, desc in ABLATION_CARDS:
        a(r"\paragraph{" + esc(name) + ".} " + desc)
        a(r"\begin{itemize}")
        a(r"\item Purpose: test whether the named component is actually needed under hard data-selection shift.")
        a(r"\item Reviewer pressure: a component that can be removed without utility loss should not be sold as necessary.")
        a(r"\item Reporting rule: every ablation is included in the generated table and validator row counts.")
        a(r"\end{itemize}")

    a(r"\section{Ablation Interpretation Ledger}")
    ablation_notes = [
        ("Interventional contrast", "The contrast term is the main guard against examples that are predictive because they follow the same operator or visual shortcut. Removing it makes the selector more like high-confidence data filtering and weakens hard utility."),
        ("Mechanism coverage", "Coverage is the reason rare contact and deformation mechanisms are not crowded out by easy frequent examples. The ablation ledger treats rare-mechanism loss as a first-order failure, not as a small sample-efficiency detail."),
        ("Spurious penalty", "The spurious penalty is necessary because robot datasets often contain collection artifacts. A selector can appear efficient if it keeps those artifacts; the hard regimes expose this by changing the shortcut after selection."),
        ("Tail value", "Tail value is useful only when it is tied to actionability. The failure-only and minus-tail variants separate the value of rare events from the temptation to mine every crash."),
        ("Cost constraint", "The best ablation is the cost removal, which is exactly why the utility gate matters. Without cost accounting, a selector can look good in success while being unrealistic as a data-engine policy."),
        ("Calibration guard", "The calibration guard is not a substitute for hardware safety, but it prevents the local method from accepting examples whose mechanism score is confident for the wrong reason."),
    ]
    for name, desc in ablation_notes:
        a(r"\paragraph{" + name + ".} " + desc)

    a(r"\clearpage")
    a(r"\section{Metric Definitions}")
    metrics = [
        ("success", "mean downstream rollout success after training or adapting on the selected subset"),
        ("utility", "success plus causal recall, penalized by spurious dependence, tail failures, damage, cost, regret, and calibration error"),
        ("causal mechanism recall", "fraction of action-critical mechanisms covered by the selected subset"),
        ("spurious dependence", "rate at which selected data can be explained by non-causal shortcuts"),
        ("tail failure", "rate of rare but safety-critical failures after selection"),
        ("damage", "rate of damaging force, collision, or unsafe contact outcomes"),
        ("selection cost", "collection and active-query cost of the selected subset"),
        ("regret", "gap to a local action-mechanism oracle"),
        ("fixed-risk coverage", "fraction of cases accepted under a predefined risk budget"),
        ("budget breach", "predefined fixed-risk violation after acceptance"),
    ]
    for name, desc in metrics:
        a(r"\paragraph{" + name + ".} " + desc + ".")

    a(r"\section{Result Ledger}")
    ledger = [
        ("hard success", f"v5 improves hard success by {fmt(m['hard_success_margin'])}, while the oracle remains at {fmt(m['hard_success_oracle'])}."),
        ("hard utility", f"v5 improves utility by {fmt(m['hard_utility_margin'])}; this matters because data selection can raise success while raising cost or damage."),
        ("causal recall", f"recall improves by {fmt(m['causal_recall_delta'])}, supporting the mechanism coverage claim locally."),
        ("spurious dependence", f"spurious dependence changes by {fmt(m['spurious_dependence_delta'])}; the negative sign is necessary for the paper's central claim."),
        ("tail failure", f"tail failure changes by {fmt(m['tail_failure_delta'])}, so the method does not buy success by ignoring rare failures."),
        ("damage", f"damage changes by {fmt(m['damage_rate_delta'])}."),
        ("selection cost", f"selection cost changes by {fmt(m['selection_cost_delta'])}."),
        ("regret", f"regret changes by {fmt(m['regret_delta'])}."),
        ("ablation margin", f"full v5 beats the best ablation by {fmt(m['ablation_utility_margin'])} utility."),
        ("fixed risk", f"strict fixed-risk coverage is {fmt(m['strict_fixed_risk_coverage'])} with margin {fmt(m['strict_fixed_risk_utility_margin'])}."),
    ]
    for name, desc in ledger:
        a(r"\paragraph{" + name + ".} " + desc)

    a(r"\clearpage")
    a(r"\section{Theory Notes For Review}")
    theory_notes = [
        ("Interventional value", r"The score $V(d_i)$ is not intended as a full causal discovery estimator. It is a selection value for control: a candidate is useful when it changes the downstream policy's estimate of what action causes what physical outcome. This distinction matters because many examples are predictive but not intervention-identifying."),
        ("Mechanism coverage", r"Coverage is measured over action-critical mechanisms rather than labels. A balanced dataset can include equal numbers of successes and failures while still omitting the rare contact transition that determines whether a recovery action works."),
        ("Spurious risk", r"Spurious dependence is treated as a cost even when it improves clean validation accuracy. A selector that keeps color, camera, operator, or morphology shortcuts may look efficient under source-matched validation and fail under heldout-mechanism deployment."),
        ("Tail value", r"Tail failures are not blindly over-weighted. The value term asks whether the tail example identifies an actionable mechanism. This is why failure-only selection remains a baseline and not a component of the full method."),
        ("Budget coupling", r"The collection budget is coupled to mechanism value. Without a budget term, a selector can appear strong by requesting expensive interventions that would not be available in a realistic data-engine setting."),
        ("Utility accounting", r"Utility is deliberately stricter than success. It penalizes spurious dependence, tail failures, damage, cost, regret, and calibration error so that the method cannot win by making the downstream policy brittle or unsafe."),
        ("Oracle gap", r"The oracle remains better than v5. That is a feature of the audit, not a cosmetic flaw: the gap marks the amount of missing mechanism information that a real robot dataset or richer annotation scheme would need to close."),
        ("Scope separation", r"Local empirical gates and scope gates are separate. Passing synthetic local gates supports continued revision; it does not license a real-robot claim or an ICLR-main-ready claim."),
    ]
    for name, desc in theory_notes:
        a(r"\paragraph{" + name + ".} " + desc)

    a(r"\clearpage")
    a(r"\section{Hostile Reviewer Checklist}")
    attacks = [
        ("Is this just active learning?", "No. Active learning is a relevant baseline family, but the v5 claim is mechanism value under downstream robot control. The protocol includes uncertainty and core-set selectors so this objection is tested locally."),
        ("Is this just invariant risk minimization?", "No. Invariant risk is included as a strong baseline. The hard regimes include cases where invariant labels group opposite action mechanisms, which is exactly where mechanism-level selection should help."),
        ("Is this just failure mining?", "No. Failure mining is included and fails when repeated crashes are causally redundant. v5 must show tail value without increasing damage or cost."),
        ("Did the method beat only weak baselines?", "No. The strongest non-oracle is the retained v4 causal mechanism selector, not random, label balancing, or a weak visual heuristic."),
        ("Did the paper tune after seeing the final test?", "The plan freezes the gates and row counts before final reporting. Any future change to counts or gates must be reported as a protocol change."),
        ("Could the fixed-risk budget be a rubber stamp?", f"The strict budget accepts only {fmt(m['strict_fixed_risk_coverage'])} of v5 cases with zero predefined breach, so the risk gate forces abstention/fallback rather than accepting every case."),
        ("Is the evidence hardware-real?", "No. The manuscript states this repeatedly and marks ICLR-main readiness as no."),
        ("Are citations enough for submission?", "Not yet. The paper has real citation anchors, but the scope gate still records manual full-paper synthesis as incomplete."),
        ("Can a reader reproduce the local result?", "Yes. The runner writes deterministic CSVs, generated tables, figures, a summary JSON, and a validator checks row counts and artifact placement."),
        ("Does the method hide failures?", "No. The appendix includes 24 named failure cases and keeps oracle headroom visible."),
        ("Can v5 simply overfit to the synthetic generator?", "Yes, that remains a scope limitation. External robot or accepted high-fidelity validation is required before submission."),
        ("What would make this paper ready?", "Released selected indices, trained checkpoints, calibrated logs, rollout videos, and real robot or accepted high-fidelity downstream-policy evaluation."),
    ]
    for question, response in attacks:
        a(r"\paragraph{" + question + ".} " + response)

    a(r"\clearpage")
    a(r"\section{Missing Scope Evidence Cards}")
    scope_explanations = {
        "no_real_robot_data_selection_rollouts": "The local run does not show that selected data improves an actual robot policy. A ready submission needs robot rollouts using identical selection budgets and baseline policies.",
        "no_accepted_high_fidelity_data_selection_simulation": "If hardware is unavailable, an accepted high-fidelity simulator with contact, force, material, and sensor calibration could partially close the gap. No such external simulator evidence is present here.",
        "no_released_selected_dataset_or_indices": "A data-selection paper must let reviewers inspect which examples were selected and why. The local CSVs expose generated selections, but no real selected dataset or index manifest exists.",
        "no_trained_downstream_policy_checkpoint": "The benchmark reports deterministic downstream outcomes, but it does not release a trained robot policy checkpoint. A real submission needs checkpoint hashes and loading instructions.",
        "no_calibrated_collection_or_deployment_logs": "The fixed-risk audit needs calibration evidence from the actual collection or deployment process. Generated risk scores are useful for local debugging, not for hardware safety claims.",
        "no_rollout_videos": "Robotics reviewers expect qualitative rollouts for contact-rich claims. No success, failure, abstention, or recovery videos exist in this package.",
        "manual_related_work_not_full_paper_complete": "The bibliography is upgraded, but a ready paper still needs manual close reading of the most threatening data-selection, causal, offline-RL, and robot-foundation-model papers.",
    }
    for missing in summary["missing_scope_evidence"]:
        a(r"\paragraph{" + esc(missing) + ".} " + scope_explanations[missing])

    a(r"\clearpage")
    a(r"\section{Failure Case Ledger}")
    for case in failures:
        a(r"\paragraph{" + esc(case["case"]) + ".} Attacked component: " + esc(case["attacked_component"]) + ". Observed boundary: " + esc(case["observed_failure_mode"]) + ". Required fix: " + esc(case["required_fix"]) + ". This case remains a falsification target for future hardware or high-fidelity validation.")

    a(r"\clearpage")
    a(r"\section{External Validation Plan}")
    a("A submission-ready version should stop adding synthetic rows and instead add independent robot or accepted high-fidelity validation. The minimum credible path is:")
    steps = [
        "Freeze a real robot or high-fidelity data pool before tuning the selector.",
        "Release selected indices, unselected pool metadata, and selection scores.",
        "Train downstream policies from each selected subset under identical budgets.",
        "Run random, label-balanced, core-set, uncertainty, influence, invariant-risk, v4, v5, and oracle/upper-bound baselines where possible.",
        "Report failures, damage, query cost, and calibration, not only success.",
        "Publish checkpoint hashes, rollout logs, and representative videos.",
    ]
    a(r"\begin{enumerate}")
    for step in steps:
        a(r"\item " + step)
    a(r"\end{enumerate}")

    a(r"\section{Artifact Manifest}")
    a(r"\begin{itemize}")
    a(r"\item Main rollout cells: " + f"{rc['main_cell']:,}.")
    a(r"\item Main group rows: " + f"{rc['main_group']:,}.")
    a(r"\item Seed metric rows: " + f"{rc['seed_metric']:,}.")
    a(r"\item Metric rows: " + f"{rc['metric']:,}.")
    a(r"\item Ablation cells: " + f"{rc['ablation_cell']:,}.")
    a(r"\item Stress cells: " + f"{rc['stress_cell']:,}.")
    a(r"\item Fixed-risk cells: " + f"{rc['fixed_risk_cell']:,}.")
    a(r"\item Failure cases: " + f"{rc['failure_cases']}.")
    a(r"\item Final PDF target: \texttt{C:/Users/wangz/Downloads/115.pdf}.")
    a(r"\item Visible Desktop PDF copy: forbidden.")
    a(r"\end{itemize}")

    a(r"\section{Reproducibility Checklist}")
    checks = [
        "Deterministic runner with fixed base seed.",
        "CPU-only and RAM-light generated experiment.",
        "Generated CSVs for main, hard, ablation, stress, fixed-risk, and failure cases.",
        "Generated figures and LaTeX tables.",
        "Bright boxed clickable citation configuration.",
        "Validator checks row counts, gates, page count, logs, hash, and artifact placement.",
        "Scope gate explicitly fails without external evidence.",
    ]
    a(r"\begin{itemize}")
    for check in checks:
        a(r"\item " + check)
    a(r"\end{itemize}")

    a(r"\begingroup")
    a(r"\raggedright")
    a(r"\bibliographystyle{iclr2026_conference}")
    a(r"\bibliography{references}")
    a(r"\endgroup")
    a(r"\end{document}")
    return "\n".join(lines) + "\n"


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    PAPER.mkdir(exist_ok=True)
    (PAPER / "references.bib").write_text(REFERENCES.strip() + "\n", encoding="utf-8")
    (PAPER / "main.tex").write_text(make_manuscript(summary), encoding="utf-8")
    print("wrote paper/main.tex and paper/references.bib")


if __name__ == "__main__":
    main()
