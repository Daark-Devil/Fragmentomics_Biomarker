from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]
IN_DIR = BASE / "results" / "end_motifs" / "WGS" / "group_compare"
OUT_DIR = IN_DIR / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_ranked(file_path):
    df = pd.read_csv(file_path, sep=r"\s+", header=None, names=["motif", "count"])
    df["percent"] = df["count"] / df["count"].sum() * 100
    df = df.sort_values("percent", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df

h5 = load_ranked(IN_DIR / "healthy_5prime_combined.tsv")
c5 = load_ranked(IN_DIR / "cancer_5prime_combined.tsv")
h3 = load_ranked(IN_DIR / "healthy_3prime_combined.tsv")
c3 = load_ranked(IN_DIR / "cancer_3prime_combined.tsv")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].plot(h5["rank"], h5["percent"], label="Healthy")
axes[0].plot(c5["rank"], c5["percent"], label="Cancer")
axes[0].set_title("5′ ranked motif distribution")
axes[0].set_xlabel("Motif rank")
axes[0].set_ylabel("Percentage (%)")
axes[0].grid(alpha=0.3)
axes[0].legend()

axes[1].plot(h3["rank"], h3["percent"], label="Healthy")
axes[1].plot(c3["rank"], c3["percent"], label="Cancer")
axes[1].set_title("3′ ranked motif distribution")
axes[1].set_xlabel("Motif rank")
axes[1].set_ylabel("Percentage (%)")
axes[1].grid(alpha=0.3)
axes[1].legend()

fig.suptitle("WGS End-Motif Global Distribution by Rank")
plt.tight_layout(rect=[0, 0, 1, 0.95])

out = OUT_DIR / "plot_04_ranked_distribution_WGS.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
