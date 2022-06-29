import geopandas
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from logging import raiseExceptions
import math
from fortune import *
from TkinterUtils import *
from PolygonUtils import *
from Structures import *
from cercles_poles import cercle_interieur
import copy 
import itertools
import time

EPS = .000001
counter = 0
x0 = 0
x1 = 0
y0 = 0
y1 = 0
k=10
e=1

def interieur_test2(point, poly):
    inside = False
    eps = 0.00001
    for i in range(-1,len(poly)-1):
        A, B = poly[i], poly[i+1]
        if A.y > B.y:
            A, B = B, A

        if point.y == A.y or point.y == B.y:
            point.y += eps

        if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
            continue

        if point.x < min(A.x, B.x): 
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
        if mod>0:
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
       
def trouve_min_cercle_fortunes(poly, centres, obstacles):    
    
    rmax=0
    candidat=None

    for c in centres:
        if interieur_test2(c, poly):
            rp=min_distance_poly(c, poly)
            if obstacles:
                rs=min_distance_obstacles(c, obstacles)
                r=min(rs, rp)
            else:
                r=rp

            if r>rmax:
                candidat=c
                rmax=r
    
    return candidat, rmax

def print_obstacles(obstacles, ax):
    for o in obstacles:
        dessin_point_matplotlib(Point(o[0], o[1]), ax, 3, 'red')
        
def dessin_point_matplotlib(p, ax, size=4, couleur="green"):
    ax.plot(p.x, p.y, marker="o", markersize=size, markerfacecolor=couleur)
 
def dessin_cercle_matplotlib(centre, rayon, ax, couleur="green"):
    cir=plt.Circle((centre.x, centre.y), rayon, color=couleur, fill=False)
    ax.add_patch(cir)

# type == 1 => on calcule la distance aux obstacles après avoir calculé Fortunes avec la polygone
# type == 2 => on calcule Fortune avec les points obstacles
def plot_centres_fortunes(data, ax, xmax, ymax, obstacles=None, type=1, affinage=1):

    poly=copy.deepcopy(data)
    poly.affinage_exterieur(affinage)
    poly.affinage_interieur(affinage)
    
    if obstacles:
        if type==1:
            centres=fortunes(poly.get_points(), xmax, ymax)
        else:
            centres=fortunes(poly.get_points()+convertir_point(obstacles), xmax,ymax)
    else:
        centres=fortunes(poly.get_points(), xmax, ymax)

    centre, rayon = trouve_min_cercle_fortunes(poly.get_points(), centres, obstacles)
    
    if centre==None:
        return 
    
    dessin_point_matplotlib(centre, ax, 4, 'green')
    dessin_cercle_matplotlib(centre, rayon, ax, couleur='green')
    
    
def trouve_min_cercle_poles(data, obstacles, ax, affinage=1):
    global k, e
    centre, rayon = cercle_interieur(data, [], k, e, obstacles=obstacles)
    dessin_point_matplotlib(centre, ax, 4, 'green')
    dessin_cercle_matplotlib(centre, rayon, ax, couleur='green')
    

x_zoom=[213000, 290000]
y_zoom=[6754000, 6820000]

zones_sensibles_file='donneegeo/Zonages_preservation_OBPNB_GIPBE/Zonages_preservation_OBPNB_GIPBE.shx'
bassins_file='donneegeo/bassin_versant/bassin_versant.shx'
mapworld=geopandas.datasets.get_path('naturalearth_lowres')

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
    return res

def get_all_points_in_perimeter(data, prec):
    res=[]
    for poly in data:
        if is_in_perimeter(poly):
            res += poly.exterior.coords[::prec]
    return res


def plot_zoom(file_obstacles, file_frontieres, x_zoom, y_zoom, type="fortunes"):
    geom=geopandas.read_file(file_obstacles)
    bassins=geopandas.read_file(file_frontieres)
    start_time = time.time()

    ax = geom.plot()
    bassins.boundary.plot(ax=ax, color="black")

    ax.set_xlim(x_zoom[0], x_zoom[1])
    ax.set_ylim(y_zoom[0], y_zoom[1])

    coords = list(geom.geometry[1].exterior.coords)
    poly_in_perimeter = get_poly_in_perimeter(bassins.geometry.to_list(), 10)
    obstacles_points = get_all_points_in_perimeter(geom.geometry.to_list(), 10)
    print('Nombre de points : ' + str(sum([ len(p) for p in poly_in_perimeter]) + len(obstacles_points)) 
          + ' / ' 
          + 'Nombre d\'obstacles : ' + str(len(obstacles_points)))

    for poly in poly_in_perimeter:
        if type=="fortunes": 
            plot_centres_fortunes(Polygone(poly), ax, x_zoom[1], y_zoom[1], obstacles_points, type=1)
        if type=="poles":
            trouve_min_cercle_poles(Polygone(poly).getExterieur(), convertir_point(obstacles_points), ax)
    
    print("--- %s seconds ---" % (time.time() - start_time))
        
    plt.show()
    
def plot_all(file1, file2):
    geom=geopandas.read_file(file1)
    bassins=geopandas.read_file(file2)

    ax = geom.plot()
    bassins.boundary.plot(ax=ax, color="black")
        
    plt.show()

#plot_zoom(zones_sensibles_file, bassins_file, x_zoom, y_zoom, type="poles")
#plot_all(zones_sensibles_file, bassins_file)