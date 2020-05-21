from threading import Thread
from queue import Queue
import urllib.request
import numpy as np
import cv2

class MyNewVideoStream:
    def __init__(self, path, queueSize=5):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = urllib.request.urlopen(path)
        self.total_bytes = b''
        self.stopped = False
        # initialize the queue used to store frames read from
        self.Q = Queue(maxsize=queueSize)
        self.start()

    def start(self):
        
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

    def update(self):
        # keep looping infinitely
        total_bytes = b''
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return
            # otherwise, ensure the queue has room in it
            if self.Q.full():
                flush = self.Q.get_nowait()

            # read the next frame from the file
            total_bytes += self.stream.read(1024)
            b = total_bytes.find(b'\xff\xd9')
            if not b == -1:
                a = total_bytes.find(b'\xff\xd8') # JPEG start
                jpg = total_bytes[a:b+2] # actual image
                total_bytes= total_bytes[b+2:] # other informations
                
                # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # add the frame to the queue
                self.Q.put(frame)        

    def read(self):
        return self.Q.get()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
