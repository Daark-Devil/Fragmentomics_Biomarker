from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
FRAG_DIR = BASE / "results/fragment_size/WGS/all"
OUT_DIR = BASE / "results/fragment_size/WGS/plots_finished_samples"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# only completed non-empty files
frag_files = sorted([f for f in FRAG_DIR.glob("*_frag.txt") if f.stat().st_size > 0])

summary_rows = []

for frag_file in frag_files:
    sample = frag_file.name.replace("_frag.txt", "")

    # load lengths
    lengths = pd.read_csv(frag_file, header=None, names=["length"])
    lengths = lengths["length"].dropna().astype(int)

    if len(lengths) == 0:
        continue

    # basic stats
    mean_val = lengths.mean()
    median_val = lengths.median()
    q1 = lengths.quantile(0.25)
    q3 = lengths.quantile(0.75)
    min_val = lengths.min()
    max_val = lengths.max()

    summary_rows.append({
        "sample": sample,
        "mean": mean_val,
        "median": median_val,
        "q1": q1,
        "q3": q3,
        "min": min_val,
        "max": max_val,
        "count": len(lengths),
    })

    # -------- Graph 1: length distribution line plot --------
    bins = np.arange(0, 1001, 10)
    counts, edges = np.histogram(lengths, bins=bins)
    mids = (edges[:-1] + edges[1:]) / 2

    plt.figure(figsize=(10, 5))
    plt.plot(mids, counts)
    plt.xlabel("Fragment length (bp)")
    plt.ylabel("Count")
    plt.title(f"{sample} - Fragment Length Distribution")
    plt.axvline(mean_val, linestyle="--", linewidth=1, label=f"Mean = {mean_val:.2f}")
    plt.axvline(median_val, linestyle=":", linewidth=1, label=f"Median = {median_val:.2f}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / f"{sample}_distribution.png", dpi=200)
    plt.close()

    # -------- Graph 2: summary stats chart --------
    plt.figure(figsize=(8, 4))
    x_positions = [1, 2]
    y_values = [mean_val, median_val]

    plt.bar(x_positions, y_values)
    plt.xticks(x_positions, ["Mean", "Median"])
    plt.ylabel("Fragment length (bp)")
    plt.title(f"{sample} - Summary Statistics")

    # show Q1-Q3 band using vertical lines at mean/median positions
    plt.vlines(1, q1, q3, linewidth=3)
    plt.vlines(2, q1, q3, linewidth=3)

    # annotate values
    plt.text(1, mean_val + 2, f"{mean_val:.2f}", ha="center")
    plt.text(2, median_val + 2, f"{median_val:.2f}", ha="center")
    plt.text(1.5, max(y_values) + 12, f"Q1={q1:.1f}  Q3={q3:.1f}", ha="center")
    plt.text(1.5, max(y_values) + 24, f"Min={min_val}  Max={max_val}", ha="center")

    plt.tight_layout()
    plt.savefig(OUT_DIR / f"{sample}_summary.png", dpi=200)
    plt.close()

# save combined summary table
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(OUT_DIR / "finished_samples_summary.tsv", sep="\t", index=False)

print(f"Finished samples plotted: {len(summary_rows)}")
print(f"Output folder: {OUT_DIR}")
