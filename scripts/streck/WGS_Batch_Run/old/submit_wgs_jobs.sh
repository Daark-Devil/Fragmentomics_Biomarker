#!/bin/bash

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

awk '$3=="WGS"' sample_manifest.tsv | while read sample group dtype status; do

  bsub -q general \
  -a 'docker(mgibio/dna-alignment)' \
  -R "select[mem>16000] rusage[mem=16000]" \
  -M 16000000 \
  -o logs/wgs_size_jobs/${sample}.out \
  -e logs/wgs_size_jobs/${sample}.err \
  scripts/wgs_size_template.sh $sample $group

done
