#!/bin/bash

INPUT_FASTQ=$1
OUTPUT_FILE=$2

zcat $INPUT_FASTQ | awk 'NR%4==2 {print substr($0,1,4)}' > ${OUTPUT_FILE}_5prime.txt

zcat $INPUT_FASTQ | awk 'NR%4==2 {print substr($0,length($0)-3,4)}' > ${OUTPUT_FILE}_3prime.txt
