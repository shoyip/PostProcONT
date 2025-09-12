import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from Bio import SeqIO

load_dotenv()
src_folder = os.getenv("SRC_FOLDER")
data_folder = os.getenv("DATA_FOLDER")
assets_folder = os.getenv("ASSETS_FOLDER")
exp_title = os.getenv("EXP_TITLE")

reads_filename = data_folder + "/interim/" + exp_title + "/reads.fasta"
reads_lengths = []

for rec in SeqIO.parse(reads_filename, "fasta"):
    reads_lengths.append(len(rec.seq))

print("Check the histogram, close the window and choose the range of read lenghts to be filtered.")

fig, ax = plt.subplots()
ax.hist(reads_lengths, bins=50)
ax.set_xlabel("Read length")
ax.set_ylabel("Count")
ax.set_title("Histogram of read lengths for "+exp_title)

plt.show()

try:
    lower = int(input("Enter minimum sequence length: "))
    upper = int(input("Enter maximum sequence length: "))
except ValueError:
    print("Invalid input. Enter integer values.")
    exit()

ax.axvline(lower, color="tab:red", linestyle="--", linewidth=1.5)
ax.axvline(upper, color="tab:red", linestyle="--", linewidth=1.5)

filtered_reads_filename = data_folder + "/interim/" + exp_title + "/filtered_reads.fasta"
with open(filtered_reads_filename, "w") as outf:
    count = SeqIO.write(
            (rec for rec in SeqIO.parse(reads_filename, "fasta") if lower <= len(rec.seq) <= upper),
            outf,
            "fasta"
            )

ymax = ax.get_ylim()[1]
ax.text(1.1*lower, 0.9*ymax, "Filtered reads:\n"+str(count), color="tab:red", ha="left", va="center")

plot_png = assets_folder + "/" + exp_title + "/reads_stats.png"
fig.savefig(plot_png, bbox_inches="tight")
plt.close()

print(f"Filtered {count} sequences to {filtered_reads_filename}.")
