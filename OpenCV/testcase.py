import cv2
import numpy as np
import imutils

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

	print xMin, yMin, xMax, yMax

	return xMin, yMin, xMax, yMax

def createData ():
	pass

fileArm = 'A_Arm'
fileHand = 'A_Hand'
fileTip = 'A_Tip'
ext = '.png'
scaling = 0.65
background = 'test.jpg'
createImage = True
numTestCases = 100


calculateBoundingBox(cv2.imread(fileArm+ext))
calculateBoundingBox(cv2.imread(fileHand+ext))
calculateBoundingBox(cv2.imread(fileTip+ext))




