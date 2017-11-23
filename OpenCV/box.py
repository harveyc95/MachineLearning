import cv2
import numpy as np
import os

class Box:
	_xMin = 0
	_xMax = 0
	_yMin = 0
	_yMax = 0

	def __init__(self, xMin, yMin, xMax, yMax):
		self._xMin = xMin
		self._xMax = xMax
		self._yMin = yMin
		self._yMax = yMax

	def __repr__(self):
		return "(" + str(self._xMin) + ", " + str(self._yMin) + ")" + "(" + str(self._xMax) + ", " + str(self._yMax) + ")"

	def area(self):
		return (abs(self._xMax - self._xMin) * abs(self._yMax - self._yMin))

def boundingBox(image):
	w = image.shape[1]
	h = image.shape[0]
	xMin = w
	xMax = 0
	yMin = h
	yMax = 0
	black = np.zeros((1,1,3), np.uint8)
	for col in range (0, w):
		for row in range (0, h):
			if (np.any(image[row][col] != black)):
				xMin = min(xMin, col)
				xMax = max(xMax, col)
				yMin = min(yMin, row)
				yMax = max(yMax, row)

	box = Box(xMin, yMin, xMax, yMax)
	return box

# Input: image
# Output: bounding box of xMin, yMin, xMax, yMax
# Note: assumes entire image is black except the part looking for bounding box

def boundingTest(image, box):
	for col in range (box._xMin, box._xMax, 1):
		image[box._yMin][col] = [255,255,255]
		image[box._yMax][col] = [255,255,255]
	for row in range (box._yMin, box._yMax, 1):
		image[row][box._xMin] = [255,255,255]
		image[row][box._xMax] = [255,255,255]
	cv2.imshow('boundingTest', image)
	return image