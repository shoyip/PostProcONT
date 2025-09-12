import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    filename_in =  "data/interim/S1AvsAAPF_20June2025/input_counts.txt"
    filename_out = "data/interim/S1AvsAAPF_20June2025/output_counts.txt"

    df_in = pd.read_csv(filename_in, sep='\t', header=None)
    df_out = pd.read_csv(filename_out, sep='\t', header=None)

    df_in.columns, df_out.columns = ['id', 'counts_in'], ['id', 'counts_out']

    df_in = df_in.set_index('id')
    df_out = df_out.set_index('id')

    df_in = df_in / df_in.sum()
    df_out = df_out / df_out.sum()

    df = df_in.join(df_out, on='id')

    df['log_enrichment'] = (df.counts_out / df.counts_in).apply(np.log)
    df['abs_log_enrichment'] = df.log_enrichment.apply(np.abs)

    #hist2d(df.counts_in, df.counts_out)

    df.sort_values('abs_log_enrichment', ascending=False).log_enrichment.to_csv('data/processed/S1AvsAAPF_20June2025/log_enrichment.csv')

    #plt.figure()
    #plt.hist(df.log_enrichment)
    #plt.ylabel('Count')
    #plt.xlabel('Log Enrichment')
    #plt.show()

def hist2d(x, y):
    # Bin edges
    xbins = np.linspace(0, 1, 100)
    ybins = np.linspace(0, 1, 100)
    
    # 2D histogram
    counts, xedges, yedges = np.histogram2d(x, y, bins=[xbins, ybins])
    
    # Plot the histogram
    plt.figure(figsize=(8, 6))
    plt.imshow(counts.T, origin='lower', extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
               cmap='Blues', aspect='auto')
    
    # Overlay scatter points for bins with low counts
    threshold = 2
    xcenters = 0.5 * (xedges[1:] + xedges[:-1])
    ycenters = 0.5 * (yedges[1:] + yedges[:-1])
    
    # Find low-count bins and plot as points
    for i in range(len(xcenters)):
        for j in range(len(ycenters)):
            if counts[i, j] < threshold and counts[i, j] > 0:
                for _ in range(int(counts[i, j])):
                    plt.plot(xcenters[i], ycenters[j], 'ro', markersize=4)
    
    plt.xlabel('in freq')
    plt.ylabel('out freq')
    plt.title('2D Histogram')
    plt.colorbar(label='Count')
    plt.show()

if __name__ == "__main__":
    main()
