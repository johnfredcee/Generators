

class Room(object):
	def __init__(self, centre, branches):
		self.centre = centre
		self.branches = branches     # indexes of connections this room makes with oter room (indexes Dungeon.connections)
		self.points = []             # points in polygon describing walls
		self.centre_point = []       # centre of room

		
	def build_geometry(self, points):
		self.centre_point = [ ( points[self.centre].x, points[self.centre].y ) ]
		for b in self.branches:
			self.points = self.points + [ ( points[b].x, points[b].y ) ]
