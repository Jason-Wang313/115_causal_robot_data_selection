# Hostile Reviewer Response

## Reviewer Attack: This is just active learning.

Response: The strongest non-oracle baseline is `invariant_risk_selection`, not random or uncertainty sampling. The proposed selector beats it by `0.105 +/- 0.008` success and wins `7/7` paired seeds.

## Reviewer Attack: Label balancing and failure mining should be enough.

Response: Label balancing collapses under spurious shift (`0.368` success) and failure mining reaches only `0.484`. They select examples correlated with labels or failures, not interventions that identify causal robot mechanisms.

## Reviewer Attack: The causal components may be decorative.

Response: Ablations reject that. The full method reaches `0.676 +/- 0.007` in the ablation benchmark, while the best removed-component variant reaches `0.640 +/- 0.007`.

## Reviewer Attack: The paper is not ready for ICLR main.

Response: Agreed. The honest decision is `STRONG_REVISE`, not ready. The v4.1 evidence has 5,880 detailed stress rows and 8 failure cases, but it still needs real robot or external high-fidelity validation and released selected datasets/policy checkpoints.
