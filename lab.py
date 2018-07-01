# from os import listdir
# from os.path import basename, isfile, join
# import re
# import math
# import matplotlib.pyplot as plt
# import statistics
import pygal
from pygal.style import Style
import random
import math

chart_style = Style(
	background='black',
	plot_background='black'
)

def draw_plot(values_gen, bounds, name):
	points = {}
	for v in values_gen:
		(x, y, energy) = v
		point = (x, y)
		if not point in points:
			points[point] = energy
		else:
			points[point] = points[point] + energy
	max_energy = max(points.values())

	chart = pygal.XY(
		dots_size=1, 
		stroke=False, 
		width=bounds[0], 
		height=bounds[1], 
		show_x_labels=False, 
		show_y_labels=False, 
		show_legend=False, 
		style=chart_style
	)
	chart.add(None, [
		{'value': point, 'color': 'rgba(0, {}, 0, 1)'.format(int((energy * 1000.0 / max_energy) * 255.0))} for (point, energy) in points.items()
	])
	chart.render_to_png("./{}.png".format(name))

bounds = (400, 400)

# Unit square
def rnd_square(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		x = int(random.random() * w)
		y = int(random.random() * h)
		yield (x, y, 1.0)

# Triangle
def rnd_triangle(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		while True:
			x = random.random()
			y = random.random()
			if x + y <= 1.0:
				a = int((0.8 * x + y) * w)
				b = int((x + 0.7 * y) * h)
				yield (a, b, 1.0)
				break

# Circle
def rnd_circle(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		theta = 2.0 * math.pi * random.random()
		r = math.sqrt(random.random())
		x = int(r * math.cos(theta) * w)
		y = int(r * math.sin(theta) * h)
		yield (x, y, 1.0)

# Sphere
def rnd_sphere(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		theta = 2.0 * math.pi * random.random()
		phi = math.acos(1.0 - 2.0 * random.random())
		x = int(theta * w)
		y = int(phi * h)
		yield (x, y, max(1.0 / math.cos(theta), 100.0))

# Lambertian sphere
def rnd_lambertian(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		phi = 2.0 * math.pi * random.random()
		theta = math.acos(1.0 - random.random())

		vec = (
			math.sin(theta) * math.cos(phi), 
			math.sin(theta) * math.sin(phi), 
			math.cos(theta) + 1.0
		)
		norm = math.sqrt((vec[0] ** 2) + (vec[1] ** 2) + (vec[2] ** 2))
	
		th = math.acos(vec[2] / norm)
		ph = math.atan2(vec[1] / norm, vec[0] / norm)

		x = int(ph * w)
		y = int(th * h)

		yield (x, y, max(1.0 / math.sin(ph), 100.0))

# draw_plot(rnd_square(bounds), bounds, 'square')
# draw_plot(rnd_triangle(bounds), bounds, 'triangle')
# draw_plot(rnd_circle(bounds), bounds, 'circle')
# draw_plot(rnd_sphere(bounds), bounds, 'sphere')
draw_plot(rnd_lambertian(bounds), bounds, 'lambertian')
