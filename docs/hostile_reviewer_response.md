# Hostile Reviewer Response

## "This is just active learning."

Active learning, core-set selection, uncertainty selection, and influence selection are included as baselines. v5 is evaluated on action-critical mechanism value, downstream utility, tail failure, damage, cost, regret, and fixed-risk behavior.

## "The result only beats weak baselines."

The strongest non-oracle baseline is the retained `proposed_causal_mechanism_selector_v4`, not a weak selector. v5 beats it by `0.08841` hard success and `0.18155` hard utility.

## "The risk audit is decorative."

The strict fixed-risk budget accepts only `0.55813` of v5 cases and has zero breach, so it is not a rubber stamp. The utility margin remains `0.20267`.

## "This is not real robotics evidence."

Correct. The paper explicitly fails the scope gate and is marked `STRONG_REVISE`, not ICLR-main ready.

## "The related work is still incomplete."

Correct. The bibliography now anchors the key active learning, invariant learning, causal confusion, offline RL, and robot data-scale areas, but manual full-paper synthesis remains a blocking scope item.
