from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
MANIFEST = BASE / "manifests/edta_wgs_manifest.tsv"
FRAG_DIR = BASE / "results/fragment_size/EDTA_WGS_streckstyle/all"
OUT_DIR = BASE / "plots/EDTA_WGS_streckstyle/violin"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def compute_ratio(sample):
    frag_file = FRAG_DIR / f"{sample}_frag.txt"
    short_count = 0
    long_count = 0
    total_count = 0

    with open(frag_file) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue

            x = int(float(line))
            total_count += 1

            if x < 140:
                short_count += 1
            elif 140 <= x <= 220:
                long_count += 1

    if long_count == 0:
        return None

    return {
        "sample": sample,
        "short_count": short_count,
        "long_count": long_count,
        "ratio": short_count / long_count,
        "total_count": total_count
    }

rows = []

with open(MANIFEST) as fh:
    for line in fh:
        sample, group, dtype = line.strip().split()
        result = compute_ratio(sample)
        if result is not None:
            result["group"] = group
            rows.append(result)

df = pd.DataFrame(rows)
df.to_csv(OUT_DIR / "EDTA_streckstyle_short_long_ratio_per_sample.tsv", sep="\t", index=False)

healthy = df[df["group"] == "healthy"]["ratio"].values
cancer = df[df["group"] == "cancer"]["ratio"].values

h_median = np.median(healthy)
c_median = np.median(cancer)

plt.figure(figsize=(7, 6))
plt.violinplot([healthy, cancer], showmedians=True)
plt.boxplot([healthy, cancer], widths=0.18, showfliers=True)

plt.scatter(np.ones(len(healthy)), healthy, alpha=0.25, s=14)
plt.scatter(np.ones(len(cancer)) * 2, cancer, alpha=0.25, s=14)

plt.text(1, h_median + 0.01, f"Median: {h_median:.3f}", ha="center", fontsize=10)
plt.text(2, c_median + 0.01, f"Median: {c_median:.3f}", ha="center", fontsize=10)

plt.xticks([1, 2], ["Healthy", "Cancer"])
plt.ylabel("Short / Long Fragment Ratio")
plt.title("EDTA WGS Per-Sample Short/Long Fragment Ratio")
plt.figtext(0.5, 0.01, "Short: <140 bp; Long: 140–220 bp", ha="center", fontsize=10)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout(rect=[0, 0.05, 1, 1])

out = OUT_DIR / "plot_04_violin_EDTA_streckstyle.png"
plt.savefig(out, dpi=300)

print(f"Saved: {out}")
print(f"Saved table: {OUT_DIR / 'EDTA_streckstyle_short_long_ratio_per_sample.tsv'}")
print(f"Healthy n: {len(healthy)}, median: {h_median:.6f}")
print(f"Cancer n: {len(cancer)}, median: {c_median:.6f}")
