#! /usr/bin/env python

import os
import sys
import math
import string
import numpy as np
from dihedral_fes_tools import ReadFes2D

Nbiases=int(sys.argv[1])

xg=np.zeros( [Nbiases,200] )
yg=np.zeros( [Nbiases,200] )
bias=np.zeros( [Nbiases,200,200] )

for k in range(0, Nbiases, 1):
    [xg[k],yg[k],bias[k]]=ReadFes2D("bias",k,Periodic=False)

gofx=np.zeros(200)
spacing=3.14159/100


for i in range(0, xg[Nbiases-1].size, 1):
    for j in range(0, yg[Nbiases-1].size, 1):
        gofx[i]+=math.exp(bias[Nbiases-1][i][j]/2.49)*spacing


hofx=np.zeros(200)

for k in range(0, Nbiases-1, 1):
    print k
    hofx=np.zeros(200)
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            hofx[i]+=math.exp(bias[Nbiases-(2+k)][i][j]/2.49)*gofx[j]*spacing
    gofx=hofx

for i in range(0, hofx.size, 1):
    hofx[i]=-2.49*math.log(hofx[i])

filename="fes_phi1_dihedral_integration"+str(Nbiases)
outputfile=open(filename, "a")
fes_min=np.amin(hofx)
for i  in range(0, xg[0].size,1):
    outputfile.write('%f %f\n' %(xg[0][i], hofx[i]-fes_min))

outputfile.close()
