#!/bin/bash
set -euo pipefail

cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics

echo -e "sample\tgroup\tmean_frag\tcount" > results/fragment_size/WGS/wgs_sample_means.tsv

for f in results/fragment_size/WGS/all/*_frag.txt; do
  sample=$(basename "$f" | sed 's/_frag.txt$//')

  if echo "$sample" | grep -q "_NC_"; then
    group="healthy"
  else
    group="cancer"
  fi

  awk -v s="$sample" -v g="$group" '
    {sum+=$1; n++}
    END{
      if(n>0){
        printf "%s\t%s\t%.3f\t%d\n", s, g, sum/n, n
      }
    }' "$f" >> results/fragment_size/WGS/wgs_sample_means.tsv

done
