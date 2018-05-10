import signal
import os

def handler(signum, frame):
   print "Forever is over!"
   raise Exception("end of time")
 
signal.signal(signal.SIGALRM, handler)

signal.alarm(1)

try:
   os.system("python looper.py &")
except Exception, exc:
   print exc
signal.alarm(0)