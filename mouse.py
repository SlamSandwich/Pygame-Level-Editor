import math

class Mouse():
	def __init__(self, app):
		# const and alias
		self.app = app
		self.position = [0, 0]
		self.tile_position = [0, 0]
		self.last_positions = {'left': [0, 0], 'middle': [0, 0], 'right': [0, 0]}
		self.pressed = {'left': False, 'middle': False, 'right': False}

	def update(self, position):
		self.position = position

		# records the locations of the most recent clicks
		for position in self.last_positions:
			if not self.pressed[position]:
				self.last_positions[position] = self.position

		# get tile position by, scaling position to buffer
		# adding camera offset (for some reason its addition)
		# taking that game coord and converting it into a tile coord
		# and then getting the floor of each coord
		self.tile_position = [math.floor(coord) for coord in self.app.map.tile_coord(self.app.camera.add(self.position))]