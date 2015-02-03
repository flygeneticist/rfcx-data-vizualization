#### Load packages and data into Python for manipluation
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# placeholder JSON data for dev work
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

# Load the JSON data into a Pandas DataFrame
data = json.loads(json_obj)
df = pd.io.json.json_normalize(data)
# Ensure column types are cast correctly
df['alert_datetime'] = pd.to_datetime(df['alert_datetime'])
df['guid'] = df['guid'].astype(str)


#### Create weekday/hours/day-night data and labels
weekday_map= {1:'MON', 2:'TUE', 3:'WED', 4:'THU',
              5:'FRI', 6:'SAT', 7:'SUN'}

# re-defines the weekday label
# def weekday_label(x, wkdays=weekdays):
#     return wkdays[x-1]

df['weekday'] = df['alert_datetime'].map(lambda x: x.isocalendar()[2])


step = 2 # hours to group by
hours = range(0,24,step) # complete range of hour time-slots

# defines the grouping of hours
def group_hours(y, hours=hours, step=step):
    for h in hours:
        if (y >= h and y < h+2):
            return h

df['hour'] = df['alert_datetime'].map(lambda y: group_hours(y.hour))


# defines day vs night hours (night = 18:00-05:00)
def day_night(z):
    if (z < 5 or z > 18):
        return 'night'
    else:
        return 'day'

df['day_night'] = df['hour'].map(lambda z: day_night(z))


# Quick reference to unique lists of various columns
types = sorted(list(set(df['sound_type'])))
# types2 = str(unique(df['sound_type']))
guids = sorted(list(set(df['guid'])))
dates = sorted(list(set(df['alert_datetime'])))
wd = range(1,8)

#### Create pivot tables of data
# create pivot tables of data for plotting
tot_guid = dict(df.groupby('guid')['alert_datetime'].count())
# data sorted by guid name
guid_pivot = df.pivot_table(index=['guid'], columns=['sound_type'],
                            values=['alert_datetime'], aggfunc='count').fillna(0)
guid_pivot

# data sorted by hour of day
tot_hr = dict(df.groupby('hour')['alert_datetime'].count())
hr_pivot = df.pivot_table(  index=['hour'], columns=['sound_type'],
                            values=['alert_datetime'], aggfunc='count').fillna(0)
hr_pivot

# data sorted by day of week
tot_day = dict(df.groupby('weekday')['alert_datetime'].count())
day_pivot = df.pivot_table(   index=['weekday'], columns=['sound_type'],
                              values=['alert_datetime'], aggfunc='count').fillna(0)
day_pivot

# data sorted by high level, day  vs night
tot_nightDay = dict(df.groupby('day_night')['alert_datetime'].count())
nightDay_pivot = df.pivot_table(index=['day_night'], values=['alert_datetime'], aggfunc='count').fillna(0)
nightDay_pivot


#### Plot the data into figures
# Create a colormap from the "Tableau Color Blind 10" color scheme.
palette = [ (0,107,164),(255,128,14),(171,171,171),(89,89,89),(95,158,209),
            (200,82,0),(137,137,137),(162,200,236),(255,188,121),(207,207,207)]
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(palette)):
    r, g, b = palette[i]
    palette[i] = (r / 255., g / 255., b / 255.)


#### Graph 1: Alerts By Guardian ID
# Create a figure of given size. Common sizes: (10, 7.5) and (12, 9)
fig = plt.figure(figsize=(10, 7.5))
# Add a subplot
ax = fig.add_subplot(111)
# set transparency
a = 0.7
ax = guid_pivot.plot(kind='barh', stacked=True, color=palette, legend=True, ax=ax, alpha=a,
                      edgecolor='w', xlim=(0,max(tot_guid.values())))
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
ax.set_title("", fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))
# Setup the legend labels properly
patches, labels = ax.get_legend_handles_labels()
# clean up auto-set labels from pivot tables
labels = [e[1] for e in [str(l).replace("(","").replace(")","").split(", ") for l in labels]]
ax.legend(patches, labels, loc='best')
# Set x axis label, set label text
xlab = 'Incidents Detected'
ax.set_xlabel(xlab, fontsize=16, alpha=a, ha='center')
# Set y axis label, set label text
ylab = 'Guardian Name'
ax.set_ylabel(ylab, fontsize=16, alpha=a, ha='center')
# Save figure as png
plt.savefig('./figures/alerts_by_guid.png', dpi=300)


#### Graph 2: Alerts By Hour
# Create a figure of given size. Common sizes: (10, 7.5) and (12, 9)
fig = plt.figure(figsize=(10, 7.5))
# Add a subplot
ax = fig.add_subplot(111)
# set transparency
a = 0.7
ax = hr_pivot.plot(kind='bar', stacked=True, color=palette, legend=True, ax=ax, alpha=a,
                    edgecolor='w', ylim=(0,max(tot_hr.values())))
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
ax.set_title("", fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))
# Setup the legend labels properly
patches, labels = ax.get_legend_handles_labels()
# clean up auto-set labels from pivot tables
labels = [e[1] for e in [str(l).replace("(","").replace(")","").split(", ") for l in labels]]
ax.legend(patches, labels, loc='best')
# Set y axis label, set label text
ylab = 'Incidents Detected'
ax.set_ylabel(ylab, fontsize=16, alpha=a, ha='center')
# Set x axis label, set label text
xlab = 'Time of Day (2 hours)'
ax.set_xlabel(xlab, fontsize=16, alpha=a, ha='center')
# Save figure as png
plt.savefig('figures/alerts_by_hour.png', dpi=300)


#### Graph 3: Alerts By Weekday
# Create a figure of given size. Common sizes: (10, 7.5) and (12, 9)
fig = plt.figure(figsize=(10, 7.5))
# Add a subplot
ax = fig.add_subplot(111)
# set transparency
a = 0.7
ax = day_pivot.plot(kind='barh', stacked=True, color=palette, legend=True, ax=ax, alpha=a,
                      edgecolor='w', xlim=(0,max(tot_day.values())))
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
ax.set_title("", fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))
# Setup the legend labels properly
patches, labels = ax.get_legend_handles_labels()
# clean up auto-set labels from pivot tables
labels = [e[1] for e in [str(l).replace("(","").replace(")","").split(", ") for l in labels]]
ax.legend(patches, labels, loc='best')
# Set x axis label, set label text
xlab = 'Incidents Detected'
ax.set_xlabel(xlab, fontsize=16, alpha=a, ha='center')
# Set y axis label, set label text
ylab = 'Day of Week'
ax.set_ylabel(ylab, fontsize=16, alpha=a, ha='center')
ys = sorted(ax.get_yticks())
ax.set_yticks(ys)
ax.set_yticks([], minor=True)
ax.set_yticklabels([weekday_map[d] for d in wd])
# Save figure as png
plt.savefig('figures/alerts_by_weekday.png', dpi=300)


#### Graph 4: Alerts by Night vs. Day
# Create a figure of given size. Common sizes: (10, 7.5) and (12, 9)
fig = plt.figure(figsize=(10, 7.5))
# Add a subplot
ax = fig.add_subplot(111)
# set transparency
a = 0.7
ax = nightDay_pivot.plot(kind='barh', stacked=False, color=palette, legend=False, ax=ax, alpha=a,
                      edgecolor='w', xlim=(0,max(tot_nightDay.values())))
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
ax.set_title("", fontsize=26, alpha=a, ha='left')
plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))
# Set x axis label, set label text
xlab = 'Incidents Detected'
ax.set_xlabel(xlab, fontsize=16, alpha=a, ha='center')
# Set y axis label, set label text
ylab = 'Night vs Day'
ax.set_ylabel(ylab, fontsize=16, alpha=a, ha='center')
# Save figure as png
plt.savefig('./figures/alerts_by_nightDay.png', dpi=300)
