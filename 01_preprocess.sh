#!/bin/bash

if [ -f data/interim/S1AvsAR_15May2025/reads.fasta ]; then
    rm data/interim/S1AvsAR_15May2025/reads.fasta
fi

touch data/interim/S1AvsAR_15May2025/reads.fasta

for file in data/raw/S1AvsAR_15May2025/*; do
    zcat $file | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' >> data/interim/S1AvsAR_15May2025/reads.fasta
done
