import os
import cv2
import pickle
import random
import csv
import multiprocessing
import time
from tqdm import tqdm
from globbing import getArmHandTip
from cv2_helper import rotate
from box import boundingBox, boundingTest
from overlay import generateData

scaling = 0.16
angles = 10

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def writeImages(images):
	folderName = 'overlay'
	i = 0
	if not os.path.isdir(folderName):
		os.mkdir(folderName)

	for frame in tqdm(images):
		savePath = os.path.join(os.getcwd(), folderName, str(i))
		savePath = savePath + ".jpg"
		#print savePath
		cv2.imwrite(savePath, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
		i = i + 1
    # p = multiprocessing.Pool(8)
    # img_chuncks = chunkIt(images,8)
    # p.map(writingSlaves, img_chuncks)

class MyImage:
	def __init__(self, _image, _hand, _tip):
		self.img = _image
		self.hand = _hand
		self.tip = _tip

def a (arm, hand, tip):
	result = []
	for i in range (0, len(armA)):
		l = []
		for angle in range (-angles, angles):
			rotatedArm = rotate(arm[i], angle)

			rotatedHand = rotate(hand[i], angle)
			boxHand = boundingBox(rotatedHand)

			rotatedTip = rotate(tip[i], angle)
			boxTip = boundingBox(rotatedTip)

			img = MyImage(rotatedArm, boxHand, boxTip)

			l.append(img)
			print i, angle
		result.append(l)

	return result

if (os.path.isfile("GestureA.pickle") and os.path.isfile("GestureB.pickle") and os.path.isfile("background.pickle")):

	# pickle_in = open("GestureA.pickle","rb")
	# gestureA = pickle.load(pickle_in)
	# for gestures in gestureA:
	# 	for myImage in gestures:
	# 		img = boundingTest(myImage.img, myImage.hand)
	# 		img = boundingTest(myImage.img, myImage.tip)
	# 		cv2.imshow('t',img)
	# 		cv2.waitKey(0)

	# pickle_in = open("GestureB.pickle","rb")
	# gestureB = pickle.load(pickle_in)
	# for gestures in gestureB:
	# 	for myImage in gestures:
	# 		img = boundingTest(myImage.img, myImage.hand)
	# 		img = boundingTest(myImage.img, myImage.tip)
	# 		cv2.imshow('t',img)
	# 		cv2.waitKey(0)

	print "pls"

	numGenerated = 0
	maxGenerated = 30000

	pickle_in = open("GestureA.pickle","rb")
	gestureA = pickle.load(pickle_in)

	pickle_in = open("GestureB.pickle","rb")
	gestureB = pickle.load(pickle_in)

	pickle_in = open("background.pickle","rb")
	background = pickle.load(pickle_in)

	print "Done Loading Pickles"

	data = []

	with open('label.csv', 'wb') as fin:
		writer = csv.writer(fin)

		for numGenerated in tqdm(range(0, maxGenerated)):
			myList = gestureA[random.randint(0,len(gestureA)-1)]
			myImage = myList[random.randint(0,len(myList)-1)]
			bg = background[random.randint(0,len(background)-1)]
			img, position = generateData(myImage.img, bg, myImage.hand, myImage.tip)
			position.append(0)
			writer.writerow(position)
			numGenerated = numGenerated + 1
			data.append(img)

		numGenerated = 0
		for numGenerated in tqdm(range(0, maxGenerated)):
			myList = gestureB[random.randint(0,len(gestureB)-1)]
			myImage = myList[random.randint(0,len(myList)-1)]
			bg = background[random.randint(0,len(background)-1)]
			img, position = generateData(myImage.img, bg, myImage.hand, myImage.tip)
			position.append(1)
			writer.writerow(position)
			numGenerated = numGenerated + 1
			data.append(img)

	t1 = time.time()
	writeImages(data)
	print time.time() - t1

else:
	pathA = os.path.join(os.getcwd(), 'Hand', 'Gesture A', 'Cropped')
	pathB = os.path.join(os.getcwd(), 'Hand', 'Gesture B', 'Cropped')

	armA, handA, tipA = getArmHandTip(pathA, scaling)
	armB, handB, tipB = getArmHandTip(pathB, scaling)

	resultA = a (armA, handA, tipA)
	resultB = a (armB, handB, tipB)

	print "pickling A"
	pickle_out = open("GestureA.pickle","wb")
	pickle.dump(resultA, pickle_out)
	pickle_out.close()
	print "done pickling"

	print "pickling B"
	pickle_out = open("GestureB.pickle","wb")
	pickle.dump(resultB, pickle_out)
	pickle_out.close()
	print "done pickling"
