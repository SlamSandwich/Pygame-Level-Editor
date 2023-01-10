import pygame as pg

class Button():
	def __init__(self, app, editor, position, size, image, tile_id, button_type):
		# const and alias
		self.app = app
		self.editor = editor
		self.image = pg.transform.scale(image, (size, size))
		self.rect = self.image.get_rect()
		self.rect = pg.Rect(self.rect[0] + position[0], self.rect[1] + position[1], self.rect[2] + position[0], self.rect[3] + position[1])
		self.tile_id = tile_id
		self.button_type = button_type

	def clicked(self):
		# change behavior based on function
		if self.button_type == 'tile':
			self.editor.tile = self.tile_id

	def draw(self):
		# draw tile
		self.app.display.blit(self.image, (self.rect.x, self.rect.y))

		# button behavior
		outline_rect = (self.rect.x-2, self.rect.y-2, self.rect.width-self.rect.x+4, self.rect.height-self.rect.y+4)
		border = 2

		# mouse is touching button
		if self.app.point_on_rect(self.app.mouse.position, self.rect):
			outline_color = (255, 255, 255)

			# mouse is clicking button
			if self.app.mouse.pressed['left']:
				self.clicked()
				border = 0

		# button is selected
		elif self.editor.tile == self.tile_id:
			outline_color = (0, 255, 0)

		# button is in default state
		else:
			outline_color = (0, 0, 0)

		pg.draw.rect(self.app.display, outline_color, outline_rect, border)




