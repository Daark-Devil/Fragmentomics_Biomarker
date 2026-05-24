from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
OUT = BASE / "plots/compare_streck_edta"
OUT.mkdir(parents=True, exist_ok=True)

# ==============================
# INPUT PATHS
# ==============================
STRECK_DIR = BASE / "results/fragment_size/WGS/group_compare"
EDTA_DIR = BASE / "results/fragment_size/EDTA_WGS_streckstyle/group_compare"

STRECK_H = STRECK_DIR / "healthy_fragment_distribution_binned.tsv"
STRECK_C = STRECK_DIR / "cancer_fragment_distribution_binned.tsv"

EDTA_H = EDTA_DIR / "healthy_binned.tsv"
EDTA_C = EDTA_DIR / "cancer_binned.tsv"

STRECK_RATIO = BASE / "results/plots_WGS_length/WGS_short_long_ratio_per_sample.tsv"
EDTA_RATIO = BASE / "plots/EDTA_WGS_streckstyle/violin/EDTA_streckstyle_short_long_ratio_per_sample.tsv"

# ==============================
# HELPERS
# ==============================
def load_binned(h_file, c_file, prefix):
    h = pd.read_csv(h_file, sep=r"\s+", header=None, names=["length", "count_h"])
    c = pd.read_csv(c_file, sep=r"\s+", header=None, names=["length", "count_c"])

    h[f"{prefix}_healthy_pct"] = h["count_h"] / h["count_h"].sum() * 100
    c[f"{prefix}_cancer_pct"] = c["count_c"] / c["count_c"].sum() * 100

    df = pd.merge(
        h[["length", f"{prefix}_healthy_pct"]],
        c[["length", f"{prefix}_cancer_pct"]],
        on="length",
        how="outer"
    ).fillna(0)

    df[f"{prefix}_diff"] = df[f"{prefix}_cancer_pct"] - df[f"{prefix}_healthy_pct"]
    return df

def region_label(length):
    if length < 140:
        return "Short <140 bp"
    elif 150 <= length <= 170:
        return "150–170 bp"
    elif 140 <= length <= 220:
        return "Other 140–220 bp"
    else:
        return ">220 bp"

def load_ratio_table(path, cohort):
    df = pd.read_csv(path, sep="\t")
    df["cohort"] = cohort

    # Normalize group names
    df["group"] = df["group"].str.lower()
    df["group_label"] = df["cohort"] + " " + df["group"].map({"healthy": "Healthy", "cancer": "Cancer"})

    return df[["sample", "group", "group_label", "cohort", "ratio"]]

# ==============================
# LOAD DATA
# ==============================
streck = load_binned(STRECK_H, STRECK_C, "streck")
edta = load_binned(EDTA_H, EDTA_C, "edta")

df = pd.merge(
    streck[["length", "streck_diff"]],
    edta[["length", "edta_diff"]],
    on="length",
    how="inner"
)

df = df[(df["length"] >= 0) & (df["length"] <= 240)].copy()
df["region"] = df["length"].apply(region_label)

# Save comparison table
df.to_csv(OUT / "streck_vs_edta_difference_by_bin.tsv", sep="\t", index=False)

# ==============================
# COLORS / MARKERS
# ==============================
colors = {
    "Short <140 bp": "#d62728",
    "150–170 bp": "#2ca02c",
    "Other 140–220 bp": "#1f77b4",
    ">220 bp": "#7f7f7f"
}

# ==============================
# FIGURE 1: QUADRANT SCATTER ONLY
# ==============================
plt.figure(figsize=(8, 7))

plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)

for region, sub in df.groupby("region"):
    plt.scatter(
        sub["streck_diff"],
        sub["edta_diff"],
        s=90,
        alpha=0.85,
        label=region,
        color=colors.get(region, "gray"),
        edgecolor="black",
        linewidth=0.5
    )

# Label important bins
for _, row in df.iterrows():
    if row["length"] in [60, 80, 100, 120, 140, 150, 160, 170, 180, 200]:
        plt.text(
            row["streck_diff"] + 0.015,
            row["edta_diff"] + 0.015,
            str(int(row["length"])),
            fontsize=8
        )

plt.xlabel("Streck Cancer − Healthy (%)")
plt.ylabel("EDTA Cancer − Healthy (%)")
plt.title("Streck vs EDTA Fragment-Length Difference Quadrant Plot")

plt.text(0.98, 0.98, "Cancer higher in both", transform=plt.gca().transAxes, ha="right", va="top", fontsize=9)
plt.text(0.02, 0.02, "Healthy higher in both", transform=plt.gca().transAxes, ha="left", va="bottom", fontsize=9)
plt.text(0.02, 0.98, "EDTA cancer higher\nStreck healthy higher", transform=plt.gca().transAxes, ha="left", va="top", fontsize=9)
plt.text(0.98, 0.02, "Streck cancer higher\nEDTA healthy higher", transform=plt.gca().transAxes, ha="right", va="bottom", fontsize=9)

plt.grid(alpha=0.3)
plt.legend(title="Fragment region", loc="best")
plt.tight_layout()

out1 = OUT / "plot_01_quadrant_scatter_streck_vs_edta.png"
plt.savefig(out1, dpi=300)
print(f"Saved: {out1}")

# ==============================
# FIGURE 2: FOUR-PANEL SUMMARY
# ==============================
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# Panel A: Streck difference curve
ax = axes[0, 0]
splot = streck[(streck["length"] >= 0) & (streck["length"] <= 240)].copy()
ax.axhline(0, linestyle="--", linewidth=1, color="black")
ax.axvspan(0, 140, alpha=0.12)
ax.axvspan(150, 170, alpha=0.16)
ax.plot(splot["length"], splot["streck_diff"], marker="o", linewidth=2)
ax.set_title("A. Streck WGS Difference Curve")
ax.set_xlabel("Fragment length bin (bp)")
ax.set_ylabel("Cancer − Healthy (%)")
ax.grid(alpha=0.3)

# Panel B: EDTA difference curve
ax = axes[0, 1]
eplot = edta[(edta["length"] >= 0) & (edta["length"] <= 240)].copy()
ax.axhline(0, linestyle="--", linewidth=1, color="black")
ax.axvspan(0, 140, alpha=0.12)
ax.axvspan(150, 170, alpha=0.16)
ax.plot(eplot["length"], eplot["edta_diff"], marker="o", linewidth=2)
ax.set_title("B. EDTA WGS Difference Curve")
ax.set_xlabel("Fragment length bin (bp)")
ax.set_ylabel("Cancer − Healthy (%)")
ax.grid(alpha=0.3)

# Panel C: quadrant scatter
ax = axes[1, 0]
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)

for region, sub in df.groupby("region"):
    ax.scatter(
        sub["streck_diff"],
        sub["edta_diff"],
        s=85,
        alpha=0.85,
        label=region,
        color=colors.get(region, "gray"),
        edgecolor="black",
        linewidth=0.5
    )

for _, row in df.iterrows():
    if row["length"] in [80, 100, 120, 140, 150, 160, 170, 180, 200]:
        ax.text(row["streck_diff"] + 0.015, row["edta_diff"] + 0.015, str(int(row["length"])), fontsize=8)

ax.set_title("C. Same vs Opposite Behavior")
ax.set_xlabel("Streck Cancer − Healthy (%)")
ax.set_ylabel("EDTA Cancer − Healthy (%)")
ax.grid(alpha=0.3)
ax.legend(title="Region", fontsize=8)

# Panel D: ratio comparison
ax = axes[1, 1]
ratio_frames = []

if STRECK_RATIO.exists():
    ratio_frames.append(load_ratio_table(STRECK_RATIO, "Streck"))
else:
    print(f"WARNING: Missing Streck ratio table: {STRECK_RATIO}")

if EDTA_RATIO.exists():
    ratio_frames.append(load_ratio_table(EDTA_RATIO, "EDTA"))
else:
    print(f"WARNING: Missing EDTA ratio table: {EDTA_RATIO}")

if ratio_frames:
    ratio_df = pd.concat(ratio_frames, ignore_index=True)
    order = ["Streck Healthy", "Streck Cancer", "EDTA Healthy", "EDTA Cancer"]
    data = [ratio_df[ratio_df["group_label"] == x]["ratio"].values for x in order]

    ax.violinplot(data, showmedians=True)
    ax.boxplot(data, widths=0.15, showfliers=True)

    for i, vals in enumerate(data, start=1):
        if len(vals) > 0:
            jitter = np.random.default_rng(42).normal(i, 0.035, len(vals))
            ax.scatter(jitter, vals, alpha=0.25, s=12)
            ax.text(i, np.median(vals), f"{np.median(vals):.3f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(range(1, len(order) + 1))
    ax.set_xticklabels(order, rotation=25, ha="right")
    ax.set_ylabel("Short / Long Ratio")
    ax.set_title("D. Per-Sample Short/Long Ratio")
    ax.grid(axis="y", alpha=0.3)
else:
    ax.text(0.5, 0.5, "Ratio tables not found", ha="center", va="center")
    ax.set_axis_off()

fig.suptitle("Streck vs EDTA WGS Fragment-Length Comparison", fontsize=16)
fig.text(0.5, 0.01, "Difference = cancer percentage − healthy percentage; Short: <140 bp; Long: 140–220 bp", ha="center", fontsize=10)
plt.tight_layout(rect=[0, 0.03, 1, 0.96])

out2 = OUT / "plot_02_four_panel_streck_vs_edta_summary.png"
plt.savefig(out2, dpi=300)
print(f"Saved: {out2}")

# ==============================
# PRINT SUMMARY
# ==============================
print("\nTop bins where Streck and EDTA agree:")
agree = df[(df["streck_diff"] * df["edta_diff"]) > 0].copy()
agree["agreement_strength"] = agree["streck_diff"].abs() + agree["edta_diff"].abs()
print(agree.sort_values("agreement_strength", ascending=False).head(10)[["length", "region", "streck_diff", "edta_diff"]].to_string(index=False))

print("\nTop bins where Streck and EDTA are opposite:")
opp = df[(df["streck_diff"] * df["edta_diff"]) < 0].copy()
opp["opposite_strength"] = opp["streck_diff"].abs() + opp["edta_diff"].abs()
print(opp.sort_values("opposite_strength", ascending=False).head(10)[["length", "region", "streck_diff", "edta_diff"]].to_string(index=False))
