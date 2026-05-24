



# exact fragment length counts
awk '{print $1}' results/fragment_size/all_fragments_combined.txt | sort -n | uniq -c > results/fragment_size/fragment_distribution.txt

#10-bp bins
awk '{bin=int($1/10)*10; count[bin]++} END{for (b in count) print b, count[b]}' results/fragment_size/WGS/all/*_frag.txt | sort -n > results/fragment_size/fragment_distribution_binned.tsv

# Samparating 2 samples types

# Healthy
awk '$3=="WGS" && $2=="healthy"{print $1}' sample_manifest.tsv > results/fragment_size/WGS/group_compare/wgs_healthy_samples.txt

awk '{print "results/fragment_size/WGS/all/"$1"_frag.txt"}' \ 
results/fragment_size/WGS/group_compare/wgs_healthy_samples.txt \#Cancer awk '$3=="WGS" && $2=="cancer"{print $1}' 
sample_manifest.tsv > results/fragment_size/WGS/group_compare/wgs_cancer_samples.txt
> results/fragment_size/WGS/group_compare/healthy_files.txt

# Healthy Binned distribution 

bsub -q general \
-a 'docker(ubuntu:22.04)' \
-o logs/healthy_dist.out \
-e logs/healthy_dist.err \
"cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics && \
awk '
{
  bin=int(\$1/10)*10
  count[bin]++
}
END {
  for(b in count) print b, count[b]
}
' results/fragment_size/WGS/all/*_frag.txt \
| sort -n \	
> results/fragment_size/WGS/group_compare/healthy_fragment_distribution_binned.tsv"

#  Cancer Binned distribution
bsub -q general \
-a 'docker(ubuntu:22.04)' \
-o logs/cancer_dist.out \
-e logs/cancer_dist.err \
"cd /storage1/fs1/christophermaher/Active/maherlab/devansh/fragmentomics && xargs cat < results/fragment_size/WGS/group_compare/cancer_files.txt | awk '{bin=int(\$1/10)*10; count[bin]++} END{for(b in count) print b, count[b]}' | sort -n > results/fragment_size/WGS/group_compare/cancer_fragment_distribution_binned.tsv"

awk '{print "results/fragment_size/WGS/all/"$1"_frag.txt"}' \ results/fragment_size/WGS/group_compare/wgs_cancer_samples.txt 
\
> results/fragment_size/WGS/group_compare/cancer_files.txt



sort -k2 -nr results/fragment_size/WGS/group_compare/healthy_fragment_distribution_binned.tsv | head -10
sort -k2 -nr results/fragment_size/WGS/group_compare/cancer_fragment_distribution_binned.tsv | head -10
