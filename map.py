import pygame as pg
import json, os

class Map():
	def __init__(self, app):
		# const and alias
		self.app = app
		self.camera = app.camera
		self.tilesize = 16 * self.app.scale

		# init
		self.load_level()
		self.load_sprites()

	# convert tile positions into pixel (non-tile) positions
	def pixel_coord(self, position):
		return [coord * self.tilesize for coord in position]

	# convert pixel (non-tile) positions into tile positions
	def tile_coord(self, position):
		return [coord / self.tilesize for coord in position]

	# do not worry about optimization since this function is only run once
	def load_sprites(self):
		self.tile_sprites = self.sprite_directory('assets/tiles')
		self.prop_sprites = self.sprite_directory('assets/props')
		self.bg_sprites = self.sprite_directory('assets/background')

		self.scale_tilesprites()
		self.scale_bgsprites()

	def sprite_directory(self, directory):
		# os.walk is a generator object that return [(dirpath, dirnames, filenames)]
		# using index [0][2] returns file names
		# second list comprehension removes all non .png files
		file_names = [sprite for sprite in [item for item in os.walk(directory)][0][2] if sprite.endswith(('.png'))]

		# create a dictionary of sprites formatted as {'image_id' : <image_file>}
		# dict key is file_name as a string with the extension stripped
		self.sprites = {}
		for file_name in file_names:
			self.sprites[str(file_name).strip('.png')] = pg.image.load(f'{directory}/{file_name}')
		return self.sprites

	def scale_bgsprites(self):
		for image_id in self.bg_sprites:
			image = pg.transform.scale(self.bg_sprites[image_id], self.map['backgrounds'][image_id]['image scale'])
			amount = self.map['backgrounds'][image_id]['amount']
			width = image.get_width()
			height = image.get_height()

			new_sprite = pg.Surface((width*amount, height))
			new_sprite.set_colorkey((0, 0, 0))
			for i in range(amount):
				new_sprite.blit(image, (width*i, 0))

			self.bg_sprites[image_id] = new_sprite


	def scale_tilesprites(self):
		for image_id in self.tile_sprites:
			self.tile_sprites[image_id] = pg.transform.scale(self.tile_sprites[image_id], (self.tilesize, self.tilesize))

	def load_level(self):
		level = open('level/level.json')
		self.map = json.load(level)

	def draw(self):
		if self.app.editor.draw_background: self.draw_background()
		self.draw_tiles()

	# draws tiles to buffer
	def draw_tiles(self):
		for y in self.map['tiles']:
			for x in self.map['tiles'][y]:
				# converts the tile position (integer coordinates) into pixel coordinates
				# converts the pixel coordinates into "game" coordinates by offsetting with the camera
				# finds sprite in sprite dictionary by tile id
				game_position = self.camera.subtract(self.pixel_coord((int(x), int(y))))
				self.app.display.blit(self.tile_sprites[self.map['tiles'][y][x]], game_position)

# THIS NEEDS TO BE REDONE
# THIS DOES NOT WORK IF THE NUMBERS ARE NOT IN CHRONOLOGICAL ORDER
	def draw_background(self):
		for background_id in range(len(self.bg_sprites)):
			background_sprite = self.bg_sprites[str(background_id)]
			bg_data = self.map['backgrounds'][str(background_id)]

			position = bg_data['position'].copy()

			# move background object to the camera while accounting for parallax slowdown
			while position[0] + bg_data['image scale'][0] < self.camera.r_position[0]*bg_data['move speed']:
				position[0] += bg_data['image scale'][0]
			while position[0] > self.camera.r_position[0]*bg_data['move speed']:
				position[0] -= bg_data['image scale'][0]

			# draw background
			self.app.display.blit(background_sprite, self.camera.subtract(position, bg_data['move speed']))




