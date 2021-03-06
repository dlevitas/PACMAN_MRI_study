#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 21:32:37 2*22

things for testing purposes

@author: dlevitas
"""
from __future__ import division
import platform, shlex
import subprocess as subp


#Determine Monitor Resolution:
if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    w_pix, h_pix = GetSystemMetrics(0), GetSystemMetrics(1)
elif platform.system() == "Darwin":
    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout)
    if '@' in output:
        w_pix, h_pix = [int(x.strip(" ")) for x in output.split(':')[-1].split("@")[0].split(' x ')]
    elif 'Retina' in output:
        w_pix, h_pix = [int(x) for x in output.split(":")[-1].split("Retina")[0:1][0].split(' x ')]
    elif 'QHD/WQHD - Wide Quad High Definition' in output:
        w_pix, h_pix = [int(x) for x in output.split(":")[-1].split("(QHD/WQHD - Wide Quad High Definition)")[0:1][0].split(' x ')]
elif platform.system() == "Linux":
    output = subp.check_output("xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'", shell=True).decode("utf-8")
    w_pix = output.split("x")[0]
    h_pix = output.split("x")[-1].split("\n")[0]
    

print(w_pix, h_pix)






grid = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,4,1,1,1,4,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0),
                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))


moveable_spaces = 0
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == 5:
            print(col*36,row*36)

        if grid[row][col] != 0:
            moveable_spaces += 1


print("")
print("There are {} moveable spaces in this grid".format(moveable_spaces))


