from tkinter import *
import math
import random
from PIL import ImageTk
import PolygonUtils as polyutils
import Examples as examples
import copy 

x, y = None, None
poly = []
k=3
e=0.1
n1=100
n2=100
cercles=[]
t=5
debug_coords=False
debug_graph=False
canvas=None

def draw_line(event):
    global x,y
    
    if (x,y) == (None, None):
        x=event.x
        y=event.y
        canvas.create_oval(x-1,y-1,x+1,y+1,fill="blue", width=6)
        poly.append((x,y))
        
    else:
        x_next=event.x
        y_next=event.y
        canvas.create_line(x,y,x_next,y_next, fill="green", width=4)
        canvas.create_oval(x_next-1,y_next-1,x_next+1,y_next+1,fill="blue", width=6)
        x=x_next
        y=y_next
        poly.append((x,y))


def pos(a,b,c):
    if a >= b and a<= c:
        return 1
    elif a<= b and a>= c:
        return 1
    else:
        return 0

def in_circle(x,y,xc,yc,r):
    if math.sqrt((x-xc)**2+(y-yc)**2) <= r:
        return True
    else:
        return False

def circle_test(x,y):
    global cercles
    res=False
    if len(cercles)==0: 
        res=False
        return res
    else:
        for cercle in cercles:
            centre=cercle[0]
            if in_circle(x,y,centre[0],centre[1],cercle[1]):
                res=True
                #print('in circle', x,y,centre[0],centre[1],cercle[1])
                break
        return res

def circle_distance(x,y,xc,yc,r):
    d=math.sqrt((x-xc)**2+(y-yc)**2)
    return abs(d-r)

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
                if m!= 0:
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
    ne = len(X)
    xmin = min(X)
    xmax = max(X)
    ymin = min(Y)
    ymax = max(Y)
    for i in range(n1):
        x = random.uniform(xmin,xmax)
        y = random.uniform(ymin,ymax)
        c = 0
        for i in range(-1,ne-1):
                p = pos(y,Y[i],Y[i+1])
                if x <= X[i+1] + (y - Y[i+1])*(X[i]-X[i+1])/(Y[i]-Y[i+1]):
                    c = (c+p)%2
        if c == 1:
            l = []
            for i in range(k):
                l.append([random.randrange(ne),random.uniform(0,1)])
            l = sorted(l)
            for i in range(k):
                l[i][1] = 1 - l[i][1]
            """Px = []
            Py = []"""
            centres_intermediaires = []
            ray_intermediaires = []
            som = 0
            for i in range(k-1):
                Xi = []
                Yi = []
                for j in range(l[i][0]+1,l[i+1][0]+1):
                    Xi.append(X[j])
                    Yi.append(Y[j])
                t = l[i+1][1]
                Xi.append(t*X[l[i+1][0]] + (1-t)*X[(l[i+1][0] + 1)%ne])
                Yi.append(t*Y[l[i+1][0]] + (1-t)*Y[(l[i+1][0] + 1)%ne])
                Xi.append(x)
                Yi.append(y)
                t = l[i][1]
                Xi.append(t*X[l[i][0]] + (1-t)*X[(l[i][0] + 1)%ne])
                Yi.append(t*Y[l[i][0]] + (1-t)*Y[(l[i][0] + 1)%ne])
                centre, ray = cercle2(Xi,Yi,n2,e)
                centres_intermediaires.append(centre)
                ray_intermediaires.append(ray)
                som += ray
            Xi = []
            Yi = []
            for j in range(l[-1][0] + 1,ne):
                Xi.append(X[j])
                Yi.append(Y[j])
            for j in range(l[0][0] + 1):
                Xi.append(X[j])
                Yi.append(Y[j])
            t = l[0][1]
            Xi.append(t*X[l[0][0]] + (1-t)*X[(l[0][0] + 1)%ne])
            Yi.append(t*Y[l[0][0]] + (1-t)*Y[(l[0][0] + 1)%ne])
            Xi.append(x)
            Yi.append(y)
            t = l[-1][1]
            Xi.append(t*X[l[-1][0]] + (1-t)*X[(l[-1][0] + 1)%ne])
            Yi.append(t*Y[l[-1][0]] + (1-t)*Y[(l[-1][0] + 1)%ne])
            centre, ray = cercle2(Xi,Yi,n2,e)
            centres_intermediaires.append(centre)
            ray_intermediaires.append(ray)
            som += ray
            if som > smax:
                smax = som
                rayons_max = ray_intermediaires
                centres_max = centres_intermediaires
    return centres_max, rayons_max, smax

def cercle2(X,Y,k,e):
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

def cercle(X,Y,k,e,canvas,visu_state=False):
    global cercles, t
    t=t*2
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
            
            if visu_state:
                canvas.create_oval(x-1,y-1,x+1,y+1,fill="red", width=3)

            dmin = math.sqrt((xmax-xmin)**2 + (ymax-ymin)**2)
            c = 0
            for i in range(-1,ne-1):
                p = pos(y,Y[i],Y[i+1])
                if ((Y[i]-Y[i+1]) !=0) and (x <= X[i+1] + (y - Y[i+1])*(X[i]-X[i+1])/(Y[i]-Y[i+1])):
                    c = (c+p)%2
            
            if circle_test(x,y): c=0

            if c==1:
                for i in range(-1,ne-1):
                    x1,y1 = X[i], Y[i]
                    x2,y2 = X[i+1], Y[i+1]
                    if x1==x2:
                        print(x1)
                    else:
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

                for cercle in cercles:
                    cc=cercle[0]
                    d= circle_distance(x,y,cc[0],cc[1],cercle[1])
                    if d < dmin and not in_circle(x,y,cc[0],cc[1],cercle[1]):
                        dmin=d
                        T[1]=d

                if dmin > T[0]:
                    T[0] = dmin
                    centre = [x,y]
                    print(centre)
                    echec=0
                else:
                    echec += 1
        
        xmin, xmax = centre[0] - (xmax - xmin) / (math.sqrt(2) * 2), centre[0] + (xmax - xmin) / (math.sqrt(2) * 2) 
        ymin, ymax = centre[1] - (ymax - ymin) / (math.sqrt(2) * 2), centre[1] + (ymax - ymin) / (math.sqrt(2) * 2)
        
        if visu_state:
            canvas.create_rectangle(xmin, ymin, xmax, ymax, outline = 'blue')
            canvas.create_oval(centre[0]-1,centre[1]-1,centre[0]+1,centre[1]+1,fill="red", width=3)
            
        precision = min(xmax - xmin, ymax - ymin)
    
    cercles.append((centre,T[0]))
    return (centre, T[0])
    
def find_circle(canvas):
    global k, e, x, y, poly, debug_graph 
    
    print('finding centre')
    X=[]
    Y=[]
    if poly != []:
        print(poly)
        if x and y:
            canvas.create_line(x,y,poly[0][0],poly[0][1], fill="green", width=4)
        for p in poly:
            X.append(p[0])
            Y.append(p[1])
        c=cercle(X, Y, k, e, canvas, debug_graph)
        centre=c[0]
        xc=centre[0]
        yc=centre[1]
        r=c[1]
        canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
        canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'yellow')
        
    
def find_circle2(canvas):
    global k, e, x, y, poly, debug_graph, n1, n2

    print('finding centre2')
    X=[]
    Y=[]
    if poly != []:
        print(poly)
        if x and y:
            canvas.create_line(x,y,poly[0][0],poly[0][1], fill="green", width=4)
        for p in poly:
            X.append(p[0])
            Y.append(p[1])
        c=centre_multiple(X, Y, n1, n2, k, e)
        centres=c[0]
        rayons=c[1]
        print(c)
        for i in range(len(centres)):
            xc=centres[i][0]
            yc=centres[i][1]
            r=rayons[i]
            canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
            canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'red')
    
def motion(event):
    global debug_coords
    if debug_coords:
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
    
def switch_debug_coords(event):
    global debug_coords
    debug_coords= not debug_coords
    
def test_polygon(data):
    print("Test polygon")
    global k, e, x, y, debug_graph, canvas
    X1,Y1 = [], []
    X2,Y2 = [], []
    for p in data[0]:
        X1.append(p[0])
        Y1.append(p[1])
    polyutils.draw_polygon(data[0], canvas)
    
    for p in data[1]:
        X2.append(p[0])
        Y2.append(p[1])
    polyutils.draw_polygon(data[1], canvas)

    X=X1+X2
    Y=Y1+Y2
    
    c=cercle(X, Y, k, e, canvas, debug_graph)
    centre=c[0]
    xc=centre[0]
    yc=centre[1]
    r=c[1]
    canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
    canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'red')

def main(background=None):
    global canvas
    root = Tk()
    root.title('Dessin')
    root.geometry("1500x1000")
    canvas=Canvas(root, width=1500, height=1000)

    if background:
        image = PhotoImage(file = "captures/capture"+str(background)+".png").subsample(2, 2)
        canvas.create_image(0, 0, image = image, anchor = NW)
        
    canvas.grid(row=0, column=0)
    canvas.bind('<Button-1>', draw_line)
    root.bind('r', lambda i: find_circle(canvas))
    root.bind('p', lambda i: find_circle2(canvas))
    root.bind('<Motion>', motion)
    root.bind('d', switch_debug_coords)
    root.mainloop()

def affichage_data(poly, n):
    for i in range(n):
        affiche_affinage(poly, i)
        
def affiche_affinage(poly, aff):
    poly_cop=copy.copy(poly) 
    poly_cop.affinage_exterieur(aff)
    pt=poly_cop.getExterieur()
    X,Y=[],[]
    res="{ \"sites\":["
    for i in range(len(pt)):
        X.append(abs(pt[i].x))
        Y.append(abs(pt[i].y))
        if i==len(pt)-1:
            res+=str(abs(pt[i].x))+","+str(abs(pt[i].y))
        else:
            res+=str(abs(pt[i].x))+","+str(abs(pt[i].y))+","
    print(X)
    print(Y)
    res+="],\"queries\":[]}"
    print(res)

def trouve_poly_simple(polypara, canvas):
    global poly
    poly=polypara
    polyutils.draw_polygon(poly, canvas)
    find_circle(canvas)
    
def trouve_poly_multi(polypara, canvas):
    global poly
    poly=polypara
    polyutils.draw_polygon(poly, canvas)
    find_circle2(canvas)

def trace_multi(polypara, result):
    global poly
    poly=polypara
    centres=result[0]
    rayons=result[1]
    polyutils.draw_polygon(poly, canvas)
    for i in range(len(centres)):
        xc=centres[i][0]
        yc=centres[i][1]
        r=rayons[i]
        canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
        canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'red')
        
def trace_resultat_voronoi(centre, rayon, poly):
    global canvas
    polyutils.draw_polygon(poly.interieur, canvas)
    polyutils.draw_polygon(poly.exterieur, canvas)
    x=centre[0]
    y=centre[1]
    canvas.create_oval(x-1,y-1,x+1,y+1,fill="black", width=1)
    canvas.create_oval(x-rayon,y-rayon,x+rayon,y+rayon, width=3, outline = 'yellow')
    
