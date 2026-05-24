from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
IN_DIR = BASE / "results/fragment_size/EDTA_WGS_streckstyle/group_compare"
OUT_DIR = BASE / "plots/EDTA_WGS_streckstyle/range"
OUT_DIR.mkdir(parents=True, exist_ok=True)

healthy = pd.read_csv(IN_DIR / "healthy_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])
cancer = pd.read_csv(IN_DIR / "cancer_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])

healthy["pct"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct"] = cancer["count"] / cancer["count"].sum() * 100

ranges = [
    (80, 100, "80–100"),
    (100, 120, "100–120"),
    (120, 140, "120–140"),
    (140, 150, "140–150"),
    (150, 170, "150–170"),
    (170, 190, "170–190"),
    (190, 210, "190–210"),
    (210, 230, "210–230"),
]

def range_pct(df):
    values = []
    for start, end, _ in ranges:
        values.append(df[(df["length"] >= start) & (df["length"] < end)]["pct"].sum())
    return values

healthy_vals = range_pct(healthy)
cancer_vals = range_pct(cancer)
labels = [x[2] for x in ranges]
x = np.arange(len(labels))

plt.figure(figsize=(11, 6))
bars1 = plt.bar(x - 0.2, healthy_vals, width=0.4, label="Healthy")
bars2 = plt.bar(x + 0.2, cancer_vals, width=0.4, label="Cancer")

for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.15, f"{height:.1f}", ha="center", fontsize=8)

for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.15, f"{height:.1f}", ha="center", fontsize=8)

plt.xticks(x, labels, rotation=30, ha="right")
plt.ylabel("Percentage (%)")
plt.title("EDTA WGS Fragment Percentage by Length Range")
plt.figtext(0.5, 0.01, "Short-fragment focus: <140 bp; nucleosomal focus: 150–170 bp", ha="center", fontsize=10)
plt.grid(axis="y", alpha=0.3)
plt.legend()
plt.tight_layout(rect=[0, 0.06, 1, 1])

out = OUT_DIR / "plot_02_range_EDTA_streckstyle.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")

print("Range\tHealthy_%\tCancer_%")
for label, hv, cv in zip(labels, healthy_vals, cancer_vals):
    print(f"{label}\t{hv:.4f}\t{cv:.4f}")
