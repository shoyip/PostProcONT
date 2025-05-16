#!/bin/bash

./minimap2/minimap2 -ax map-ont -k8 -w2 -A1 -B1 -O2,16 -E1,0 -z 100,50 --score-N 0 -N 10 --secondary=no data/raw/S1A_library.fasta data/interim/S1AvsAR_15May2025/input.fasta > data/interim/S1AvsAR_15May2025/input_matches.sam
./minimap2/minimap2 -ax map-ont -k8 -w2 -A1 -B1 -O2,16 -E1,0 -z 100,50 --score-N 0 -N 10 --secondary=no data/raw/S1A_library.fasta data/interim/S1AvsAR_15May2025/output.fasta > data/interim/S1AvsAR_15May2025/output_matches.sam

cat data/interim/S1AvsAR_15May2025/input_matches.sam | grep -v '^@' | cut -f3 | sort | uniq -c | sort -nr  | awk '$2 != "*" {print $2 "\t" $1}' > data/interim/S1AvsAR_15May2025/input_counts.txt
cat data/interim/S1AvsAR_15May2025/output_matches.sam | grep -v '^@' | cut -f3 | sort | uniq -c | sort -nr | awk '$2 != "*" {print $2 "\t" $1}' > data/interim/S1AvsAR_15May2025/output_counts.txt
