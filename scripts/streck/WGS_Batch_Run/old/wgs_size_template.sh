#!/bin/bash
set -euo pipefail

SAMPLE=$1
GROUP=$2

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

if [ "$GROUP" = "healthy" ]; then
  R1="data/WGS_hc/${SAMPLE}_R1.fastq.gz"
  R2="data/WGS_hc/${SAMPLE}_R2.fastq.gz"
else
  R1="data/WGS_ca/${SAMPLE}_R1.fastq.gz"
  R2="data/WGS_ca/${SAMPLE}_R2.fastq.gz"
fi

REF="/storage1/fs1/christophermaher/Active/maherlab/lil1/annot/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
OUTBAM="alignments/wgs_all/${SAMPLE}.sorted.bam"
OUTFRAG="results/fragment_size/WGS/all/${SAMPLE}_frag.txt"

echo "[$(date)] START sample=$SAMPLE group=$GROUP"
echo "R1=$R1"
echo "R2=$R2"

which bwa
which samtools

bwa mem -t 2 "$REF" "$R1" "$R2" | samtools sort -o "$OUTBAM"
samtools index "$OUTBAM"

samtools view -f 2 "$OUTBAM" \
| awk '{print $9}' \
| awk '{print ($1>0)?$1:-$1}' \
| awk '$1>0 && $1<1000' \
> "$OUTFRAG"

awk '{sum+=$1; count++} END {print "Mean:", sum/count, "Count:", count}' "$OUTFRAG"

rm -f "$OUTBAM" "${OUTBAM}.bai"

echo "[$(date)] DONE sample=$SAMPLE"
