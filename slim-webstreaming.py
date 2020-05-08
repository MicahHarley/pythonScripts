# USAGE
# python webstreaming.py --ip 0.0.0.0

# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import Adafruit_DHT

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

sensor = Adafruit_DHT.DHT11
text = ""

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
vs = VideoStream(usePiCamera=1).start()
#vs = VideoStream(src=0).start()
time.sleep(2.0)

def weather():
        global text, sensor
        while True:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, 14)
                if humidity is not None and temperature is not None:
                        temperature = temperature * 9/5.0 + 32
                        text = '{}F'.format(temperature) + '{}%'.format(humidity)

@app.route("/")
def index():
        # return the rendered template
        return render_template("index.html")

def detect_motion():
        # grab global references to the video stream, output frame, and
        # lock variables
        global vs, outputFrame, lock, text

        # loop over frames from the video stream
        while True:
                # read the next frame from the video stream, resize it,
                # convert the frame to grayscale, and blur it
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                #cv2.putText(frame, text, (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

                # acquire the lock, set the output frame, and release the
                # lock
                with lock:
                        outputFrame = frame.copy()
def generate():
        # grab global references to the output frame and lock variables
        global outputFrame, lock

        # loop over frames from the output stream
        while True:
                # wait until the lock is acquired
                with lock:
                        # check if the output frame is available, otherwise skip
                        # the iteration of the loop
                        if outputFrame is None:
                                continue

                        # encode the frame in JPEG format
                        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

                        # ensure the frame was successfully encoded
                        if not flag:
                                continue

                # yield the output frame in the byte format
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                        bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
        # return the response generated along with the specific media
        # type (mime type)
        return Response(generate(),
                mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
        # construct the argument parser and parse command line arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--ip", type=str, required=True,
                help="ip address of the device")
        args = vars(ap.parse_args())

        # start a thread that will perform motion detection
        t = threading.Thread(target=detect_motion)
        t.daemon = True
        t.start()

        #threading.Thread(target=weather).start()

        # start the flask app
        app.run(host=args["ip"], port=8000, debug=True,
                threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
