import numpy as np
from subprocess import call
import os

def pick(marker):
    '''
    picks the nodal points
    marker = #
    writes to tmp file and then reads and returns outputs
    returns:
        nodal points
    '''
    f = open('tmp','w')
    call(['picknps','-d','2','-n','tecin.dat.nps','-m',str(marker)],stdout = f)
    f.close()
    nodes = []
    with open("tmp",'r') as tmp:
        for line in tmp:
            nodes.append(int(line))
    os.remove('tmp')
    return nodes
def setBndry(boundryFile,markerList,boundaryType):
    '''
    create boundary condition file
    inputs:
        boundaryFile < name of file for outputs
        list of markers to pick
        boundaryType = type of boundary [x,y]
            0 = None
            1 = Disp
            2 = Vel
            3 = Forc
    '''
    f = open(boundryFile,'w')
    #write first line
    for i,marker in enumerate(markerList):
        nodes = pick(marker)
        for node in nodes:
            f.write("%12d%5d%5d\n" %(node,boundaryType[i][0],boundaryType[i][1]))
    f.write('end ibc\n')
    f.write('end bc\n')
    f.write('end iwink\n')
    f.write('end wink\n')
    f.write('end Euler\n')
    f.close()
