import cv2
import numpy as np
import imutils

class Box:
	xMin = 0
	xMax = 0
	yMin = 0
	yMax = 0

	def __init__(self, xMin, yMin, xMax, yMax):
		self.xMin = xMin
		self.xMax = xMax
		self.yMin = yMin
		self.yMax = yMax

	def __repr__(self):
		return "(" + str(self.xMin) + ", " + str(self.yMin) + ")" + "(" + str(self.xMax) + ", " + str(self.yMax) + ")"

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

# Input: image, filename, extension, scaling, save
# Output: 
# Note: 
def resize(image, filename, extension, scaling, save):
	width = image.shape[1]
	height = image.shape[0]

	widthResized = int(width*scaling)
	heightResized = int(height*scaling)
	resized = cv2.resize(image, (widthResized,heightResized))
	resizedName = filename + '_' + str(scaling) + 'x_' + str(widthResized) + 'x' + str(heightResized) + extension
	if (save == True):
		cv2.imwrite(resizedName, resized)

	return resized

def createData (filename, extension, scaling, save):
	image = cv2.imread(filename+extension)
	resized = resize(image, filename, extension, scaling, save)
	boundingBox(resized)
	pass

fileArm = 'A_Arm'
fileHand = 'A_Hand'
fileTip = 'A_Tip'
ext = '.png'
scaling = 0.65
background = 'test.jpg'
save = True
numTestCases = 100

createData(fileHand, ext, scaling, save)
