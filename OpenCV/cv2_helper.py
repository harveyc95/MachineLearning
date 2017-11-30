import cv2
import imutils

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