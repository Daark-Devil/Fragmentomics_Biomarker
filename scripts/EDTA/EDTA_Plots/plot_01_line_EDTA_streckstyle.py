from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
IN_DIR = BASE / "results/fragment_size/EDTA_WGS_streckstyle/group_compare"
OUT_DIR = BASE / "plots/EDTA_WGS_streckstyle/line"
OUT_DIR.mkdir(parents=True, exist_ok=True)

healthy = pd.read_csv(IN_DIR / "healthy_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])
cancer = pd.read_csv(IN_DIR / "cancer_binned.tsv", sep=r"\s+", header=None, names=["length", "count"])

healthy["pct"] = healthy["count"] / healthy["count"].sum() * 100
cancer["pct"] = cancer["count"] / cancer["count"].sum() * 100

healthy = healthy[(healthy["length"] >= 0) & (healthy["length"] <= 240)]
cancer = cancer[(cancer["length"] >= 0) & (cancer["length"] <= 240)]

h_peak = healthy.loc[healthy["pct"].idxmax()]
c_peak = cancer.loc[cancer["pct"].idxmax()]

plt.figure(figsize=(10, 6))

plt.axvspan(0, 140, alpha=0.12, label="Short region (<140 bp)")
plt.axvspan(150, 170, alpha=0.16, label="150–170 bp region")

plt.plot(healthy["length"], healthy["pct"], marker="o", linewidth=2, label="Healthy")
plt.plot(cancer["length"], cancer["pct"], marker="o", linewidth=2, label="Cancer")

plt.scatter([h_peak["length"]], [h_peak["pct"]], s=80)
plt.scatter([c_peak["length"]], [c_peak["pct"]], s=80)

plt.text(
    h_peak["length"], h_peak["pct"] + 0.35,
    f"Healthy peak\n{int(h_peak['length'])} bp, {h_peak['pct']:.2f}%",
    ha="center", fontsize=9
)

plt.text(
    c_peak["length"], c_peak["pct"] + 0.35,
    f"Cancer peak\n{int(c_peak['length'])} bp, {c_peak['pct']:.2f}%",
    ha="center", fontsize=9
)

plt.xlabel("Fragment length bin (bp)")
plt.ylabel("Percentage (%)")
plt.title("EDTA WGS Fragment Length Distribution")
plt.figtext(0.5, 0.01, "Percentage = bin count / total fragments × 100", ha="center", fontsize=10)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout(rect=[0, 0.05, 1, 1])

out = OUT_DIR / "plot_01_line_EDTA_streckstyle.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
print(f"Healthy peak: {int(h_peak['length'])} bp, {h_peak['pct']:.4f}%")
print(f"Cancer peak: {int(c_peak['length'])} bp, {c_peak['pct']:.4f}%")
