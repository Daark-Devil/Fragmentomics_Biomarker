from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(".")
SUMMARY_FILE = BASE / "summary.tsv"
DIST_DIR = BASE / "dist"
OUT_DIR = BASE / "plots"
OUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# 1. Load summary table
# -----------------------------
summary = pd.read_csv(SUMMARY_FILE, sep="\t")

# infer group from sample name
def infer_group(sample_name: str) -> str:
    if "_NC_" in sample_name:
        return "healthy"
    return "cancer"

summary["group"] = summary["sample"].apply(infer_group)

print("Loaded samples:", len(summary))
print(summary.head())

# -----------------------------
# 2. Overview plot: sample means
# -----------------------------
plt.figure(figsize=(14, 6))
plt.plot(summary["sample"], summary["mean"], marker="o")
plt.xticks(rotation=90)
plt.ylabel("Mean fragment length (bp)")
plt.title("Mean Fragment Length per Sample")
plt.tight_layout()
plt.savefig(OUT_DIR / "all_samples_mean_line.png", dpi=200)
plt.close()

# -----------------------------
# 3. Overview plot: min/mean/max per sample
# -----------------------------
plt.figure(figsize=(14, 6))
x = range(len(summary))
plt.vlines(x, summary["min"], summary["max"], linewidth=1)
plt.scatter(x, summary["mean"], s=20)
plt.xticks(x, summary["sample"], rotation=90)
plt.ylabel("Fragment length (bp)")
plt.title("Per-sample Range (min-max) with Mean")
plt.tight_layout()
plt.savefig(OUT_DIR / "all_samples_range_mean.png", dpi=200)
plt.close()

# -----------------------------
# 4. Group overview if both exist
# -----------------------------
if summary["group"].nunique() > 1:
    plt.figure(figsize=(8, 6))
    data = [
        summary.loc[summary["group"] == "healthy", "mean"],
        summary.loc[summary["group"] == "cancer", "mean"],
    ]
    plt.boxplot(data, tick_labels=["healthy", "cancer"])
    plt.ylabel("Mean fragment length (bp)")
    plt.title("Healthy vs Cancer Mean Fragment Length")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "healthy_vs_cancer_boxplot.png", dpi=200)
    plt.close()
else:
    print("Only one group present so far. Group comparison plot skipped.")

# -----------------------------
# 5. Per-sample plots from dist files
# -----------------------------
if DIST_DIR.exists():
    dist_files = sorted(DIST_DIR.glob("*_dist.tsv"))
    print("Distribution files found:", len(dist_files))

    for dist_file in dist_files:
        sample = dist_file.name.replace("_dist.tsv", "")
        dist = pd.read_csv(dist_file, sep=r"\s+", header=None, names=["bin", "count"])

        if dist.empty:
            continue

        # Graph 1: distribution line plot
        plt.figure(figsize=(10, 5))
        plt.plot(dist["bin"], dist["count"], marker="o")
        plt.xlabel("Fragment length bin (bp)")
        plt.ylabel("Count")
        plt.title(f"{sample} - Fragment Length Distribution")
        plt.tight_layout()
        plt.savefig(OUT_DIR / f"{sample}_distribution.png", dpi=200)
        plt.close()

        # Graph 2: summary chart for this sample
        row = summary.loc[summary["sample"] == sample]
        if not row.empty:
            row = row.iloc[0]

            plt.figure(figsize=(8, 4))
            x_positions = [1, 2, 3]
            y_values = [row["min"], row["mean"], row["max"]]

            plt.bar(x_positions, y_values)
            plt.xticks(x_positions, ["Min", "Mean", "Max"])
            plt.ylabel("Fragment length (bp)")
            plt.title(f"{sample} - Summary Statistics")
            plt.text(1, row["min"] + 2, f'{row["min"]}', ha="center")
            plt.text(2, row["mean"] + 2, f'{row["mean"]:.2f}', ha="center")
            plt.text(3, row["max"] + 2, f'{row["max"]}', ha="center")
            plt.figtext(0.5, 0.01, f'Count = {int(row["count"])}', ha="center")
            plt.tight_layout()
            plt.savefig(OUT_DIR / f"{sample}_summary.png", dpi=200)
            plt.close()
else:
    print("No dist directory found. Per-sample distribution plots skipped.")

print("Plots written to:", OUT_DIR.resolve())
