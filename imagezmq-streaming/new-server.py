# USAGE
# python server.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --montageW 2 --montageH 2

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

frameDict = {}

FPS = {"raspberrypi":0,"USB":0}
last = {"raspberrypi":datetime.now(),"USB":datetime.now()}
cam1FPS = 0
cam2FPS = 0

mW = 2
mH = 1

while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    
    FPS["raspberrypi"] = (datetime.now() - last["raspberrypi"])
    FPS["USB"] = (datetime.now() - last["USB"])
  
    #for i in FPS:
    #    FPS[i] = (datetime.now() - last[i]).microseconds
    print(FPS)
    last[rpiName] = datetime.now()

    frame = imutils.resize(frame, width=800)
    (h, w) = frame.shape[:2]

    # update the new frame in the frame dictionary
    frameDict[rpiName] = frame

    # build a montage using images in the frame dictionary
    montages = build_montages(frameDict.values(), (w, h), (mW, mH))

    # display the montage(s) on the screen
    for (i, montage) in enumerate(montages):
        cv2.imshow("Cameras ({})".format(i), montage)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()