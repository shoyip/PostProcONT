#!/bin/bash

mkdir -p data/interim/S1AvsAAPF_20June2025

if [ -f data/interim/S1AvsAAPF_20June2025/reads.fasta ]; then
    rm data/interim/S1AvsAAPF_20June2025/reads.fasta
fi

touch data/interim/S1AvsAAPF_20June2025/reads.fasta

for file in /run/media/shoichi/EMTEC\ C410/S1AvsAAPF/*; do
    zcat "$file" | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' >> data/interim/S1AvsAAPF_20June2025/reads.fasta
done
