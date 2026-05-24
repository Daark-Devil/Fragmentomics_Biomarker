#!/bin/bash
set -euo pipefail

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

while read -r sample group dtype status; do

  jid1=$(bsub \
    -q general \
    -a 'docker(mgibio/dna-alignment)' \
    -R "select[mem>64000] rusage[mem=64000]" \
    -M 64000000 \
    -o "logs/wgs_stage1/${sample}.out" \
    -e "logs/wgs_stage1/${sample}.err" \
    scripts/wgs_stage1_bwa_worker.sh "$sample" "$group" \
    | awk '{gsub(/[<>]/,"",$2); print $2}')

  bsub \
    -q general \
    -w "done(${jid1})" \
    -a 'docker(biocontainers/samtools:v1.9-4-deb_cv1)' \
    -R "select[mem>16000] rusage[mem=16000]" \
    -M 16000000 \
    -o "logs/wgs_stage2/${sample}.out" \
    -e "logs/wgs_stage2/${sample}.err" \
    scripts/wgs_stage2_samtools_worker.sh "$sample" "$group"

done < manifests/wgs_manifest.tsv
