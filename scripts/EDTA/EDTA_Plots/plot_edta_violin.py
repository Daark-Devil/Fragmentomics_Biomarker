from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE = Path("/storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics")
MANIFEST = BASE / "manifests" / "edta_wgs_manifest.tsv"
FRAG_DIR = BASE / "results" / "fragment_size" / "EDTA_WGS" / "all"
OUT_DIR = BASE / "plots" / "EDTA_WGS" / "violin"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def ratio_for_sample(sample):
    f = FRAG_DIR / f"{sample}_frag.txt"
    short = 0
    long = 0
    with open(f) as fh:
        for line in fh:
            try:
                x = int(line.strip())
            except:
                continue
            if x < 140:
                short += 1
            elif 140 <= x <= 220:
                long += 1
    return short / long if long > 0 else None

healthy = []
cancer = []

with open(MANIFEST) as fh:
    for line in fh:
        sample, group, dtype = line.strip().split()
        r = ratio_for_sample(sample)
        if r is None:
            continue
        if group == "healthy":
            healthy.append(r)
        elif group == "cancer":
            cancer.append(r)

print("Healthy samples:", len(healthy))
print("Cancer samples:", len(cancer))
print("Healthy median:", np.median(healthy))
print("Cancer median:", np.median(cancer))

plt.figure(figsize=(7,6))
plt.violinplot([healthy, cancer], showmeans=False, showmedians=True)

plt.boxplot(
    [healthy, cancer],
    widths=0.18,
    showfliers=False,
    medianprops={"color": "black"},
)

plt.xticks([1,2], ["Healthy", "Cancer"])
plt.ylabel("Short / Long Fragment Ratio")
plt.title("EDTA WGS Short/Long Fragment Ratio by Group")
plt.figtext(0.5, 0.01, "Short: <140 bp; Long: 140–220 bp", ha="center", fontsize=10)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout(rect=[0,0.04,1,1])

out = OUT_DIR / "edta_violin_short_long_ratio.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
