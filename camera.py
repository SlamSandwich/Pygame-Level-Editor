
class Camera():
	def __init__(self, app, position=[0, 0]):
		# const and alias
		self.app = app
		self.mouse = app.mouse

		# variable
		self.r_position = position
		self.tile_position = [0, 0]
		self.last_position = [0, 0]
		self.move_vector = [0, 0]

	# convert screen position to game position
	def subtract(self, position, multiplier=1):
		return [p1 - p2*multiplier for (p1, p2) in zip(position, self.r_position)]

	# offset position by camera position
	def add(self, position):
		return [p1 + p2 for (p1, p2) in zip(position, self.r_position)]

	# this applys the move vector
	def apply_move_vector(self):
		self.last_position[0] += self.move_vector[0]
		self.last_position[1] += self.move_vector[1]
		self.move_vector = [0, 0]

	def update(self):
		# gets the move vector from mouse last position to new position, then scales it by ratio
		if self.mouse.pressed['middle']:
			self.move_vector[0] = (self.mouse.last_positions['middle'][0] - self.mouse.position[0])
			self.move_vector[1] = (self.mouse.last_positions['middle'][1] - self.mouse.position[1])

		# The camera position the user sees (relative position),
		# is set to be the actual position plus the move vector.
		# This allows for smooth click and drag behavior from the app.
		self.r_position[0] = self.last_position[0] + self.move_vector[0]
		self.r_position[1] = self.last_position[1] + self.move_vector[1]



