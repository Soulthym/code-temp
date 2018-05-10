import freenect
import cv2
import numpy as np
import socket
import os
import signal
import time

"""
Grabs a depth map from the Kinect sensor and creates an image from it.
"""

def handler(signum, frame):
    print "Timed Out"
    exit(1)
    raise Exception("timeout")

def nothing(x):
    pass

def getDepthMap():	
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)

    return depth

def imshow2(one, two):
    cv2.imshow("image",np.hstack((one,two)))

def imshow3(one, two, three):
    cv2.imshow("image",np.hstack((one,two,three)))


kinectx = 640.0
kinecty = 480.0
pcx = 1600.0
pcy = 900.0
rx = kinectx/pcx
ry = kinecty/pcy

nbCalibrationFrames = 128

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

# two = np.asarray([c for c in [r for r in one]], dtype=np.uint8)
print "============================================"
print "                Calibrating"
print "============================================"
print
for i in range(nbCalibrationFrames):
    m = getDepthMap()
    minit = np.minimum(minit,m)
    progress = int((i+1)/(nbCalibrationFrames*0.01))
    print '\033[4;0f[{0}{1}] {2}%'.format('#'*(progress/10),' '*(10-progress/10), progress)
    # \033[H
    # imshow2(minit,m)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit


print "============================================"
print "                 Tracking"
print "============================================"
cv2.namedWindow('image')
cv2.createTrackbar('L','image',0,255,nothing)
# cv2.createTrackbar('H','image',0,255,nothing)
# cv2.createTrackbar('iterations','image',0,15,nothing)
# hote = ''
# port = 12800

# connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connexion_principale.bind((hote, port))
# connexion_principale.listen(5)
# print "Le serveur ecoute a present sur le port {}".format(port)

# connexion_avec_client, infos_connexion = connexion_principale.accept()
# msg_a_envoyer = b""

kernel = np.ones((3,3),np.uint8)

while True:
    m = getDepthMap()
    m = np.where(m==255,0,m)
    sub = m-minit
    l = cv2.getTrackbarPos('L','image')
    # h = cv2.getTrackbarPos('H','image')
    # i = cv2.getTrackbarPos('iterations','image')
    # _,thresh = cv2.threshold(sub,l,255,cv2.THRESH_TOZERO_INV)
    # thresh2 = cv2.threshold(sub,l,255,cv2.THRESH_BINARY)[1]
    thresh = cv2.threshold(sub,254,255,cv2.THRESH_TOZERO)[1]
    
    erode = cv2.erode(thresh,kernel,iterations = 2)
    x,y = np.where(erode==255)
    if len(x) > 0:
        n = 1.0
        mx = 0
        my = 0
        for xx,yy in zip(x,y):
            mx += xx
            my += yy
            n  += 1
            # print "({0}, {1})".format(xx,yy),
        mx /= n
        my /= n
        print "({0}, {1})".format(mx*rx,my*ry)
        # msg_a_envoyer = str(int(my*ry))+" "+str(int(mx*rx))
        # msg_a_envoyer = msg_a_envoyer.encode()
        # connexion_avec_client.send(msg_a_envoyer)
        # msg_recu = connexion_avec_client.recv(1024)
        # print(msg_recu.decode())

    px=x
    py=y
    imshow3(m,thresh,erode)
        #,thresh2)
    # break
    # print(np.average(minit),np.average(m),np.average(sub))
    if cv2.waitKey(1) == 27: 
        break  # esc to quit

cv2.destroyAllWindows()
