# Results

This directory contains representative outputs generated during the fragmentomics analysis workflow. Results are organized by sample type, analysis type, quality-control summaries, and visualization outputs.

## Directory Structure

```text
results/
├── EDTA/
├── streck/
├── plots/
└── qc/
```

---

# EDTA

Results generated from EDTA plasma samples.

## Directory Structure

```text
EDTA/
├── 5mer/
└── WGS_length/
```

---

## 5mer

Results from 5-mer end-motif analysis.

### group_compare

Contains cohort-level motif summaries used for healthy-versus-cancer comparisons.

Included files:

- cancer_5prime_combined.tsv
- cancer_3prime_combined.tsv
- healthy_5prime_combined.tsv
- healthy_3prime_combined.tsv

Sample lists:

- edta_wgs_cancer_samples.txt
- edta_wgs_healthy_samples.txt

These files contain aggregated motif frequencies used to identify differential motif enrichment between cohorts.

### motif_length_sampled_1k

Contains motif-length distributions generated using randomly sampled fragments.

### selected_motifs

Contains selected motifs used for downstream comparisons and visualization.

---

## WGS_length

Results from fragment-length analysis.

### group_compare

Included files:

- cancer_binned.tsv
- healthy_binned.tsv
- cancer_fragments.txt
- healthy_fragments.txt

These files contain fragment-length distributions and binned fragment counts used for healthy-versus-cancer comparisons.

---

# streck

Results generated from WGS/Streck plasma samples.

## Directory Structure

```text
streck/
├── WGS_length/
├── 4mer/
└── 5mer/
```

---

## WGS_length

Fragment-length analysis results.

### group_compare

Key files:

- cancer_fragment_distribution_binned.tsv
- healthy_fragment_distribution_binned.tsv
- wgs_cancer_samples.txt
- wgs_healthy_samples.txt

Generated figure:

- plot_01_normalized_line.png

This figure shows normalized fragment-length distributions for healthy and cancer cohorts.

### export_for_plotting

Contains processed data prepared for visualization workflows.

### plots_data

Intermediate files used by plotting scripts.

### plots

Final visualization outputs generated from WGS fragment-length analyses.

### Summary Files

- sample_fragment_sizes.txt
- sample_fragment_sizes_filtered.txt
- sample_fragment_sizes_abs.txt
- wgs_sample_means.tsv

These files contain per-sample fragment statistics and cohort-level summary metrics.

---

## 5mer

Results from WGS 5-mer end-motif analysis.

Included files:

- cancer_5prime_combined.tsv
- cancer_3prime_combined.tsv
- healthy_5prime_combined.tsv
- healthy_3prime_combined.tsv

Sample lists:

- wgs_cancer_samples.txt
- wgs_healthy_samples.txt

### plots

Contains visualization outputs generated from motif-frequency analyses.

These results were used to identify motif enrichment patterns associated with cancer and healthy samples.

---

## 4mer

Results from WGS 4-mer end-motif analysis.

Contains motif-frequency summaries and downstream comparison results used to generate motif enrichment figures.

---

# plots

Centralized collection of visualization outputs generated throughout the project.

## Directory Structure

```text
plots/
├── EDTA_WGS/
├── EDTA_WGS_5mer/
├── EDTA_WGS_streckstyle/
├── compare_streck_edta/
├── end_motif_length_1k/
├── end_motif_length_1k_v2/
└── end_motif_length_10k_core/
```

### EDTA_WGS

Fragment-length comparison plots generated from EDTA samples.

### EDTA_WGS_5mer

5-mer motif comparison plots generated from EDTA samples.

### EDTA_WGS_streckstyle

EDTA analyses processed using the Streck-style workflow.

### compare_streck_edta

Direct comparisons between Streck and EDTA sample cohorts.

### end_motif_length_1k

Motif-length analyses generated using 1,000 sampled fragments.

### end_motif_length_1k_v2

Updated version of the 1k motif-length workflow.

### end_motif_length_10k_core

Motif-length analyses generated using 10,000 sampled fragments.

These figures were used to evaluate motif distributions across cohorts and processing methods.

---

# qc

Quality-control summaries used to monitor workflow progress and sample processing.

Included files:

- progress_status.tsv
- group_counts.tsv

These files track processed samples, cohort composition, and overall workflow status.

---

# Workflow Context

The results in this directory were generated using the following workflow:

```text
FASTQ
↓
BWA Alignment
↓
SAM/BAM Processing
↓
Fragment-Length Extraction
↓
Length Binning
↓
Healthy vs Cancer Comparison
↓
End-Motif Analysis (4-mer / 5-mer)
↓
Quality Control
↓
Visualization
```

# Notes

Large raw sequencing files, BAM files, and intermediate processing files are not included in the GitHub version of this project.

Only representative outputs and summary results are provided to demonstrate the workflow and analyses.
