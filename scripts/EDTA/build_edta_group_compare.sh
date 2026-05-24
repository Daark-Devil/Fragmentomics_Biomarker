#!/bin/bash
set -euo pipefail

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

mkdir -p results/fragment_size/EDTA_WGS/group_compare
mkdir -p logs/edta_group_compare

# clean outputs
: > results/fragment_size/EDTA_WGS/group_compare/healthy_fragments.txt
: > results/fragment_size/EDTA_WGS/group_compare/cancer_fragments.txt

echo "[$(date)] START healthy concat"
while read -r sample group dtype; do
  cat "results/fragment_size/EDTA_WGS/all/${sample}_frag.txt" >> results/fragment_size/EDTA_WGS/group_compare/healthy_fragments.txt
done < manifests/edta_wgs_healthy_manifest.tsv
echo "[$(date)] DONE healthy concat"

echo "[$(date)] START cancer concat"
while read -r sample group dtype; do
  cat "results/fragment_size/EDTA_WGS/all/${sample}_frag.txt" >> results/fragment_size/EDTA_WGS/group_compare/cancer_fragments.txt
done < manifests/edta_wgs_cancer_manifest.tsv
echo "[$(date)] DONE cancer concat"

echo "[$(date)] START healthy binning"
awk '{bin=int($1/10)*10; count[bin]++} END{for(b in count) print b, count[b]}' \
  results/fragment_size/EDTA_WGS/group_compare/healthy_fragments.txt \
  | sort -k1 -n \
  > results/fragment_size/EDTA_WGS/group_compare/healthy_binned.tsv
echo "[$(date)] DONE healthy binning"

echo "[$(date)] START cancer binning"
awk '{bin=int($1/10)*10; count[bin]++} END{for(b in count) print b, count[b]}' \
  results/fragment_size/EDTA_WGS/group_compare/cancer_fragments.txt \
  | sort -k1 -n \
  > results/fragment_size/EDTA_WGS/group_compare/cancer_binned.tsv
echo "[$(date)] DONE cancer binning"

echo "[$(date)] FINISHED EDTA group compare"
