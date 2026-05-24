#!/bin/bash
set -euo pipefail

SAMPLE="$1"
GROUP="$2"

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

if [ "$GROUP" = "healthy" ]; then
  R1="data/WGS_hc/${SAMPLE}_R1.fastq.gz"
  R2="data/WGS_hc/${SAMPLE}_R2.fastq.gz"
else
  R1="data/WGS_ca/${SAMPLE}_R1.fastq.gz"
  R2="data/WGS_ca/${SAMPLE}_R2.fastq.gz"
fi

REF="/storage1/fs1/christophermaher/Active/maherlab/lil1/annot/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
OUTSAM="alignments/wgs_stage1_sam/${SAMPLE}.sam"

START_EPOCH=$(date +%s)
echo "[$(date)] START stage1 sample=$SAMPLE group=$GROUP"
echo "R1=$R1"
echo "R2=$R2"
echo "REF=$REF"

bwa mem -t 2 "$REF" "$R1" "$R2" > "$OUTSAM"

END_EPOCH=$(date +%s)
ELAPSED=$((END_EPOCH - START_EPOCH))

echo "[$(date)] DONE stage1 sample=$SAMPLE"
echo "elapsed_seconds=$ELAPSED"
echo "outsam=$OUTSAM"
