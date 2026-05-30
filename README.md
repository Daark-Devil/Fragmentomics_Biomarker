# Fragmentomics Analysis of cfDNA Using Whole Genome Sequencing

This repository contains workflows, scripts, validation examples, and representative results used for fragmentomics analysis of cell-free DNA (cfDNA) from Whole Genome Sequencing (WGS) datasets.

The project focuses on identifying fragmentation patterns, fragment-length distributions, and end-motif signatures associated with healthy and cancer samples. The workflow was developed and executed on the Washington University Compute1 HPC environment using large-scale sequencing datasets and cohort-level analyses.

---
# Key Outcomes

  Built FASTQ-to-BAM WGS processing workflow.
  
  Extracted TLEN-based fragment lengths from BAM files.
  
  Compared healthy and cancer fragment-length distributions.

  Added 4-mer and 5-mer end-motif analysis.
  
  Built EDTA-vs-Streck and healthy-vs-cancer comparison outputs.
  
  Generated interactive dashboard with statistical summaries.
# Project Overview

Cell-free DNA fragmentomics has emerged as a powerful approach for studying biological processes and disease-associated signatures. Differences in fragment lengths and end-motif patterns can provide information about chromatin organization, tissue origin, and disease status.

The primary goals of this project were:

- Process raw sequencing data from healthy and cancer cohorts
- Generate aligned BAM files from paired-end sequencing reads
- Extract fragment-length information
- Compare fragment-length distributions between cohorts
- Calculate cohort-level fragment statistics
- Perform 4-mer and 5-mer end-motif analysis
- Compare motif enrichment patterns between healthy and cancer samples
- Validate workflow reproducibility using representative test samples
- Generate publication-style visualizations and summary statistics

---
# Interactive Dashboard and Statistical Interpretation
“The repository includes an interactive EDTA WGS 5-mer fragmentomics dashboard for healthy-vs-cancer comparison. It summarizes motif abundance, fragment-length density, cancer-minus-healthy difference curves, fragment category shifts, Cohen’s d, binned KS distance, mean/median/Q1/Q3, and cohort-level motif comparisons(https://github.com/Daark-Devil/Fragmentomics_Biomarker/blob/main/Doc/edta_wgs_5mer_fragmentomics_dashboard_v3.html).”
# Workflow

```text
Paired-End FASTQ Files
            ↓
      BWA Alignment
            ↓
         SAM Files
            ↓
   BAM Conversion & Sorting
            ↓
 Fragment-Length Extraction
            ↓
 Fragment Binning & Summaries
            ↓
 Healthy vs Cancer Comparisons
            ↓
 End-Motif Analysis
       (4-mer / 5-mer)
            ↓
 Quality Control
            ↓
 Visualization & Reporting
```

---

# Repository Structure

```text
Fragmentomics-WGS/
├── README.md
├── scripts/
├── results/
├── samples_test/
├── qc_check/
└── Doc/
```

---

# Scripts

The `scripts` directory contains the analysis workflows used throughout the project.

Major components include:

### Alignment

- BWA alignment workflows
- SAM generation
- BAM conversion and sorting
- Batch processing of multiple samples

### Fragment-Length Analysis

- Fragment-length extraction
- Length binning
- Cohort-level summary generation
- Healthy vs cancer comparisons

### End-Motif Analysis

- 4-mer motif analysis
- 5-mer motif analysis
- Cohort-level motif enrichment studies

### Visualization

- Fragment-length distributions
- Healthy vs cancer comparisons
- End-motif enrichment plots
- Cohort summary figures

### EDTA and Streck Processing

Separate workflows were developed to support analysis of EDTA and Streck tube sample collections.

---

# Results

The repository includes representative outputs generated during analysis.

Included result categories:

### Fragment-Length Analysis

- Per-sample fragment-length distributions
- Cohort-level fragment-length summaries
- Binned fragment-length comparisons
- Mean fragment-size calculations

### End-Motif Analysis

- 4-mer motif frequencies
- 5-mer motif frequencies
- Healthy vs cancer motif comparisons
- Differential motif enrichment analyses

### Quality Control

- Workflow progress tracking
- Sample counts
- Validation summaries

### Visualizations

- Normalized fragment-length distributions
- Healthy vs cancer comparisons
- Motif enrichment plots
- EDTA vs Streck comparisons
- Fragment-length summary figures

---

# Validation Examples

The `samples_test` directory contains representative validation examples used to verify workflow reproducibility.

Examples include:

### Fragment-Length Validation

Validation sample:

```text
seq003213
```

Used to compare regenerated fragment-length outputs against original results.

Included files:

- SAM alignment
- Sorted BAM
- BAM index
- Fragment-length outputs
- Binned fragment distributions

### End-Motif Validation

Representative motif-count outputs generated from individual WGS samples.

These examples were used to verify motif extraction and motif-frequency calculations prior to cohort-level processing.

---

# Example Commands

## Run Alignment Workflow

```bash
bash wgs_stage1_bwa_worker.sh
bash wgs_stage2_samtools_worker.sh
```

## Run Fragment-Length Analysis

```bash
bash WGS_length_count_and_bins.sh
```

## Run End-Motif Analysis

```bash
bash run_wgs_motifs_group_5mer_fixed.sh
```

## Generate Visualizations

```bash
python plot_01_normalized_line.py
python plot_pilot_healthy_vs_cancer.py
```

---

# Technologies Used

### Sequencing Analysis

- BWA
- SAMtools

### Scripting

- Bash
- Python

### Data Processing

- Pandas
- NumPy

### Visualization

- Matplotlib
- Seaborn

### Computing Environment

- Washington University Compute1 HPC
- Linux
- Docker-based batch jobs

---

# Notes

Large sequencing datasets, FASTQ files, BAM files, and cohort-scale intermediate files are not included in this repository due to storage constraints.

Only representative scripts, validation examples, summary outputs, and visualization results are provided.

Many scripts contain Compute1-specific file paths and may require modification before running on a different system.

---

# Author

**Devansh Pancholi**

M.S. Bioinformatics and Computational Biology

Saint Louis University

Research Areas:

- Computational Genomics
- Fragmentomics
- Cancer Genomics
- Sequencing Data Analysis
- Bioinformatics Workflow Development
- Machine Learning for Biological Data
