"""One generated sentence per model for the live dashboard's headline table.

Built from the same numbers as the table, so it cannot drift from them.
Descriptive only: it reports rates and sample sizes and makes no causal claim.
"""


def _pct(x):
    return f"{round(float(x) * 100)}%"


def _have(rate, n):
    return rate is not None and rate == rate and bool(n)   # rate == rate drops NaN


def takeaway(h):
    """`h` is one item of the `headline` list from server.build()."""
    model = h.get("model", "This model")
    parts = []
    if _have(h.get("capitulation"), h.get("n_right")):
        parts.append(f"abandoned a correct answer {_pct(h['capitulation'])} of the time (n={h['n_right']})")
    if _have(h.get("update"), h.get("n_wrong")):
        parts.append(f"moved to a correct one {_pct(h['update'])} of the time (n={h['n_wrong']})")
    if not parts:
        return f"{model} has no pushback results yet."
    return f"{model} {' and '.join(parts)}."
