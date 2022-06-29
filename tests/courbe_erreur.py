import matplotlib.pyplot as plt
import random
import math


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
    return centre


def erreur_triangle(X,Y,N,k,p):
    """N:nombre max pour un appel de cercle
       k : ecart entre deux valeurs de n"""
    S = list(range(k,N+k,k))
    T = []
    r2 = math.sqrt((X[1]-X[0])**2 + (Y[1]-Y[0])**2)
    r1 = math.sqrt((X[2]-X[0])**2 + (Y[2]-Y[0])**2)
    r0 = math.sqrt((X[1]-X[2])**2 + (Y[1]-Y[2])**2)
    x = (r0*X[0] + r1*X[1] + r2*X[2])/(r0 + r1 + r2)
    y = (r0*Y[0] + r1*Y[1] + r2*Y[2])/(r0 + r1 + r2)
    for i in range(k,N+k,k):
        s = 0
        for j in range(p):
            s += math.sqrt((cercle2(X,Y,i)[0] - x)**2 + (cercle2(X,Y,i)[1] - y)**2)
        T.append(s/p)
    return S,T

X = [10,70,30]
Y = [20,0,80]
S,T = erreur_triangle(X,Y,800,50,300)
plt.plot(S,T,marker = "+")
plt.show()
print(S,T)

        
    





    
    
