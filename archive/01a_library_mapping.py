#!/bin/python

import pandas as pd
from Bio import SeqIO

def main():
    amaury_descs, amaury_seqs = [], []
    for record in SeqIO.parse("data/raw/S1A_library_amaury.fasta", "fasta"):
        amaury_descs.append(record.description)
        amaury_seqs.append(record.seq)

    sho_descs, sho_seqs = [], []
    for record in SeqIO.parse("data/raw/S1A_library.fasta", "fasta"):
        sho_descs.append(record.description)
        sho_seqs.append(record.seq)

    df_amaury = pd.DataFrame({'descs': amaury_descs, 'seqs': amaury_seqs})
    df_sho = pd.DataFrame({'descs': sho_descs, 'seqs': sho_seqs})

    df_sho.merge(df_amaury, on='seqs', how='inner', suffixes=('_sho', '_amaury')).to_csv('data/ra\
w/desc_mapping.csv', index=None)

if __name__ == "__main__":
    main()
