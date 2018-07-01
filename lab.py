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
		phi = 2.0 * math.pi * random.random()
		theta = math.acos(2.0 * random.random() - 1.0)
		x = int(phi * w)
		y = int(theta * h)
		yield (x, y, min(1.0 / math.sin(theta), 100.0))

# Lambertian sphere
def rnd_lambertian(bounds, n=10000):
	(w, h) = bounds
	for _ in range(0, n):
		phi = 2.0 * math.pi * random.random()
		theta = math.acos(1.0 - random.random())
		# theta = math.acos(2.0 * random.random() - 1.0)

		vec = (
			math.sin(theta) * math.cos(phi), 
			math.sin(theta) * math.sin(phi), 
			math.cos(theta) + 1.0
		)
		norm = math.sqrt((vec[0] ** 2) + (vec[1] ** 2) + (vec[2] ** 2))
	
		th = math.acos(vec[2] / norm)
		ph = math.atan2(vec[1] / norm, vec[0] / norm) + math.pi

		x = int(ph * w)
		y = int(th * h)

		yield (x, y, min(1.0 / math.sin(th) / math.cos(th), 100.0))

# Cosine
def rnd_cosine(bounds, n=10000):
	(w, h) = bounds
	def gamma_gen():
		gamma = 0.0
		while gamma < math.pi / 2.0:
			yield gamma
			gamma = gamma + math.pi / 180.0

	def integral(fn, a, b, s=2):
		h = (b - a) / s
		return sum([fn(a + k * h) * h for k in range(0, s)])

	integrals = [0.0]
	results = []
	gammas = [gamma for gamma in gamma_gen()]
	sin2x = lambda x: math.sin(2.0 * x)
	for i in range(0, len(gammas) - 1):
		result = integral(sin2x, gammas[i], gammas[i + 1]) / 2.0
		if result < 0.0:
			result = -result
		integrals.append(integrals[i] + result)
		results.append(result)
	s = sum(results)
	for _ in range(0, n):
		z = random.random() * integrals[-1]
		i = 0
		while z > integrals[i]:
			i = i + 1
		b = i * math.pi / 180.0
		a = max(0.0, b - math.pi / 180.0)

		f = max(sin2x(a), sin2x(b))

		theta = a + (b - a) * random.random()
		z = random.random() * f
		if z <= sin2x(theta):
			phi = 2.0 * math.pi * random.random()
			x = int(phi * w)
			y = int(theta * h)
			yield (x, y, min(1.0 / (sin2x(theta) / 2.0), 100.0))

draw_plot(rnd_square(bounds, 50000), bounds, 'square')
draw_plot(rnd_triangle(bounds, 50000), bounds, 'triangle')
draw_plot(rnd_circle(bounds, 50000), bounds, 'circle')
draw_plot(rnd_sphere(bounds, 50000), bounds, 'sphere')
draw_plot(rnd_lambertian(bounds, 50000), bounds, 'lambertian')
draw_plot(rnd_cosine(bounds, 50000), bounds, 'cosine')
