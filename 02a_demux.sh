#!/bin/bash

source .env
STATS_FILE=$DATA_FOLDER/interim/$EXP_TITLE/demux_stats.txt
if [ -f $STATS_FILE ]; then
    rm $STATS_FILE
fi 
touch $STATS_FILE

python minibar/minibar.py -p $DEMUX_THR -T -F -P demuxed_ $DATA_FOLDER/raw/indexes.txt $DATA_FOLDER/interim/$EXP_TITLE/filtered_reads.fasta

echo "Number of input matches:"
cat demuxed_in.fasta | grep "^>" | wc -l | tee -a $STATS_FILE

echo "Number of output matches:"
cat demuxed_out.fasta | grep "^>" | wc -l | tee -a $STATS_FILE

echo "Number of multiple matches:"
cat demuxed_Multiple_Matches.fasta | grep "^>" | wc -l | tee -a $STATS_FILE

echo "Number of unknown sequences:"
cat demuxed_unk.fasta | grep "^>" | wc -l | tee -a $STATS_FILE

mv demuxed_in.fasta $DATA_FOLDER/interim/$EXP_TITLE/input.fasta
mv demuxed_out.fasta $DATA_FOLDER/interim/$EXP_TITLE/output.fasta

rm demuxed_unk.fasta demuxed_Multiple_Matches.fasta
