import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load
healthy = pd.read_csv("results/fragment_size/EDTA_WGS/group_compare/healthy_binned.tsv", sep=" ", header=None, names=["length","count"])
cancer = pd.read_csv("results/fragment_size/EDTA_WGS/group_compare/cancer_binned.tsv", sep=" ", header=None, names=["length","count"])

# Normalize
healthy["pct"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct"] = cancer["count"] / cancer["count"].sum() * 100

# Define bins
bins = [
    (100,120),(120,140),(140,150),(150,170),
    (170,190),(190,210),(210,230)
]

labels = [f"{a}-{b}" for a,b in bins]

def compute(df):
    values = []
    for a,b in bins:
        values.append(df[(df["length"]>=a)&(df["length"]<b)]["pct"].sum())
    return values

h_vals = compute(healthy)
c_vals = compute(cancer)

x = np.arange(len(labels))

plt.figure(figsize=(10,6))
plt.bar(x-0.2, h_vals, width=0.4, label="Healthy")
plt.bar(x+0.2, c_vals, width=0.4, label="Cancer")

plt.xticks(x, labels)
plt.ylabel("Percentage (%)")
plt.title("EDTA Fragment Distribution by Range")
plt.legend()
plt.tight_layout()

plt.savefig("plots/EDTA_WGS/range/edta_range_plot.png", dpi=300)
