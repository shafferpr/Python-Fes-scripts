#! /usr/bin/env python

import sys
import numpy as np

fn_fes = sys.argv[1]
fn_out = sys.argv[1].replace('.data','').replace('.dat','') + ".normalized.data"

# Free energy surface => f(s)
# Read FES
fes_tmp=[]; cv_tmp=[]
file = open(fn_fes,'r')
for line in file.readlines():
    if (line[0:1] != '#' and line.split() != [] and line[0:1] != '@'):
        cv_tmp.append( float( line.split()[0] ) )
        fes_tmp.append( float( line.split()[1] ) )
file.close()

fes = np.array(fes_tmp)
cv  = np.array(cv_tmp)
del fes_tmp; del cv_tmp

fes_max = np.amax(fes)
fes_min = np.amin(fes)

fes_deriv = np.diff(fes)/np.diff(cv)
fes_deriv.resize(fes.size)
fes_deriv[-1] = fes_deriv[0]

# Write the data to the output file 
file = open(fn_out,'w')
file.write('#   F(s)_min = {0:<20.10f}\n'.format(fes_min))
file.write('#   F(s)_max = {0:<20.10f}\n'.format(fes_max))
for i in xrange(fes.size):
    out_str = '{0:>20.10f}{1:>20.10f}{2:>20.10f}{3:>20.10f}{4:>20.10f}\n'.format(cv[i],fes[i],fes[i]-fes_min,fes[i]-fes_max,fes_deriv[i])
    file.write(out_str)
file.close()
