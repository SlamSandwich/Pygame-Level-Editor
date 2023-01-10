from camera import *
from editor import *
from mouse import *
from map import *
import pygame as pg

class App():
	def __init__(self):
		# const and alias
		self.resolution = self.width, self.height = (1200, 800)
		self.scale = 2.5
		self.fps = 60
		self.bg_color = (0, 0, 0)

		# init
		pg.init()
		self.display = pg.display.set_mode(self.resolution)
		self.clock = pg.time.Clock()
		self.create_objects()

	# point to rect collision
	def point_on_rect(self, point, rect):
		return (point[0] >= rect[0] and point[0] <= rect[2] and point[1] >= rect[1] and point[1] <= rect[3])

	def create_objects(self):
		self.mouse = Mouse(self)
		self.camera = Camera(self)
		self.map = Map(self)
		self.editor = Editor(self)

	def update(self):
		self.mouse.update(pg.mouse.get_pos())
		self.camera.update()
		self.editor.update()

	def draw(self): 
		self.display.fill(self.bg_color)
		self.map.draw()
		self.editor.draw()

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit()

			# mouse events
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.mouse.pressed['left']   = True
				if event.button == 2:
					self.mouse.pressed['middle'] = True
				if event.button == 3:
					self.mouse.pressed['right']  = True

			if event.type == pg.MOUSEBUTTONUP:
				if event.button == 1:
					self.mouse.pressed['left']   = False
				if event.button == 2:
					self.mouse.pressed['middle'] = False
					self.camera.apply_move_vector()
				if event.button == 3:
					self.mouse.pressed['right'] = False

			# keyboard events
			if event.type == pg.KEYDOWN:
				# hoverselect toggling functionality
				if event.key == pg.K_h:
					if self.editor.show_hoverselect: self.editor.show_hoverselect = False
					else:							 self.editor.show_hoverselect = True

				# toggle background
				if event.key == pg.K_b:
					if self.editor.draw_background: self.editor.draw_background = False
					else:							self.editor.draw_background = True

				# eraser tool
				if event.key == pg.K_e: self.editor.tile = None

	def run(self):
		while True:
			self.handle_events()
			self.update()
			self.draw()

			# pygame update
			pg.display.update()
			pg.display.set_caption(str(self.clock.get_fps()))
			self.clock.tick(self.fps)

if __name__ == '__main__':
	app = App()
	app.run()



