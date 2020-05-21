# import the necessary packages
import cv2
from MyNewVideoStream import MyNewVideoStream
# construct the argument parse and parse the arguments
url = 'http://192.168.0.101:8000/video_feed'
# start the file video stream thread and allow the buffer to

# start to fill
fvs = MyNewVideoStream(path=url, queueSize=5)

# loop over frames from the video file stream
while True:
    frame = fvs.read()	
    
    cv2.imshow("Frame", frame)  

    if cv2.waitKey(1) == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()