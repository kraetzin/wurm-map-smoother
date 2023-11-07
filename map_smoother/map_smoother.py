#!/usr/bin/env python

import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter

MAPSIZE = 4096

def process_map(mapfile):
    MAPSIZE = 4096
    maxbytes = MAPSIZE*MAPSIZE
    with open(mapfile, 'rb') as f:
        data = f.read()
    start = 1024
    row = []
    mapdata = np.ndarray(shape=(MAPSIZE, MAPSIZE), dtype=int)
    tiledata = np.ndarray(shape=(MAPSIZE, MAPSIZE), dtype=int)
    print("Created empty mapdata")
    for i in range(0,MAPSIZE*MAPSIZE):
        x = i % MAPSIZE
        y = int(i / MAPSIZE)
        part = data[start+i*4 : start+4+(i*4)]
        tile = int.from_bytes(part[0:2], signed=True)
        height = int.from_bytes(part[2:4], signed=True)
        tiledata[x,y] = tile
        mapdata[x,y] = height
    return mapdata, tiledata

def get_preamble(mapfile):
    with open(mapfile, 'rb') as f:
        data = f.read()
    return data[0:1024]

def smooth_map(mapdata):
    sigma = [0.7, 0.7]
    smoothdata = gaussian_filter(mapdata, sigma)
    return smoothdata

def write_map(mapdata, tiledata, preamble, outfile):
    with open(outfile, 'wb') as f:
        f.write(preamble)
        for y in range(0,MAPSIZE):
            print(f'\r{y+1}/{MAPSIZE}', end='')
            for x in range(0,MAPSIZE):
                tile = int(tiledata[x,y])
                height = int(mapdata[x,y])
                tilebytes = tile.to_bytes(2, 'big', signed=True)
                heightbytes = height.to_bytes(2, 'big', signed=True)
                f.write(tilebytes + heightbytes)
    print()

if __name__ == "__main__":
    mapfile1 = sys.argv[1]
    mapfile2 = sys.argv[2]
    preamble = get_preamble(mapfile1)
    mapdata1, tiledata1 = process_map(mapfile1)
    smoothmap1 = smooth_map(mapdata1)
    output1 = write_map(smoothmap1, tiledata1, preamble, "output/rock_layer.map")
    mapdata2, tiledata2 = process_map(mapfile2)
    smoothmap2 = smooth_map(mapdata2)
    output2 = write_map(smoothmap2, tiledata2, preamble, "output/top_layer.map")
