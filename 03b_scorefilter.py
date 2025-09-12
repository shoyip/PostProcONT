import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from Bio import SeqIO

load_dotenv()
src_folder = os.getenv("SRC_FOLDER")
data_folder = os.getenv("DATA_FOLDER")
assets_folder = os.getenv("ASSETS_FOLDER")
exp_title = os.getenv("EXP_TITLE")

for dataset in ["input", "output"]:
    assignments_filename = data_folder + "/interim/" + exp_title + f"/assignments_{dataset}.tsv"
    assignments_df = pd.read_csv(assignments_filename, sep="\t", header=None)
    assignments_df.columns = ["qseqid", "sseqid", "pident", "evalue", "bitscore"]
    
    plt.show()
    
    print("Check the histogram, close the window and choose the bitscore lower bound.")
    
    fig, ax = plt.subplots()
    ax.hist(assignments_df["bitscore"], bins=50)
    ax.set_xlabel("BLAST Bitscore")
    ax.set_ylabel("Count")
    ax.set_title("Histogram of BLAST bitscores for "+exp_title)
    
    plt.show()
    
    try:
        lower = int(input("Enter minimum bitscore: "))
    except ValueError:
        print("Invalid input. Enter integer values.")
        exit()
    
    ax.axvline(lower, color="tab:red", linestyle="--", linewidth=1.5)
    
    filtered_assignments_filename = data_folder + "/interim/" + exp_title + f"/filtered_assignments_{dataset}.tsv"
    
    filtered_assignments_df = assignments_df[assignments_df["bitscore"] >= lower]
    filtered_assignments_df[["qseqid", "sseqid"]].to_csv(filtered_assignments_filename, sep="\t", index=None)
    count = len(filtered_assignments_df)
    
    ymax = ax.get_ylim()[1]
    ax.text(1.1*lower, 0.9*ymax, "Filtered reads:\n"+str(count), color="tab:red", ha="left", va="center")
    
    plot_png = assets_folder + "/" + exp_title + "/bitscore_stats.png"
    fig.savefig(plot_png, bbox_inches="tight")
    plt.close()
    
    print(f"Filtered {count} sequences to {filtered_assignments_filename}.")
