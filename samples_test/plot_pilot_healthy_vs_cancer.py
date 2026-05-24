import pandas as pd
import matplotlib.pyplot as plt

healthy_file = "seq015764_NC_wgs_binned.tsv"
cancer_file = "seq015743_IV_wgs_binned.tsv"

healthy = pd.read_csv(healthy_file, sep=r"\s+", header=None, names=["bin", "count"])
cancer = pd.read_csv(cancer_file, sep=r"\s+", header=None, names=["bin", "count"])

# Plot 1: Healthy sample
plt.figure(figsize=(10, 5))
plt.plot(healthy["bin"], healthy["count"], marker="o")
plt.xlabel("Fragment length (bp)")
plt.ylabel("Count")
plt.title("Pilot Healthy Sample Fragment Length Distribution: seq015764_NC_wgs")
plt.tight_layout()
plt.savefig("seq015764_NC_wgs_fragment_distribution.png", dpi=300)
plt.close()

# Plot 2: Cancer sample
plt.figure(figsize=(10, 5))
plt.plot(cancer["bin"], cancer["count"], marker="o")
plt.xlabel("Fragment length (bp)")
plt.ylabel("Count")
plt.title("Pilot Cancer Sample Fragment Length Distribution: seq015743_IV_wgs")
plt.tight_layout()
plt.savefig("seq015743_IV_wgs_fragment_distribution.png", dpi=300)
plt.close()

# Plot 3: Overlay comparison
plt.figure(figsize=(10, 5))
plt.plot(healthy["bin"], healthy["count"], marker="o", label="Healthy: seq015764_NC_wgs")
plt.plot(cancer["bin"], cancer["count"], marker="o", label="Cancer: seq015743_IV_wgs")
plt.xlabel("Fragment length (bp)")
plt.ylabel("Count")
plt.title("Pilot Healthy vs Cancer Fragment Length Distribution")
plt.legend()
plt.tight_layout()
plt.savefig("pilot_healthy_vs_cancer_fragment_distribution.png", dpi=300)
plt.close()

print("Saved:")
print("- seq015764_NC_wgs_fragment_distribution.png")
print("- seq015743_IV_wgs_fragment_distribution.png")
print("- pilot_healthy_vs_cancer_fragment_distribution.png")
