import numpy as np
import matplotlib.pyplot as plt


# Create heatmap and save img.
def plotting(values, x_min, x_max, y_min, y_max):
	plt.xlabel("Real Axis")
	plt.ylabel("Imaginary Axis")
	plt.title("The Mandelbrot Set.")
	plt.grid(True)
	plt.imshow(values, origin="0,0", interpolation="none", extent=[x_min, x_max, y_min, y_max])
	plt.savefig("MandelBrot.png", bbox_inches="tight")
	plt.show()


# Fractal formula
def fractal_model(point, colors):
	z = 0
	for i in range(1, colors):
		if abs(z) > 2:
			return i
		z = z*z + point
	return 0


def main(x_min, x_max, y_min, y_max, num_iter, colors):
	"""
	The number of leading spaces in a string
    :param x_min
    :param x_max
    :param y_min
    :param y_max
    :param num_iter - col iteration 
    :param colors - num of colors 
    :return: Mandelbrot set
    """
	real = np.linspace(x_min, x_max, num_iter)
	imag = np.linspace(y_min, y_max, num_iter)
	values = np.empty((num_iter, num_iter))
	for i in range(num_iter):
		for j in range(num_iter):
			values[j, i] = fractal_model(real[i] + 1j*imag[j], colors)
	plotting(values, x_min, x_max, y_min, y_max)
	return

if __name__ == "__main__":
	main(x_min=-2.25, x_max=0.75, y_min=-1.25, y_max=1.25, num_iter=100, colors=2)