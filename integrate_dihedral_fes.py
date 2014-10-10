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

print bias[0][1][0]
