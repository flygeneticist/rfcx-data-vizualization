import sys
import os
import datetime

out_file = '/home/kak9699/Documents/code/RFCx/rfcx-data-vizualization/alert_mod_times.txt'
base_path = '/media/2GB/'
event_files = [1422006590326,1422007672668,1422008394211,1422010198247,
1422012363033,1422012723811,1422013084563,1422013445350,1422013806137,
1422014166899,1422023186129,1422027154676,1422027515501,1422030401858,
1422033648917,1422034731267,1422036174437,1422039061212,1422039061212,
1422045555256,1422061791092,1422062151916,1422065399030,1422065759897,
    1422067564442,1422067925519,1422070813646,1422070813646]
dates = [
Fri Jan 23 2015 10:49:50
Fri Jan 23 2015 11:07:52
Fri Jan 23 2015 11:19:54
Fri Jan 23 2015 11:49:58

]
with open(out_file, 'w') as f:
    for snd in event_files:
        try:
            date_modified = datetime.datetime.fromtimestamp(snd[:-4]).strftime('%Y-%m-%d %H:%M:%S')
            f.write(snd + '\t' + date_modified + '\n')
        except:
            f.write(snd + ' ERROR!\n')
