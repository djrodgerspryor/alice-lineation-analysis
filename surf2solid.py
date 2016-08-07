from math import *
from numpy import *
import os
import sys

def surf2solid(
    fn,
    filename,
    size=(65, 65), # mm
    resolution=150,
    x_min=-1.,
    x_max=1.,
    y_min=-1.,
    y_max=1.,
    z_min=0.,
    stlmode=True,
    use_file=True,
):
    filename += '.stl'

    xsize, ysize = size

    sys.stderr.write(" ".join(sys.argv))
    sys.stderr.write("\n")
    sys.stderr.write("%s\n"%len(sys.argv))

    if len(sys.argv)>1:
        if 'help' in sys.argv[1]:
            print "I didn't write any help yet"
            exit(0)
        if '.stl'==sys.argv[1][-4:]:
            sys.stderr.write("using stl file mode\n")
            use_file = True
            stlmode = True
            filename = sys.argv[1]
        if '.scad'==sys.argv[1][-5:]:
            sys.stderr.write("using scad file mode\n")
            use_file = True
            stlmode = False
            filename = sys.argv[1]

    def poly(theta,n=4,r=10):
        theta = (int(theta*180/pi)%(360/n))*pi/180
        theta = theta-0.5*(360/n)*pi/180
        if theta<-pi/2: theta=-pi/2
        if theta>pi/2: theta=pi/2
        x = r/(0.001+cos(theta))
        return x

    def evaluate(x,y,fn):
        r = sqrt(x*x+y*y)
        theta = atan2(y,x)
        return fn(x=x, y=y, r=r, theta=theta)

    def mag(a):
        return sqrt(sum(a*a))

    def unit(a):
        return a/mag(a)

    points = []
    triangles = []

    xstep=(x_max-x_min)/(resolution-1)
    ystep=(y_max-y_min)/(resolution-1)
    X=array(range(resolution))*xstep+x_min
    Y=array(range(resolution))*ystep+y_min
    sys.stderr.write(str((len(X),len(Y))))

    x_scalar = xsize/(x_max-x_min)
    y_scalar = ysize/(y_max-y_min)
    z_scalar = 0.5*(x_scalar+y_scalar)

    for i,x in enumerate(X):
        for j,y in enumerate(Y):
            points.append(array([x*x_scalar,y*y_scalar,z_scalar*max(0,-z_min+evaluate(x,y,fn))]))
            if i>0 and j>0:
                p1 = i+j*resolution
                p2 = p1-1
                p3 = p1-resolution
                p4 = p3-1
                triangles.append([p1,p2,p4])
                triangles.append([p1,p4,p3])

    xstep=100.0/(resolution-1)
    ystep=100.0/(resolution-1)
    X=array(range(resolution))*xstep-50
    Y=array(range(resolution))*ystep-50

    for i,x in enumerate(X):
        points.append([x,-ysize/2.,0])
        if i>0:
            p1 = i*resolution
            p2 = p1-resolution
            p3 = resolution**2+i
            p4 = p3-1
            triangles.append([p1,p4,p2])
            triangles.append([p1,p3,p4])

    for i,x in enumerate(X):
        points.append([x,ysize/2.,0])
        if i>0:
            p1 = i*resolution+resolution-1
            p2 = p1-resolution
            p3 = resolution**2+resolution+i
            p4 = p3-1
            triangles.append([p1,p2,p4])
            triangles.append([p1,p4,p3])

    for j,y in enumerate(Y):
        points.append([-xsize/2.,y,0])
        if j>0:
            p1 = j
            p2 = p1-1
            p3 = resolution**2+2*resolution+j
            p4 = p3-1
            triangles.append([p1,p2,p4])
            triangles.append([p1,p4,p3])

    for j,y in enumerate(Y):
        points.append([xsize/2.,y,0])
        if j>0:
            p1 = resolution**2-resolution+j
            p2 = p1-1
            p3 = resolution**2+3*resolution+j
            p4 = p3-1
            triangles.append([p1,p4,p2])
            triangles.append([p1,p3,p4])

    points+=map(array,[[0,0,0],[-xsize/2.,-ysize/2.,0],[xsize/2.,-ysize/2.,0],[xsize/2.,ysize/2.,0],[-xsize/2.0,ysize/2.0,0]])

    triangles.append(list(array([0,1,2])+4*resolution+resolution**2))
    triangles.append(list(array([0,2,3])+4*resolution+resolution**2))
    triangles.append(list(array([0,3,4])+4*resolution+resolution**2))
    triangles.append(list(array([0,4,1])+4*resolution+resolution**2))

    data = ''
    if stlmode:
        '''
        solid name
        facet normal ni nj nk
          outer loop
            vertex v1x v1y v1z
            vertex v2x v2y v2z
            vertex v3x v3y v3z
          endloop
        endfacet
        endsolid name
        '''
        import time
        t = time.localtime()
        name = 'object%s%s%s%s%s%s'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        data+= 'solid %s\n'%name
        for facet in triangles:
            #try:
            p=[array(points[f]) for f in facet]
            #except IndexError:
            #   sys.stderr.write(str(facet)+"\n")
            #point=unit(cross(p[1]-p[0],p[2]-p[0]))
            #point=unit(cross(p[0]-p[2],p[2]-p[1]))
            point=[0,0,0]
            data+='facet normal %s\n'%' '.join(map(str,point))
            data+='  outer loop\n'
            #if inward_wall:
            p=[p[0],p[2],p[1]]
            for point in p:
                data+= '    vertex %s\n'%' '.join(map(str,point))
            data+= '  endloop\n'
            data+= 'endfacet\n'
        data+= 'endsolid %s\n'%name
    else:
        tos = lambda f:"%0.7f"%f
        maptos = lambda a:'['+','.join(map(tos,a))+']'
        mapmaptos = lambda a:'['+','.join(map(maptos,a))+']'
        data="polyhedron(\npoints=\n%s,\ntriangles\n=%s);"%(mapmaptos(points),triangles)

    if use_file:
        f = open(filename, "w")
        f.write(data)
        f.close()
        #os.system("meshlab %s"%filename)
    else:
        print data

