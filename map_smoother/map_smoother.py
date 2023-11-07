#!/usr/bin/env python

import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

mpl.use("GTK3Agg")

def process_map(mapfile):
    mapsize = 4096
    maxbytes = mapsize*mapsize
    with open(mapfile, 'rb') as f:
        data = f.read()
    start = 1024
    row = []
    mapdata = np.ndarray(shape=(mapsize, mapsize), dtype=int)
    tiledata = np.ndarray(shape=(mapsize, mapsize), dtype=int)
    print("Created empty mapdata")
    for i in range(0,mapsize*mapsize):
        x = i % mapsize
        y = int(i / mapsize)
        part = data[start+i*4 : start+4+(i*4)]
        tile = int.from_bytes(part[0:2], signed=True)
        height = int.from_bytes(part[2:4], signed=True)
        tiledata[x,y] = tile
        mapdata[x,y] = height
        #mapdata[
        #row.append(height)
        #print(i, part, part[3], tile, height, tile.to_bytes(2, 'big', signed=True) +  height.to_bytes(2, 'big', signed=True))
    return mapdata, tiledata

def write_map(mapdata):
    pass

def smooth_and_plot_row(row):
    row_smooth = savgol_filter(row, 20, 3)
    plt.plot(row_smooth, lw=1)
    return row_smooth
    

if __name__ == "__main__":
    mapfile1 = sys.argv[1]
    mapfile2 = sys.argv[2]
    mapdata1, tiledata1 = np.array(process_map(mapfile1))
    mapdata2, tiledata2 = np.array(process_map(mapfile2))
    #plt.plot(row1, linewidth=1)
    #plt.plot(row2, linewidth=1)
    #smooth_and_plot_row(row1)
    #smooth_and_plot_row(row2)
    #slope1 = [row1[i]-row1[i+1] for i in range(0,len(row1)-1)]
    #slope1hat = savgol_filter(slope1, 20, 3)
    #slope2 = [row2[i]-row2[i+1] for i in range(0,len(row2)-1)]
    #slope2hat = savgol_filter(slope2, 20, 3)
    #plt.plot(row2 - row1, lw=1)
    #plt.plot(slope1, lw=1)
    #plt.plot(slope2, lw=1)
    #plt.plot(np.rint(slope1hat), lw=1)
    #plt.plot(np.rint(slope2hat), lw=1)
    #plt.plot(slope1-slope1hat, lw=1)
    #plt.plot(slope2-slope2hat, lw=1)
    print(mapdata1)
    plt.show()
