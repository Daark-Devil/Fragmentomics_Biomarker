# Healthy combine

awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_frag.txt$/,"",sample)
  if(sample in keep) print $0
}' \
manifests/edta_wgs_healthy_manifest.tsv \
results/fragment_size/EDTA_WGS/all/*_frag.txt \
> results/fragment_size/EDTA_WGS/group_compare/healthy_fragments.txt


# Cancer combine

awk 'FNR==NR{keep[$1]=1; next}
{
  sample=FILENAME
  sub(/^.*\//,"",sample)
  sub(/_frag.txt$/,"",sample)
  if(sample in keep) print $0
}' \
manifests/edta_wgs_cancer_manifest.tsv \
results/fragment_size/EDTA_WGS/all/*_frag.txt \
> results/fragment_size/EDTA_WGS/group_compare/cancer_fragments.txt



# Create binned distribution

# Healthy
awk '{bin=int($1/10)*10; count[bin]++}
END{for(b in count) print b, count[b]}' \
results/fragment_size/EDTA_WGS/group_compare/healthy_fragments.txt \
| sort -k1 -n \
> results/fragment_size/EDTA_WGS/group_compare/healthy_binned.tsv

# Cancer

awk '{bin=int($1/10)*10; count[bin]++}
END{for(b in count) print b, count[b]}' \
results/fragment_size/EDTA_WGS/group_compare/cancer_fragments.txt \
| sort -k1 -n \
> results/fragment_size/EDTA_WGS/group_compare/cancer_binned.tsv
