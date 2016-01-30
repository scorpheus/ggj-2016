import gs
import gs.plus
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.clock as clock

import os
import sys
import math
import random

if getattr(sys, 'frozen', False):
	app_path = os.path.dirname(sys.executable)
else:
	app_path = os.path.dirname(os.path.realpath(__file__))

gs.LoadPlugins(gs.get_default_plugins_path())

# gs.plus.create_workers()
render.init(1024, 768, os.path.normcase(os.path.realpath(os.path.join(app_path, "pkg.core"))))#, 1, gs.Window.Fullscreen)

# get the big resolution
size = render.get_renderer().GetCurrentOutputWindow().GetSize()

big_resolution = gs.Vector2(160, 144)

size_pixel = gs.Vector2(size.x / big_resolution.x, size.y / big_resolution.y)
half_size_pixel = size_pixel * 0.5

gameboy_palette = [gs.Color(50/255, 60/255, 37/255),
				   gs.Color(83/255, 101/255, 61/255),
				   gs.Color(117/255, 141/255, 86/255),
				   gs.Color(151/255, 174/255, 122/255)
				   ]


def drange(start, stop, step):
	r = start
	while r <= stop:
		yield r
		r += step


def draw_pixel(x, y, color=gs.Color.Blue):
	center = gs.Vector2(int(x), int(y)) * size_pixel
	render.quad2d(center.x-half_size_pixel.x, center.y-half_size_pixel.y, center.x-half_size_pixel.x, center.y+half_size_pixel.y, center.x+half_size_pixel.x, center.y+half_size_pixel.y, center.x+half_size_pixel.x, center.y-half_size_pixel.y, color, color, color, color)


def draw_circle_explosion(center_x, center_y, radius, inner_radius, color=gs.Color.Blue):
	for x in drange(-1.57, 1.57, 0.1):
		pos_x = int(math.cos(x) * radius)
		draw_line(center_x - pos_x, center_y + math.sin(x) * radius, center_x - pos_x + inner_radius, center_y + math.sin(x) * radius, color)
		draw_line(center_x + pos_x - inner_radius, center_y + math.sin(x) * radius, center_x + pos_x, center_y + math.sin(x) * radius, color)

	# for x in drange(-radius, radius, 1):
	# 	angle = math.asin(x/radius)
	# 	pos_x = int(math.cos(angle) * radius)
	# 	draw_line(center_x - pos_x, center_y + math.sin(angle) * radius, center_x + pos_x, center_y + math.sin(angle) * radius, color)



def draw_circle(center_x, center_y, radius, color=gs.Color.Blue, full=False):
	center_x = int(center_x)
	center_y = int(center_y)
	if full:
		f = 1 - radius
		ddf_x = 1
		ddf_y = -2 * radius
		x = 0
		y = radius
		draw_pixel(center_x, center_y + radius, color)
		draw_pixel(center_x, center_y - radius, color)
		draw_line(center_x + radius, center_y, center_x - radius, center_y, color)

		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			draw_line(center_x + x, center_y + y, center_x - x, center_y + y, color)
			draw_line(center_x + x, center_y - y, center_x - x, center_y - y, color)
			draw_line(center_x + y, center_y + x, center_x - y, center_y + x, color)
			draw_line(center_x + y, center_y - x, center_x - y, center_y - x, color)

	else:

		f = 1 - radius
		ddf_x = 1
		ddf_y = -2 * radius
		x = 0
		y = radius
		draw_pixel(center_x, center_y + radius, color)
		draw_pixel(center_x, center_y - radius, color)
		draw_pixel(center_x + radius, center_y, color)
		draw_pixel(center_x - radius, center_y, color)
	
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			draw_pixel(center_x + x, center_y + y, color)
			draw_pixel(center_x - x, center_y + y, color)
			draw_pixel(center_x + x, center_y - y, color)
			draw_pixel(center_x - x, center_y - y, color)
			draw_pixel(center_x + y, center_y + x, color)
			draw_pixel(center_x - y, center_y + x, color)
			draw_pixel(center_x + y, center_y - x, color)
			draw_pixel(center_x - y, center_y - x, color)


def draw_line(x0, y0, x1, y1, color=gs.Color.Blue):
	x0 = int(x0)
	y0 = int(y0)
	x1 = int(x1)
	y1 = int(y1)
	dx = abs(x1-x0)
	dy = abs(y1-y0)
	sx = sy = 0

	if x0 < x1:
		sx = 1
	else:
		sx = -1
	if y0 < y1:
		sy = 1
	else:
		sy = -1

	err = dx - dy

	while True:
		draw_pixel(x0, y0, color)

		if x0 == x1 and y0 == y1:
			break

		e2 = 2 * err
		if e2 > -dy:
			err = err - dy
			x0 += sx

		if x0 == x1 and y0 == y1:
			draw_pixel(x0, y0, color)
			break

		if e2 < dx:
			err = err + dx
			y0 += sy


def get_random_color():
	return gameboy_palette[random.randint(0, len(gameboy_palette)-1)]


def lerp(x, a, b):
	return a + (b - a)*x

default_font = gs.RasterFont("@core/fonts/default.ttf", 12)
radius_circle_eye = 10
counter_seed = 0

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()

	random.seed(counter_seed)

	render.clear(gs.Color(16/255, 19/255, 12/255))
	# render.clear(gs.Color.Black)

	draw_circle_explosion(big_resolution.x * .5, big_resolution.y * .5, radius_circle_eye, 10, get_random_color())
	draw_circle(big_resolution.x * .5, big_resolution.y * .5, lerp((2 * radius_circle_eye / big_resolution.x), radius_circle_eye, radius_circle_eye + 10), get_random_color())
	draw_circle(big_resolution.x * .5, big_resolution.y * .5, radius_circle_eye + 10, get_random_color())

	radius_circle_eye += dt_sec * 40
	if radius_circle_eye > big_resolution.x*.5:
		radius_circle_eye = 10

	if input.key_press(gs.InputDevice.KeyA) or math.floor(radius_circle_eye)%10 == 0:
		counter_seed += 1

	# create symbol
	nb_point = random.randint(2, 8)
	size_symbol = random.randint(10, 32)
	nb_line = random.randint(1, nb_point-1)

	# center_symbol = gs.Vector3(random.randint(size_symbol, big_resolution.x-1-size_symbol), random.randint(size_symbol, big_resolution.y-1-size_symbol), 0)
	center_symbol = gs.Vector3(big_resolution.x*.5, big_resolution.y*.5, 0)
	array_point = []
	array_size_point = []
	for i in range(nb_point):
		check = False
		counter_check = 0
		while not check and counter_check < 10:
			counter_check += 1
			check = True
			size_point = random.randint(2, 3)
			pos_point = gs.Vector3(random.randint(center_symbol.x - size_symbol, center_symbol.x + size_symbol), random.randint(center_symbol.y - size_symbol, center_symbol.y + size_symbol), 0)
			for y in range(len(array_point)):
				if gs.Vector3.Dist(pos_point, array_point[y]) < size_point + array_size_point[y]:
					check = False

		array_size_point.append(size_point)
		array_point.append(pos_point)

	for point, pos in zip(array_point, array_size_point):
		draw_circle(point.x, point.y, pos, get_random_color(), random.randint(0, 1))

	if nb_line != 0:
		array_id_line = []
		for i in range(nb_line):
			second_point = first_point = random.randint(0, nb_point-1)
			while second_point == first_point:
				second_point = random.randint(0, nb_point-1)
			array_id_line.append([first_point, second_point])

		for id_line in array_id_line:
			pos_a = array_point[id_line[0]] + ((array_point[id_line[1]] - array_point[id_line[0]]) / gs.Vector3.Dist(array_point[id_line[0]], array_point[id_line[1]])) * (array_size_point[id_line[0]]+1)
			pos_b = array_point[id_line[1]] + ((array_point[id_line[0]] - array_point[id_line[1]]) / gs.Vector3.Dist(array_point[id_line[0]], array_point[id_line[1]])) * (array_size_point[id_line[1]]+1)
			if gs.Vector3.Dist(pos_a, pos_b) > 1:
				draw_line(pos_a.x, pos_a.y, pos_b.x, pos_b.y, get_random_color())



	# gs.DrawRenderSystemStats(render.get_render_system(), default_font, 10, 370)
	render.flip()
	# render.get_render_system().BeginFrame()
	# render.get_render_system().EndFrame()
render.uninit()