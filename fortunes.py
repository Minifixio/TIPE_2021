import math
from tkinter import *
import numpy as np
import sys
from Structures import Point
from PolygonUtils import affiner_poly
from TkinterUtils import *
from Examples import *

# VARIABLES GLOBALES
y_pos=None # La position y de la ligne de passage
Queue=None # La queue des événements
Racine=None # L'arbre de la beachline
Voronoi=None # La DCEL du diagramme
Sommets=[] # Sommets du diagramme
debug_logs=False # Afficher les infos de debug
debug_coords=False # Affiche les coordonées du pointeur dans le terminal
debug_grap=False
debug_aretes=False # Aficher les aretes (certaines sont buguées pour l'instant mais c'est pour l'esthétique car ce qui nous interesse c'est les points)
eps=0.00001 # Epsilon
cvs=None #Le canvas global
dessin_on=False #Est-on en mode dessin

y_max=1000 # Les bordures du cadre
x_max=1000 # Les bordures du cadre


# OBJETS
class Arete:   
    valide = False # Pour savoir quand l'arete est achevée
    
    # Forme de la droite bissectrie du segment [gauche, droite]:
    # Formule : y = m * x + k
    m = None
    k = None
    
    # Point d'origine et de fin
    origine = None
    fin = None # initialisé à None, remplit à la complétion d'un circle event
    
    # Initialisation de l'arête à partir de deux point de l'espace
    # droite : point à droite du segment
    # gauche : point à gauche du segment
    # origine_x : abscisse du point d'origine associé
    def __init__(self, gauche, droite, origine_x = None):
        self.gauche = gauche
        self.droite = droite

        # équation de la bissectrice des deux points
        if droite.y == gauche.y: # Cas particulier ou les deux points sont sur la même ordonnée Y
            self.m = math.inf
            
            ## A REVOIR PRECISEMENT
            self.k = 0
        else:
            self.m = - (gauche.x - droite.x) / (gauche.y - droite.y)
            self.k = (0.5 * (gauche.x ** 2 - droite.x ** 2 + gauche.y ** 2 - droite.y ** 2)) / (gauche.y - droite.y)
        
        if origine_x != None:
            self.origine = Point(origine_x, self.calcul_y(origine_x))
          
    # y=mx+k          
    def calcul_y(self, x):
        if self.m == math.inf: 
            return None
        else: 
            return x * self.m + self.k
        
    # x=(y-k)/m  
    def calcul_x(self, y):
        if self.m == math.inf: 
            return self.origine.x
        else: 
            return (y - self.k) / self.m 
            
    def achever(self, fin):
        self.fin = fin
        self.valide = True
    
    def __str__(self):            
        return "Arete: ori={origine}, fin={fin}".format(origine = self.origine, fin = self.fin)
    
class CercleEvnt(Point):
    # parabole : la parabole qui a généré l'event
    # centre : le centre du cercle
    # x,y : les corrdonnées du bas du cercle
    
    #      .───────.                  
    #    ,'         `.                
    #  ,'             `.              
    # ;                 :             
    # │                 │   ┌────────┐
    # │        ◀────────┼───┤ centre │
    # :                 ;   └────────┘
    #  ╲               ╱              
    #   `.           ,'               
    #     `.       ,'                 
    #       `─────'                   
    #          ▲                      
    # ┌────────┴────────┐             
    # │  bas du cercle  │             
    # └─────────────────┘ 
    
                
    def __init__(self, x, y, parabole, centre):
        super().__init__(x, y)
        self.parabole=parabole
        self.centre=centre
        self.actif=True

    def __str__(self):
        return "Circle Event : {point}".format(point = super(CercleEvnt, self).__str__())
    
class SiteEvnt(Point):
    def __init__(self, x, y, parabole=None):
        super().__init__(x, y)
        self.parabole=parabole
        self.id = ""

    def __str__(self):
        return "Site Event -> point:{point} / parabole:{para}".format(point = super(SiteEvnt, self).__str__(), para=self.parabole.__str__())

class Parabole:
    # site : le point directeur de la parabole
    # prec : la parabole précédente dans le défilement gauche droite des paraboles
    # suiv : la parabole suivante dans le défilement gauche droite des paraboles
    # ar_droite / ar_gauche : arete droite / gauche
    # evnt : si la parabole est lié à un circle event
    
    # On fait une liste chaînée des paraboles : -prec est la parabole de gauche dans la file
    #                                           -suiv est la parabole de droite dans la file
    
    prec = None
    suiv = None
    evnt = None
    
    def __init__(self, site, prec=None, suiv=None, ar_gauche=None, ar_droite=None):
        self.site = site
        self.prec = prec
        self.suiv = suiv
        self.ar_droite = ar_droite
        self.ar_gauche = ar_gauche
        
    # Retourne a, b et c 
    # solution de y=ax^2+bx+c pour la parabole   
    def expr_poly(self, y_actuel):
        xs=self.site.x
        ys=self.site.y
        if ys != y_actuel:
            g=1/(2*(ys-y_actuel))
            a=1*g
            b=-2*xs*g
            c=(ys**2 - y_actuel**2 + xs**2)*g
            return a, b, c
        else:
            g=math.inf
            # On retourne None si les deux paraboles sont au même y
            return None, None, None

    
    def __str__(self):
        return "Parabole : site = {site}, précédente ? {a_prec}, suivante ? {a_suiv}".format(site = self.site, a_prec = self.prec != None, a_suiv = self.suiv != None)

# Gestion de la pile d'évènements
class QueueOfEvents:
    queue=[]
    def __init__(self, points):
        sites=[ SiteEvnt(p.x,p.y) for p in points ]    
        sites.sort(key=lambda p: p.y)
        self.queue=sites
        self.fix_meme_coord()
        
    def fix_meme_coord(self):
        for i in range(1,len(self.queue)):
            if self.queue[i].y==self.queue[i-1].y:
                self.queue[i].y=self.queue[i].y+0.1

    def vide(self):
        if len(self.queue)==0:
            return True
        else:
            return False
    
    # Insertion de l'évènement de façon ordonnée par rapport à sa coordonnée Y (utiliser une pile binaire à la place)
    def insert(self, evnt):
        i=0
        while i<len(self.queue):
            if self.queue[i].y >= evnt.y:
                break
            else:
                i+=1
        self.queue= self.queue[:i] + [evnt] + self.queue[i:]
    
    # Retire le premier élément de la queue et le retourne
    def pop(self):
        if self.vide():
            return False
        else:
            x=self.queue.pop(0)
            return x
    
    def remove(self, evnt):
        try:
            self.queue.remove(evnt)
        except ValueError:
            return
    
    def debug(self):
        debug("Dumping de la pile : ")
        for event in self.queue:
            debug(event)

def find_new_y(p, x):
    global y_pos, eps
    dp = 2.0 * (p.y - y_pos)
    b1 = -(2 * float(p.x)) / float(dp or eps)
    c1 = y_pos + float(dp/4.0) + (p.x**2) / float(dp or eps)
    return float(x**2) / float(dp or eps) + float(b1*x) + c1

def para_intersect_x(para1, para2, y=None):
    global y_pos, eps
    if not y: y=y_pos
    
    if para1.site.y == y:
        y=y+eps

    a1,b1,c1=para1.expr_poly(y)
    a2,b2,c2=para2.expr_poly(y)

    # Si a2==None, la Beachline est actuellement à la position y_pos=para2.site.y
    # Donc le point d'intersection avec para2 est le site de cette même parabole
    if a2 == None:
        return para2.site.x
    else:
        a=a1-a2
        b=b1-b2
        c=c1-c2
        
        det = b*b - 4*a*c

        # Si det<0, cela signifie (étude empirique) que para2.site.y est quasiment égal à y_pos
        # les valeurs renvoyées par expr_poly sont alors de l'odre de math.inf d'ou le signe <0
        if det<0:
            # print(a2,b2,c2)
            # print(para1.__str__())
            # print(para2.__str__())
            # print(y_pos)
            # print('Déterminant négatif', det)
            return para2.site.x
        else:
            if a==0:
                if c==0:
                    return para2.site.x
                else:
                    return -c/b
                
            x1=(-b-math.sqrt(det))/(2*a)
            x2=(-b+math.sqrt(det))/(2*a)
            
            # On prend toujours l'intersection de droite
            if para1.site.y < para2.site.y:
                return min(x1, x2)
            else:
                return max(x1, x2)

def traite_site_evnt(evnt):
    global Racine, Voronoi, Queue

    debug("Site event -> Traitement du site {}".format(evnt))
    
    # Si c'est le premier évènement traité, on a pas encore de racine dans le graphe des paraboles
    if Racine == None:
        Racine = Parabole(evnt) # Création de la première parabole et affectation à la racine
        debug("Site Event -> Pas encore de parabole, création de la première. " + Racine.__str__())
        return

    # Sinon, recherche de la parabole qui est directement au dessus du site en cours de traitement, et qui va être divisée
    parabole = Racine
    while parabole.suiv != None and para_intersect_x(parabole, parabole.suiv) <= evnt.x:
        parabole = parabole.suiv
    debug("Site Event -> Parabole à l'aplomb trouvée : {parabole}.".format(parabole = parabole))

    # Création des deux arrêtes opposées à partir de ce point d'intersection
    arete_gauche = Arete(parabole.site, evnt, evnt.x)
    arete_droite = Arete(evnt, parabole.site, evnt.x)
    
    # Réordonne les paraboles : parabole.prec <-> parabole <-> parabole_evnt <-> parabole_droite <-> parabole.suiv

    # Création de la parabole associé au site traité et la parabole trouvée devient la parabole gauche de cette nouvelle parabole
    parabole_evnt = Parabole(evnt, parabole, None, arete_gauche, arete_droite)
    parabole_extreme_droite = parabole.suiv
    parabole.suiv = parabole_evnt
    parabole.ar_droite = arete_gauche

    # Découpe la parabole trouvée en deux, avec les arêtes au milieu
    parabole_droite = Parabole(parabole.site, parabole_evnt, parabole_extreme_droite, arete_droite, parabole_extreme_droite.ar_gauche if parabole_extreme_droite else None) 
    parabole_evnt.suiv = parabole_droite
    if parabole_extreme_droite: 
        parabole_extreme_droite.prec = parabole_droite
        if parabole_extreme_droite.ar_gauche.valide == False:
            parabole_extreme_droite.ar_gauche = arete_droite
    
    # Parabole r est coupée :
    #  X                   X   X                   X   X                   X               
    #  X                 X     X                 X     X                 X                      
    #  X                 X     X                 X     X                 X                    
    #   X               X       X               X       X               X             
    #    XX           XX        X             XX                      XX         X
    #     X           X         X             X                       X          X
    #      XX       XX   +--->  X   X       XX     ---      X       XX     ---   X   X
    #        XX   XX            X   XXX   XX                 XX   XX             X   X
    #          XXX               X X   XXX                     XXX                X X
    #                            X X                                              X X
    #                            X X                                              X X
    #     X                       X                                                X
    #
    # Parabole r de départ      Rajout de evnt            Les deux paraboles     para1 
    #                                                       r et para2           à part
    #                                                        séparées
    
    # On enlève les possibles circle events associés
    if parabole.evnt:
        Queue.remove(parabole.evnt)
        parabole.evnt.actif=False
        parabole.evnt=None
        
    creer_cercle_evnt(parabole)
    creer_cercle_evnt(parabole_droite)
    #creer_cercle_evnt(parabole_evnt)

    Voronoi.append(arete_gauche)
    Voronoi.append(arete_droite)

# Création d'un "Circle" event, c'est à dire une ordonnée Y correspondant au cercle passant par les trois sites formés par les sites de la parabole à gauche, la courante et celle à droite du site de la parabole courante
def creer_cercle_evnt(parabole):
    global y_pos, y_max, Queue, debug_grap, cvs, dessin_on

    debug("Création d'un circle event. " + parabole.__str__())
    
    # Il faut trois sites pour pouvoir produire un Circle events
    if parabole.prec == None or parabole.suiv == None: return
    
    # Extraction des trois sites à utiliser pour trouver le cercle inscrit
    site_gauche = parabole.prec.site
    site_parabole = parabole.site
    site_droit = parabole.suiv.site
    
    # Est il possible de créer un cercle inscrit passant par les trois sites
    # Calcul du determinant des trois points pour voir si ils sont dans le sens antihoraire
    if ((site_parabole.x - site_gauche.x) * (site_droit.y - site_gauche.y) - (site_droit.x - site_gauche.x) * (site_parabole.y - site_gauche.y) <= 0):
        return
    
    # Si la parabole courant n'a pas d'arête gauche ou droite, pas de Circle Event
    #if parabole.ar_gauche == None or parabole.ar_droite == None: return
    
    # Le centre du cercle est à l'intersecion des arêtes de la parabole traitéee (à vérifier...)
    centre_cercle = intersection_aretes(parabole.ar_gauche, parabole.ar_droite)
    if centre_cercle==None or parabole.site==None: return
    else : rayon = math.sqrt((centre_cercle.x - parabole.site.x) ** 2 + (centre_cercle.y - parabole.site.y) ** 2)
    
    if debug_grap and dessin_on:
        cvs.create_oval(centre_cercle.x - rayon,
                        centre_cercle.y - rayon,
                        centre_cercle.x + rayon,
                        centre_cercle.y + rayon,
                        outline = "grey",
                        dash=(3,5),
                        width = 1)
    
    # On détermine l'ordonnée Y de la tangente afin de positionner le circle event dans la pile
    evnt_position_y = rayon + centre_cercle.y
    
    # Cette position doit être après la beach line (et plus petite que la limite i.e evnt_position_y<y_max mais elevé pour l'instant)
    if evnt_position_y > y_pos:
        cirle_event = CercleEvnt(centre_cercle.x, evnt_position_y, parabole, centre_cercle)
        parabole.evnt = cirle_event
        #parabole.prec.evnt = cirle_event
        #parabole.suiv.evnt = cirle_event
        debug("Circle event ajoutée à la pile. " + cirle_event.__str__())
        Queue.insert(cirle_event)

# Permet de déterminer le point d'intersection de deux arêtes
def intersection_aretes(arete_1, arete_2):
    if arete_1.m == math.inf: 
        return Point(arete_1.origine.x, arete_2.calcul_y(arete_1.origine.x))
    else:
        if arete_2.m == math.inf:
            return Point(arete_2.origine.x, arete_1.calcul_y(arete_2.origine.x))
        else:
            dir_dif = arete_1.m - arete_2.m
            if dir_dif == 0: return None
            x = (arete_2.k - arete_1.k) / dir_dif
            y = arete_1.calcul_y(x)
            return Point(x, y)

# Traitement d'un Circle Event
def traite_cercle_evnt(evnt):
    global Voronoi, Sommets, Queue

    debug("Cercle event -> Traitement du cercle induit par le site {}".format(evnt.parabole.site))

    parabole = evnt.parabole # Parabole qui a créé cet event
    
    # On désactive les circle event des paraboles adjacentes, car ils ne sont plus nécessaires
    if parabole.prec.evnt: 
        Queue.remove(parabole.prec.evnt)
        parabole.prec.evnt.actif = False
    if parabole.suiv.evnt: 
        parabole.suiv.evnt.actif = False
        Queue.remove(parabole.suiv.evnt)

    # Création d'une nouvelle arête entre deux sites des paraboles adjacentes et on les relie aux paraboles associées
    nouvelle_arete = Arete(parabole.prec.site, parabole.suiv.site)
    nouvelle_arete.origine = evnt.centre
    
    # On ajuste la beachline en retirant cette parabole
    parabole.prec.ar_droite = nouvelle_arete
    parabole.suiv.ar_gauche = nouvelle_arete
    parabole.prec.suiv = parabole.suiv
    parabole.suiv.prec = parabole.prec
    
    Voronoi.append(nouvelle_arete)
    
    if not point_dehors(evnt.centre):
        Sommets.append(evnt.centre)
    
    # Les arêtes liées à la parabole courante sont maintenant achevées
    parabole.ar_droite.achever(evnt.centre)
    parabole.ar_gauche.achever(evnt.centre)
    
    creer_cercle_evnt(parabole.prec)
    creer_cercle_evnt(parabole.suiv)
        
# Certaines arêtes ne sont pas terminée lors de l'exécution, cela permet de les tracer en fonction de leur équation
# Pas 100% fonctionnel encore
def terminer_aretes():
    global Voronoi, x_max, y_max
    
    for ar in Voronoi:
        # A VERIFIER PRECISEMENT
        if ar.origine.y==None:
            return
        else:
            if ar.fin == None and not point_dehors(ar.origine) and not ar.valide:
                yl = ar.calcul_y(x_max)
                if ar.k >= 0:
                    if yl>y_max:
                        xl=ar.calcul_x(y_max)
                        yl=y_max
                    else:
                        xl=x_max
                    ar.achever(Point(xl,yl))
                else:
                    yl=ar.calcul_y(x_max)
                    if yl<0:
                        xl=ar.calcul_x(0)
                        yl=0
                    else:
                        xl=x_max
                    ar.achever(Point(xl,yl))
        
def point_dehors(point):
    global x_max, y_max
    return point.x < 0 or point.x > x_max or point.y < 0 or point.y > y_max
    
# Fonction principale
def fortunes(points, xmax=None, ymax=None, canvas=None):
    global Queue, Racine, Voronoi, y_pos, Sommets, x_max, y_max
    
    if xmax!=None and ymax!=None:
        x_max=xmax
        y_max=ymax
        
    Queue = QueueOfEvents(points)
    Voronoi=[]
    
    while not Queue.vide():
        event = Queue.pop()
        y_pos = event.y
        debug("Traitement d'un nouvel évènement. Position de la beach_line = {}".format(y_pos))
        debug(event)
        if isinstance(event, SiteEvnt):
            traite_site_evnt(event)
        else:
            if event.actif:
                traite_cercle_evnt(event)
            else:
                print(event.__str__())
    
    # terminer_aretes()
    # for arete in Voronoi:
    #     if arete:
    #         if debug_aretes and canvas:
    #             dessin_arete(arete, canvas)
    #         if debug_logs:
    #             debug(arete)
    #         if debug_grap and canvas:
    #             dessin_ori_arete(arete, canvas)
    
    #print([i.__str__() for i in Sommets])
    
    return Sommets
        
## Fonctions d'utils / GUI

def convertir_point(points_t):
    res=[]
    for p in points_t:
        res.append(Point(p[0], p[1]))
    return res

def debug(data):
    global debug_logs
    if debug_logs:
        print(data)

def coeff_droite(p1, p2):
    if p1.x == p2.x:
        return 0
    else:
        return (p2.y-p1.y)/(p2.x-p1.x)

# droite y=kx+m 
# renvoi (x,y(x))
def point_droite(k, m, x):
    return Point(x, k*x + m)
    
def dessin(data, interieur=None):
    global Voronoi, Sommets, cvs, dessin_on
    dessin_on = True
    root = Tk()
    root.title('VORONOI')
    root.geometry("1000x1000")
    root.bind('<Escape>', lambda i: sys.exit(0))
    cvs=Canvas(root, width=1000, height=1000, background="white")
    cvs.grid(row = 0, column = 0)

    if isinstance(data[0], tuple):
        points = convertir_point(data)
    else:
        points=data
    
    dessin_poly(points, cvs)
    
    if interieur:
        if isinstance(data[0], tuple):
            inte_points=convertir_point(interieur)
        else:
            inte_points=interieur
        dessin_poly(inte_points, cvs)
        points=points+inte_points
    
    for point in points:
        dessin_point(point, 5, cvs)
        
    fortunes(points, cvs)
    
    debug('Longueur résultat : ' + str(len(Voronoi)))
    
    debug('Résultat avant compression :')
    for arete in Voronoi:
        if arete:
            if debug_logs:
                debug(arete)
         
    #terminer_aretes()
    
    debug('Résultat après compression :')
    for arete in Voronoi:
        if arete:
            if arete.fin==None:
                print(arete.__str__())
            if debug_aretes:
                dessin_arete(arete, cvs)
            if debug_logs:
                debug(arete)
            if debug_grap:
                dessin_ori_arete(arete, cvs)
                
    # Ce sont les points verts ceux de Voronoi
    for sommet in Sommets:
        dessin_point(sommet, 8, cvs, couleur="green")
    
    root.bind('<Button 1>', coord_souris)
    root.bind('<Motion>', mouvement)
    root.mainloop()
    


#dessin(affiner_poly(read_from_file('voronoi_test/save.dat'), 30))
#write_to_file('voronoi_test/export.dat', affiner_poly(read_from_file('voronoi_test/save.dat'), 1))
#test_affinage(poly2, 5)

# dessin(
#     affiner_poly(convertir_point(poly7), 10), 
#     interieur=affiner_poly(convertir_point(inte_poly7), 10)
#     )

# TODO:
# - Tracer correctement les arêtes (pour l'esthétique)
# - Déterminant de l'orientation d'un polygone à comprendre (dans creer_cercle_evnt deuxième if)