import cv2
import os
import glob
import pickle

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

def show(frames):
	print len(frames)
	for frame in frames:
		cv2.imshow('frame', frame)
		cv2.waitKey(0)

def writeFrames(frames):
	i = 0
	for frame in frames:
		savePath = os.path.join(os.getcwd(), 'background', str(i))
		savePath = savePath + ".png"
		print savePath
		frame = cv2.resize(frame, (600, 400)) 
		cv2.imwrite(savePath, frame)
		i = i + 1
		if (i%100 == 0):
			print i

def resizeFrames(frames):
	resized = []
	for frame in frames:
		frame = cv2.resize(frame, (600, 400))
		resized.append(frame)
	return resized

path = os.path.join(os.getcwd(), 'Video')

frames = []
framesToSkip = 100
for video in glob.glob(path+"/*.mp4"):
	print video
	frames.extend(getFrames(video, framesToSkip))

frames = resizeFrames(frames)

print "pickling"
pickle_out = open("background.pickle","wb")
pickle.dump(frames, pickle_out)
pickle_out.close()
print "done pickling"

writeFrames(frames)