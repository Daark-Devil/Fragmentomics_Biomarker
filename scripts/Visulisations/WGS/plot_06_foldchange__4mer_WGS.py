from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
IN_DIR = BASE / "results" / "end_motifs" / "WGS" / "group_compare"
OUT_DIR = IN_DIR / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_fc(hfile, cfile, title, outname):
    h = pd.read_csv(hfile, sep=r"\s+", header=None, names=["motif", "count"])
    c = pd.read_csv(cfile, sep=r"\s+", header=None, names=["motif", "count"])

    h["pct_h"] = h["count"] / h["count"].sum() * 100
    c["pct_c"] = c["count"] / c["count"].sum() * 100

    m = h[["motif", "pct_h"]].merge(
        c[["motif", "pct_c"]],
        on="motif", how="outer"
    ).fillna(0)

    # pseudo-count to avoid division by zero
    m["log2_fc"] = np.log2((m["pct_c"] + 1e-6) / (m["pct_h"] + 1e-6))
    m["abs_fc"] = m["log2_fc"].abs()
    top = m.sort_values("abs_fc", ascending=False).head(12).sort_values("log2_fc")

    colors = ["tab:red" if x > 0 else "tab:blue" for x in top["log2_fc"]]

    plt.figure(figsize=(10, 6))
    plt.barh(top["motif"], top["log2_fc"], color=colors)
    plt.axvline(0, color="black", linewidth=1)
    plt.xlabel("log2(Cancer / Healthy)")
    plt.title(title)
    plt.figtext(
        0.5, 0.01,
        "Positive = enriched in cancer; Negative = enriched in healthy",
        ha="center", fontsize=10
    )
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout(rect=[0, 0.05, 1, 1])

    out = OUT_DIR / outname
    plt.savefig(out, dpi=300)
    print(f"Saved: {out}")

load_fc(
    IN_DIR / "healthy_5prime_combined.tsv",
    IN_DIR / "cancer_5prime_combined.tsv",
    "WGS 5′ End-Motif Fold Change",
    "plot_06_foldchange_5prime_WGS.png"
)

load_fc(
    IN_DIR / "healthy_3prime_combined.tsv",
    IN_DIR / "cancer_3prime_combined.tsv",
    "WGS 3′ End-Motif Fold Change",
    "plot_06_foldchange_3prime_WGS.png"
)
