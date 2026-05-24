from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
IN_DIR = BASE / "results" / "end_motifs" / "WGS_5mer" / "group_compare"
OUT_DIR = IN_DIR / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

healthy = pd.read_csv(IN_DIR / "healthy_5prime_combined.tsv", sep=r"\s+", header=None, names=["motif", "count"])
cancer  = pd.read_csv(IN_DIR / "cancer_5prime_combined.tsv", sep=r"\s+", header=None, names=["motif", "count"])

healthy["percent"] = healthy["count"] / healthy["count"].sum() * 100
cancer["percent"]  = cancer["count"] / cancer["count"].sum() * 100

merged = healthy.merge(cancer, on="motif", how="outer", suffixes=("_healthy", "_cancer")).fillna(0)
merged["total"] = merged["count_healthy"] + merged["count_cancer"]
top10 = merged.sort_values("total", ascending=False).head(10).copy()

x = np.arange(len(top10))
w = 0.38

plt.figure(figsize=(12, 6))
plt.bar(x - w/2, top10["percent_healthy"], width=w, label="Healthy")
plt.bar(x + w/2, top10["percent_cancer"], width=w, label="Cancer")

plt.xticks(x, top10["motif"], rotation=35, ha="right")
plt.ylabel("Percentage of motif counts (%)")
plt.xlabel("5′ end 5-mer motifs")
plt.title("Top 10 WGS 5′ End Motifs (5-mer): Healthy vs Cancer")
plt.figtext(0.5, 0.01,
            "Percentage = (motif count / total motif counts in group) × 100",
            ha="center", fontsize=10)
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout(rect=[0, 0.05, 1, 1])

out = OUT_DIR / "plot_01_top10_5prime_WGS_5mer.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
