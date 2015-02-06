#! /usr/bin/env python

import os
import sys
import math
import string
import numpy as np
from dihedral_fes_tools import ReadFes2D

Nbiases=int(sys.argv[1])
targetbias=int(sys.argv[2])
biasfactor=float(sys.argv[3])
temperature=float(sys.argv[4])
#init=int(sys.argv[4])

scalefactor=biasfactor/(biasfactor-1)
kbt=2.49*temperature/300


xg=np.zeros( [Nbiases,200] )
yg=np.zeros( [Nbiases,200] )
bias=np.zeros( [Nbiases,200,200] )

for k in range(0, Nbiases, 1):
    [xg[k],yg[k],bias[k]]=ReadFes2D("bias",k,Periodic=False)

gofx=np.ones(200)
bofx=np.ones(200)
spacing=3.14159/100


hofx=np.zeros(200)

for k in range(0, Nbiases-targetbias-1, 1):
    hofx=np.zeros(200)
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            hofx[i]+=math.exp(scalefactor*bias[Nbiases-(1+k)][i][j]/kbt)*gofx[j]*spacing
    gofx=hofx

for k in range(0, targetbias, 1):
    hofx=np.zeros(200)
    for i in range(0, xg[0].size, 1):
        for j in range(0, yg[0].size, 1):
            hofx[i]+=math.exp(scalefactor*bias[k][j][i]/kbt)*bofx[j]*spacing
    bofx=hofx

fes=np.zeros( [200,200] )
probability=np.zeros( [200,200] )
integral=0
for i in range(0, gofx.size, 1):
    for j in range(0, bofx.size, 1):
        fes[i][j] = -scalefactor*bias[targetbias][i][j]-kbt*math.log(gofx[j])-kbt*math.log(bofx[i])
        probability[i][j]= math.exp(-fes[i][j]/kbt)
        integral+=probability[i][j]

for i in range(0, gofx.size, 1):
    for j in range(0, bofx.size, 1):
        probability[i][j]=probability[i][j]/integral

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

probability_uncorrelated=np.zeros( [200,200] )
integral=0
for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        fes_uncorrelated[i][j]=fes1dx[i]+fes1dy[j]
        probability_uncorrelated[i][j]= math.exp(-fes_uncorrelated[i][j]/kbt)
        integral+=probability_uncorrelated[i][j]

for i in range(0, xg[0].size, 1):
    for j in range(0, yg[0].size, 1):
        probability_uncorrelated[i][j]=probability_uncorrelated[i][j]/integral


filename="fes"+str(targetbias)
outputfile=open(filename, "a")
fes_min=np.amin(fes)
fes_min2=np.amin(fes_uncorrelated)

for i  in range(0, xg[0].size,1):
    for j in range(0, yg[0].size,1):
        outputfile.write('%f %f %f %f\n' %(xg[0][i], yg[0][j], fes[i][j]-fes_min, fes_uncorrelated[i][j]-fes_min2))
    outputfile.write('\n')

outputfile.close()

targetCV2=targetbias+1
filename="probability"+str(targetbias)+"."+str(targetCV2)
outputfile=open(filename, "a")
mutualinformation=0
for i  in range(0, xg[0].size,1):
    for j in range(0, yg[0].size,1):
        mutualinformation+=probability[i][j]*math.log(probability[i][j]/probability_uncorrelated[i][j])
        outputfile.write('%f %f %.12f %.12f\n' %(xg[0][i], yg[0][j], probability[i][j], probability[i][j]*math.log(probability[i][j]/probability_uncorrelated[i][j])))
    outputfile.write('\n')

outputfile.close()
print mutualinformation

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
