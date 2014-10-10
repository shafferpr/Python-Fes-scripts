#! /usr/bin/env python
    
import numpy as np

def ReadFes2D(filename, Periodic=False):
    # Get gridsize
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

def WriteFes2D(filename,header,grids,surfaces):
    x_grid=grids[0]; y_grid=grids[1]
    fmt = '{:>20.9f} '
    file = open(filename,'w')
    for k in header: file.write(k)
    for j in xrange(y_grid.size):
        for i in xrange(x_grid.size):
            str = fmt.format(x_grid[i]) + fmt.format(y_grid[j])
            for k in surfaces: str += fmt.format(k[i,j])
            str += '\n'
            file.write(str)
        file.write('\n')
    file.close()

def getValuesInsideRegion2D(grids,surface,R):
    values = []
    num_values=0
    x=grids[0]; y=grids[1]
    for j in xrange(y.size):
        for i in xrange(x.size):
            if( x[i]>=R[0] and x[i]<=R[2] and y[j]>=R[1] and y[j]<=R[3]): 
                values.append(surface[i,j])
                num_values+=1
    return [np.array(values), num_values]
        
def ReadFes1D(filename, Periodic=False):
    surface_tmp=[]; x_tmp=[]
    file = open(filename,'r')
    for line in file.readlines():
        if (line[0:1] != '#' and line.split() != [] and line[0:1] != '@'):
            x_tmp.append( float( line.split()[0] ) )
            surface_tmp.append( float( line.split()[1] ) )
    file.close()
    x_grid  = np.array(x_tmp)
    surface = np.array(surface_tmp)
    del x_tmp; del surface_tmp
    if(Periodic):
        x_grid.resize(x_grid.size+1)
        surface.resize(surface.size+1)
        x_grid[-1]=-x_grid[0]
        surface[-1]=surface[0]
    return [x_grid, surface]

def WriteFes1D(filename,header,grid,surfaces):
    x_grid=grid[0]
    fmt = '{:>20.9f} '
    file = open(filename,'w')
    for k in header: file.write(k)
    for i in xrange(x_grid.size):
        str = fmt.format(x_grid[i])
        for k in surfaces: str += fmt.format(k[i])
        str += '\n'
        file.write(str)
    file.close()
 
def getValuesInsideRegion1D(grid,surface,R):
    values = []
    num_values=0
    x=grid[0]
    for i in xrange(x.size):
        if( x[i]>=R[0] and x[i]<=R[1] ): 
            values.append(surface[i])
            num_values+=1
    return [np.array(values), num_values]
        
