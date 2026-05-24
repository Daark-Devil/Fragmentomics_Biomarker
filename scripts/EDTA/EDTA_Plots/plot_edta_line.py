import pandas as pd
import matplotlib.pyplot as plt

# Load data
healthy = pd.read_csv(
    "results/fragment_size/EDTA_WGS/group_compare/healthy_binned.tsv",
    sep=" ", header=None, names=["length", "count"]
)
cancer = pd.read_csv(
    "results/fragment_size/EDTA_WGS/group_compare/cancer_binned.tsv",
    sep=" ", header=None, names=["length", "count"]
)

# Normalize
healthy["pct"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct"] = cancer["count"] / cancer["count"].sum() * 100

# Limit range (clean visualization)
healthy = healthy[healthy["length"] <= 220]
cancer = cancer[cancer["length"] <= 220]

# Find peaks
h_peak = healthy.loc[healthy["pct"].idxmax()]
c_peak = cancer.loc[cancer["pct"].idxmax()]

# Plot
plt.figure(figsize=(10,6))

plt.plot(healthy["length"], healthy["pct"], label="Healthy", linewidth=2)
plt.plot(cancer["length"], cancer["pct"], label="Cancer", linewidth=2)

# Shade regions
plt.axvspan(0, 140, color='gray', alpha=0.15, label="Short (<140)")
plt.axvspan(150, 170, color='blue', alpha=0.1, label="Nucleosome (150–170)")

# Annotate peaks
plt.scatter(h_peak["length"], h_peak["pct"])
plt.scatter(c_peak["length"], c_peak["pct"])

plt.text(h_peak["length"], h_peak["pct"]+0.5, f"H peak {int(h_peak['length'])}bp")
plt.text(c_peak["length"], c_peak["pct"]-1.5, f"C peak {int(c_peak['length'])}bp")

plt.xlabel("Fragment length (bp)")
plt.ylabel("Percentage (%)")
plt.title("EDTA WGS Fragment Length Distribution")
plt.legend()
plt.tight_layout()

plt.savefig("plots/EDTA_WGS/line/edta_line_plot.png", dpi=300)
