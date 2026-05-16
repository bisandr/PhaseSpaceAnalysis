"""Plot histograms with KDE overlay for each element CSV."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

DATA_DIR = "data"
ELEMENTS = ["1st", "2nd", "3rd", "4th", "5th"]

fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharey=False)

for ax, label in zip(axes, ELEMENTS):
    values = pd.read_csv(f"{DATA_DIR}/element_{label}.csv", header=None).iloc[:, 0].astype(float).to_numpy()

    bins = np.arange(values.min() - 0.5, values.max() + 1.5, 1)
    ax.hist(values, bins=bins, density=True, color="steelblue", alpha=0.7, label="Histogram")

    kde = gaussian_kde(values)
    x = np.linspace(values.min(), values.max(), 500)
    ax.plot(x, kde(x), color="crimson", linewidth=2, label="KDE")

    peak_x = x[np.argmax(kde(x))]
    ax.axvline(peak_x, color="crimson", linestyle="--", linewidth=1, alpha=0.8, label=f"Peak: {peak_x:.1f}")

    sd = np.std(values, ddof=1)
    ax.set_title(f"Element {label}\nSD = {sd:.2f}")
    ax.set_xlabel("Value")
    if ax is axes[0]:
        ax.set_ylabel("Density")
    ax.legend(fontsize=7)

plt.suptitle("Histograms of 1st–5th Elements", fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
