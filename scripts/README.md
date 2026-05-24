# Fragmentomics Analysis Scripts

This directory contains the scripts used for alignment, fragment-length analysis, end-motif analysis, cohort comparisons, quality-control assessment, and visualization of cfDNA fragmentomics data from WGS and EDTA plasma samples.

## Directory Structure

```text
scripts/
├── EDTA/
├── sample_run/
├── streck/
└── Visulisations/
```

---

# EDTA

Scripts used for processing EDTA plasma samples and generating EDTA-specific fragmentomics analyses.

## Included Scripts

### build_edta_group_compare.sh

Creates healthy-versus-cancer group comparison datasets from processed EDTA samples.

### EDTA_length_count_and_bins.sh

Calculates fragment-length distributions and generates binned fragment-length counts.

### make_edta_wgs_sample_manifest.sh

Builds sample-manifest files used to organize and process EDTA cohorts.

### run_edta_wgs_motifs_group_5mer.sh

Runs cohort-level 5-mer end-motif analysis on EDTA samples.

### run_edta_wgs_streckstyle_size_worker.sh

Processes EDTA samples using the same fragment-length workflow used for WGS/Streck datasets.

---

## EDTA_Plots

Visualization scripts for EDTA fragmentomics analyses.

### plot_edta_line.py

Generates normalized fragment-length distribution plots.

### plot_edta_range.py

Visualizes fragment-length ranges across samples.

### plot_edta_difference.py

Shows fragment-length differences between groups.

### plot_edta_violin.py

Creates violin plots for fragment-length distributions.

### plot_streck_vs_edta_fragment_comparison.py

Direct comparison of Streck and EDTA fragment-length profiles.

### plot_01_line_EDTA_streckstyle.py

### plot_02_range_EDTA_streckstyle.py

### plot_03_difference_EDTA_streckstyle.py

### plot_04_violin_EDTA_streckstyle.py

Alternative EDTA visualizations generated using the Streck-style processing workflow.

---

# sample_run

Contains example scripts used to test and validate the workflow on individual samples.

## Included Scripts

### run_seq015743_wgs.sh

Example workflow execution script for a single WGS sample.

Used for pipeline validation before large-scale cohort processing.

---

# streck

Scripts used for WGS/Streck plasma fragmentomics analyses.

## Directory Structure

```text
streck/
├── WGS_Batch_Run/
├── Hmc_Batch_runs/
└── end_motif/
```

---

## WGS_Batch_Run

Core WGS processing pipeline.

### wgs_stage1_bwa_worker.sh

Performs alignment of paired-end FASTQ files against the reference genome using BWA.

Input:

- FASTQ files

Output:

- SAM alignment files

### wgs_stage2_samtools_worker.sh

Converts SAM files to BAM format and performs sorting/indexing.

Input:

- SAM files

Output:

- Sorted BAM files

### submit_wgs_two_stage_jobs.sh

Batch submission script for large-scale WGS processing.

Coordinates alignment and BAM-generation jobs across multiple samples.

### WGS_length_count_and_bins.sh

Extracts fragment lengths from BAM files and generates binned fragment-length distributions.

### wgs_compute_means.sh

Computes cohort-level summary statistics and average fragment-length profiles.

### old/

Archive directory containing earlier versions of workflow scripts.

---

## end_motif

Scripts used for cfDNA end-motif analysis.

### WGS/4mer

Analysis of 4-mer end motifs.

### WGS/5mer

Analysis of 5-mer end motifs.

#### end_motif_count_5mer.sh

Counts 5-mer motif frequencies from processed fragment data.

#### run_wgs_motifs_group_5mer_fixed.sh

Generates cohort-level 5-mer motif summaries and group comparisons.

### hmc

Equivalent end-motif workflows for 5hmC datasets.

---

# Visulisations

Scripts used to generate publication-style figures and cohort-level summaries.

## WGS

### plot_01_normalized_line.py

Normalized fragment-length distribution.

### plot_01_normalized_line_regions_WGS.py

Regional fragment-length distribution comparisons.

### plot_pilot_healthy_vs_cancer.py

Healthy-versus-cancer cohort comparison.

### plot_WGS_legth_mean_.py

Mean fragment-length visualization.

### plot_01_top10_5prime_4mer_WGS.py

Top 10 enriched 5′ 4-mer motifs.

### plot_02_top10_3prime_4mer_WGS.py

Top 10 enriched 3′ 4-mer motifs.

### plot_03_difference_4mer_WGS.py

Differential 4-mer motif analysis.

### plot_04_ranked_distribution_4mer_WGS.py

Ranked motif-frequency distributions.

### plot_06_foldchange__4mer_WGS.py

4-mer motif fold-change analysis.

### plot_01_top10_5prime_WGS_5mer.py

Top 10 enriched 5′ 5-mer motifs.

### plot_02_top10_3prime_WGS_5mer.py

Top 10 enriched 3′ 5-mer motifs.

### plot_03_simplified_difference_WGS_5mer.py

Simplified motif-difference visualization.

### plot_04_foldchange_WGS_5mer.py

5-mer motif fold-change analysis.

### plot_combined_5prime_4mer_motifs.py

Combined motif-comparison visualization.

### plot_finished_wgs_samples.py

Summary visualization of completed WGS sample processing.

## Hmc

Visualization scripts used for 5hmC fragmentomics analyses.

---

# Workflow Overview

```text
FASTQ
↓
BWA Alignment
↓
SAM
↓
BAM Conversion and Sorting
↓
Fragment-Length Extraction
↓
Length Binning and Cohort Summaries
↓
Healthy vs Cancer Comparisons
↓
End-Motif Analysis (4-mer / 5-mer)
↓
Visualization and Reporting
```

# Notes

These scripts were developed and executed on the Washington University Compute1 HPC environment.

Most scripts contain project-specific paths and may require modification before execution on a different computing environment.

Large sequencing files and intermediate outputs are not included in this repository.
