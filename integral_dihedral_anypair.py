#! /usr/bin/env python

import os
import sys
import math
import string
import numpy as np
from dihedral_fes_tools import ReadFes2D

Nbiases=int(sys.argv[1])
targetCV1=int(sys.argv[2])
targetCV2=int(sys.argv[3])
biasfactor=float(sys.argv[4])
temperature=float(sys.argv[5])
#init=int(sys.argv[4])

scalefactor=biasfactor/(biasfactor-1)
kbt=2.49*temperature/300

print scalefactor
xg=np.zeros( [Nbiases,200] )
yg=np.zeros( [Nbiases,200] )
bias=np.zeros( [Nbiases,200,200] )

for k in range(0, Nbiases, 1):
    [xg[k],yg[k],bias[k]]=ReadFes2D("bias",k,Periodic=False)

gofx=np.ones(200)
bofx=np.ones(200)
spacing=3.14159/100


hofx=np.zeros(200)

for k in range(0, Nbiases-targetCV2, 1):
    print k
    hofx=np.zeros(200)
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            hofx[i]+=math.exp(scalefactor*bias[Nbiases-(1+k)][i][j]/kbt)*gofx[j]*spacing
    gofx=hofx

for k in range(0, targetCV1, 1):
    print k
    hofx=np.zeros(200)
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            hofx[i]+=math.exp(scalefactor*bias[k][j][i]/kbt)*bofx[j]*spacing
    bofx=hofx

Gofx=np.zeros( [200,200] )

for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        for q in range(0, yg[0].size, 1):
            Gofx[i][j] += gofx[i]*math.exp(scalefactor*(bias[targetCV1][i][q]+bias[targetCV1+1][q][j])/kbt)

for k in range(targetCV1+2, targetCV2, 1):
    Hofx=np.zeros( [200,200] )
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            for q in range(0, yg[0].size, 1):
                Hofx[i][j] +=  Gofx[i][q]*math.exp(scalefactor*bias[k][q][j])
    Gofx=Hofx




fes=np.zeros( [200,200] )

for i in range(0, gofx.size, 1):
    for j in range(0, bofx.size, 1):
        fes[i][j] = -kbt*math.log(Gofx[i][j])-kbt*math.log(bofx[i])


fes1dx=np.zeros(200)
fes1dy=np.zeros(200)

for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        fes1dx[i]+=math.exp(-fes[i][j]/kbt)
    fes1dx[i]=-kbt*math.log(fes1dx[i])

for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        fes1dy[i]+=math.exp(-fes[j][i]/kbt)
    fes1dy[i]=-kbt*math.log(fes1dy[i])

fes_uncorrelated=np.zeros( [200,200] )

for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        fes_uncorrelated[i][j]=fes1dx[i]+fes1dy[j]


filename="fes"+str(targetbias)
outputfile=open(filename, "a")
fes_min=np.amin(fes)
fes_min2=np.amin(fes_uncorrelated)

for i  in range(0, xg[0].size,1):
    for j in range(0, yg[0].size,1):
        outputfile.write('%f %f %f %f\n' %(xg[0][i], yg[0][j], fes[i][j]-fes_min, fes_uncorrelated[i][j]-fes_min2))
    outputfile.write('\n')

outputfile.close()

'''
def f(x):
    return -2.49*math.log(x)

f=np.vectorize(f)

filename="gofx"+str(targetbias)+str(Nbiases)
outputfile=open(filename, "a")
gofx=f(gofx)
gmin=np.min(gofx)
for i  in range(0, xg[0].size,1):
    outputfile.write('%f %f\n' %(xg[0][i], gofx[i]-gmin))

outputfile.close()


filename="bofx"+str(targetbias)+str(init)
outputfile=open(filename, "a")
bofx=f(bofx)
bmin=np.min(bofx)
for i  in range(0, xg[0].size,1):
    outputfile.write('%f %f\n' %(xg[0][i], bofx[i]-bmin))

outputfile.close()
'''
