#!/bin/bash
set -euo pipefail

SAMPLE="$1"
GROUP="$2"

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

INSAM="alignments/hmc_stage1_sam/${SAMPLE}.sam"
OUTBAM="alignments/hmc_stage2_bam/${SAMPLE}.sorted.bam"
OUTFRAG="results/fragment_size/hmC/all/${SAMPLE}_frag.txt"

START_EPOCH=$(date +%s)
echo "[$(date)] START stage2 sample=$SAMPLE group=$GROUP"
echo "insam=$INSAM"
echo "outbam=$OUTBAM"
echo "outfrag=$OUTFRAG"

samtools view -bS "$INSAM" | samtools sort -o "$OUTBAM"
samtools index "$OUTBAM"

samtools view -f 2 "$OUTBAM" \
| awk '{print $9}' \
| awk '{print ($1>0)?$1:-$1}' \
| awk '$1>0 && $1<1000' \
> "$OUTFRAG"

rm -f "$INSAM"

END_EPOCH=$(date +%s)
ELAPSED=$((END_EPOCH - START_EPOCH))

echo "[$(date)] DONE stage2 sample=$SAMPLE"
echo "elapsed_seconds=$ELAPSED"
echo "deleted_sam=$INSAM"
