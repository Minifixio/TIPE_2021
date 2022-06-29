from logging import raiseExceptions
import math
from fortune import *
from tkinter import *
from Examples import *
import numpy as np
from numpy.linalg import norm
import copy 

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
        if couleurs:
            self.dessin_champ(self.exterieur, canvas)
            self.dessin_lac(self.interieur, canvas)
            
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
                p1.dessin_point(canvas, 4, 'green')
                
    
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
        if precision==1:
            return data
        else:
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

def getDistance(event):
    global counter, x0, y0, x1, y1
    print(event)
    if counter == 0:
        x0 = event.x
        y0 = event.y
        counter += 1
    elif counter == 1:
        x1 = event.x
        y1 = event.y
        counter += 1
    elif counter == 2:
        distance = math.sqrt(((x0 - x1)**2)+((y0 - y1)**2))
        print(distance)
        counter = 0

def interieur_test(point, poly):
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

def interesection_rayon(point, p1, p2):
    if point.y==p1.y or point.y==p2.y:
        point.y=point.y+EPS
    elif point.x>=max(p1.x, p2.x):
        return False
    else:
        if point.x<min(p1.x, p2.x):
            return True
        else:
            if p2.x != p1.x:
                m1=(p2.y-p1.y)/(p2.x-p1.x)
            else:
                m1=math.inf
            
            if p1.x != point.x:
                m2=(point.y-p1.y)/(point.x-p1.x)
            else:
                m2=math.inf
            
            if m2>=m1:
                return True
            else:
                return False

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
           
def trouve_min_cercle(poly, centres):    
    
    rmax=0
    candidat=None
    #print(poly)
    print('Nombres de centres trouvés:', len(centres))

    for c in centres:
        if interieur_test(c, poly):
            r=min_distance_poly(c, poly)
            #print((c.x, c.y), r)
            #dessin_cercle(c, r, 'red', epaisseur=1)
            if r>rmax:
                candidat=c
                rmax=r
    
    print(candidat, rmax)
    return candidat, rmax


def plot_centres(data, canvas, affinage=1):

    poly=copy.deepcopy(data)
    poly.affinage_exterieur(affinage)
    centres=fortunes(poly.get_points(), canvas)

    centre, rayon = trouve_min_cercle(poly.get_points(), centres)
    print(centre, rayon)

    poly.dessin_poly(canvas, 'black', 4, debug_points=False, couleurs=True)

    for c in centres:
        dessin_point(c, 4, canvas, 'blue')
        
    dessin_point(centre, 4, canvas, 'green')
    dessin_cercle(centre, rayon, canvas, couleur='green', epaisseur=4)
    
def init_tk_canvas(width, height):
    tk = Tk()
    tk.title('VORONOI')
    tk.geometry(str(width) + "x" + str(height))
    canvas=Canvas(tk, width=width, height=height, background="white")
    canvas.grid(row = 0, column = 0)
    return tk, canvas

def show_tk(tk):
    tk.bind('<Button-1>', coord_souris)
    tk.bind("<Button-3>", getDistance)
    tk.bind('<Motion>', mouvement)
    tk.mainloop()

# tk, canvas = init_tk_canvas(1000, 1000)
# plot_centres(poly_c7, canvas, 10)
# show_tk(tk)