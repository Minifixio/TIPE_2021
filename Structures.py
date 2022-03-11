# coding=utf-8
# Types des données
class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y

class Sommet:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.areteIncidente # une arrete qui a pour origine ce sommet

class Arete: # en realite une demi-arrete de p1 vers p2
    def __init__(self, p1, p2):
        self.precedent = None # l'arete précédente dans le chainage arrivant à p1
        self.jumelle = None # arete qui va de p2 vers p1 paralle, dans le sens inverse
        self.suivant = None # arete suivante dans le chainage partant de p2
        self.face = None # face à la droite de l'arrête

    def getDestination(self):
        return self.suivant
    
    def getOrigine(self):
        return self.precedent

class Face:
    def __init__(self):
        self.arrete=None

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
        
class Noeud:        
    def __init__(self, val):
        self.racine=val
        self.parent=None
        self.gauche=None
        self.droite=None
    
    def add_gauche(self, val):
        if self.gauche==None:
            self.gauche=Noeud(val)
        else:
            perm_arbre=Noeud(val)
            perm_arbre.add_gauche(self.gauche)
            self.gauche=perm_arbre

    def add_droite(self, val):
        if self.droite==None:
            self.droite=Noeud(val)
        else:
            perm_arbre=Noeud(val)
            perm_arbre.add_gauche(self.droite)
            self.droite=perm_arbre

class Pile:
    def __init__(self):
        self.vider_pile()

    def test_vide(self):
        return self.pile==[]

    def vider_pile(self):
        self.pile=[]
    
    def empiler(self, val):
        self.pile.append(val)
    
    def depiler(self):
        if self.test_vide():
            return None
        else:
            return self.pile.pop()
    
    def taille_pile(self):
        return len(self.pile)

class SiteEvent:
    def __init__(self, point):
        self.point=point
        self.priority=self.point.y # Les événements sont triés selon leur y croissants (voir defilement de la ligne sweep)
    
class QueueEvenements:
    def __init__(self):
        self.queue=Pile()
    
    def add_evenement(self, evenement):
        temp_pile=Pile()
        i=self.queue.taille_pile()
        # On ajoute les evenements selon leur y croissants
        while i>0:
            el=self.queue.depiler()
            temp_pile.empiler(el)
            # lorsqu'on trouve le y tel que notre evenement ait une priorite juste superieure, on l'ajoute
            if el.priority<evenement.priority:
                for i in range(temp_pile.taille_pile-1):
                    val=temp_pile.depiler()
                    self.queue.empiler(val)
                break
            i=(i-1)
        self.queue.empiler(evenement)
    
    def get_evenement(self):
        return self.queue.depiler()

    def initialiser_sommets(self, sommets):
        # On ajoute tous les sommets
        # sommets_tries=sorted(sommets, key=lambda sommet: sommet.y)
        for sommet in sommets:
            self.add_evenement(sommet)

class ArbreSommets:
    # sommet represente le premier sommet que l'on va ajouter dans l'arbre 
    # i.e le premier sommet de la liste selon y
    def __init__(self, sommet): 
        self.arbre=Noeud(sommet)