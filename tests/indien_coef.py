import math
import random
from tkinter import *
debug_coords=False
x, y = None, None
poly = []

#X1 = [0,1,4,3,-2]
#Y1 = [2,4,2,-1,0]
X1=[]
Y1=[]
for i in range(8):
    X1.append(random.uniform(0,100))
    Y1.append(random.uniform(0,100))

def pos(a,b,c):
    if a >= b and a<= c:
        return 1
    elif a<= b and a>= c:
        return 1
    else:
        return 0

def cercle(X,Y,k,e):
    xmin = min(X)
    xmax = max(X)
    ymin = min(Y)
    ymax = max(Y)
    ne = len(X)
    r = 0
    centre = [X[0],Y[0]]
    c = 0
    echec = 0
    precision = min(xmax - xmin, ymax - ymin)
    T = [0,math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)]
    while precision > e:
        echec = 0
        while echec < k:
            x = random.uniform(xmin,xmax)
            y = random.uniform(ymin,ymax)
            dmin = math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)
            c = 0
            for i in range(-1,ne-1):
                p = pos(y,Y[i],Y[i+1])
                if x <= X[i+1] + (y - Y[i+1])*(X[i]-X[i+1])/(Y[i]-Y[i+1]):
                    c = (c+p)%2
            if c == 1:
                for i in range(-1,ne-1):
                    x1,y1 = X[i], Y[i]
                    x2,y2 = X[i+1], Y[i+1]
                    m = (y2-y1)/(x2-x1)
                    p = y1 - m*x1
                    x3 = m*(y1 + (x1/m) + m*x - y)/(m**2 +1)
                    x4 = m*(y2 + (x2/m) + m*x - y)/(m**2 +1)
                    if pos(x,x3,x4) == 0:
                        d = min(math.sqrt((x-x1)**2  + (y-y1)**2),math.sqrt((x-x2)**2  + (y-y2)**2))
                    else:
                        d = (abs(y - m*x - p))/(math.sqrt(1 + m**2))
                    if d < dmin:
                        dmin = d
                        T[1] = d
                if dmin > T[0]:
                    T[0] = dmin
                    centre = [x,y]
            echec += 1
        xmin, xmax = centre[0] - (xmax - xmin) / (math.sqrt(2) * 2), centre[0] + (xmax - xmin) / (math.sqrt(2) * 2) 
        ymin, ymax = centre[1] - (ymax - ymin) / (math.sqrt(2) * 2), centre[1] + (ymax - ymin) / (math.sqrt(2) * 2)
        precision = min(xmax - xmin, ymax - ymin)
    return (centre, T[0])


def cercle2(X,Y,n,R):
    xmin = min(X)
    xmax = max(X)
    ymin = min(Y)
    ymax = max(Y)
    ne = len(X)
    r = 0
    centre = (X[0],Y[0])
    c = 0
    rmax = max(R)
    T = [0,rmax*(math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2))]
    for j in range(n):
        x = random.uniform(xmin,xmax)
        y = random.uniform(ymin,ymax)
        dmin = rmax*(math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2))
        c = 0
        for i in range(-1,ne-1):
            p = pos(y,Y[i],Y[i+1])
            if x <= X[i+1] + (y - Y[i+1])*(X[i]-X[i+1])/(Y[i]-Y[i+1]):
                c = (c+p)%2
        if c == 1:
            for i in range(-1,ne -1):
                x1,y1 = X[i], Y[i]
                x2,y2 = X[i+1], Y[i+1]
                m = (y2-y1)/(x2-x1)
                p = y1 - m*x1
                x3 = m*(y1 + (x1/m) + m*x - y)/(m**2 +1)
                x4 = m*(y2 + (x2/m) + m*x - y)/(m**2 +1)
                if pos(x,x3,x4) == 0:
                    d = R[i]*(min(math.sqrt((x-x1)**2  + (y-y1)**2),math.sqrt((x-x2)**2  + (y-y2)**2)))
                else:
                    d = R[i]*(abs(y - m*x - p))/(math.sqrt(1 + m**2))
                if d < dmin:
                    dmin = d
                    T[1] = d
            if dmin > T[0]:
                T[0] = dmin
                centre = (x,y)
    return (centre,T[0])

def convertir_coord(X,Y):
    res=[]
    for i in range(len(X)):
        res.append((X[i], Y[i]))
    return res

coords=convertir_coord(X1,Y1)
#centre, rayon=cercle(X1,Y1,5000,0.0001)
centre, rayon = cercle2(X1,Y1,100000,[0.5,0.7,0.4,0.8,0.3,0.5,0.9,0.2])
visu = Visualisation(coords)
visu.add_point(centre[0],centre[1])
visu.add_circle((centre[0],centre[1]), rayon)
print(centre, rayon)
visu.affiche()
