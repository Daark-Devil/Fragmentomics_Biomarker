# Create sample lists
awk '$3=="WGS" && $2=="healthy"{print $1}' sample_manifest.tsv > results/end_motifs/WGS_5mer/group_compare/wgs_healthy_samples.txt
awk '$3=="WGS" && $2=="cancer"{print $1}' sample_manifest.tsv > results/end_motifs/WGS_5mer/group_compare/wgs_cancer_samples.txt



# combine the four grouped
#Healthy 5′:

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
results/end_motifs/WGS_5mer/group_compare/wgs_healthy_samples.txt \
results/end_motifs/WGS_5mer/all_clean/*_5prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS_5mer/group_compare/healthy_5prime_combined.tsv


# Cancer 5′:
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
results/end_motifs/WGS_5mer/group_compare/wgs_cancer_samples.txt \
results/end_motifs/WGS_5mer/all_clean/*_5prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS_5mer/group_compare/cancer_5prime_combined.tsv



# Healthy 3′:

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
results/end_motifs/WGS_5mer/group_compare/wgs_healthy_samples.txt \
results/end_motifs/WGS_5mer/all_clean/*_3prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS_5mer/group_compare/healthy_3prime_combined.tsv



# Cancer 3′:
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
results/end_motifs/WGS_5mer/group_compare/wgs_cancer_samples.txt \
results/end_motifs/WGS_5mer/all_clean/*_3prime_counts.txt \
| sort -k2 -nr \
> results/end_motifs/WGS_5mer/group_compare/cancer_3prime_combined.tsv
