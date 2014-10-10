#! /usr/bin/env python


import os
import sys
import math
import string
import numpy as np


def ReadFes2D(filename, label, Periodic=False):
    # Get gridsize
    filename+=str(label)
    i=0 ;j=0
    file = open(filename,'r')
    for line in file.readlines():
        if(line[0:1] != '#' and line[0:1] != '@'):
            if( line.split() == [] ):
                i=0; j=j+1
            else:
                surface_gridsize_x = i
                surface_gridsize_y = j
                i=i+1
    file.close()
    surface_gridsize_x += 1; surface_gridsize_y += 1
    if(Periodic): surface_gridsize_x += 1; surface_gridsize_y += 1
    x_grid  = np.zeros( surface_gridsize_x )
    y_grid  = np.zeros( surface_gridsize_y )
    surface = np.zeros( [surface_gridsize_x,surface_gridsize_y] )
    i=0 ;j=0
    file = open(filename,'r')
    for line in file.readlines():
        if(line[0:1] != '#' and line[0:1] != '@'):
            if(line.split()==[]):
                i=0; j=j+1;
            else:
                x_grid[i]     = float(line.split()[0])
                y_grid[j]     = float(line.split()[1])
                surface[i,j]  = float(line.split()[2])
                i=i+1
    file.close()
    if(Periodic):
        x_grid[-1]=-x_grid[0]
        y_grid[-1]=-y_grid[0]
        surface[-1,:]=surface[0,:]
        surface[:,-1]=surface[:,0]
    return [x_grid, y_grid, surface]
