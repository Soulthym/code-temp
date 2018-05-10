import freenect
import numpy as np
import os
import signal
import time

def handler(signum, frame):
    print "Timed Out"
    exit(2)
    raise Exception("timeout")

def getDepthMap():	
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)

    return depth

print "Initialisation"
signal.signal(signal.SIGALRM, handler)
i = 0
while True:
    signal.alarm(3)
    try :
        minit = getDepthMap()
    except Exception, exc:
        if exc == "timeout":
            print "Timed out : ",
        else :
            print "No connection to the Kinect :",
        print "Error loading the depth image ! \tTrying again ({})...".format(i)
        i+=1
        # signal.alarm(4)
    else :
        print"Loaded correctly !"
        break

signal.alarm(0)
time.sleep(1)
os.system('clear')
os.system('python ~/code/python/2.7/test-kinect.py')