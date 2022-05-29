def dessin_point(point, taille, canvas, couleur = "red"):
    x = point.x
    y = point.y
    canvas.create_oval(x - taille, 
                           y - taille, 
                           x + taille, 
                           y + taille, 
                           fill = couleur)

def dessin_cercle(centre, rayon, canvas, couleur="black", type=None, epaisseur=1):
    canvas.create_oval(centre.x - rayon, 
                        centre.y - rayon, 
                        centre.x + rayon, 
                        centre.y + rayon, 
                        width=epaisseur,
                        outline=couleur)

def dessin_arete(arete, canvas):    
    if arete.fin == None or arete.origine == None:
        return
    else:
        o=arete.origine
        f=arete.fin
        canvas.create_line(o.x, o.y, f.x, f.y, fill = "green", width=2)

def dessin_ori_arete(arete, canvas):
    dessin_point(arete.origine, 2, canvas, couleur="orange")

def dessin_poly(poly, canvas, couleur="blue", epaisseur=2, debug_points=False):
    for i in range(len(poly)-1):
        p1=poly[i]
        p2=poly[i+1]
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill = couleur, width=epaisseur)
        if debug_points:
            dessin_point(p1, 4, canvas, "green")
            dessin_point(p2, 4, canvas, "green")

    canvas.create_line(poly[-1].x, poly[-1].y, poly[0].x, poly[0].y, fill = couleur, width=epaisseur)

def mouvement(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
      
def coord_souris(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))