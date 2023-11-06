#!/usr/bin/env python

import matplotlib.pyplot as plt
import os
import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = f.read()
    start = 1024 + 4096*4*70
    for i in range(0,4096):
        part = data[start +  i*4:start+4 + i*4]
        tile = int.from_bytes(data[start+i*4:start+2+i*4], signed=True)
        height = int.from_bytes(data[start+2+i*4:start+4+i*4], signed=True)
        print(i, part, part[3], tile, height, tile.to_bytes(2, 'big', signed=True) +  height.to_bytes(2, 'big', signed=True))
