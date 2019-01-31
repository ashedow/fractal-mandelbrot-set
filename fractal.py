import os
import argparse
import sys
import math

from tkinter import *
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk

from palettes import palettes
from utils import fractal_calc

class Mandelbrot(object):
	def __init__(self, imgWidth, imgHeight):
		self.root = Tk()
		self.root.resizable(0, 0)
		self.root.title("Mandelbrot set")
		self.imgWidth = imgWidth
		self.imgHeight = imgHeight

		menubar = Menu(self.root)
		filemenu = Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "Reset", command = self.handleReset, accelerator = "R")
		filemenu.add_command(label = "Save as", command = self.handleSave, accelerator = "S")
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = self.handleQuit, accelerator = "Q")
		
		palettesmenu = Menu(menubar, tearoff = 0)
		palette_keys = sorted(list(palettes.keys()))
		self.palette_var = StringVar()
		for key in palette_keys:
			palettesmenu.add_radiobutton(label = key, variable = self.palette_var, value = key,
				command = self.handlePalette)
		self.palette_var.set(palette_keys[0])
		self.palette = palettes[self.palette_var.get()]

		menubar.add_cascade(label = "File", menu = filemenu)
		menubar.add_cascade(label = "Color Palette", menu = palettesmenu)
		self.root.config(menu = menubar)

		self.resetCoords()
		
		self.canvas = Canvas(self.root, width = imgWidth, height = imgHeight)

		self.image = None
		self.compute()
		self.draw()

		self.canvas.pack()
		self.canvas.bind("<Button-1>", self.handleClick)
		self.canvas.bind("<B1-Motion>", self.handleClick)
		self.canvas.bind("<ButtonRelease-1>", self.handleRelease)
		self.canvas.focus_set()
		self.canvas.bind("<q>", self.handleQuit)
		self.canvas.bind("<r>", self.handleReset)
		self.canvas.bind("<s>", self.handleSave)

		self.start = None
		self.rect = None
	
	def handlePalette(self, event = None):
		self.palette = palettes[self.palette_var.get()]
		self.draw()

	def handleSave(self, event = None):
		self.save()

	def handleQuit(self, event = None):
		self.root.quit()

	def handleReset(self, event = None):
		self.resetCoords()
		self.compute()
		self.draw()

	def handleClick(self, event):
		if self.start:
			if self.rect:
				self.canvas.delete(self.rect)
			w = abs(event.x - self.start[0]) + 1
			h = w * self.imgHeight / self.imgWidth
			y = self.start[1] + h
			self.rect = self.canvas.create_rectangle(self.start[0], self.start[1],
				event.x, y, outline = "red", width = 2, dash = (2,4))
		else:
			self.start = [event.x, event.y]

	def handleRelease(self, event):
		if self.rect:
			self.canvas.delete(self.rect)
		if self.start:
			w = abs(event.x - self.start[0]) + 1
			if w > 5:
				self.x0 = self.x0 + self.start[0] / self.imgWidth * self.width
				self.y0 = self.y0 + self.start[1] / self.imgHeight * self.height
				self.width = w / self.imgWidth * self.width
				self.height = self.width * self.imgHeight / self.imgWidth
				self.compute()
				self.draw()
		self.start = None
		self.rect = None

	def save(self):
		filename = asksaveasfilename(title = "Save as",
			defaultextension = ".png",
			filetypes=[('PNG', ".png")])
		self.photo.write(filename, 'png')

	def compute(self):
		self.data = [[0 for x in range(self.imgWidth)] for y in range(self.imgHeight)]
		for x in range(self.imgWidth):
			for y in range(self.imgHeight):
				val = fractal_calc(self.x0 + x / self.imgWidth * self.width,
					self.y0 + y / self.imgHeight * self.height)
				val = 255 - val % 256
				self.data[y][x] = val

	def draw(self):
		self.photo = PhotoImage(width = self.imgWidth, height = self.imgHeight)
		self.photo.put(" ".join(map(
			lambda line: "{" + " ".join(map(
				lambda val: self.palette[val], line)) + "}", self.data)))
		if self.image:
			self.canvas.delete(self.image)
		self.image = self.canvas.create_image(0, 0, anchor = NW, image = self.photo)

	def resetCoords(self):
		self.x0 = -2.5
		self.y0 = -1.5
		self.width = 4
		self.height = self.width * self.imgHeight / self.imgWidth

	def run(self):
		self.root.mainloop()
