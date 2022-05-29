import math
import random
from Visualisation import Visualisation

"""XX = [0,2,1]
YY = [0,0.5,1]"""

"""XX=[]
YY=[]
for i in range(3):
    XX.append(random.uniform(0,100))
    YY.append(random.uniform(0,100))"""

"""XX = [4.64,5.36,6.9,6.74,7.05,6.2,5.14,5.71]
YY = [4.92,6.08,5.98,3.62,2.19,0.86,1.83,4.11]"""

XX = [7.26, 3.05, 2.02, 4.42, 6.4, 7.97]
YY = [2.87, 2.46, 3.29, 6.86, 7.34, 5.53]

"""XX = [0,6.4,3.6]
YY = [0,4.8,7.2]"""

"""XX = [235,486,760,699,611,482,372]
YY = [209,154,261,498,649,625,532]"""

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
    precision = max(xmax - xmin, ymax - ymin)
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
                    if m!=0:
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
        precision = max(xmax - xmin, ymax - ymin)
    return (centre, T[0])

def pos(a,b,c):
    if a >= b and a<= c:
        return 1
    elif a<= b and a>= c:
        return 1
    else:
        return 0

def cercle2(X,Y,n):
    xmin = min(X)
    xmax = max(X)
    ymin = min(Y)
    ymax = max(Y)
    ne = len(X)
    r = 0
    centre = (X[0],Y[0])
    c = 0
    T = [0,math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)]
    for j in range(n):
        x = random.uniform(xmin,xmax)
        y = random.uniform(ymin,ymax)
        dmin = math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)
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
                    d = min(math.sqrt((x-x1)**2  + (y-y1)**2),math.sqrt((x-x2)**2  + (y-y2)**2))
                else:
                    d = (abs(y - m*x - p))/(math.sqrt(1 + m**2))
                if d < dmin:
                    dmin = d
                    T[1] = d
            if dmin > T[0]:
                T[0] = dmin
                centre = (x,y)
    return (centre,T[0])

def centre_multiple(X,Y,n1,n2,k,e):
    centres_max = [(X[0],Y[0])]*k
    rayons_max = [0]*k
    smax = 0
    for i in range(n1):
        Tx = [X]
        Ty = [Y]
        for s in range(k-1):
            j = random.randrange(s+1)
            m = len(Tx[j])
            i1 = random.randrange(m)
            i2 = random.randrange(m)
            while i2 == i1:
                i2 = random.randrange(m)
            i1, i2 = min(i1, i2), max(i1, i2)
            t1 = random.uniform(0,1)
            t2 = random.uniform(0,1)
            x1 = t1*Tx[j][i1] + (1-t1)*Tx[j][i1-1]
            y1 = t1*Ty[j][i1] + (1-t1)*Ty[j][i1-1]
            x2 = t2*Tx[j][i2] + (1-t2)*Tx[j][i2-1]
            y2 = t2*Ty[j][i2] + (1-t2)*Ty[j][i2-1]
            X1 = [x1]
            Y1 = [y1]
            for d in range(i1,i2):
                X1.append(Tx[j][d])
                Y1.append(Ty[j][d])
            X1.append(x2)
            Y1.append(y2)
            X2 = [x2]
            Y2 = [y2]
            for d in range(i2,m):
                X2.append(Tx[j][d])
                Y2.append(Ty[j][d])
            for d in range(i1):
                X2.append(Tx[j][d])
                Y2.append(Ty[j][d])
            X2.append(x1)
            Y2.append(y1)
            del Tx[j]
            Tx.append(X1)
            Tx.append(X2)
            del Ty[j]
            Ty.append(Y1)
            Ty.append(Y2)
        centres_intermediaires = []
        ray_intermediaires = []
        som = 0
        for d in range(k):
            centre, ray = cercle(Tx[d],Ty[d],n2,e)
            centres_intermediaires.append(centre)
            ray_intermediaires.append(ray)
            som += ray
        if som > smax:
            smax = som
            rayons_max = ray_intermediaires
            centres_max = centres_intermediaires
    return centres_max, rayons_max, smax


def centre_multiple2(X,Y,n1,n2,k):
    centres_max = [(X[0],Y[0])]*k
    rayons_max = [0]*k
    smax = 0
    for i in range(n1):
        Tx = [X]
        Ty = [Y]
        for s in range(k-1):
            j = random.randrange(s+1)
            m = len(Tx[j])
            i1 = random.randrange(m)
            i2 = random.randrange(m)
            while i2 == i1:
                i2 = random.randrange(m)
            i1, i2 = min(i1, i2), max(i1, i2)
            t1 = random.uniform(0,1)
            t2 = random.uniform(0,1)
            x1 = t1*Tx[j][i1] + (1-t1)*Tx[j][i1-1]
            y1 = t1*Ty[j][i1] + (1-t1)*Ty[j][i1-1]
            x2 = t2*Tx[j][i2] + (1-t2)*Tx[j][i2-1]
            y2 = t2*Ty[j][i2] + (1-t2)*Ty[j][i2-1]
            X1 = [x1]
            Y1 = [y1]
            for d in range(i1,i2):
                X1.append(Tx[j][d])
                Y1.append(Ty[j][d])
            X1.append(x2)
            Y1.append(y2)
            X2 = [x2]
            Y2 = [y2]
            for d in range(i2,m):
                X2.append(Tx[j][d])
                Y2.append(Ty[j][d])
            for d in range(i1):
                X2.append(Tx[j][d])
                Y2.append(Ty[j][d])
            X2.append(x1)
            Y2.append(y1)
            del Tx[j]
            Tx.append(X1)
            Tx.append(X2)
            del Ty[j]
            Ty.append(Y1)
            Ty.append(Y2)
            centres_intermediaires = []
            ray_intermediaires = []
        som = 0
        for d in range(k):
            centre, ray = cercle2(Tx[d],Ty[d],n2)
            centres_intermediaires.append(centre)
            ray_intermediaires.append(ray)
            som += ray
        if som > smax:
            smax = som
            rayons_max = ray_intermediaires
            centres_max = centres_intermediaires
    return centres_max, rayons_max, smax



def convertir_coord(X,Y):
    res=[]
    for i in range(len(X)):
        res.append((X[i], Y[i]))
    return res

coords=convertir_coord(XX,YY)
#centre, rayon, s =centre_multiple2(XX,YY,2000,500,2)
centre, rayon, s = centre_multiple(XX,YY,300,120,3,1)
visu = Visualisation(coords)
for i in range(len(centre)):
    visu.add_point(centre[i][0],centre[i][1])
    visu.add_circle((centre[i][0],centre[i][1]), rayon[i])
print(centre, rayon,s)
visu.affiche()
