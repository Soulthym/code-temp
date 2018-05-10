import numpy as np
import sys
import freenect
import cv2
import os
import signal
import time

def handler(signum, frame):
    print "Timed Out"
    exit(2)
    raise Exception("timeout")

print "Initialisation"
# time.sleep(5)
signal.signal(signal.SIGALRM, handler)
i = 0
while True:
    signal.alarm(2)
    try :
        depth = freenect.sync_get_depth()[0]
    except Exception, exc:
        if exc == "timeout":
            print "Timed out : ",
        else :
            print "Can't connect to the Kinect :",
        print "Error loading the depth image ! \tTrying again ({})...".format(i)
        i+=1
        signal.alarm(2)
    else :
        print"Loaded correctly !"
        break

signal.alarm(0)
time.sleep(1)
os.system('clear')
while True:
    depth = freenect.sync_get_depth()
    print np.shape(depth)
    # cv2.imshow("image",depth)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()