import signal

def handler(signum, frame):
   print "Forever is over!"
   raise Exception("end of time")
 
def loop_forever():
   import time
   while 1:
      print "sec"
      time.sleep(1)

# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

# Define a timeout for your function
signal.alarm(2)

try:
   loop_forever()
except Exception, exc: 
   print exc

# Cancel the timer if the function returned before timeout
# (ok, mine won't but yours maybe will :)
signal.alarm(0)
