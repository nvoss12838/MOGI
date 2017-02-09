import numpy as np

def make_mesh(L,H,mogi_depth,mogi_radius,numpoints):
    '''
    Make a .poly file for axi_symetric mogi source
    inputs:
        L = Domain Length
        H= Downain Height
        mogi_depth = Depth of the mogi source
        mogi_radius = Radius of spherical boundary
        numpoints = Number of points on boundary of sphere
    outputs:
        mogi.poly file for use with Triangle
    '''
    #constants
    y1,x1 = 0,0 #top left
    #mogi_depth = -8000
    #mogi_radius = 1000.
    x4,y4 = 0,-H #botttom left
    x2,y2 = L,0 #top right
    x3,y3 = L,-H
    # calculate mogi source
    # x=rcos(t) y = r sin(t)

    #Find number of angles to calculate
    angle = 180./numpoints
    cX,cY = [],[]
    a = -90
    for i in range(numpoints):
        cX.append(mogi_radius*np.cos(np.radians(a)))
        cY.append(mogi_radius*np.sin(np.radians(a)))
        a+=angle
    cY.append(mogi_radius)
    cX.append(0)
    cY = [c+mogi_depth for c in cY]
    X= [x1,x2,x3,x4]
    X.extend(cX)
    Y=[y1,y2,y3,y4]
    Y.extend(cY)
    #write poly file
    f = open('mogi.poly','w')
    #write points
    f.write('# points #\n')
    f.write(str(len(X))+' 2 0 1\n')
    for i in range(len(X)):
        f.write('%s: %d %d %s\n' % (i,X[i],Y[i],i+1))
    #do segments
    f.write('# domain boundary #\n')
    f.write('%s 1\n' % (len(X)))
    for i in range(len(X)):
        print i
        if i<len(X)-1:
            f.write('%s: %d %d %s\n' % (i,i,i+1,i+100))
        else:
            f.write('%s: %d %d %s\n' % (i,i,0,i+100))
    f.write('# no gaps #\n')
    f.write('0\n')
    f.write('# material markers #\n')
    f.write('1\n')
    f.write('0:   0.5 0.5 1\n')
    f.close()
    return
