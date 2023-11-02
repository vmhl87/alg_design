from PIL import Image

def average_img(filename):
	i = Image.open(filename)
	h = list(i.getdata())
	r,g,b = 0,0,0
	a = 0
	for x in h:
		try:
			r += x[0]
			g += x[1]
			b += x[2]
		except:
			a += 1
	r /= 160*160
	g /= 160*160
	b /= 160*160
	return (r,g,b)

import os

for filename in os.listdir("all"):
	f = os.path.join("all", filename)
	if os.path.isfile(f):
		print(average_img(f))
