import argparse

from fractal import Mandelbrot

def main():
	parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
	parser.add_argument('--width', type=int, help='The width of the frame in px. For example 640 or 1024')
	parser.add_argument('--height', type=int, help='The width of the frame in px. For example 480 or 768')
	args = parser.parse_args()
	print(args)
	print(args.height)
	if None not in [args.width, args.height]:
		render = Mandelbrot(imgWidth=args.width, imgHeight=args.height)
	else:
		if not all(arg is None for arg in [args.width, args.height]):
			print("Arguments ignored. Please provide all of height and width.")
		render = Mandelbrot(imgWidth=640, imgHeight=480)
	render.run()

if __name__ == '__main__':
	main()