#!/bin/bash

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

mkdir -p results/end_motifs/hmC/all_raw
mkdir -p results/end_motifs/hmC/all_clean

while read sample group dtype status; do

  if [ "$dtype" = "5hmC" ]; then

    if [ "$group" = "healthy" ]; then
      R1="data/hmC_hc/${sample}_R1.fastq.gz"
    else
      R1="data/hmC_ca/${sample}_R1.fastq.gz"
    fi

    OUT_PREFIX="results/end_motifs/hmC/all_raw/${sample}"

    zcat $R1 | awk 'NR%4==2 {print substr($0,1,4)}' > ${OUT_PREFIX}_5prime.txt
    zcat $R1 | awk 'NR%4==2 {print substr($0,length($0)-3,4)}' > ${OUT_PREFIX}_3prime.txt

    grep -v N ${OUT_PREFIX}_5prime.txt | sort | uniq -c | sort -nr \
    > results/end_motifs/hmC/all_clean/${sample}_5prime_counts.txt

    grep -v N ${OUT_PREFIX}_3prime.txt | sort | uniq -c | sort -nr \
    > results/end_motifs/hmC/all_clean/${sample}_3prime_counts.txt

  fi

done < sample_manifest.tsv
