import cv2
import numpy as np
import imutils
import pickle
import os
import random
from box import boundingBox, boundingTest

def overlay(arm, background, hand, tip, xDesired, yDesired):
	xTip = ((tip._xMin + tip._xMax)/2)
	yTip = ((tip._yMin + tip._yMax)/2)
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

	wHand = hand._xMax - hand._xMin 
	hHand = hand._yMax - hand._yMin
	xBoxStart = max(0, hand._xMin + xOffset)
	yBoxStart = max(0, hand._yMin + yOffset)
	xBoxEnd = min(wBg, hand._xMax + xOffset)
	yBoxEnd = min(hBg, hand._yMax + yOffset)

	bgCrop = background[yBgStart:yBgEnd, xBgStart:xBgEnd]
	
	xFgStart = xBgStart - xOffset
	yFgStart = yBgStart - yOffset
	xFgEnd = xBgEnd - xOffset
	yFgEnd = yBgEnd - yOffset

	fgCrop = arm[yFgStart:yFgEnd, xFgStart:xFgEnd]

	if (abs(xBoxEnd - xBoxStart) * abs(yBoxEnd - yBoxStart)) < hand.area()*0.9:
		# print "illegal"
		return False, None, ""

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

	# for col in range (xBoxStart, xBoxEnd, 1):
	# 	result[yBoxStart][col] = [255,255,255]
	# 	result[yBoxEnd][col] = [255,255,255]
	# for row in range (yBoxStart, yBoxEnd, 1):
	# 	result[row][xBoxStart] = [255,255,255]
	# 	result[row][xBoxEnd] = [255,255,255]

	# result[yDesired][xDesired] = [255,0,0]
	# result[yDesired-1][xDesired] = [255,0,0]
	# result[yDesired][xDesired-1] = [255,0,0]
	# result[yDesired-1][xDesired-1] = [255,0,0]

	# cv2.imshow('res',result)
	# cv2.waitKey(0)

	position = [xBoxStart, yBoxStart, xBoxEnd, yBoxEnd, xDesired, yDesired]
	#position = str(xBoxStart) + ', ' + str(yBoxStart) + str(xBoxEnd) + ', '  str(yBoxEnd) + ', ' + str(xDesired) + ', ' +str(yDesired)
	return True, result, position

def generateData (arm, background, hand, tip):
	generated = False
	while not generated:
		x = random.randint(0,600-1)
		y = random.randint(0,400-1)
		generated, img, position = overlay(arm, background, hand, tip, x, y)
	return img, position

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

	
