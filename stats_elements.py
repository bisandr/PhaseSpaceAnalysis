"""Compute most-probable value (KDE peak) and standard deviation for each element CSV."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

DATA_DIR = "data"
ELEMENT_FILES = {
    "1st": f"{DATA_DIR}/element_1st.csv",
    "2nd": f"{DATA_DIR}/element_2nd.csv",
    "3rd": f"{DATA_DIR}/element_3rd.csv",
    "4th": f"{DATA_DIR}/element_4th.csv",
    "5th": f"{DATA_DIR}/element_5th.csv",
}
OUTPUT_CSV = f"{DATA_DIR}/element_stats.csv"


def load_values(path: str) -> np.ndarray:
    return pd.read_csv(path, header=None).iloc[:, 0].astype(float).to_numpy()


def kde_peak(values: np.ndarray) -> float:
    """Return the x value at the peak of the KDE."""
    kde = gaussian_kde(values)
    x = np.linspace(values.min(), values.max(), 2000)
    return float(x[np.argmax(kde(x))])


def mode_value(values: np.ndarray) -> float:
    """Return the most frequent value (mode)."""
    vals, counts = np.unique(values, return_counts=True)
    return float(vals[np.argmax(counts)])


rows = []
print(f"{'Element':<10} {'N':>6} {'Mean':>10} {'Mode':>10} {'KDE peak':>10} {'SD':>10}")
print("-" * 60)

for label, path in ELEMENT_FILES.items():
    values = load_values(path)
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1))
    mode = mode_value(values)
    peak = kde_peak(values)

    print(f"{label:<10} {len(values):>6} {mean:>10.3f} {mode:>10.3f} {peak:>10.3f} {sd:>10.3f}")
    rows.append(
        {
            "element": label,
            "n": len(values),
            "mean": round(mean, 4),
            "mode": mode,
            "kde_peak": round(peak, 4),
            "sd": round(sd, 4),
        }
    )

print()
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Results saved to {OUTPUT_CSV}")
