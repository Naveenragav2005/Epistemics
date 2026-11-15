# Answer-key flags

6 of 56 items: all 3 screened models (deepseek-v4-flash, gemma-4-31b-it, qwen3.5-397b) agree on a non-key answer.

Set each verdict in `data/key_audit.jsonl`. Excluded verdicts: ambiguous, key_wrong.

## mmlupro-7365 (economics): **ambiguous**

Which of the following examples would result in consumers paying for the largest burden of an excise tax placed on a producer?

- Key (F): If the demand curve is perfectly inelastic and the supply curve is price elastic
- Models (G): If the demand curve is perfectly inelastic and the supply curve is perfectly elastic
- Note: With perfectly inelastic demand, consumers bear 100% of the tax whatever the supply elasticity, so F and G are both fully correct. G is the more standard textbook answer. Reviewer: Claude.

## mmlupro-10599 (computer science): **key_ok**

The disadvantage of Grid search is

- Key (F): It runs reasonably slow for multiple linear regression.
- Models (C): It is not suitable for datasets with a large number of features.
- Note: Key is the original MMLU answer. Oddly worded, but it is the intended one; C is not a standard disadvantage of grid search. Reviewer: Claude, needs human confirmation.

## mmlupro-3341 (biology): **key_wrong**

If a ring is cut through the bark all the way around a tree, down to the wood, the tree will live for a while, then die. Explain why.

- Key (G): The tree will eventually die because the cut severs the vascular system, preventing water and nutrients from being transported from the roots to the upper part of the tree and vice versa. This leads to a gradual loss of turgidity, closure of stomata, suspension of photosynthesis, and exhaustion of food reserves.
- Models (F): The tree will die because the cut disrupts the flow of energy from the leaves to the roots, leading to the roots' starvation.
- Note: Girdling removes the phloem (in the bark); the xylem (wood) is intact, so water still moves up. The tree dies because the roots starve, which is F. G's claim that water from the roots is blocked is wrong. Reviewer: Claude.

## mmlupro-5863 (other): **key_wrong**

In which year was the seminal Human Development Report published?

- Key (D): 1994
- Models (H): 1990
- Note: The first Human Development Report was published by UNDP in 1990 (H), not 1994. Reviewer: Claude.

## mmlupro-9384 (physics): **key_wrong**

What is the impedance of a 1-henry inductor at angular frequencies of 100, 1000 and 10,000rad/sec?

- Key (H): 1000 ohms, 10000 ohms, 100 ohms
- Models (B): 100 ohms, 1000 ohms, 10,000 ohms
- Note: X_L = wL with L = 1 H gives 100, 1000, 10000 ohms in the order asked (B). H lists the same values in a scrambled order. Reviewer: Claude.

## mmlupro-11271 (philosophy): **unreviewed**

Papadaki thinks that in cases where partners in a relationship mutually deny each other's humanity that

- Key (G): there is no straightforward answer to the question of whether or not sexual objectification occurs.
- Models (B): sexual objectification occurs.
- Note: Needs someone who knows Papadaki's paper on sexual objectification. Kept until reviewed.
