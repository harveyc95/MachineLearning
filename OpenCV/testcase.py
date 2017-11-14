import cv2
import numpy as np
import imutils
import pickle
import math
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

def resize(image, scaling):
	width = image.shape[1]
	height = image.shape[0]
	widthResized = int(width*scaling)
	heightResized = int(height*scaling)
	resized = cv2.resize(image, (widthResized,heightResized))
	return resized

def rotate(image, angle):
	rotated = imutils.rotate_bound(image, angle)
	return rotated

def process(image, scaling, angle):
	resized = resize(image, scaling)
	rotatedAndResized = rotate(resized, angle)
	return rotatedAndResized

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

def overlay(arm, background, box, xDesired, yDesired, xTip, yTip):
	wBg = background.shape[1] -1
	hBg = background.shape[0] -1
	wFg = arm.shape[1] -1
	hFg = arm.shape[0] -1
	xOffset = xDesired - xTip
	yOffset = yDesired - yTip
	xBgStart = max(0, 0 + xOffset)
	yBgStart = max(0, 0 + yOffset)
	xBgEnd = min(wBg, wFg + xOffset)
	yBgEnd = min(hBg, hFg + yOffset)

	wHand = box._xMax - box._xMin 
	hHand = box._yMax - box._yMin
	xBoxStart = max(0, box._xMin + xOffset)
	yBoxStart = max(0, box._yMin + yOffset)
	xBoxEnd = min(wBg, box._xMax + xOffset)
	yBoxEnd = min(hBg, box._yMax + yOffset)
	print xBoxStart, xBoxEnd, yBoxStart, yBoxEnd

	bgCrop = background[yBgStart:yBgEnd, xBgStart:xBgEnd]
	
	xFgStart = xBgStart - xOffset
	yFgStart = yBgStart - yOffset
	xFgEnd = xBgEnd - xOffset
	yFgEnd = yBgEnd - yOffset

	fgCrop = arm[yFgStart:yFgEnd, xFgStart:xFgEnd]

	# Now create a mask and create its inverse
	fgImgGray = cv2.cvtColor(fgCrop,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(fgImgGray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# Now black-out the area of logo in ROI
	bgCropMasked = cv2.bitwise_and(bgCrop,bgCrop, mask = mask_inv)

	# Put logo in ROI and modify the main image
	overlayed = cv2.add(bgCropMasked,fgCrop)
	result = np.copy(background)
	result[yBgStart:yBgEnd, xBgStart:xBgEnd] = overlayed

	for col in range (xBoxStart, xBoxEnd, 1):
		result[yBoxStart][col] = [255,255,255]
		result[yBoxEnd][col] = [255,255,255]
	for row in range (yBoxStart, yBoxEnd, 1):
		result[row][xBoxStart] = [255,255,255]
		result[row][xBoxEnd] = [255,255,255]

	cv2.imshow('res',result)
	cv2.waitKey(0)

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


# def overlay (bgImg, fgImg, x, y):
# 	fgBox = adjust(0,0,fgImg.shape[1],fgImg.shape[0], x, y)

# 	xStart = 0 if (fgBox._xMin < 0) else fgBox._xMin
# 	yStart = 0 if (fgBox._yMin < 0) else fgBox._yMin

def createData (armImg, handImg, tipImg, backgroundImg, scaling, angle):
	arm = process(armImg, scaling, angle)

	hand = process(handImg, scaling, angle)
	handBox = boundingBox(hand)

	tip = process(tipImg, scaling, angle)
	tipBox = boundingBox(tip)

	xTip = ((tipBox._xMin + tipBox._xMax)/2)
	yTip = ((tipBox._yMin + tipBox._yMax)/2)

	for i in range (10, 1000, 200):
		for j in range (10, 1000, 200):
			overlay(arm, backgroundImg, handBox, i, j, xTip, yTip)

def pad (arm, hand, tip):
	box = boundingBox(arm)
	cX = arm.shape[1] // 2
	cY = arm.shape[0] // 2
	radius = max(math.hypot((cX-box._xMin),(cY-box._yMin)),math.hypot((box._xMax-cX),(box._yMax-cY)))
	radius = ((radius + 44) // 5 * 5)
	diameter = int(2*radius)
	new = np.zeros((diameter,diameter,3), np.uint8)
	newX = new.shape[1] // 2
	newY = new.shape[0] // 2

	xStart = new.shape[1] // 2 - cX
	yStart = new.shape[0] // 2 - cY
	xEnd = new.shape[1] // 2 + cX
	yEnd = new.shape[0] // 2 + cY	

	for col in range (0, arm.shape[1], 1):
		for row in range (0, arm.shape[0], 1):
			new[yStart+row][xStart+col] = tip[row][col]
	cv2.imwrite("Tip_Pad.png", new)

	for col in range (0, arm.shape[1], 1):
		for row in range (0, arm.shape[0], 1):
			new[yStart+row][xStart+col] = hand[row][col]
	cv2.imwrite("Hand_Pad.png", new)

	for col in range (0, arm.shape[1], 1):
		for row in range (0, arm.shape[0], 1):
			new[yStart+row][xStart+col] = arm[row][col]
	cv2.imwrite("Arm_Pad.png", new)

# return list of frames from videoFile at framesToSkip intervals
def getFrames (videoFile, framesToSkip):
	vid = cv2.VideoCapture(videoFile)
	length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
	print length
	frames = []
	for i in range (0, (length//framesToSkip)):
		vid.set(1, i*framesToSkip)
		ret, frame = vid.read()
		frames.append(frame)
	return frames

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

# createData(arm, hand, tip, background, scaling, angle)
# for angle in range (-10, 10, 3):
# 	createData(arm.img, hand.img, tip.img, background.img, scaling, angle)

# pad(arm.img, hand.img, tip.img)

cwd = os.getcwd()
frames = getFrames(cwd+'/Video/'+'Cosmos.mp4', 500)

print len(frames)
for frame in frames:
	cv2.imshow('frame', frame)
	cv2.waitKey(0)

