cat results/end_motifs/WGS/all_clean/*_5prime_counts.txt \
| awk '{count[$2]+=$1} END{for(m in count) print m, count[m]}' \
| sort -k2 -nr \
> results/end_motifs/WGS/combined_5prime_motifs.tsv

# healthy 5′
awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_5prime_counts\.txt$/,"",sample)
  if(sample in keep) count[$2]+=$1
}
END{
  for(m in count) print m, count[m]
}' \
results/end_motifs/WGS/group_compare/wgs_healthy_samples.txt \
results/end_motifs/WGS/all_clean/*_5prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS/group_compare/healthy_5prime_combined.tsv

#healthy 3′

awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_3prime_counts\.txt$/,"",sample)
  if(sample in keep) count[$2]+=$1
}
END{
  for(m in count) print m, count[m]
}' \
results/end_motifs/WGS/group_compare/wgs_healthy_samples.txt \
results/end_motifs/WGS/all_clean/*_3prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS/group_compare/healthy_3prime_combined.tsv


cat results/end_motifs/WGS/all_clean/*_3prime_counts.txt \
| awk '{count[$2]+=$1} END{for(m in count) print m, count[m]}' \
| sort -k2 -nr \
> results/end_motifs/WGS/combined_3prime_motifs.tsv

#cancer 5′
awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_5prime_counts\.txt$/,"",sample)
  if(sample in keep) count[$2]+=$1
}
END{
  for(m in count) print m, count[m]
}' \
results/end_motifs/WGS/group_compare/wgs_cancer_samples.txt \
results/end_motifs/WGS/all_clean/*_5prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS/group_compare/cancer_5prime_combined.tsv


# cancer 3′
awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_3prime_counts\.txt$/,"",sample)
  if(sample in keep) count[$2]+=$1
}
END{
  for(m in count) print m, count[m]
}' \
results/end_motifs/WGS/group_compare/wgs_cancer_samples.txt \
results/end_motifs/WGS/all_clean/*_3prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS/group_compare/cancer_3prime_combined.tsv
