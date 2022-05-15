from Structures import Point, Polygone
import numpy as np

# utils fonctions 
def read_from_file(filename): 
    file = open(filename, 'r')
    points = []
    for line in file: 
        x,y = line.split(' ')
        points.append(Point(float(x),float(y)))
    file.close()
    return points

def write_to_file(filename, points): # Save the point set to a file
    file = open(filename,'w')
    for p in points: 
        file.write(str(p.x) + ' ' + str(p.y) + '\n')
    file.close()

def convertir_point(points_t):
    res=[]
    for p in points_t:
        res.append(Point(p[0], p[1]))
    return res

def coeff_droite(p1, p2):
    if p1.x == p2.x:
        return 0
    else:
        return (p2.y-p1.y)/(p2.x-p1.x)

# droite y=kx+m 
# renvoi (x,y(x))
def point_droite(k, m, x):
    return Point(x, k*x + m)

def affiner_poly(poly, precision):
    if precision==1:
        return poly
    res=[]
    for i in range(-1,len(poly)-1):
        p1=poly[i]
        p2=poly[i+1]
        x1=min(p1.x, p2.x)
        x2=max(p1.x, p2.x)
        points=[]
        if x1==x2:
            y1=min(p1.y, p2.y)
            y2=max(p1.y, p2.y)
            valy=np.linspace(y1, y2, num=precision)
            for y in valy:
                points.append(Point(x1, y))
        else:    
            k=coeff_droite(p1, p2)
            valx=np.linspace(x1, x2, num=precision)
            for x in valx:
                points.append(point_droite(k, poly[i].y - k*poly[i].x, x))
        if points[0].y != p1.y:
            points=points[::-1]
        if points[0].x != p1.x:
            points=points[::-1]

        print(p1.__str__(), p2.__str__())
        print([p.__str__() for p in points])

        res=res+points

    return res