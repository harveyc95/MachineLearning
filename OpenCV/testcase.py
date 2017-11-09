import cv2
import numpy as np
import imutils

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

# Input: image
# Output: bounding box of xMin, yMin, xMax, yMax
# Note: assumes entire image is black except the part looking for bounding box
def boundingBox (image):
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
				image[row][col] = [255,255,255]

	box = Box(xMin, yMin, xMax, yMax)
	print box
	return box

def boudingTest(image, box):
	for col in range (box._xMin, box._xMax, 1):
		image[box._yMin][col] = [255,255,255]
		image[box._yMax][col] = [255,255,255]
	for row in range (box._yMin, box._yMax, 1):
		image[row][box._xMin] = [255,255,255]
		image[row][box._xMax] = [255,255,255]
	return image

# Input: image, filename, extension, scaling, save
# Output: 
# Note: 
def resize(image, filename, extension, scaling):
	width = image.shape[1]
	height = image.shape[0]

	widthResized = int(width*scaling)
	heightResized = int(height*scaling)
	resized = cv2.resize(image, (widthResized,heightResized))
	resizedName = filename + '_' + str(scaling) + 'x_' + str(widthResized) + 'x' + str(heightResized) + extension
	return resized

def rotate(image, filename, extension, start, end, step):
	for angle in np.arange(start, end+1, step):
		rotated = imutils.rotate_bound(image, angle)
		dst = filename + '_' + str(angle) + extension
		# cv2.imwrite(dst, rotated)
		box = boundingBox(rotated)
		test = boudingTest(rotated, box)
		cv2.imwrite(dst, test)

def createData (filename, extension, scaling, save):
	image = cv2.imread(filename+extension)
	resized = resize(image, filename, extension, scaling)
	rotate(resized, filename, extension, 0, 360, 30)
	# box = boundingBox(resized)
	pass

fileArm = 'A_Arm'
fileHand = 'A_Hand'
fileTip = 'A_Tip'
ext = '.png'
scaling = 0.25
background = 'test.jpg'
save = True
numTestCases = 100

createData(fileHand, ext, scaling, save)
