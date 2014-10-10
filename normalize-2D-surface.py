#! /usr/bin/env python

import sys
import numpy as np
import argparse

help_text = '\
'

parser = argparse.ArgumentParser(description=help_text)
parser.add_argument('-f', '--input',   dest='fn_in', required=True)
parser.add_argument('-o', '--output',  dest='fn_out',  required=False)
parser.add_argument('-T','--Temperature',   dest='temperature',           type=float, required=True)
parser.add_argument('--natural-units', dest='natural_units', action='store_true', required=False)
args = parser.parse_args()

fn_in = args.fn_in
if(args.fn_out):
    fn_out = args.fn_out
else:
    fn_out = fn_in.replace('.data','').replace('.dat','') + ".normalized.data"

# Surface 
# Get gridsize
i=0 ;j=0
file = open(fn_in,'r')
for line in file.readlines():
    if(line[0:1] != '#' and line[0:1] != '@'):
        if( line.split() == [] ):
            i=0; j=j+1
        else:
            surface_gridsize_x = i
            surface_gridsize_y = j
            i=i+1
file.close()
surface_gridsize_x = surface_gridsize_x + 1
surface_gridsize_y = surface_gridsize_y + 1
x_grid  = np.zeros( surface_gridsize_x )
y_grid  = np.zeros( surface_gridsize_y )
surface = np.zeros( [surface_gridsize_x,surface_gridsize_y] )
i=0 ;j=0
file = open(fn_in,'r')
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

surface_min = np.amin(surface)

file = open(fn_out,'w')
file.write('#---------------------------------------'  + '\n' )
file.write('# surface: ' + str(fn_in) + '\n')
file.write('# surface_min = {0:<20.9f}\n'.format(surface_min))
file.write('#---------------------------------------' + '\n' )
for j in xrange(surface_gridsize_y):
    for i in xrange(surface_gridsize_x):
        out_str = '{0:>20.9f} {1:>20.9f} {2:>20.9f} {3:>20.9f}\n'.format(x_grid[i],y_grid[j],surface[i,j],surface[i,j]-surface_min)
        file.write(out_str)
    file.write('\n')
file.close()













