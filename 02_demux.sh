#!/bin/bash

python minibar/minibar.py -p 0.5 -T -F -P demuxed_ data/raw/indexes.txt data/interim/S1AvsAR_15May2025/reads.fasta

echo "Number of input matches:"
cat demuxed_in.fasta | grep "^>" | wc -l

echo "Number of output matches:"
cat demuxed_out.fasta | grep "^>" | wc -l

echo "Number of multiple matches:"
cat demuxed_Multiple_Matches.fasta | grep "^>" | wc -l

echo "Number of unknown sequences:"
cat demuxed_unk.fasta | grep "^>" | wc -l

mv demuxed_in.fasta data/interim/S1AvsAR_15May2025/input.fasta
mv demuxed_out.fasta data/interim/S1AvsAR_15May2025/output.fasta

rm demuxed_unk.fasta demuxed_Multiple_Matches.fasta
