import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt

# Read the data into a Pandas DataFrame.
results = pd.read_csv('/home/kak9699/Documents/code/RFCx/rfcx-data-viz/data/SFID_guardian_arrays.csv')
data = pd.DataFrame(results).groupby('guid')

# These are the "Tableau Color Blind 10" colors as RGB.
palette = [ (0,107,164),(255,128,14),(171,171,171),(89,89,89),(95,158,209),
            (200,82,0),(137,137,137),(162,200,236),(255,188,121),(207,207,207)]

# Scale RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(palette)):
    r, g, b = palette[i]
    palette[i] = (r / 255., g / 255., b / 255.)

# Common sizes: (10, 7.5) and (12, 9)
plt.figure(figsize=(10, 7.5))

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
plt.ylim(0, max(data.count())+1)
plt.xlim(0, 24)

# Make sure your axis ticks are large enough to be easily read.
plt.yticks(range(0, max(data.count()), 2), fontsize=14)
plt.xticks(fontsize=14)

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# If title is descriptive enough, it is unnecessary to include axis labels.
plt.title("Alerts per week by guardian", fontsize=17, ha="center")

# Include data source(s), copyright notice, etc
plt.text(0, -0.25, "Author: Rainforest Connection (rfcx.org / contact@rfcx.org)"
       "\nNote: .....", fontsize=10)

# Save the figure as a PNG, PDF, JPEG, etc.
plt.savefig("line_chart.png", bbox_inches="tight");
