import cv2
import numpy as np
import imutils

def overlay (bgImg, fgImg, x, y):
	# Load two images
	bgImg = cv2.imread('test.jpg')
	fgImg = cv2.imread('A_Cut_Black_1402_791.png')

	# I want to put logo on top-left corner, So I create a ROI
	rows,cols,channels = fgImg.shape
	roi = bgImg[x:rows, y:cols ]

	# Now create a mask of logo and create its inverse mask also
	fgImgGray = cv2.cvtColor(fgImg,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(fgImgGray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# Now black-out the area of logo in ROI
	bgImg_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

	# Take only region of logo from logo image.
	fgImg_fg = cv2.bitwise_and(fgImg,fgImg,mask = mask)

	# Put logo in ROI and modify the main image
	dst = cv2.add(bgImg_bg,fgImg_fg)
	bgImg[x:rows, y:cols ] = dst
	cv2.imshow('res',bgImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def rotate(image, filename, extension, start, end, step):
	# loop over the rotation angles again, this time ensure the
	# entire pill is still within the ROI after rotation
	bgImg = cv2.imread(background)
	for angle in np.arange(start, end, step):
		rotated = imutils.rotate_bound(image, angle)
		# overlay(bgImg, rotated, 0, 0)
		dst = filename + '_' + str(angle) + extension
		cv2.imwrite(dst, rotated)
		cv2.imshow("Rotated (Correct)", rotated)
		cv2.waitKey(0)

def resize(original, scaling):
	image = cv2.imread(filename+extension)

	scaling = 0.7

	width = image.shape[1]	#current image's width
	height = image.shape[0]	#current image's height
	print "width : %d\nheight : %d"%(width,height)
	cv2.imshow("original", image)

	widthResized = int(width*scaling)
	heightResized = int(height*scaling)
	resized = cv2.resize(image, (widthResized,heightResized))
	print "width : %d\nheight : %d"%(widthResized,heightResized)
	cv2.imshow("resized", resized)
	resizedName = filename + '_' + str(widthResized) + '_' + str(heightResized) + extension
	cv2.imwrite(resizedName, resized)

	cv2.waitKey(0)

fileA = 'A_Cut_Black_1402_791'
fileB = 'B_Cut_Black_1490_785'
background = 'test.jpg'
extension = '.png'

handA = cv2.imread(fileA+extension)
handB = cv2.imread(fileB+extension)
rotate(handA,fileA,extension,-10,10,1)
rotate(handB,fileB,extension,-10,10,1)