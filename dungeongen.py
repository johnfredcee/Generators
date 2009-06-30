#!/usr/bin/env python

import pyglet
from pyglet.gl import *
from geom import vec3
from geom import vec2
import math
import random
import geom
from connection import Connection
from corridor import Corridor
from room import Room

config = Config(sample_buffers=1, samples=4,
		depth_size=16, double_buffer=True,)
window = pyglet.window.Window(resizable=True, config=config)

		
class Dungeon(object):
	def __init__(self, gridx, gridy):
		self.gridx = gridx
		self.gridy = gridy
		self.end_points = []
		self.point_connection_count = []
		self.connections = []
		self.corridors = []		
		self.rooms = []
		self.room_outlines =  []	
		self.corridors = {}
		self.corridor_width = 0.01
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
		connections = set()
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
			connections.add(Connection(ic,ix))
			done[ic] = True
			#done[ix] = True
			ic = ic + 1
		for c in connections:
			self.connections += [ c ]
		return

	def build_end_lines(self):
		""" Build a set of lines connecting each other to serve as our corridors """
		self.end_lines = {}
		for i in range(0, len(self.end_points)):
			self.end_lines[i] = []
		for c in self.connections:
			(p1, p2) = geom.line_end_perp2d(self.end_points[c[0]], self.end_points[c[1]], 0.05)
			self.end_lines[c[0]].append((p1,p2))
			(p1, p2) = geom.line_end_perp2d(self.end_points[c[1]], self.end_points[c[0]], 0.05)
			self.end_lines[c[1]].append((p1,p2))

	def build_corridor_geometry(self):
		""" Create corridors from the already identified pairs od endpoints """
		ci = 0
		for c in self.connections:
			corridor = Corridor(ci, self.end_points[c[0]], self.end_points[c[1]])
			corridor.make_geometry(self.corridor_width)
			self.corridors[ci] =  corridor 
			ci = ci + 1

			
	def connection_count(self, point_index):
		""" Calculate the number of connections associated with a single point"""		
		result = 0
		for c in self.connections:
			if point_index in c:
				result = result + 1
		return result

	def connection_branches(self, point_index):
		""" Return a list of points connected to the given point """
		result = []
		for c in self.connections:
			if point_index in c:
				result = result + [ c.other(point_index) ]
		return result
	
	def connection_indexes(self, point_index):
		""" Given the index of the end point in our array, look for the connections that contain it and return a list indexes of them """
		result = []
		ic = 0
		for c in self.connections:
			if point_index in c:
				result = result + [ ic ]
			ic = ic + 1
		return result
	
	def count_connections(self):
		""" Calculate the number of connections associated with each point """
		i = 0
		for i in range(0, len(self.end_points)):
			self.point_connection_count.append(self.connection_count(i))		

	def identify_rooms(self):
		""" Build a list of connections to each room """
		self.rooms = []
		self.count_connections()
		for i in range(0, len(self.end_points)):
			if self.point_connection_count[i] > 2:	
				self.rooms.append(Room(i, self.connection_branches(i), self.connection_indexes(i)))
		#print "%d Rooms" % (len(self.rooms))
		#for r in self.rooms:
		#	print "Room"
		#	print "Centre %s Branches %s " % (r.centre, r.branches)
		return

	
	def build_room_geometry(self):
		""" Given that the rooms have been identified, flesh out their geometry """
		for r in self.rooms:
			r.build_geometry(self.end_points)
			doors = []
			for point in r.points:
				line = ( r.centre_point, point )
				## now, interoplate a bit along the line in order to get the vertex of a polygon
				door_point = vec2((line[1].x - line[0].x) * 0.25 + line[0].x,
						  (line[1].y - line[0].y) * 0.25 + line[0].y)
				r.doors += [ door_point ]
				# door_line = ( door_point, geom.line_exp_perp_2d(line[0], line[1], door_point) )
				# door_line_delta = door_line[1] - door_line[0]
				# door_line_delta = door_line_delta * 1.0 / door_line_delta.length()
				# door_line = ( door_point + ( door_line_delta * 0.02 ) , door_point - ( door_line_delta * 0.02 ) )
				# r.doors = r.doors + [ door_line ]
			# print "Points: ", r.points
			for ci in r.connections:
				connection = self.connections[ci]
				print "Room centere %s " % r.centre_point
				print "Connection %d (%d,%d) " % (ci, self.connections[ci][0], self.connections[ci][1] )
				print "Connection %s %s " % (self.end_points[self.connections[ci][0]], self.end_points[self.connections[ci][1]] ) 
				corridor = self.corridors[ci]
				print "Corridor ends 0 %s 1 % s " % (corridor.end_points[0], corridor.end_points[1])
				end = connection.closest(r.centre_point, self.end_points)
				print "end is %d " % end
				assert(corridor.end_points[end] == vec3(r.centre_point.x, r.centre_point[1], 0.0))
				corridor.shorten(0.25, end, self.corridor_width)
				
		return
	
			
	def build_display_list(self):
		"""" Actually build a list of primitives to draw """
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
		self.doors = []
		for r in self.rooms:
			for d in r.doors:
				self.doors = self.doors + [ d.x, d.y ]
		
	def draw(self):
		""" Do the drawing """
		#centre points
		glColor3f(0.0,1.0,1.0)
		pyglet.graphics.draw( len(self.vertices) / 2, pyglet.gl.GL_POINTS, ('v2f', self.vertices ))
		# connections
		glColor3f(1.0,0.0,0.0)
		pyglet.graphics.draw( len(self.lines) / 2, pyglet.gl.GL_LINES, ('v2f', self.lines ))
		# corridors
		glColor3f(0.0,0.0,1.0)		
		for corridor in self.corridors.values():
#			print dir(items[1])
			pyglet.graphics.draw( len(corridor.geometry) / 2, pyglet.gl.GL_LINES, ('v2f', corridor.geometry ))
		glColor3f(0.0,0.0,0.0)
		pyglet.graphics.draw( len(self.doors) / 2, pyglet.gl.GL_POINTS, ('v2f', self.doors ))
		
#		for door in self.doors:
#			pyglet.graphics.draw( len(door) / 2, pyglet.gl.GL_LINES, ('v2f', door ))
			
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
dungeon = Dungeon(6,6)
dungeon.generate_end_points(0.65)
dungeon.build_lines()
dungeon.build_end_lines()
dungeon.identify_rooms()
dungeon.build_corridor_geometry()
dungeon.build_room_geometry()
dungeon.build_display_list()

#print end_points
pyglet.app.run()
