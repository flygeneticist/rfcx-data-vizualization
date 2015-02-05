import sys
import os
import datetime

out_file = '/home/kak9699/Documents/code/RFCx/rfcx-data-vizualization/alert_mod_times.txt'
base_path = '/media/2GB/'
event_files = ["1422006590326.m4a",
"1422007672668.m4a",
"1422008394211.m4a",
"1422010198247.m4a",
"1422012363033.m4a",
"1422012723811.m4a",
"1422013084563.m4a",
"1422013445350.m4a",
"1422013806137.m4a",
"1422014166899.m4a",
"1422023186129.m4a",
"1422027154676.m4a",
"1422027515501.m4a",
"1422030401858.m4a",
"1422033648917.m4a",
"1422034731267.m4a",
"1422036174437.m4a",
"1422039061212.m4a",
"1422039061212.m4a",
"1422045555256.m4a",
"1422061791092.m4a",
"1422062151916.m4a",
"1422065399030.m4a",
"1422065759897.m4a",
"1422067564442.m4a",
"1422067925519.m4a",
"1422070813646.m4a",
"1422070813646.m4a"]

with open(out_file, 'w') as f:
    for snd in event_files:
        try:
            date_modified = datetime.datetime.fromtimestamp(os.stat(base_path+snd).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            f.write(snd + '\t' + date_modified + '\n')
        except:
            f.write(snd + ' ERROR!\n')
