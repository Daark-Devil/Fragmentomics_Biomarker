from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
IN_DIR = BASE / "results/fragment_size/EDTA_WGS_streckstyle/group_compare"
OUT_DIR = BASE / "plots/EDTA_WGS_streckstyle/difference"
OUT_DIR.mkdir(parents=True, exist_ok=True)

healthy = pd.read_csv(IN_DIR / "healthy_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])
cancer = pd.read_csv(IN_DIR / "cancer_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])

healthy["pct_h"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct_c"] = cancer["count"] / cancer["count"].sum() * 100

df = pd.merge(
    healthy[["length", "pct_h"]],
    cancer[["length", "pct_c"]],
    on="length",
    how="outer"
).fillna(0)

df["diff"] = df["pct_c"] - df["pct_h"]
df = df[(df["length"] >= 0) & (df["length"] <= 240)]

max_row = df.loc[df["diff"].idxmax()]
min_row = df.loc[df["diff"].idxmin()]

plt.figure(figsize=(10, 6))
plt.axhline(0, linestyle="--", linewidth=1)
plt.axvspan(0, 140, alpha=0.12, label="Short region (<140 bp)")
plt.axvspan(150, 170, alpha=0.16, label="150–170 bp region")

plt.plot(df["length"], df["diff"], marker="o", linewidth=2)

plt.scatter([max_row["length"]], [max_row["diff"]], s=80)
plt.scatter([min_row["length"]], [min_row["diff"]], s=80)

plt.text(
    max_row["length"], max_row["diff"] + 0.15,
    f"Max cancer higher\n{int(max_row['length'])} bp, +{max_row['diff']:.2f}%",
    ha="center", fontsize=9
)

plt.text(
    min_row["length"], min_row["diff"] - 0.25,
    f"Max healthy higher\n{int(min_row['length'])} bp, {min_row['diff']:.2f}%",
    ha="center", fontsize=9
)

plt.xlabel("Fragment length bin (bp)")
plt.ylabel("Cancer − Healthy (%)")
plt.title("EDTA WGS Difference Curve")
plt.figtext(0.5, 0.01, "Positive values = higher in cancer; negative values = higher in healthy", ha="center", fontsize=10)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout(rect=[0, 0.05, 1, 1])

out = OUT_DIR / "plot_03_difference_EDTA_streckstyle.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
print(f"Max cancer higher: {int(max_row['length'])} bp, {max_row['diff']:.4f}%")
print(f"Max healthy higher: {int(min_row['length'])} bp, {min_row['diff']:.4f}%")
