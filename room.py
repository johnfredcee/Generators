import geom
from geom import vec2

class Room(object):
	def __init__(self, centre, branches):
		self.centre = centre
		self.branches = branches     # indexes of connections this room makes with oter room (indexes Dungeon.connections)
		self.points = []             # points in polygon describing walls
		self.centre_point = []       # centre of room
		self.doors = []
		self.radius = 0
		
	def build_geometry(self, points):
		length = 0
		self.centre_point = vec2( points[self.centre].x, points[self.centre].y ) 
		for b in self.branches:
			end_point = vec2( points[b].x, points[b].y ) 
			self.points = self.points + [ end_point ]
			length = geom.line_exp_len_2d(self.centre_point, end_point)
			if (self.radius < length):
				self.radius = length
		return self.radius
			
