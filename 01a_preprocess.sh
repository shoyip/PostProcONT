#!/bin/bash

source .env

mkdir -p $DATA_FOLDER/{raw,interim,processed}/$EXP_TITLE
mkdir -p $ASSETS_FOLDER/$EXP_TITLE

if [ -f $DATA_FOLDER/interim/$EXP_TITLE/reads.fasta ]; then
    rm $DATA_FOLDER/interim/$EXP_TITLE/reads.fasta
fi

touch $DATA_FOLDER/interim/$EXP_TITLE/reads.fasta

for file in "$SRC_FOLDER"/*.gz; do
    zcat "$file" | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' >> $DATA_FOLDER/interim/$EXP_TITLE/reads.fasta
done
