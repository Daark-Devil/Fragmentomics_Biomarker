#!/bin/bash
set -euo pipefail

GROUP_MANIFEST="$1"
LABEL="$2"

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

mkdir -p results/end_motifs/EDTA_WGS_5mer/all_clean
mkdir -p logs/edta_wgs_endmotif_5mer

while IFS=$'\t' read -r sample group; do
  echo "[$(date)] START sample=$sample group=$group"

  if [ "$group" = "healthy" ]; then
    R1="/storage1/fs1/christophermaher/Active/maherlab/netra/rawdata/FASTQ_FILES/Noncancer_EDTA/23-12-22/fastq/concat/${sample}_R1.fastq.gz"
  else
    R1="/storage1/fs1/christophermaher/Active/maherlab/netra/rawdata/FASTQ_FILES/CRC_EDTA/23-05-15/concat/${sample}_R1.fastq.gz"
  fi

  OUT5="results/end_motifs/EDTA_WGS_5mer/all_clean/${sample}_5prime_counts.txt"
  OUT3="results/end_motifs/EDTA_WGS_5mer/all_clean/${sample}_3prime_counts.txt"

  zcat "$R1" | awk '
    NR%4==2 {
      m=substr($0,1,5)
      if (m !~ /N/ && length(m)==5) c[m]++
    }
    END {for (k in c) print c[k], k}
  ' | sort -nr > "$OUT5"

  zcat "$R1" | awk '
    NR%4==2 {
      m=substr($0,length($0)-4,5)
      if (m !~ /N/ && length(m)==5) c[m]++
    }
    END {for (k in c) print c[k], k}
  ' | sort -nr > "$OUT3"

  echo "[$(date)] DONE sample=$sample"
done < "$GROUP_MANIFEST"

echo "[$(date)] FINISHED label=$LABEL"
