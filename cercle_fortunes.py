from logging import raiseExceptions
import math
from fortunes import *
from tkinter import *
from numpy.linalg import norm
import numpy as np
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

# Ray Casting
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
            
def interieur_test(point, poly):
    total=0
    for i in range(-1,len(poly)-1):
        if poly[i].y<=poly[i+1].y:
            p1=poly[i]
            p2=poly[i+1]
        else:
            p1=poly[i+1]
            p2=poly[i]
            
        if interesection_rayon(point, p1, p2):
            total+=1
            
    if total%2==0:
        return True
    else:
        return False

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
 
def min_distance_poly3(point, poly):
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
        if interieur_test2(c, poly):
            r=min_distance_poly3(c, poly)
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
    poly.affinage_interieur(affinage)
    centres=fortunes(poly.get_points(), canvas)

    centre, rayon = trouve_min_cercle(poly.get_points(), centres)

    poly.dessin_poly(canvas, 'black', 4, debug_points=False, couleurs=False)

    for c in centres:
        dessin_point(c, 2, canvas, 'blue')
        
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
    
poly_c1=Polygone(
    [(89, 188), (147, 108), (228, 64), (291, 85), (354, 131), (453, 313), (296, 300), (240, 402), (159, 249)],
    [(238, 145), (276, 144), (312, 178), (343, 244), (226, 248)]
)

poly_c2=Polygone(
    [(143, 363), (52, 276), (112, 241), (146, 271), (181, 268), (202, 238), (184, 204), (84, 199), (83, 169), (108, 117), (186, 131), (219, 126), (220, 92), (183, 49), (239, 15), (304, 32), (429, 164), (442, 212), (430, 219), (371, 225), (358, 277), (448, 314), (459, 335), (453, 374), (430, 416), (362, 433), (289, 438), (282, 402), (323, 349), (286, 328), (248, 328), (214, 377), (190, 428), (154, 449), (130, 442)],
    [(343, 127), (311, 114), (273, 119), (250, 135), (235, 162), (245, 178), (255, 197), (258, 211), (261, 235), (273, 265), (289, 290), (313, 310), (341, 323), (358, 330), (354, 362), (353, 381), (374, 386), (388, 368), (387, 326), (370, 313), (342, 294), (334, 279), (327, 250)]
)
poly_c3=Polygone(
    [(183, 42), (164, 44), (147, 55), (135, 77), (127, 106), (121, 122), (108, 127), (90, 132), (73, 142), (68, 155), (65, 174), (68, 197), (80, 211), (97, 216), (112, 222), (128, 241), (128, 257), (123, 270), (106, 282), (95, 291), (93, 321), (101, 348), (113, 352), (129, 360), (155, 371), (163, 389), (167, 407), (179, 423), (203, 427), (229, 428), (250, 421), (263, 415), (279, 411), (304, 411), (323, 419), (350, 427), (375, 430), (405, 430), (420, 430), (433, 424), (441, 416), (452, 401), (455, 379), (455, 360), (455, 345), (450, 336), (433, 334), (416, 335), (402, 350), (380, 366), (365, 355), (363, 338), (384, 315), (411, 306), (423, 302), (433, 290), (441, 264), (449, 247), (457, 217), (457, 184), (457, 155), (437, 139), (408, 139), (390, 148), (380, 167), (362, 189), (337, 216), (322, 219), (302, 220), (296, 201), (314, 181), (336, 181), (349, 173), (357, 156), (368, 143), (382, 130), (400, 116), (417, 83), (424, 64), (421, 47), (402, 27), (371, 15), (353, 15), (308, 18), (291, 20), (290, 33), (275, 50), (262, 56), (254, 47), (244, 33)],
    [(311, 263), (299, 265), (277, 261), (269, 249), (266, 235), (253, 234), (235, 235), (231, 241), (228, 257), (228, 269), (228, 294), (243, 299), (270, 305), (273, 312), (273, 322), (270, 339), (262, 340), (247, 341), (242, 350), (242, 365), (254, 382), (284, 391), (316, 391), (332, 392), (334, 379), (335, 364), (326, 344), (324, 323), (331, 297), (378, 283), (401, 261), (418, 228), (414, 211), (394, 210), (373, 222)]
)

poly_c4=Polygone(
    [(170, 155), (505, 68), (583, 174), (622, 250), (685, 277), (682, 396), (649, 558), (538, 596), (343, 715), (227, 629), (107, 630), (84, 532), (294, 488), (367, 450), (355, 412), (296, 386), (209, 384), (117, 348), (214, 293), (269, 265), (271, 241), (257, 211), (188, 207), (120, 234)],
    [(502, 175), (473, 158), (404, 152), (359, 160), (318, 153), (268, 163), (279, 179), (303, 192), (327, 216), (327, 251), (316, 275), (335, 288), (358, 308), (361, 336), (385, 336), (447, 323), (511, 323), (536, 331), (561, 327), (563, 308), (536, 297), (494, 289), (470, 277), (473, 249), (516, 234), (547, 224)]
)

tk, canvas = init_tk_canvas(900, 900)
plot_centres(poly_c4, canvas)
show_tk(tk)