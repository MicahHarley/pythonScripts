import imutils
import time
import cv2

url = 'http://192.168.2.4:8000/video_feed'

vcap = cv2.VideoCapture(url)
vcap.set(cv2.CAP_PROP_BUFFERSIZE,1) 
FPS = 1/30
FPS_MS = int(FPS * 1000)

time.sleep(2.0)

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    ret, frame = vcap.read()
    #frame = imutils.resize(frame, width=400)
    
    if ret:
        # show the output frame
        cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(FPS_MS) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vcap.release()