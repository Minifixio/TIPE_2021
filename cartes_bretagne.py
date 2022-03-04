import geopandas
import matplotlib.pyplot as plt
import numpy as np
from logging import raiseExceptions
import math
from fortunes import *
from numpy.linalg import norm
import copy 
import itertools

EPS = .000001
counter = 0
x0 = 0
x1 = 0
y0 = 0
y1 = 0


class Polygone:
    exterieur=[]
    interieur=[]
    def __init__(self, points, interieur=[]):
        self.exterieur=self.convertir_point(points)
        self.interieur=self.convertir_point(interieur)
    
    def convertir_point(self, data):
        res=[]
        for p in data:
            res.append(Point(p[0], p[1]))
        return res

    def dessin_poly(self, canvas, couleur="blue", epaisseur=2, debug_points=False, couleurs=False):
        for i in range(-1, len(self.exterieur)-1):
            p1=self.exterieur[i]
            p2=self.exterieur[i+1]
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill = couleur, width=epaisseur)
            if debug_points:
                p1.dessin_point(canvas, 4, 'green')

        # canvas.create_line(
        #     self.exterieur[-1].x, 
        #     self.exterieur[-1].y, 
        #     self.exterieur[0].x, 
        #     self.exterieur[0].y, 
        #     fill = couleur, width=epaisseur)

        for j in range(-1,len(self.interieur)-1):
            p1=self.interieur[j]
            p2=self.interieur[j+1]
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill = couleur, width=epaisseur)
            if debug_points:
                p1.dessin_point(canvas, 4, 'cyan')
                
        if couleurs:
            self.dessin_champ(self.exterieur, canvas)
            self.dessin_lac(self.interieur, canvas)
    
    def dessin_lac(self, lac, canvas):
        lac_tuple=[]
        for p in lac:
            lac_tuple.append(p.x)
            lac_tuple.append(p.y)
        lac_tuple=tuple(lac_tuple)
        canvas.create_polygon(lac_tuple, fill="blue")
        
    def dessin_champ(self, champ, canvas):
        champ_tuple=[]
        for p in champ:
            champ_tuple.append(p.x)
            champ_tuple.append(p.y)
        champ_tuple=tuple(champ_tuple)
        canvas.create_polygon(champ_tuple, fill="#F8E994")
        
    def coeff_droite(self, p1, p2):
        if p1.x == p2.x:
            return 0
        else:
            return (p2.y-p1.y)/(p2.x-p1.x)

    # droite y=kx+m 
    # renvoi (x,y(x))
    def point_droite(self, k, m, x):
        return Point(x, k*x + m)

    def affiner(self, data, precision):
        res=[]
        for i in range(-1,len(data)-1):
            p1=data[i]
            p2=data[i+1]
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
                k=self.coeff_droite(p1, p2)
                valx=np.linspace(x1, x2, num=precision)
                for x in valx:
                    points.append(self.point_droite(k, data[i].y - k*data[i].x, x))
            if points[0].y != p1.y:
                points=points[::-1]
            if points[0].x != p1.x:
                points=points[::-1]
            # print(p1.__str__(), p2.__str__())
            # print([p.__str__() for p in points])
            res=res+points
        return res
            
    def affinage_exterieur(self, precision):
        self.exterieur=self.affiner(self.exterieur,precision)

    def affinage_interieur(self, precision):
        self.interieur=self.affiner(self.interieur,precision)

    def get_points(self):
        return self.interieur + self.exterieur

    def print_points(self):
        res=''
        for p in (self.interieur + self.exterieur):
            res=res+'('+str(p.x)+','+str(p.y)+')'
        print(res)

# Ray Casting 2
def interieur_test2(point, poly):
    inside = False
    eps = 0.00001
    for i in range(-1,len(poly)-1):
        # Make sure A is the lower point of the edge
        A, B = poly[i], poly[i+1]
        if A.y > B.y:
            A, B = B, A

        # Make sure point is not at same height as vertex
        if point.y == A.y or point.y == B.y:
            point.y += eps

        if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
            # The horizontal ray does not intersect with the edge
            continue

        if point.x < min(A.x, B.x): # The ray intersects with the edge
            inside = not inside
            continue

        try:
            m_edge = (B.y - A.y) / (B.x - A.x)
        except ZeroDivisionError:
            m_edge = math.inf

        try:
            m_point = (point.y - A.y) / (point.x - A.x)
        except ZeroDivisionError:
            m_point = math.inf

        if m_point >= m_edge:
            # The ray intersects with the edge
            inside = not inside
            continue

    return inside

# https://www.geeksforgeeks.org/minimum-distance-from-a-point-to-the-line-segment-using-vectors/
def minDistance(p1, p2, p) :
    r=0
    AB = [None, None];
    AB[0] = p2.x - p1.x
    AB[1] = p2.y - p1.y
    BE = [None, None];
    BE[0] = p.x - p2.x
    BE[1] = p.y - p2.y
    AE = [None, None];
    AE[0] = p.x - p1.x
    AE[1] = p.y - p1.y
    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
    if (AB_BE > 0) :

        y = p.y - p2.y
        x = p.x - p2.x
        r = math.sqrt(x * x + y * y);
    elif (AB_AE < 0) :
        y = p.y - p1.y
        x = p.x - p1.x
        r = math.sqrt(x * x + y * y);
    else:
        x1 = AB[0]
        y1 = AB[1]
        x2 = AE[0]
        y2 = AE[1]
        mod = math.sqrt(x1 * x1 + y1 * y1)
        r = abs(x1 * y2 - y1 * x2) / mod

    return r
 
def min_distance_poly(point, poly):
    rmin=(-1)
    for i in range(-1,len(poly)-1):
        r=minDistance(poly[i],poly[i+1],point)
        if rmin==(-1) or r<rmin:
            rmin=r
    return rmin
 
def min_distance_obstacles(point, obs):
    rmin=(-1)
    for o in obs:
        r=math.sqrt((point.x-o[0])**2 + (point.y-o[1])**2)
        if rmin==(-1) or r<rmin:
            rmin=r
    return rmin  
       
def trouve_min_cercle(poly, centres, obstacles):    
    
    rmax=0
    candidat=None
    print('Nombres de centres trouvés:', len(centres))

    for c in centres:
        if interieur_test2(c, poly):
            rp=min_distance_poly(c, poly)
            if obstacles:
                rs=min_distance_obstacles(c, obstacles)
                r=min(rs, rp)
            else:
                r=rp
            #print((c.x, c.y), r)
            #dessin_cercle(c, r, 'red', epaisseur=1)
            if r>rmax:
                candidat=c
                rmax=r
    
    print(candidat, rmax)
    return candidat, rmax

def print_obstacles(obstacles, ax):
    for o in obstacles:
        dessin_point(Point(o[0], o[1]), ax, 3, 'red')
        
def dessin_point(p, ax, size=4, couleur="green"):
    ax.plot(p.x, p.y, marker="o", markersize=size, markerfacecolor=couleur)
 
def dessin_cercle(centre, rayon, ax, couleur="green"):
    cir=plt.Circle((centre.x, centre.y), rayon, color=couleur, fill=False)
    ax.add_patch(cir)

def plot_centres(data, ax, xmax, ymax, obstacles=None, affinage=1):

    poly=copy.deepcopy(data)
    poly.affinage_exterieur(affinage)
    poly.affinage_interieur(affinage)
    centres=fortunes(poly.get_points(), xmax, ymax)
    centre, rayon = trouve_min_cercle(poly.get_points(), centres, obstacles)

    #poly.dessin_poly(canvas, 'black', 4, debug_points=False, couleurs=False)
    # for c in centres:
    #     dessin_point(c, ax, 2, 'blue')
        
    print_obstacles(obstacles, ax)
    dessin_point(centre, ax, 4, 'green')
    dessin_cercle(centre, rayon, ax, couleur='green')

x_zoom=[300000, 400000]
y_zoom=[6750000, 6800000]

zones_sensibles_file='donneegeo/Zonages_preservation_OBPNB_GIPBE/Zonages_preservation_OBPNB_GIPBE.shx'
bassins_file='donneegeo/bassin_versant/bassin_versant.shx'
mapworld=geopandas.datasets.get_path('naturalearth_lowres')

geom=geopandas.read_file(zones_sensibles_file)
bassins=geopandas.read_file(bassins_file)

ax = geom.plot()
bassins.boundary.plot(ax=ax)

ax.set_xlim(x_zoom[0], x_zoom[1])
ax.set_ylim(y_zoom[0], y_zoom[1])

coords = list(geom.geometry[1].exterior.coords)

def is_in_perimeter(polygon):
    if type(polygon).__name__ == 'Polygon':
        coords=polygon.exterior.coords
        res=False
        for p in coords:
            x=p[0]
            y=p[1]
            if x >= x_zoom[0] and x <= x_zoom[1] and y >= y_zoom[0] and y <= y_zoom[1] :
                res=True
                return res
        return res

def get_poly_in_perimeter(data, prec):
    res=[]
    count=0
    for poly in data:
        if is_in_perimeter(poly):
            count+=1
            res.append(poly.exterior.coords[::prec])
            #res.append([ (x-x_zoom[0], y-y_zoom[0]) for (x,y) in poly.exterior.coords[::20] ])
    print(count)
    return res

def get_all_points_in_perimeter(data, prec):
    res=[]
    for poly in data:
        if is_in_perimeter(poly):
            res += poly.exterior.coords[::prec]
    return res

#poly_in_perimeter1 = get_poly_in_perimeter(geom.geometry.to_list(), 90)
poly_in_perimeter2 = get_poly_in_perimeter(bassins.geometry.to_list(), 20)
obstacles_points=get_all_points_in_perimeter(geom.geometry.to_list(), 90)
print(len(geom.geometry.to_list()), len(obstacles_points))

for poly in poly_in_perimeter2:
    plot_centres(Polygone(poly), ax, x_zoom[1], y_zoom[1], obstacles_points)
    
plt.show()
    

