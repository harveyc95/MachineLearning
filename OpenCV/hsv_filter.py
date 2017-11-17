import cv2
import numpy as np

frame = cv2.imread('IMG_0207.jpg')

windowName_hand = 'hand_filter'
cv2.namedWindow(windowName_hand)
cv2.createTrackbar('MinH', windowName_hand, 0, 255, lambda x: x)
cv2.createTrackbar('MaxH', windowName_hand, 74, 255, lambda x: x)
cv2.createTrackbar('MinS', windowName_hand, 69, 255, lambda x: x)
cv2.createTrackbar('MaxS', windowName_hand, 255, 255, lambda x: x)
cv2.createTrackbar('MinV', windowName_hand, 0, 255, lambda x: x)
cv2.createTrackbar('MaxV', windowName_hand, 255, 255, lambda x: x)

def get_hsv(window_name):
    MinH = cv2.getTrackbarPos('MinH', window_name)
    MaxH = cv2.getTrackbarPos('MaxH', window_name)
    MinS = cv2.getTrackbarPos('MinS', window_name)
    MaxS = cv2.getTrackbarPos('MaxS', window_name)
    MinV = cv2.getTrackbarPos('MinV', window_name)
    MaxV = cv2.getTrackbarPos('MaxV', window_name)
    return [MinH, MaxH, MinS, MaxS, MinV, MaxV]

while(1):

    frame = cv2.resize(frame, (600, 600))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    MinH, MaxH, MinS, MaxS, MinV, MaxV = get_hsv(windowName_hand)
    res = cv2.inRange(hsv, (MinH, MinS, MinV), (MaxH, MaxS, MaxV))

    cv2.imshow('frame',frame)
    cv2.imshow('mask',hsv)
    cv2.imshow('res',res)
    if cv2.waitKey(0):
        break

cv2.destroyAllWindows()