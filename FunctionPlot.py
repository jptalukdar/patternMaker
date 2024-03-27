from PIL import Image, ImageDraw
import math

def plot_function(draw, func, *args, **kwargs):

  max_theta = kwargs.get("max_theta", 360)

  resolution = 100

  sub_resolution = [ i/resolution for i in range(0, resolution)]

  # Plot the values in the image
  for theta in range(max_theta+1):
    for s in sub_resolution:
      value = func(theta+s, *args, **kwargs)
      x = int(image_size[0] / 2 + value * 100 * math.cos(math.radians(theta)))
      y = int(image_size[1] / 2 + value * 100 * math.sin(math.radians(theta)))
      draw.point((x, y), fill="black")

  # Define the function that takes theta and returns a value
def lotus(theta, *args, **kwargs):
  radians = math.radians(theta)
  X = kwargs.get("X",0.25)
  Y = kwargs.get("Y",8)
  N = kwargs.get("N",1)

  A = kwargs.get("A",3)

  a = abs(math.cos(A * radians))
  b = 2 * (X - abs(math.cos(A*radians + math.pi/2)))
  c = 2 + Y * abs(math.cos(2*A*radians+math.pi/2))
  
  return N + (a + b) / c

def sine(theta, *args, **kwargs):
  radians = math.radians(theta)

  r = 1
  n = 4
  a = math.sin(n*radians)
  return r + a

def cos(theta, *args, **kwargs):
  radians = math.radians(theta)

  r = 1
  n = 4
  a = math.cos(n*radians)
  return r + a

def sinecos(theta, *args, **kwargs):
  radians = math.radians(theta)

  r = 1
  n = 4
  a = math.sin(2*n*radians)
  b = math.cos(4*n*radians)
  return r + a + b

def sinepluscos(theta, *args, **kwargs):
  radians = math.radians(theta)

  r = 1
  n = 1
  a = math.sin(n*radians)
  b = math.cos(n*radians)
  return r + a + b

def circe(theta, *args, **kwargs):
  return kwargs.get("R",1)

def sineplus(theta, *args, **kwargs):
  radians = math.radians(theta)
  return 1 + math.sin(radians) + radians

def sine3(theta, *args, **kwargs):
  radians = math.radians(theta)
  return 1 + math.sin(-1*radians)+math.sin(2*radians)+math.sin(3*radians)

def abs_sine(theta, *args, **kwargs):
  radians = math.radians(theta)
  radius = kwargs.get("R",1)
  return radius+abs(math.sin(12*radians))

def rose(theta, *args, **kwargs):
  radians = math.radians(theta)
  d = 20
  n = d-1
  k = d/n
  return math.cos(k*radians)
  # Create a blank image
image_size = (1000, 1000)
image = Image.new("RGB", image_size, "white")
draw = ImageDraw.Draw(image)

# Call the function to plot the values
# plot_function(draw, lotus)
# plot_function(draw, lotus, X=0.5 )
# plot_function(draw, lotus, X=0.5, Y=12 )
# plot_function(draw, lotus, X=1, Y=2)
# plot_function(draw, lotus, X=0.5, Y=2, A=3)
# plot_function(draw, lotus, X=0.5, Y=2, A=0.5)
# plot_function(draw, lotus, X=0.1, Y=2)
# plot_function(draw, sine)
plot_function(draw, abs_sine, max_theta=360, R=1)
plot_function(draw, rose, max_theta=9054, R=1)
# plot_function(draw, abs_sine, max_theta=360, R=-1)
plot_function(draw, circe)
# plot_function(draw, circe, R=2)

"""
Y controls the height of the curvature. A higher value will lead to circular.
X controls the inwardness of the curvature.
  A lower value will lead to a more consticted shape.
  A higher value will lead to a more open shape.
N controls the radius of the shape.
A controls the number of petals.


"""

# Save the image
image.save("function_plot.png")