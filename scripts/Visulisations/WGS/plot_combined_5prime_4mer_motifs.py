import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Load data
# ==============================
df = pd.read_csv("combined_5prime_motifs.tsv", sep="\t", header=None, names=["motif", "count"])

# ==============================
# Normalize to percentage
# ==============================
total_count = df["count"].sum()
df["percent"] = (df["count"] / total_count) * 100

# Keep top motifs for plotting
top_n = 15
top_df = df.head(top_n).copy()

# ==============================
# Plot 1: Raw counts
# ==============================
plt.figure(figsize=(12, 6))
bars = plt.bar(top_df["motif"], top_df["count"])

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f"{int(height):,}", ha="center", va="bottom", fontsize=8)

plt.xlabel("5′ end motif")
plt.ylabel("Raw count")
plt.title("Top 15 Combined 5′ End Motifs (Raw Counts)")
plt.xticks(rotation=45)

# Add explanation
plt.figtext(
    0.5, 0.01,
    "Raw counts represent total occurrences of each 4-mer motif across all samples.",
    ha="center",
    fontsize=10
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig("combined_5prime_motifs_raw_counts.png", dpi=300)
plt.close()

# ==============================
# Plot 2: Normalized percentage
# ==============================
plt.figure(figsize=(12, 6))
bars = plt.bar(top_df["motif"], top_df["percent"])

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.2f}%", ha="center", va="bottom", fontsize=8)

plt.xlabel("5′ end motif")
plt.ylabel("Percentage of total motifs (%)")
plt.title("Top 15 Combined 5′ End Motifs (Normalized Percentage)")
plt.xticks(rotation=45)

# Add normalization equation
plt.figtext(
    0.5, 0.01,
    "Normalization: Percentage = (motif count / total motif count) × 100",
    ha="center",
    fontsize=10
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig("combined_5prime_motifs_percentage.png", dpi=300)
plt.close()

# ==============================
# Save full table
# ==============================
df.to_csv("combined_5prime_motifs_with_percentage.tsv", sep="\t", index=False)

# ==============================
# Print summary
# ==============================
print("Total motif count =", total_count)
print("Top motifs preview:")
print(top_df.head())

print("\nFiles generated:")
print(" - combined_5prime_motifs_raw_counts.png")
print(" - combined_5prime_motifs_percentage.png")
print(" - combined_5prime_motifs_with_percentage.tsv")
