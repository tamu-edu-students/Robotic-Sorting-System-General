###testing openCv and raspberry pi camera connection
from picamera2 import Picamera2, Preview
import cv2
import sys
import time
#import json

num_sec = 15
#address = "/home/lifeofpi/BLEProject/subsystem_connection.json"

#with open(address, "r") as f:      # read the json file   ##note, you have to change this address when working with the raspi
#  variables = json.load(f)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280) #<-------this will screw up the camera quality
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720) #<---------
start_time = time.time()

num_sec = 15
while(True):

    ret,frame = cap.read()
    frame = frame[150:720,400:1100]
    #cv2.imshow("Frame", frame)
    #cv2.imwrite('intg_test.jpg', frame)
    
    #print("picture taken")
    #ch = cv2.waitKey(1)
    #if ch & 0xFF == ord('q'):
    #    break
    if time.time() - start_time >= num_sec:  #<---check if 15 sec passed
        cv2.imwrite('intg_test.jpg', frame)
        print("picture taken")
        start_time = time.time()
    #cap.release()
    #cv2.destroyAllWindows()