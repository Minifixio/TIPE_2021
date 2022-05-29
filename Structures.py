import numpy as np

class Point: 
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def dessin_point(self, canvas, taille, couleur = "red"):
        canvas.create_oval(self.x - taille, 
                            self.y - taille, 
                            self.x + taille, 
                            self.y + taille, 
                            fill = couleur)
    def __str__(self):
        return "(x={x}, y={y})".format(x = self.x, y = self.y)


class PolygoneSimple:
    # liste de points dans l'ordre de construction du polygone (le dernier rejoint le premier)
    # liste de la forme [(x,y),...,(x,y)]
    def __init__(self, points):
        self.points = []
        for pt in points:
            self.points.append(Point(pt[0], pt[1]))
        self.points.append(self.points[0]) # on ajoute le premier point pour fermer le polygone

    def extrait_coord(self):
        y_coord=[]
        x_coord=[]
        for pt in self.points:
            x_coord.append(pt.x)
            y_coord.append(pt.y)
        return (x_coord,y_coord)
    
class Polygone:
    exterieur=[]
    interieur=[]
    obstacles=[]
    def __init__(self, points, interieur=[], obstacles=[]):
        self.exterieur=self.convertir_point(points)
        self.interieur=self.convertir_point(interieur)
        self.obstacles=self.convertir_point(obstacles)
    
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
    
    def getExterieur(self):
        return self.exterieur

    def getInterieur(self):
        return self.interieur
    
    def getObstacles(self):
        return self.obstacles

    def print_points(self):
        res=''
        for p in (self.interieur + self.exterieur):
            res=res+'('+str(p.x)+','+str(p.y)+')'
        print(res)