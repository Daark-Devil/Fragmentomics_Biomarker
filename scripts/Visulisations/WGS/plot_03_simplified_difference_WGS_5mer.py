from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]
IN_DIR = BASE / "results" / "end_motifs" / "WGS_5mer" / "group_compare"
OUT_DIR = IN_DIR / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_delta(hfile, cfile):
    h = pd.read_csv(hfile, sep=r"\s+", header=None, names=["motif", "count"])
    c = pd.read_csv(cfile, sep=r"\s+", header=None, names=["motif", "count"])
    h["pct_h"] = h["count"] / h["count"].sum() * 100
    c["pct_c"] = c["count"] / c["count"].sum() * 100
    m = h[["motif", "pct_h"]].merge(
        c[["motif", "pct_c"]],
        on="motif", how="outer"
    ).fillna(0)
    m["delta"] = m["pct_c"] - m["pct_h"]
    m["abs_delta"] = m["delta"].abs()
    return m.sort_values("abs_delta", ascending=False).head(8).sort_values("delta")

d5 = load_delta(IN_DIR / "healthy_5prime_combined.tsv", IN_DIR / "cancer_5prime_combined.tsv")
d3 = load_delta(IN_DIR / "healthy_3prime_combined.tsv", IN_DIR / "cancer_3prime_combined.tsv")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, df, title in [
    (axes[0], d5, "5′ strongest differences (5-mer)"),
    (axes[1], d3, "3′ strongest differences (5-mer)")
]:
    colors = ["tab:red" if x > 0 else "tab:blue" for x in df["delta"]]
    ax.barh(df["motif"], df["delta"], color=colors)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Cancer % - Healthy %")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)

fig.suptitle("WGS End-Motif Simplified Difference View (5-mer)")
fig.text(0.5, 0.01,
         "Positive = relatively higher in cancer; Negative = relatively higher in healthy",
         ha="center", fontsize=10)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])

out = OUT_DIR / "plot_03_simplified_difference_WGS_5mer.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
