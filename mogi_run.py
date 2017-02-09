import numpy as np
from make_mogi_mesh import make_mesh
import set_boundry as sbn
from set_pr import setPr
from subprocess import call
#Make the mesh
L = 100000 #length of domain
H = 100000 #hieght of domain
md = -8000 #mogi source depth
mr = 1000 #mogi Radius
np = 4 #mogi source number of points

make_mesh(L,H,md,mr,np)

#triangulate the make_mesh
Area = 20000000
call(["triangle","-pqACa%s"% (Area),"mogi.poly"])
#refine mesh around center of mogi source
factor= 0.05#refinement ratio
typ=1 #type of refinemnt
dist= 25000 #absolute distants to which the mesh should be refines
of = 'mogi.1.area' #output file name
#call(["setarea","mogi.1","-p" ,"0.",str(md),"-f",str(factor),"-r",str(typ),"-d",str(dist),">",of])
call(["setarea mogi.1 -p 0. %s -f %s -r %s -d %s > %s " % (md,factor,typ,dist,of)],shell = True)
# retrianulate based on refine results
call(["triangle","-pra","mogi.1"])
# convert to Finite Element
call(['tri2fe','-n','mogi.2.node','-e','mogi.2.ele'])
#set boundary conditions
bndryFile = 'mogi.dat.bcs'
nodes = [4,3,102,103,1]
bndrcnd = [[1,1],[1,1],[0,1],[1,0],[1,0]]
sbn.setBndry(bndryFile,nodes,bndrcnd)
#partition the files
processor = 4
#the file names here cannot be changes because of tri2fe limitations
call(['partition','-n','tecin.dat.nps','-e','tecin.dat.elm','-d','2','-p',str(processor),'-f'])
#create pressure bounary condition file
prm = [6,7,8,9,105,106,107,108] #pressure markers for nodes and sides
prv = -50000000. #pressure value
setPr('tecin.dat.pr',prm,prv)
#run main
yng=40e9
pois=0.25
call(["""sed "s/ MAT=.*/ MAT='      1     %12d     %12f  1.0e30       1        1      1'/" dotecin.sh > dotmp"""%(yng,pois)],shell=True)
call(['sh dotmp > TECIN.DAT'],shell=True)
if processor == 1:
    call(['axi as feout workpath=`pwd` partinfo=partition.info fein=TECIN.DAT fedsk=fedsk.par echo=1 -log_info '],shell=True)
else:
    call(["""/usr/lib64/openmpi/bin/mpirun -np %d axi as feout workpath=`pwd` partinfo=partition.info fein=TECIN.DAT fedsk=fedsk.par echo=1 -log_info""" % (processor)],shell=True)
#merge
call(['mergefiles partinfo=partition.info as fedsk=fedsk.par'],shell=True)
