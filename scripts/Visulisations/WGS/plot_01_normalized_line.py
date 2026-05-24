import pandas as pd
import matplotlib.pyplot as plt

# Input files
healthy_file = "healthy_fragment_distribution_binned.tsv"
cancer_file = "cancer_fragment_distribution_binned.tsv"

# Load data
healthy = pd.read_csv(healthy_file, sep=r"\s+", header=None, names=["bin", "count"])
cancer = pd.read_csv(cancer_file, sep=r"\s+", header=None, names=["bin", "count"])

# Keep biologically useful region only
healthy = healthy[healthy["bin"] <= 250].copy()
cancer = cancer[cancer["bin"] <= 250].copy()

# Normalize to percentage
healthy["percent"] = healthy["count"] / healthy["count"].sum() * 100
cancer["percent"] = cancer["count"] / cancer["count"].sum() * 100

# Find peak bins
h_peak = healthy.loc[healthy["percent"].idxmax()]
c_peak = cancer.loc[cancer["percent"].idxmax()]

# Plot
plt.figure(figsize=(10, 5))

plt.plot(
    healthy["bin"], healthy["percent"],
    linewidth=2.5, marker="o", markersize=4,
    label="Healthy"
)
plt.plot(
    cancer["bin"], cancer["percent"],
    linewidth=2.5, marker="o", markersize=4,
    label="Cancer"
)

# Highlight peak dots
plt.scatter(h_peak["bin"], h_peak["percent"], s=120, zorder=5)
plt.scatter(c_peak["bin"], c_peak["percent"], s=120, zorder=5)

# Peak annotations
plt.annotate(
    f"Healthy peak: {int(h_peak['bin'])} bp",
    xy=(h_peak["bin"], h_peak["percent"]),
    xytext=(h_peak["bin"] + 12, h_peak["percent"] * 0.92),
    arrowprops=dict(arrowstyle="->", lw=1)
)

plt.annotate(
    f"Cancer peak: {int(c_peak['bin'])} bp",
    xy=(c_peak["bin"], c_peak["percent"]),
    xytext=(c_peak["bin"] - 65, c_peak["percent"] * 0.72),
    arrowprops=dict(arrowstyle="->", lw=1)
)

# Axes and labels
plt.xlim(0, 250)
plt.xticks(range(0, 251, 30))
plt.xlabel("Fragment length (bp)")
plt.ylabel("Percentage of fragments (%)")
plt.title("Healthy vs Cancer WGS Fragment Length Distribution (All Samples)")

# Equation
plt.figtext(
    0.5, 0.01,
    "Normalization: Percentage = (count in each 10 bp bin / total fragments in group) × 100",
    ha="center",
    fontsize=10
)

plt.grid(alpha=0.3)
plt.legend(frameon=False)
plt.tight_layout(rect=[0, 0.05, 1, 1])

# Save
plt.savefig("plot_01_normalized_line.png", dpi=300)
print("Saved: plot_01_normalized_line.png")
