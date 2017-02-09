import numpy as np
from subprocess import call
from set_boundry import pick
import os

def setPr(prFile,markerList,pressure):
        '''
        create pressure boundary condition file
        inputs:
            boundaryFile < name of file for outputs
            list of markers to pick
            pressure = value of pressure boundary condition q
        '''
        f = open(prFile,'w')
        #make file with list of nodes
        fN = open('ndFile','w')
        nodes = []
        for i,marker in enumerate(markerList):
            nodes.extend(pick(marker))
        nodes2 = sorted(list(set(nodes)))
        for node in nodes2:
            fN.write("%d\n" %(node))
        fN.close()
        call(['elmside','l=ndFile','e=tecin.dat.partf.elm','n=tecin.dat.partf.nps','d=2','s=1'],stdout=f)
        f.close()
        string_to_add = '\t'+str(pressure)
        with open(prFile, 'r') as f:
            file_lines = [''.join([x.strip(), string_to_add, '\n']) for x in f.readlines()]

        with open(prFile, 'w') as f:
            f.writelines(file_lines)
        return
