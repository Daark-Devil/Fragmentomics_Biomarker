#!/bin/bash

# Alignment
bwa mem -t 2 \
/storage1/fs1/christophermaher/Active/maherlab/lil1/annot/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
data/WGS_ca/seq015743_IV_wgs_R1.fastq.gz \
data/WGS_ca/seq015743_IV_wgs_R2.fastq.gz \
> alignments/test/seq015743_IV_wgs.sam
