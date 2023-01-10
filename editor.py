from button import *
import pygame as pg

class Editor():
	def __init__(self, app):
		# const and alias
		self.app = app
		self.mouse = app.mouse
		self.camera = app.camera
		self.map = app.map
		self.tile_map = app.map.map['tiles']
		self.tilesize = self.map.tilesize
		self.grid_color = [155, 155, 155]
		self.hoverselect_color = [255, 255, 255]
		self.gui_bgcolor = [50, 50, 50]
		self.gui_ocolor = [155, 155, 155]

		self.gui_rect = [0, 0, self.app.width // 5, self.app.height]
		self.button_size = self.app.width // 50
		self.button_spacing = self.app.width // 75

		# variable
		self.mouse_on_editor = False
		self.draw_background = True
		self.show_hoverselect = True
		self.tile = '0'

		# init
		self.load_gui()
		self.create_grid_sprite()

	# round pixel position to NEAREST tile position
	def round_to_tile_coord(self, position):
		return [self.tilesize * int(coord / self.tilesize) for coord in position]

	def load_gui(self):
		self.load_buttons()

	# create list of buttons that can be looped over and updated
	def load_buttons(self):

		# declare list of buttons
		self.buttons = []

		# create tile buttons
		for tile_id in self.map.tile_sprites:
			# fancy math to get button positions
			x = int(tile_id) % 7
			y = int(int(tile_id) / 7)
			button_position = [x * self.button_spacing * 2 + self.button_spacing//2, y * self.button_spacing * 2 + self.button_spacing//2]
			
			# look up sprite in sprite dictionary with tile_id
			button_image = self.map.tile_sprites[tile_id]

			# add button object with params to list
			self.buttons.append(Button(self.app, self, button_position, self.button_size, button_image, tile_id, 'tile'))


		# create prop buttons
		for i, item_name in enumerate(self.map.prop_sprites):
			# get button position
			x = int(i) % 7
			y = int(int(i) / 7) + 2
			button_position = [x * self.button_spacing * 2 + self.button_spacing//2, self.app.height - y * self.button_spacing * 2 + self.button_spacing]

			# look up sprite in sprite dictionary with item name
			button_image = self.map.prop_sprites[item_name]

			# add button object to list
			self.buttons.append(Button(self.app, self, button_position, self.button_size, button_image, item_name, 'prop'))

	# creating a singular image is more efficient than running
	# a nested loop every frame
	def create_grid_sprite(self):
		# generate surface
		self.grid_surface = pg.Surface((32*self.tilesize, 22*self.tilesize))

		# fill grid black
		self.grid_surface.fill([0, 0, 0])
		for x in range(32):
			for y in range(22):
				rect = [x*self.tilesize, y*self.tilesize, self.tilesize, self.tilesize]
				pg.draw.rect(self.grid_surface, self.grid_color, rect, 1)

		# make all black transparent
		self.grid_surface.set_colorkey((0, 0, 0))
		self.grid_surface.set_alpha(95)

	def update(self):
		self.check_gui_collision()
		if self.app.mouse.pressed['left'] and self.mouse_on_editor:
			self.place_tile()

	def check_gui_collision(self):
		if self.app.point_on_rect(self.app.mouse.position, self.gui_rect):
			self.mouse_on_editor = False
		else:
			self.mouse_on_editor = True

	def place_tile(self):
		# convert tile_position into a string to use as a dict key
		# check if y coordinate exists in map dictionary
			# replace or append tile if so
		# if y coordinate does not exist then create one
		# run the function again
		x = str(self.app.mouse.tile_position[0])
		y = str(self.app.mouse.tile_position[1])
		if y in self.tile_map:
			if self.tile == None:
				if x in self.tile_map[y]: self.tile_map[y].pop(x)
			else:
				self.tile_map[y][x] = self.tile
		else:
			self.tile_map[y] = {}
			self.place_tile()

	def draw(self):
		if self.mouse_on_editor and self.show_hoverselect: self.draw_hoverselect()
		self.draw_gui()
		self.draw_buttons()

	def draw_hoverselect(self):
		# tile location
		position = self.camera.subtract(self.app.map.pixel_coord(self.mouse.tile_position))

		# ghost tile
		if self.tile != None:
			image = pg.transform.scale(self.map.tile_sprites[self.tile], [self.tilesize, self.tilesize])
			image.set_alpha(99)
			self.app.display.blit(image, position)
		
		# outline
		pg.draw.rect(self.app.display, self.hoverselect_color, [position[0], position[1], self.tilesize+1, self.tilesize+1], 2)

	def draw_gui(self):
		width = self.app.width // 5
		pg.draw.rect(self.app.display, self.gui_bgcolor, self.gui_rect)
		pg.draw.rect(self.app.display, self.gui_ocolor, self.gui_rect, 2)

	def draw_buttons(self):
		for button in self.buttons:
			button.draw()







