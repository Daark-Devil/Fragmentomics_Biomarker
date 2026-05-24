#!/bin/bash
set -euo pipefail

MANIFEST="$1"
LABEL="$2"

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

mkdir -p results/fragment_size/EDTA_WGS_streckstyle/all
mkdir -p logs/edta_wgs_streckstyle_size

while read -r sample group dtype; do
  echo "[$(date)] START sample=$sample group=$group dtype=$dtype"

  if [ "$group" = "healthy" ]; then
    BAM="data/EDTA_WGS_hc/${sample}.bam"
  else
    BAM="data/EDTA_WGS_ca/${sample}.bam"
  fi

  OUT="results/fragment_size/EDTA_WGS_streckstyle/all/${sample}_frag.txt"

  samtools view -f 2 "$BAM" \
  | awk '{print $9}' \
  | awk '{print ($1>0)?$1:-$1}' \
  | awk '$1>0 && $1<1000' \
  > "$OUT"

  echo "[$(date)] DONE sample=$sample group=$group out=$OUT"
done < "$MANIFEST"

echo "[$(date)] FINISHED label=$LABEL"
