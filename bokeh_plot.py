import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# script parameters for tweaking graph looks
guid_pivot_xmax = 25 # x-axis limit for guid graph

json_obj = """
[
{"alert_datetime":"01/30/2015 09:00:00", "guid":"A", "sound_type":"truck"},
{"alert_datetime":"01/26/2015 05:00:00", "guid":"A", "sound_type":"truck"},
{"alert_datetime":"01/31/2015 11:00:00", "guid":"A", "sound_type":"truck"},
{"alert_datetime":"01/25/2015 17:00:00", "guid":"A", "sound_type":"motorcycle"},
{"alert_datetime":"01/27/2015 08:00:00", "guid":"A", "sound_type":"truck"},
{"alert_datetime":"01/25/2015 13:10:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/26/2015 22:00:00", "guid":"B", "sound_type":"motorcycle"},
{"alert_datetime":"01/29/2015 16:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/31/2015 12:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/26/2015 15:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/26/2015 18:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/29/2015 12:00:00", "guid":"B", "sound_type":"motorcycle"},
{"alert_datetime":"01/28/2015 14:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/25/2015 13:00:00", "guid":"B", "sound_type":"truck"},
{"alert_datetime":"01/29/2015 08:00:00", "guid":"C", "sound_type":"motorcycle"},
{"alert_datetime":"01/27/2015 20:00:00", "guid":"C", "sound_type":"truck"},
{"alert_datetime":"01/28/2015 19:00:00", "guid":"C", "sound_type":"truck"},
{"alert_datetime":"01/31/2015 06:00:00", "guid":"C", "sound_type":"truck"},
{"alert_datetime":"01/27/2015 21:00:00", "guid":"C", "sound_type":"truck"}
]
"""

data = json.loads(json_obj)
df = pd.io.json.json_normalize(data)
df['alert_datetime'] = pd.to_datetime(df['alert_datetime'])
df['guid'] = df['guid'].astype(str)

# Create weekday/hours data and labels from alert timestamp
weekdays = 'Mon Tue Wed Thu Fri Sat Sun'.split()
hours = range(0,24,2)
df['week'] = df['alert_datetime'].map(lambda x: x.isocalendar()[1])
df['hour'] = df['alert_datetime'].map(lambda y: y.hour)

# quick reference to unique lists of various columns
types = sorted(list(set(df['sound_type'])))
guids = sorted(list(set(df['guid'])))
dates = sorted(list(set(df['alert_datetime'])))

# map the alerts categories to an int value
# for t in types:
#     df[t] = df['sound_type'].map(lambda x: {t:1}.get(x, 0))

# # setup the grouping date range for a week's worth of data
# start_date = '01/25/2015'
# end_date = '01/31/2015'
# hours = pd.date_range(start_date, end_date+" 23:59:59", freq='2H')

# create pivot tables of data for plotting
guid_pivot = df.pivot_table(   index=['guid'], columns=['sound_type'],
                                    values=['alert_datetime'], aggfunc='count').fillna(0)

hr_pivot = df.pivot_table(  index=['hour'], columns=['sound_type'],
                            values=['alert_datetime'], aggfunc='count').fillna(0)


# Plot the data into figures
# Create a colormap from the "Tableau Color Blind 10" color scheme.
palette = [ (0,107,164),(255,128,14),(171,171,171),(89,89,89),(95,158,209),
            (200,82,0),(137,137,137),(162,200,236),(255,188,121),(207,207,207)]
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(palette)):
    r, g, b = palette[i]
    palette[i] = (r / 255., g / 255., b / 255.)

# Create a figure of given size. Common sizes: (10, 7.5) and (12, 9)
fig = plt.figure(figsize=(10, 7.5))
# Add a subplot
ax = fig.add_subplot(111)
# Set title
ttl = 'You RFCx Alerts For This Week'
# Set color transparency (0: transparent; 1: solid)
a = 0.7

ax = guid_pivot.plot(kind='barh', stacked=True, color=palette, legend=True, ax=ax, alpha=a,
                      edgecolor='w', xlim=(0,guid_pivot_xmax), title=ttl)
# Remove the plot frame lines
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
# Remove grid lines (dotted lines inside plot)
ax.grid(False)
# Remove plot frame
ax.set_frame_on(False)
# Pandas trick: remove weird dotted line on axis
ax.lines[0].set_visible(False)

# Customize title, set position, allow space on top of plot for title
ax.set_title(ax.get_title(), fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))

# Set x axis label on top of plot, set label text
ax.xaxis.set_label_position('top')
xlab = 'Population (in millions)'
ax.set_xlabel(xlab, fontsize=20, alpha=a, ha='left')
ax.xaxis.set_label_coords(0, 1.04)

# Position x tick labels on top
ax.xaxis.tick_top()
# Remove tick lines in x and y axes
ax.yaxis.set_ticks_position('none')
ax.xaxis.set_ticks_position('none')

# Customize x tick lables
xticks = [5,10,20,50,80]
ax.xaxis.set_ticks(xticks)
ax.set_xticklabels(xticks, fontsize=16, alpha=a)

# Customize y tick labels
yticks = [item.get_text() for item in ax.get_yticklabels()]
ax.set_yticklabels(yticks, fontsize=16, alpha=a)
ax.yaxis.set_tick_params(pad=12)

plt.show()




# ax1 = hr_pivot.plot(kind='bar', stacked=True, color=palette, legend=True)
# plt.show()

# # Remove the plot frame lines
# ax = plt.subplot(111)
# ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
# ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
# # Ensure that the axis ticks only show up on the bottom and left of the plot.
# ax.get_xaxis().tick_bottom()
# ax.get_yaxis().tick_left()

# plt.ylabel('Guardian', fontsize=16)
# plt.xlabel('Alerts', fontsize=16)
# plt.savefig("/home/kak9699/Documents/code/figures/alerts_by_guid.png", bbox_inches="tight");

