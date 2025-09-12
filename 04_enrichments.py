import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
from dotenv import load_dotenv

load_dotenv()
data_folder = os.getenv("DATA_FOLDER")
assets_folder = os.getenv("ASSETS_FOLDER")
exp_title = os.getenv("EXP_TITLE")
ref_variant = os.getenv("REF_VARIANT")

def bsenr(input_counts, output_counts, Nb=1000, pseudocount=1):
    input_counts = np.array(input_counts)
    output_counts = np.array(output_counts)

    input_freqs = input_counts / input_counts.sum()
    output_freqs = output_counts / output_counts.sum()

    n_variants = len(input_counts)
    enrichment_means = np.zeros(n_variants)
    enrichment_stds = np.zeros(n_variants)

    boot_matrix = []

    for _ in range(Nb):
        input_boot = np.random.multinomial(input_counts.sum(), input_freqs)
        output_boot = np.random.multinomial(output_counts.sum(), output_freqs)
        enrichment_boot = np.log10((output_boot + pseudocount) / (input_boot + pseudocount))
        boot_matrix.append(enrichment_boot)

    boot_matrix = np.stack(boot_matrix)
    enrichment_means = boot_matrix.mean(axis=0)
    enrichment_stds = boot_matrix.std(axis=0, ddof=1)

    return enrichment_means, enrichment_stds

def main():
    filename_input = data_folder + "/interim/" + exp_title + "/counts_input.tsv"
    filename_output = data_folder + "/interim/" + exp_title + "/counts_output.tsv"

    df_in = pd.read_csv(filename_input, sep='\t')
    df_out = pd.read_csv(filename_output, sep='\t')

    df_in.columns, df_out.columns = ['sseqid', 'counts_in'], ['sseqid', 'counts_out']

    df = df_in.merge(df_out, on='sseqid', how='outer').fillna(0).set_index('sseqid')
    df['enrichment_means'], df['enrichment_stds'] = bsenr(df.counts_in, df.counts_out)
    df = df.sort_values(by="enrichment_means", ascending=False)

    fig = plt.figure(figsize=(20, 5))
    plt.errorbar(df.index, df.enrichment_means, df.enrichment_stds, fmt='.', label='S1A library variants')
    plt.xticks(rotation=90)
    plt.ylabel('Log10 Enrichments')
    if ref_variant != "":
        plt.axhline(df.loc[ref_variant, "enrichment_means"], color="tab:red", label=f"Reference {ref_variant}")
    plt.legend()
    fig.savefig(assets_folder + "/" + exp_title + "/enrichments.png", bbox_inches="tight")

    # df['log_enrichment'] = (df.counts_out / df.counts_in).apply(np.log)
    # df['abs_log_enrichment'] = df.log_enrichment.apply(np.abs)

    # df.sort_values('abs_log_enrichment', ascending=False).log_enrichment.to_csv(data_folder + "/processed/" + exp_name + "/enrichments.tsv", sep="\t")

if __name__ == "__main__":
    main()
