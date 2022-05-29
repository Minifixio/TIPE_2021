from tkinter import *
from numpy.linalg import norm
import numpy as np
import copy 
import math
import random
from TkinterUtils import *
from PolygonUtils import *
from Structures import * 
from Examples import *

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

def pos(a,b,c):
    if a >= b and a<= c:
        return 1
    elif a<= b and a>= c:
        return 1
    else:
        return 0
    
def cercle_interieur(ext, inte, k, e, obstacles=None, canvas=None, visu_state=False):
    xmin = min([p.x for p in ext])
    xmax = max([p.x for p in ext])
    ymin = min([p.y for p in ext])
    ymax = max([p.y for p in ext])
    ne = len(ext)
    ni = len(inte)
    
    centre = Point(ext[0].x,ext[0].y)
    c = 0
    echec = 0
    precision = min(xmax - xmin, ymax - ymin)
    T = [0,math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)]
    
    while precision > e:
        echec = 0
        while echec < k:
            x = random.uniform(xmin,xmax)
            y = random.uniform(ymin,ymax)
            
            if visu_state:
                canvas.create_oval(x-1,y-1,x+1,y+1,fill="red", width=3)

            dmin = math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)
            ce = 0
            ci = 0
            
            for i in range(-1,ne-1):
                p = pos(y, ext[i].y, ext[i+1].y)
                if ((ext[i].y-ext[i+1].y) !=0) and (x <= ext[i+1].x + (y - ext[i+1].y)*(ext[i].x-ext[i+1].x)/(ext[i].y-ext[i+1].y)):
                    ce = (ce+p)%2
                    
            if ni>0:
                for i in range(-1,ni-1):
                    p = pos(y, inte[i].y, inte[i+1].y)
                    if ((inte[i].y-inte[i+1].y) !=0) and (x <= inte[i+1].x + (y - inte[i+1].y)*(inte[i].x-inte[i+1].x)/(inte[i].y-inte[i+1].y)):
                        ci = (ci+p)%2
                
            if ce==1 and ci==0:
                for i in range(-1,ne-1):
                    x1,y1 = ext[i].x, ext[i].y
                    x2,y2 = ext[i+1].x, ext[i+1].y
                    if x2!=x1:
                        m = (y2-y1)/(x2-x1)
                    else:
                        m=0
                    p = y1 - m*x1
                    if m != 0:
                        x3 = m*(y1 + (x1/m) + m*x - y)/(m**2 +1)
                        x4 = m*(y2 + (x2/m) + m*x - y)/(m**2 +1)
                        if pos(x,x3,x4) == 0:
                            d = min(math.sqrt((x-x1)**2  + (y-y1)**2),math.sqrt((x-x2)**2  + (y-y2)**2))
                        else:
                            d = (abs(y - m*x - p))/(math.sqrt(1 + m**2))
                        if d < dmin:
                            dmin = d
                            T[1] = d
                            
                if ni>0:   
                    for i in range(-1,ni-1):
                        x1,y1 = inte[i].x, inte[i].y
                        x2,y2 = inte[i+1].x, inte[i+1].y
                        m = (y2-y1)/(x2-x1)
                        p = y1 - m*x1
                        if m != 0:
                            x3 = m*(y1 + (x1/m) + m*x - y)/(m**2 +1)
                            x4 = m*(y2 + (x2/m) + m*x - y)/(m**2 +1)
                            if pos(x,x3,x4) == 0:
                                d = min(math.sqrt((x-x1)**2  + (y-y1)**2),math.sqrt((x-x2)**2  + (y-y2)**2))
                            else:
                                d = (abs(y - m*x - p))/(math.sqrt(1 + m**2))
                            if d < dmin:
                                dmin = d
                                T[1] = d
                
                if obstacles:
                    for o in obstacles:
                        d=math.sqrt((x-o.x)**2  + (y-o.y)**2)
                        if d<dmin:
                            dmin=d
                            T[1]=d

                if dmin > T[0]:
                    T[0] = dmin
                    centre = Point(x,y)
                    #print(centre.__str__())
                    echec=0
                else:
                    echec += 1
        
        xmin, xmax = centre.x - (xmax - xmin) / (math.sqrt(2) * 2), centre.x + (xmax - xmin) / (math.sqrt(2) * 2) 
        ymin, ymax = centre.y - (ymax - ymin) / (math.sqrt(2) * 2), centre.y + (ymax - ymin) / (math.sqrt(2) * 2)
        
        if visu_state:
            canvas.create_rectangle(xmin, ymin, xmax, ymax, outline = 'blue')
            canvas.create_oval(centre.x-1,centre.y-1,centre.x+1,centre.y+1,fill="red", width=3)
            # self.visu.add_point(centre[0],centre[1])
            # self.visu.add_square(xmin, ymin,  xmax-xmin, ymax-ymin)
            
        precision = min(xmax - xmin, ymax - ymin)
    
    return centre, T[0]
    
def plot_centres(poly, k, e, canvas, affinage=1):

    poly.affinage_exterieur(affinage)
    poly.affinage_interieur(affinage)
    centre, rayon = cercle_interieur(poly.getExterieur(), poly.getInterieur(), k, e, canvas=canvas)

    poly.dessin_poly(canvas, 'black', 4, debug_points=True, couleurs=True)

    dessin_point(centre, 2, canvas, 'blue')
        
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
    tk.bind("<Button-3>", getDistance)
    tk.mainloop()

# tk, canvas = init_tk_canvas(900, 900)
# plot_centres(poly_c5, 100, 0.01, canvas, 1)
# show_tk(tk)