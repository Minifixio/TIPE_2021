import matplotlib.pyplot as plt 
import matplotlib.patches as patches

from Structures import PolygoneSimple, Point

#fig = plt.figure()
figure, axes = plt.subplots()

class Visualisation:
    def __init__(self, points):
        self.points = points
        self.polygone = PolygoneSimple(self.points)
        coords=self.polygone.extrait_coord()
        self.x_coords=coords[0]
        self.y_coords=coords[1]
        self.x_points = [] 
        self.y_points = []
        self.cercles = []
    
    # affiche le polygone dans mathplotlib
    def affiche(self):
        #plt.figure()
        plt.plot(self.x_coords, self.y_coords, zorder=1)
        plt.scatter(self.x_points, self.y_points, zorder=2)
        if len(self.cercles)>0:
            for cercle in self.cercles:
                centre=cercle[0]
                rayon=cercle[1]
                circle1 = plt.Circle(centre, rayon, color='b', fill=False)
                axes.add_patch(circle1)
        axes.set_aspect(1)
        plt.show()
    
    def add_point(self,x,y):
        self.x_points.append(x)
        self.y_points.append(y)
    
    def add_circle(self,centre,rayon):
        self.cercles.append((centre, rayon))

    def add_square(self,x,y,largeur,hauteur):
        rect = patches.Rectangle((x, y), largeur, hauteur, linewidth=1, edgecolor='r', facecolor='none')
        axes.add_patch(rect)