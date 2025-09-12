#!/bin/bash
source .env
cd $DATA_FOLDER/raw/ && \
    makeblastdb -in $LIBRARY_FILE -dbtype nucl -out library_db
