import geom
from geom import vec2
from corridor import Corridor

class Room(object):
	def __init__(self, centre, branches, connections):
		self.centre = centre
		self.branches = branches     # indexes of endpoints of connections this room makes with oter room (indexes end_points)
		self.connections = connections # this one is same, but indexes connections
		self.points = []             # points in polygon describing walls
		self.centre_point = None     # centre of room
		self.doors = []
		self.radius = 0
		self.floorplan = []
		
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
		#print "Radius %s " % self.radius
		return

	def convert_to_polar(self, point):
		""" Convert this point to a polar coordinate (r, theta) centred on the room itself """
		# need to look this up
		point - self.centre_point
		return geom.xy_to_polar(point - self.centre_point)
	
	def build_floorplan(self, corridors, room_centre_points):
		for ci in self.connections:
			corridor = corridors[ci]
			end = corridor.connection.closest(self.centre_point, room_centre_points) # which end of the corridor is closest to this room?
			for point in corridor.door_geometry(end):
				self.floorplan += [ self.convert_to_polar(point) ]
		# sort them in radial order
		self.floorplan.sort(lambda p0, p1: p0.theta - p1.theta)
