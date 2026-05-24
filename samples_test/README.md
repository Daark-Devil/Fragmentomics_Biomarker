# Sample Tests and Validation Examples

This folder contains small test outputs used to validate the fragmentomics workflow before running full cohort analyses.

## Directory Structure

```text
samples_test/
├── end_motif_exp/
└── validation_seq003213/
```

## end_motif_exp

This folder contains example outputs from single-sample end-motif testing.

Included files:

- `test_sample_5prime.txt`
- `test_sample_3prime.txt`
- `seq036965_NC_wgs_5prime_counts.txt`
- `seq036965_NC_wgs_3prime_counts.txt`
- `seq044371_IV_wgs_3prime_counts.txt`

These files were used to confirm that the end-motif extraction workflow correctly generated 5′ and 3′ motif count tables from FASTQ reads.

## validation_seq003213

This folder contains a validation run for sample `seq003213`.

Included files:

- `seq003213_validation.sam`
- `seq003213_validation.sorted.bam`
- `seq003213_validation.sorted.bam.bai`
- `fresh_seq003213_frag.txt`
- `fresh_seq003213_binned.tsv`
- `original_seq003213_frag.txt`
- `original_seq003213_binned.tsv`

Purpose:

This validation sample was used to compare newly regenerated fragment-length outputs against previously generated outputs. It helped confirm that the alignment, BAM processing, and fragment-length extraction workflow was reproducible.

## Example: Run end-motif extraction on one sample

```bash
bash scripts/extract_end_motifs.sh \
  data/WGS_hc/seq015764_NC_wgs_R1.fastq.gz \
  results/end_motifs/WGS/test_sample
```

Check output:

```bash
head results/end_motifs/WGS/test_sample_5prime_counts.txt
```

Expected output files:

```text
results/end_motifs/WGS/test_sample_5prime_counts.txt
results/end_motifs/WGS/test_sample_3prime_counts.txt
```

## Example: Run 5-mer motif analysis on one healthy sample

```bash
bash scripts/run_wgs_motifs_group_5mer_fixed.sh \
  <(printf "seq015764_NC_wgs\thealthy\n") \
  healthy_test
```

## Example: Run 5-mer motif analysis on one cancer sample

```bash
bash scripts/run_wgs_motifs_group_5mer_fixed.sh \
  <(printf "seq015743_IV_wgs\tcancer\n") \
  cancer_test
```

## Example: Submit cohort-level WGS 5-mer jobs on Compute1

Healthy cohort:

```bash
bsub -q general \
  -a 'docker(ubuntu:22.04)' \
  -o logs/wgs_endmotif_5mer/healthy.out \
  -e logs/wgs_endmotif_5mer/healthy.err \
  "cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics && bash scripts/run_wgs_motifs_group_5mer_fixed.sh manifests/wgs_healthy_manifest.tsv healthy"
```

Cancer cohort:

```bash
bsub -q general \
  -a 'docker(ubuntu:22.04)' \
  -o logs/wgs_endmotif_5mer/cancer.out \
  -e logs/wgs_endmotif_5mer/cancer.err \
  "cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics && bash scripts/run_wgs_motifs_group_5mer_fixed.sh manifests/wgs_cancer_manifest.tsv cancer"
```

## Notes

The commands above reflect the original Compute1 HPC environment and may require path changes before running elsewhere.

Large raw FASTQ files are not included in this GitHub version. This folder only contains small validation outputs and representative test results.
