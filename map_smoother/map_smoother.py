#!/usr/bin/env python

import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

mpl.use("GTK3Agg")

def process_map(mapfile):
    with open(mapfile, 'rb') as f:
        data = f.read()
    start = 1024 + 4096*4*1000
    row = []
    for i in range(0,4096):
        part = data[start+i*4 : start+4+(i*4)]
        tile = int.from_bytes(part[0:2], signed=True)
        height = int.from_bytes(part[2:4], signed=True)
        row.append(height)
        #print(i, part, part[3], tile, height, tile.to_bytes(2, 'big', signed=True) +  height.to_bytes(2, 'big', signed=True))
    return row

if __name__ == "__main__":
    mapfile1 = sys.argv[1]
    mapfile2 = sys.argv[2]
    row1 = np.array(process_map(mapfile1))
    row2 = np.array(process_map(mapfile2))
    slope1 = [row1[i]-row1[i+1] for i in range(0,len(row1)-1)]
    slope1hat = savgol_filter(slope1, 20, 3)
    slope2 = [row2[i]-row2[i+1] for i in range(0,len(row2)-1)]
    slope2hat = savgol_filter(slope2, 20, 3)
    #plt.plot(row1, linewidth=1)
    #plt.plot(row2, linewidth=1)
    #plt.plot(row2 - row1, lw=1)
    #plt.plot(slope1, lw=1)
    #plt.plot(slope2, lw=1)
    #plt.plot(np.rint(slope1hat), lw=1)
    #plt.plot(np.rint(slope2hat), lw=1)
    plt.plot(slope1-slope1hat, lw=1)
    plt.plot(slope2-slope2hat, lw=1)
    plt.show()
