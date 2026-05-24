import pandas as pd
import matplotlib.pyplot as plt

# Load
healthy = pd.read_csv("results/fragment_size/EDTA_WGS/group_compare/healthy_binned.tsv", sep=" ", header=None, names=["length","count"])
cancer = pd.read_csv("results/fragment_size/EDTA_WGS/group_compare/cancer_binned.tsv", sep=" ", header=None, names=["length","count"])

# Normalize
healthy["pct"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct"] = cancer["count"] / cancer["count"].sum() * 100

# Merge
df = pd.merge(healthy, cancer, on="length", suffixes=("_h","_c"))
df["diff"] = df["pct_c"] - df["pct_h"]

df = df[df["length"] <= 220]

# Plot
plt.figure(figsize=(10,6))
plt.plot(df["length"], df["diff"], color="black")

plt.axhline(0, linestyle="--")
plt.axvspan(0,140, alpha=0.1)
plt.axvspan(150,170, alpha=0.1)

plt.xlabel("Fragment length (bp)")
plt.ylabel("Cancer - Healthy (%)")
plt.title("EDTA Difference Curve")

plt.tight_layout()
plt.savefig("plots/EDTA_WGS/difference/edta_difference_plot.png", dpi=300)
