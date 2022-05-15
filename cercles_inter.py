from tkinter import *
import math
import random

x, y = None, None
poly = []
k=100
e=0.01
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
        poly.append((x,y))
        
    else:
        x_next=event.x
        y_next=event.y
        canvas.create_line(x,y,x_next,y_next, fill="green", width=2)
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

            # if c==0:
            #     canvas.create_oval(x-1,y-1,x+1,y+1,fill="red", width=3)
            # else:
            #     canvas.create_oval(x-1,y-1,x+1,y+1,fill="green", width=3)
                
            if c==1:
                for i in range(-1,ne-1):
                    x1,y1 = X[i], Y[i]
                    x2,y2 = X[i+1], Y[i+1]
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
                    #print(x,y,centre[0],centre[1],cercle[1],d)
                    if d < dmin and not in_circle(x,y,cc[0],cc[1],cercle[1]):
                        #canvas.create_oval(x-1,y-1,x+1,y+1,fill="black", width=t)
                        dmin=d
                        T[1]=d

                if dmin > T[0]:
                    T[0] = dmin
                    centre = [x,y]
                    print(centre)
                    echec=0
                else:
                    #canvas.create_oval(x-1,y-1,x+1,y+1,fill="red", width=t)
                    echec += 1
        
        xmin, xmax = centre[0] - (xmax - xmin) / (math.sqrt(2) * 2), centre[0] + (xmax - xmin) / (math.sqrt(2) * 2) 
        ymin, ymax = centre[1] - (ymax - ymin) / (math.sqrt(2) * 2), centre[1] + (ymax - ymin) / (math.sqrt(2) * 2)
        
        if visu_state:
            canvas.create_rectangle(xmin, ymin, xmax, ymax, outline = 'blue')
            canvas.create_oval(centre[0]-1,centre[1]-1,centre[0]+1,centre[1]+1,fill="red", width=3)
            # self.visu.add_point(centre[0],centre[1])
            # self.visu.add_square(xmin, ymin,  xmax-xmin, ymax-ymin)
            
        precision = min(xmax - xmin, ymax - ymin)
    
    cercles.append((centre,T[0]))
    print(cercles)
    return (centre, T[0])
    
def find_circle(canvas):
    global k, e, x, y, poly, debug_graph 
    
    print('finding centre')
    X=[]
    Y=[]
    if poly != []:
        print(poly)
        canvas.create_line(x,y,poly[0][0],poly[0][1], fill="green", width=2)
        for p in poly:
            X.append(p[0])
            Y.append(p[1])
        c=cercle(X, Y, k, e, canvas, debug_graph)
        centre=c[0]
        xc=centre[0]
        yc=centre[1]
        r=c[1]
        canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
        canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'red')
        #poly=[]
    
def motion(event):
    global debug_coords
    if debug_coords:
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
    
def switch_debug_coords(event):
    global debug_coords
    debug_coords= not debug_coords
    
    
def draw_polygon(data):
    global canvas
    print("Drawing polygon")
    for i in range(len(data)-1):
        x1=data[i][0]
        y1=data[i][1]
        x2=data[i+1][0]
        y2=data[i+1][1]
        canvas.create_line(x1,y1,x2,y2, fill="green", width=2)
        canvas.create_oval(x1-1, y1-1, x1+1, y1+1, fill="red")
        canvas.create_oval(x2-1, y2-1, x2+1, y2+1, fill="red")
    canvas.create_line(data[-1][0], data[-1][1], data[0][0], data[0][1], fill="green", width=2)

    
def test_polygon(data):
    print("Test polygon")
    global k, e, x, y, debug_graph, canvas
    X1,Y1 = [], []
    X2,Y2 = [], []
    for p in data[0]:
        X1.append(p[0])
        Y1.append(p[1])
    draw_polygon(data[0])
    
    for p in data[1]:
        X2.append(p[0])
        Y2.append(p[1])
    draw_polygon(data[1])

    X=X1+X2
    Y=Y1+Y2
    
    c=cercle(X, Y, k, e, canvas, debug_graph)
    centre=c[0]
    xc=centre[0]
    yc=centre[1]
    r=c[1]
    canvas.create_oval(xc-1,yc-1,xc+1,yc+1,fill="black", width=1)
    canvas.create_oval(xc-r,yc-r,xc+r,yc+r, width=3, outline = 'red')

def main():
    global canvas
    root = Tk()
    root.title('Dessin')
    root.geometry("1000x1000")
    canvas=Canvas(root, width=1000, height=1000, background="white")
    canvas.grid(row=0, column=0)
    canvas.bind('<Button-1>', draw_line)
    root.bind('r', lambda i: find_circle(canvas))
    root.bind('<Motion>', motion)
    root.bind('d', switch_debug_coords)
    root.bind('t', test_polygon(poly_c5))
    root.mainloop()

poly_c5=(
    [(319, 118), (243, 76), (109, 81), (47, 278), (301, 555), (263, 663), (285, 714), (710, 713), (760, 591), (826, 474), (906, 434), (909, 298), (824, 134), (620, 81), (569, 217), (463, 330), (351, 330), (324, 255)],
    [(817, 392), (839, 379), (857, 297), (761, 175), (663, 181), (634, 251), (602, 341), (590, 426), (646, 466)]
)

