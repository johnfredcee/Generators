import geom
from geom import vec2

class Room(object):
	def __init__(self, centre, branches, connections):
		self.centre = centre
		self.branches = branches     # indexes of endpoints of connections this room makes with oter room (indexes end_points)
		self.connections = connections # this one is same, but indexes connections
		self.points = []             # points in polygon describing walls
		self.centre_point = []       # centre of room
		self.doors = []
		self.radius = 0
		
	def build_geometry(self, points):
		length = 0
		radius = 0.0
		self.centre_point = vec2( points[self.centre].x, points[self.centre].y ) 
		for b in self.branches:
			end_point = vec2( points[b].x, points[b].y ) 
			self.points = self.points + [ end_point ]
			length = geom.line_exp_len_2d(self.centre_point, end_point)
			radius  = radius + length
		self.radius = radius / ( len(self.branches) * 2.0 )
		return	
