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

def adjust(xMin, yMin, xMax, yMax, x, y):
	xMin = x - xMin
	yMin = y - yMin
	xMax = xMax - xMin
	yMax = yMax - yMin
	box = Box(xMin, yMin, xMax, yMax)
	print box
	return box

class MyImage:
	def __init__(self, img_name, img_ext):
		self.img = cv2.imread(img_name+img_ext)
		self.name = img_name
		self.ext = img_ext
		self.box = None

	def __str__(self):
		return self.name

	def show(self):
		cv2.imshow(self.name, self.img)
		cv2.waitKey(0)

	def resize(self, scaling):
		width = self.img.shape[1]
		height = self.img.shape[0]
		widthResized = int(width*scaling)
		heightResized = int(height*scaling)
		resized = cv2.resize(self.img, (widthResized,heightResized))
		resizedName = self.name + '_' + str(scaling) + 'x_' + str(widthResized) + 'x' + str(heightResized) + self.ext
		self.img = resized
		self.name = resizedName

	def rotate(self, angle):
		rotated = imutils.rotate_bound(self.img, angle)
		rotatedName = self.name + '_' + str(angle) + self.ext
		self.img = rotated
		self.name = rotatedName

	def boundingBox(self):
		w = self.img.shape[1]
		h = self.img.shape[0]
		xMin = w
		xMax = 0
		yMin = h
		yMax = 0
		black = np.zeros((1,1,3), np.uint8)
		for col in range (0, w):
			for row in range (0, h):
				if (np.any(self.img[row][col] != black)):
					xMin = min(xMin, col)
					xMax = max(xMax, col)
					yMin = min(yMin, row)
					yMax = max(yMax, row)

		box = Box(xMin, yMin, xMax, yMax)
		self.box = box

	def overlay(self, background, xDesired, yDesired, xTip, yTip):
		black = np.zeros((1080,1920,3), np.uint8)
		w = self.img.shape[1]
		h = self.img.shape[0]
		xOffset = xDesired - xTip
		yOffset = yDesired - yTip
		xBgStart = max(0, 0 + xOffset)
		yBgStart = max(0, 0 + yOffset)
		xBgEnd = min(1920, w + xOffset)
		yBgEnd = min(1080, h + yOffset)

		print xBgEnd-xBgStart, yBgEnd-yBgStart

		bgCrop = background.img[yBgStart:yBgEnd, xBgStart:xBgEnd]
		# cv2.imshow('bgCrop', bgCrop)
		
		xFgStart = xBgStart - xOffset
		yFgStart = yBgStart - yOffset
		xFgEnd = xBgEnd - xOffset
		yFgEnd = yBgEnd - yOffset

		print xFgEnd-xFgStart, yFgEnd-yFgStart

		fgCrop = self.img[yFgStart:yFgEnd, xFgStart:xFgEnd]

		# Now create a mask and create its inverse
		fgImgGray = cv2.cvtColor(fgCrop,cv2.COLOR_BGR2GRAY)
		ret, mask = cv2.threshold(fgImgGray, 10, 255, cv2.THRESH_BINARY)
		mask_inv = cv2.bitwise_not(mask)

		# Now black-out the area of logo in ROI
		bgCropMasked = cv2.bitwise_and(bgCrop,bgCrop, mask = mask_inv)

		# Put logo in ROI and modify the main image
		overlayed = cv2.add(bgCropMasked,fgCrop)
		result = np.copy(background.img)
		result[yBgStart:yBgEnd, xBgStart:xBgEnd] = overlayed
		cv2.imshow('res',result)
		cv2.waitKey(0)

# Input: image
# Output: bounding box of xMin, yMin, xMax, yMax
# Note: assumes entire image is black except the part looking for bounding box

def boudingTest(image, box):
	for col in range (box._xMin, box._xMax, 1):
		image[box._yMin][col] = [255,255,255]
		image[box._yMax][col] = [255,255,255]
	for row in range (box._yMin, box._yMax, 1):
		image[row][box._xMin] = [255,255,255]
		image[row][box._xMax] = [255,255,255]
	return image


# def overlay (bgImg, fgImg, x, y):
# 	fgBox = adjust(0,0,fgImg.shape[1],fgImg.shape[0], x, y)

# 	xStart = 0 if (fgBox._xMin < 0) else fgBox._xMin
# 	yStart = 0 if (fgBox._yMin < 0) else fgBox._yMin

def createData (arm, hand, tip, background, scaling, angle):
	arm.resize(scaling)
	arm.rotate(angle)

	hand.resize(scaling)
	hand.rotate(angle)

	tip.resize(scaling)
	tip.rotate(angle)
	tip.boundingBox()
	fgBox = tip.box
	xFg = ((fgBox._xMin + fgBox._xMax)/2)
	yFg = ((fgBox._yMin + fgBox._yMax)/2)
	print xFg, yFg
	xDesired = 200
	yDesired = 600

	print "overlay"

	for i in range (10, 1000, 200):
		for j in range (10, 1000, 200):
			arm.overlay(background, i, j, xFg, yFg)

fileArm = 'A_Arm'
fileHand = 'A_Hand'
fileTip = 'A_Tip'
ext = '.png'
scaling = 0.75
angle = 0
background = 'test'
numTestCases = 100

arm = MyImage(fileArm,ext)
hand = MyImage(fileHand,ext)
tip = MyImage(fileTip,ext)
background = MyImage(background,'.jpg')

createData(arm, hand, tip, background, scaling, angle)



