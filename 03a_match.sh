#!/bin/bash

source .env

DEST_FOLDER=$DATA_FOLDER/interim/$EXP_TITLE/
DB_FILE=$DATA_FOLDER/raw/library_db

for dataset in input output; do
    blastn -query $DATA_FOLDER/interim/$EXP_TITLE/$dataset\.fasta -db $DB_FILE -out $DEST_FOLDER/assignments_$dataset.tsv -outfmt "6 qseqid sseqid pident evalue bitscore"
done
