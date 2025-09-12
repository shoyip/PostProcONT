#!/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ar_logenr = pd.read_csv("data/processed/S1AvsAR_15May2025/log_enrichments.csv")
    aapf_enr = pd.read_csv("data/processed/S1AvsAR_15May2025/AAPF_enrichments.csv")
    mapping = pd.read_csv("data/raw/desc_mapping.csv")

    aapf_enr = aapf_enr.merge(mapping, left_on="mutant", right_on="descs_amaury")[['descs_sho', 'count_init', 'count_sort']]
    aapf_enr['log_enrichment'] = (aapf_enr.count_sort / aapf_enr.count_init).apply(np.log)

    df = ar_logenr.merge(aapf_enr, left_on='id', right_on='descs_sho', suffixes=('_ar', '_aapf'))

    print('AAPF specific variants')
    print(df.query("log_enrichment_ar < 0 & log_enrichment_aapf > 0"))

    print('AR specific variants')
    print(df.query("log_enrichment_ar > 0 & log_enrichment_aapf < 0"))

    print('AAPF and AR specific variants')
    print(df.query("log_enrichment_ar > 0 & log_enrichment_aapf > 0"))

    plt.figure()
    plt.scatter(df.log_enrichment_ar, df.log_enrichment_aapf, s=3, label='Library sequence')
    plt.axvline(0.537688, c='tab:orange', label='Trypsin reference enrichment')
    plt.axhline(-0.09531, c='tab:green', label='Chymotrypsin reference enrichment')
    plt.xlabel('Enrichment wrt AR substrate')
    plt.ylabel('Enrichment wrt AAPF substrate')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
