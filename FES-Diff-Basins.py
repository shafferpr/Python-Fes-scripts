#! /usr/bin/env python

import sys
import numpy as np
import argparse
from FesFileTools import ReadFes2D
from FesFileTools import WriteFes2D
from FesFileTools import getValuesInsideRegion2D
from trapz2d import trapz2d




help_text = '\
'

parser = argparse.ArgumentParser(description=help_text)
parser.add_argument('-f', '--fes',   dest='fn_fes', required=True)
parser.add_argument('-T','--Temperature',   dest='temperature', default=300.0, type=float, required=False)
parser.add_argument('--natural-units', dest='natural_units', action='store_true', required=False)
parser.add_argument('--Periodic-CVs', dest='periodic_fes', action='store_true', required=False)
parser.add_argument('--prefix',   dest='prefix', default='    ', required=False)
parser.add_argument('--basin-1',  dest='basin1', type=float, nargs=4, required=True)
parser.add_argument('--basin-2',  dest='basin2', type=float, nargs=4, required=True)
parser.add_argument('--write-debug-FES', dest='write_debug_fes', action='store_true', required=False)
args = parser.parse_args()

if(args.natural_units): kB = 1.0
else: kB = 8.311451e-3
T = args.temperature
kT = kB*T
beta = 1.0/kT
kJ2kcal=0.23900573614

rB1 = np.array(args.basin1)
rB2 = np.array(args.basin2)
[xg, yg, fes] = ReadFes2D(args.fn_fes,Periodic=args.periodic_fes)
fes = fes - np.amin(fes)
pFull = trapz2d(z=np.exp(-beta*fes), x=xg, y=yg)
[vB1, nvB1] = getValuesInsideRegion2D([xg,yg],fes,rB1)
[vB2, nvB2] = getValuesInsideRegion2D([xg,yg],fes,rB2)

bVol = (xg[1]-xg[0])*(yg[1]-yg[0])
nvT = xg.size*yg.size

pB1 = 0.0
for i in xrange(vB1.size): pB1 +=np.exp(-beta*vB1[i])
pB1=(pB1*bVol)/pFull
zB1 = -kT*np.log(pB1)

pB2 = 0.0
for i in xrange(vB2.size): pB2 +=np.exp(-beta*vB2[i])
pB2=(pB2*bVol)/pFull
zB2 = -kT*np.log(pB2)

print ' {:>10.10s}    {:>20.9f} {:>20.9f} {:>20.9f}    {:>20.9f} {:>20.9f} {:>20.9f}    {:>9d} {:>9d} {:>9d}  {:>10.4f}'.format(args.prefix,zB1,zB2,zB1-zB2, pB1,pB2,pFull, nvB1,nvB2,nvT,T)

if(args.write_debug_fes):
    pdf = np.exp(-beta*fes)/pFull
    WriteFes2D('debug1.data', [], [xg,yg],[fes,pdf])
