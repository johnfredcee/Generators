#!/usr/bin/env python

import pyglet
from pyglet.gl import *
from geom import vec3
import math
import random
import geom
from connection import Connection
from sets import Set

config = Config(sample_buffers=1, samples=4,
				depth_size=16, double_buffer=True,)
window = pyglet.window.Window(resizable=True, config=config)


class Dungeon(object):
	def __init__(self, gridx, gridy):
		self.gridx = gridx
		self.gridy = gridy
		self.end_points = []
		self.point_connection_count = []
		self.connections = Set()		
		return
		   
	def generate_end_points(self, peturbation):
		self.end_points = []
		max_dist = math.sqrt(self.gridx * self.gridx + self.gridy * self.gridy)
		for x in range(-self.gridx,self.gridx):
			for y in range(-self.gridy, self.gridy):
				distance = math.sqrt(x * x + y * y) / max_dist
				if (random.gauss(0.0,1.0) > distance):
					x_peturbation = random.random() * peturbation
					y_peturbation = random.random() * peturbation
					self.end_points.append(vec3((x + x_peturbation) / self.gridx, (y + y_peturbation) / self.gridy, 0.0))
		return



	def build_lines(self):
		self.closest = []
		done = [ False ] * len(self.end_points)
		ic = 0
		for c in self.end_points[:-1]:
			# find closest point
			i = 0
			ix = 0
			min_distance = 10000.0
			#print "Point ", ic
			for cn in self.end_points:
				delta = c - cn
				if ((delta.x == 0) and (delta.y == 0) and (delta.z == 0)):
					i = i + 1
					continue
				if (done[i]):
					i = i + 1
					continue
				dist = delta.length()
				#print "dist ", dist
				#print "mindist ", min_distance
				if (dist < min_distance):
					min_distance = dist
					ix = i
					#print "!!", ix
				i = i + 1    
			#print ic, ix
			self.connections.add(Connection(ic,ix))
			done[ic] = True
			#done[ix] = True
			ic = ic + 1
		return

	def build_end_lines(self):
		self.end_lines = {}
		for i in range(0, len(self.end_points)):
			self.end_lines[i] = []
		for c in self.connections:
			(p1, p2) = geom.line_end_perp2d(self.end_points[c[0]], self.end_points[c[1]], 0.05)
			self.end_lines[c[0]].append((p1,p2))
			(p1, p2) = geom.line_end_perp2d(self.end_points[c[1]], self.end_points[c[0]], 0.05)
			self.end_lines[c[1]].append((p1,p2))
			
	def build_display_list(self):
		glPointSize(4)
		glEnable(GL_POINT_SMOOTH)
		self.vertices = []
		for v in self.end_points:
			self.vertices.append( v.x )
			self.vertices.append( v.y )
		self.lines = []
		for c in  self.connections:
			self.lines.append( self.end_points[c[0]].x )
			self.lines.append( self.end_points[c[0]].y )
			self.lines.append( self.end_points[c[1]].x )
			self.lines.append( self.end_points[c[1]].y )
			
	def draw(self):
		glColor3f(0.0,1.0,1.0)
		pyglet.graphics.draw( len(self.vertices) / 2, pyglet.gl.GL_POINTS, ('v2f', self.vertices ))
		glColor3f(1.0,0.0,0.0)
		pyglet.graphics.draw( len(self.lines) / 2, pyglet.gl.GL_LINES, ('v2f', self.lines ))

def update(dt):
		#print dt
		return

pyglet.clock.schedule(update)   
   
def setup():
	# One-time GL setup
	glClearColor(1, 1, 1, 1)
	glColor3f(1, 0, 0)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_CULL_FACE)

	# Uncomment this line for a wireframe view
	#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	# Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
	# but this is not the case on Linux or Mac, so remember to always
	# include it.
	glDisable(GL_LIGHTING)
	#glEnable(GL_LIGHT0)
	#glEnable(GL_LIGHT1)



@window.event
def on_resize(width, height):
	# Override the default on_resize handler to create a 3D projection
	print width, height
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glViewport(0, 0, width, height)
	return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	glDisable(GL_DEPTH_TEST)
	glClearColor(1,1,1,1)
	glColor3f(1.0,0.0,0.0)
	dungeon.draw()

# Try and crete a window with multisampling (antialiasing)
dungeon = Dungeon(8,8)
dungeon.generate_end_points(0.65)
dungeon.build_lines()
dungeon.build_display_list()
dungeon.build_end_lines()

#print end_points
pyglet.app.run()
