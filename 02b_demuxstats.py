import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
data_folder = os.getenv("DATA_FOLDER")
assets_folder = os.getenv("ASSETS_FOLDER")
exp_title = os.getenv("EXP_TITLE")

with open(data_folder + "/interim/" + exp_title + "/demux_stats.txt") as f:
    values = [int(line.strip()) for line in f if line.strip()]

labels = ["Input", "Output", "Multiple", "Unknown"]
labels_values = [l+": "+str(v) for l, v in zip(labels, values)]

fig = plt.figure()
plt.pie(values, labels=labels_values, startangle=90)
plt.title(f"Proportions of demultiplexed reads for {exp_title}")
plt.show()
plot_png = assets_folder + "/" + exp_title + "/demux_stats.png"
fig.savefig(plot_png, bbox_inches="tight")
plt.close()
