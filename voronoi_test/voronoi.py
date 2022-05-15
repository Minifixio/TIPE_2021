################################################################################
#                           VORONOI DIAGRAM GENERATION                         #
#                                Mattias Lundberg                              #
#                                                                              #
#                      Run with Python 2.7 and tkinter toolkit                 #
#                                                                              #
################################################################################

from Tkinter import *
import math, sys, random, tkFileDialog, time
import heapq as hq

### SETTINGS ###
width=600; height=600
EPS = .000001 # Avoid zero division
file_opt = {'filetypes': [('save files', '.dat')], 'initialfile': 'save.dat'}


### DATATYPES ###
class Point(object):
	""" Represent a single point in 2d space """
	def __init__(self, x_, y_):
		super(Point, self).__init__()
		self.x = x_; self.y = y_
	
	""" Formatted printing """
	def __str__(self): return '%s %s' % (int(round(self.x)), int(round(self.y)))
	def __repr__(self): return '%s %s' % (int(round(self.x)), int(round(self.y)))
	def __cmp__(self, other):
		if self.y < other.y or (self.y == other.y and self.x < other.x): return 1
		elif self.y > other.y or (self.y == other.y and self.x > other.x): return -1
		else: return 0
	
	def draw(self, large=False): # Draw the point
		if large: canvas.create_oval(self.x-2, self.y-2, self.x+2, self.y+2)
		else: canvas.create_oval(self.x-.5, self.y-.5, self.x+.5, self.y+.5)

class Edge(object): # Edge to be in the final voronoi diagram
	def __init__(self,start,left,right):
		self.start = start; self.left = left; self.right = right
		# k and m are expected line direction, y = kx + m
		self.k = 2**31 if left.y == right.y else float(right.x - left.x) / float(left.y - right.y)
		self.m = float(start.y - self.k * start.x)
		self.xdir = float(right.y - left.y)
		self.ydir = float(left.x - right.x)
		self.neighbour = self.end = None
	
	""" Formatted printing """
	def __str__(self): return '{%s, %s}' % (self.start, self.end)
	def __repr__(self): return '{%s, %s}' % (self.start, self.end)
	
	def draw(self): # Draw the edge as a line.
		if self.start is not None and self.end is not None: draw_line(self.start, self.end)

class Event(Point):
	""" Generic event type. """
	def __init__(self,x_,y_): super(Event, self).__init__(x_,y_)

class SiteEvent(Event):
	""" Site event """
	def __init__(self,x,y): super(SiteEvent, self).__init__(x,y)

class CircleEvent(Event):
	""" Circle event """
	parabola = None
	def __init__(self,x,y): super(CircleEvent, self).__init__(x,y)

class Parabola(object):
	""" A parabola connected to a point used in the beachline """
	left = right = edge = ce = parent = None
	def __init__(self, site=None):
		self.site = site
		self.leaf = site is not None
	def set_left(self, par):
		self.left = par
		par.parent = self
	def set_right(self, par):
		self.right = par
		par.parent = self

### GLOBALS ###
evntq = []; root = None; edges = []; points = []; curr_y = None

### DIAGRAM GENERATION ###
def generate_voronoi():
	""" Use fortune sweep (down->up) to calculate voronoi diagram. """
	global curr_y, evntq, root, edges; root = None; edges = []
	
	if len(points) <= 1: return [] # Empty diagram.
	
	# Build the event queue from all sites
	for point in points: hq.heappush(evntq, SiteEvent(point.x, point.y))
	
	while len(evntq) > 0:
		evnt = hq.heappop(evntq) # Next event
		curr_y = evnt.y # Save current y position
		if isinstance(evnt, SiteEvent): handle_site(evnt)
		elif isinstance(evnt, CircleEvent): handle_circle(evnt)
	end_edges(root)
	for edge in edges: # Make start points correct.
		if(edge.neighbour is not None):
			edge.start = edge.neighbour.end
	return edges

def handle_site(evnt):
	""" Handle a single site event """
	global root, edges, evntq
	
	if not isinstance(root,Parabola): # First event, just add as root
		root = Parabola(evnt); return
	
	par = get_parabola(evnt.x) # Where to add the new edge.
	
	if par.ce: # Remove circle events that might be invalid from now..
		if par.ce in evntq: evntq.remove(par.ce); hq.heapify(evntq)
		par.ce = None
	
	# Create new edges and parabolas and connect them
	conn = Point(evnt.x, find_new_y(par.site, evnt.x))
	
	el = Edge(conn, par.site, evnt)
	er = Edge(conn, evnt, par.site)
	
	el.neighbour = er
	edges.append(el)
	
	par.edge = er
	par.leaf = False
	
	a = Parabola(par.site)
	b = Parabola(evnt)
	c = Parabola(par.site)
	
	par.set_right(c)
	par.set_left(Parabola())
	par.left.edge = el
	
	par.left.set_left(a)
	par.left.set_right(b)
	
	create_circle_event(a)
	create_circle_event(c)

def handle_circle(evnt):
	""" Handle a single circle event """
	global evntq
	
	b = parabola = evnt.parabola # current
	
	xl = get_left_parent(b); xr = get_right_parent(b)
	
	a = get_left_child(xl); c = get_right_child(xr) # closest to left and right
	
	# Remove parabola of current event from beachline
	grandparent = b.parent.parent
	if b.parent.left is b:
		if grandparent.left is b.parent:
			grandparent.set_left(b.parent.right)
		elif grandparent.right is b.parent:
			grandparent.set_right(b.parent.right)
	else: # b is right child
		if grandparent.left is b.parent:
			grandparent.set_left(b.parent.left)
		elif grandparent.right is b.parent:
			grandparent.set_right(b.parent.left)
	
	# Remove circle events that might be invalid from now on...
	if a.ce is not None:
		if a.ce in evntq: evntq.remove(a.ce); hq.heapify(evntq)
		a.ce = None
	if c.ce is not None:
		if c.ce in evntq: evntq.remove(c.ce); hq.heapify(evntq)
		c.ce = None
	
	# End the two edges merged and end in circle center
	xr.edge.end = xl.edge.end = Point(evnt.x, find_new_y(b.site, evnt.x))
	
	# Which one to replace?
	while parabola != root:
		parabola = parabola.parent
		if parabola == xl: rep = xl
		if parabola == xr: rep = xr
	
	rep.edge = Edge(xl.edge.end, a.site, c.site)
	edges.append(rep.edge)
	
	create_circle_event(a)
	create_circle_event(c)

def get_parabola(x_):
	""" Get the parabola to split for the new point. """
	par = root
	while not par.leaf:
		x = get_edge_from_parabola(par)
		if x < x_: par = par.right
		else: par = par.left
	return par

def end_edges(n):
	""" Recursively fix edges in tree by setting their endpoints. """
	if n.leaf: return
	# Drag edge to end of view.
	if n.edge.xdir < 0: res = min(0, n.edge.start.x)
	else: res = max(width, n.edge.start.x)
	n.edge.end = Point(res, (n.edge.k * res) + n.edge.m)
	end_edges(n.right); end_edges(n.left)

def calc_values(p):
	dp = 2.0 * (p.y - curr_y) or EPS
	a = 1/float(dp)
	b = -2.0 * p.x / float(dp)
	c = curr_y + float(dp/4.0) + ((p.x**2)/float(dp))
	return a,b,c

def get_edge_from_parabola(par):
	""" Get the edge x value for this parabola """
	left = get_left_child(par); right = get_right_child(par)
	p = left.site; r = right.site
	
	a1,b1,c1 = calc_values(p); a2,b2,c2 = calc_values(r)
	a = a1 - a2 or EPS; b = b1 - b2; c = c1 - c2
	
	d = math.sqrt(abs(b**2 - 4 * a * c))
	e1 = float(-b + d) / float(2*a)
	e2 = float(-b - d) / float(2*a)
	if p.y < r.y: res = max(e1, e2)
	else: res = min(e1, e2)
	return res

def find_new_y(p, x):
	""" Get y-coordinate for a new point. """
	dp = 2.0 * (p.y - curr_y)
	b1 = -(2 * float(p.x)) / float(dp or EPS)
	c1 = curr_y + float(dp/4.0) + (p.x**2) / float(dp or EPS)
	return float(x**2) / float(dp or EPS) + float(b1*x) + c1

def create_circle_event(par):
	""" Create new circle events based on the parameter parabola """
	global evntq
	
	lp = get_left_parent(par); rp = get_right_parent(par)
	lc = get_left_child(lp); rc = get_right_child(rp)
	if lc is None or rc is None or lc.site is None or rc.site is None or lc.site == rc.site: return
	
	intersection = calc_intersection(lp.edge, rp.edge)
	if intersection is None: return
	
	cevnt = CircleEvent(intersection.x, intersection.y - dist(lc.site, intersection))
	
	par.ce = cevnt; cevnt.parabola = par; hq.heappush(evntq, cevnt)

def calc_intersection(e1, e2):
	""" Get the point where the two edges will collide """
	x = float(e2.m - e1.m) / float((e1.k - e2.k) or EPS)
	y = float(e1.k * x) + float(e1.m)
	
	if (e1.xdir == 0) or (e2.xdir == 0) or (e1.ydir == 0) or (e2.ydir == 0): return # Avoid zero division
	if ((x - e1.start.x) / e1.xdir) < 0 or ((y - e1.start.y) / e1.ydir) < 0: return
	if ((x - e2.start.x) / e2.xdir) < 0 or ((y - e2.start.y) / e2.ydir) < 0: return
	return Point(x, y)

### Helpers for working with tree ###
def get_left_child(parabola):
	""" Get closest parabola to the left that is a child """
	if parabola is None: return
	par = parabola.left
	while par is not None and not par.leaf: par = par.right
	return par

def get_right_child(parabola):
	""" Get closest parabola to the right that is a child """
	if parabola is None: return
	par = parabola.right
	while par is not None and not par.leaf:
		par = par.left
	return par

def get_left_parent(parabola):
	""" Top left parent, before going to the right """
	last = parabola; par = last.parent
	while par.left is last:
		if par.parent is None: return
		last = par; par = par.parent
	return par

def get_right_parent(parabola):
	""" Top right gerent, before going to the left """
	last = parabola; par = last.parent
	while par.right is last:
		if par.parent is None: return
		last = par; par = par.parent
	return par

### UTILS ###
def rnd(max): # Generate random number in between 0 and max
	return random.random()*max

def write_to_file(): # Save the point set to a file
	filename = tkFileDialog.asksaveasfilename(**file_opt)
	if filename is None or filename == u'': return
	file = open(filename,'w')
	for p in points: file.write('%s\n' % p)
	file.close()

def read_from_file(): # Overwrite the complete point set with a new one from file.
	filename = tkFileDialog.askopenfilename(**file_opt)
	if filename is None or filename == u'': return
	file = open(filename, 'r')
	del points[:]
	for line in file: x,y = line.split(' '); points.append(Point(float(x),float(y)))
	file.close()
	redraw()

### GENERIC GUI STUFF ###
def add_point(event): ## Add a point
	points.append(Point(event.x, event.y)); redraw()

def dist(p1,p2): # distance between two points.
	return float(math.sqrt(float(p1.x - p2.x)**2 + float(p1.y - p2.y)**2))

def draw_line(begin, end): # Draw line between two points
	canvas.create_line(begin.x, begin.y, end.x, end.y, fill='red')

def redraw(): # Do a complete redraw of the canvas
	canvas.delete(ALL)
	start = time.time() * 1000
	edges = generate_voronoi()
	end = time.time() * 1000
	
	# Timing the generation.
	print 'Generating voronoi diagram for %d points took %.2f milliseconds.' % (len(points) , end - start)
	for point in points: point.draw() # Draw all points
	for edge in edges: edge.draw()

def delete_points(): del points[:]; redraw() # Delete all points and clear canvas.

def generate(): # Generate 100 random points.
	for i in xrange(100): points.append(Point(rnd(width), rnd(height)))
	redraw()

if __name__ == '__main__': # initialize GUI if running as main
	root = Tk(); root.title('Voronoi generation')
	root.bind('<Escape>', lambda(i): sys.exit(0))
	root.bind('q', lambda(i): sys.exit(0))
	root.bind('o', lambda(i): read_from_file())
	root.bind('s', lambda(i): write_to_file())
	root.bind('c', lambda(i): delete_points())
	root.bind('r', lambda(i): generate())
	frame = Frame(root, bg='gray', width=width, height=40)
	frame.pack(fill='x')
	canvas = Canvas(root, width=width, height=height)
	# canvas.grid(column=0, row=0, sticky=(N, W, E, S))
	canvas.bind("<Button-1>", add_point)
	canvas.pack()
	Button(frame, text='(C)lear', command=delete_points).pack(side='left')
	Button(frame, text='Generate (r)andom', command=generate).pack(side='left')
	Button(frame, text='(S)ave', command=write_to_file).pack(side='left')
	Button(frame, text='L(o)ad', command=read_from_file).pack(side='left')
	Button(frame, text='(Q)uit', command=lambda: sys.exit(0)).pack(side='left')
	root.mainloop()
