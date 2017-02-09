import numpy as np
from make_mogi_mesh import make_mesh
from subprocess import call
#Make the mesh
L = 100000 #length of domain
H = 100000 #hieght of domain
md = -8000 #mogi source depth
mr = 1000 #mogi Radius
np = 4 #mogi source number of points

make_mesh(L,H,md,mr,np)

#triangulate the make_mesh
Area = 100000
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
call(['tri2fe','-n','mogi.2.node','-e','mogi.2.ele'],shell=True)
