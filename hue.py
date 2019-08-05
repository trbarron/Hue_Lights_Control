import pygame, pygame.midi, pprint, math, lightpack, sys, time, colorsys, csv, threading
from phue import Bridge
import pandas as pd
from scapy.all import *
import extPS, extBS, extTimer

################################

b = Bridge('192.168.0.2')
MACs = ['78:e1:03:f6:27:dc','18:74:2e:25:ec:12','18:74:2e:80:4c:c7','68:37:e9:2e:55:4a']
exitFlag = 0

lightpack_enabled = False

# Configuration
# host = '192.168.0.4' # (default)
# port = 3636 # (default)

# api_key = '{secret-code}' # Default is None

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Connect to the Lightpack API
if lightpack_enabled:
        lp = lightpack.Lightpack()
        try:
                lp.connect()
        except lightpack.CannotConnectError as e:
                print(repr(e))
                sys.exit(1)

        # Lock the Lightpack so we can make changes
        lp.lock()
else: lp = None

################################

pygame.init()
pygame.fastevent.init()
pygame.midi.init()

event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

input_id = pygame.midi.get_default_input_id()
light = b.get_light_objects('name')

[r,g,bl] = [0,0,0]

colored_lights = ['living room 1','living room 2','living room 3','bedroom 1','bedroom 2']
bnw_lights = ['dressing room','bathroom 1','bathroom 2','bathroom 3','bathroom 4','entryway 1']
lightpack = ['lightpack']

lights = b.get_light_objects('id')

f = 'weatherScenes.csv' #point it towards CSV
data = pd.read_csv(f)

hunk_of_data = [data,lights,input_id,colored_lights,lightpack,bnw_lights,light,lp,MACs,lightpack_enabled]

################################

class padSniffer (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
           extPS.extPadSniffer(hunk_of_data)
                
class buttonSniffer (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
           extBS.extButtonSniffer(hunk_of_data)

class wakeupTimer (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
           extTimer.extWakeupTimer(hunk_of_data)


# Create new threads
thread1 = padSniffer(1, "Thread-1", 1)
thread2 = buttonSniffer(2, "Thread-2", 2)
thread3 = wakeupTimer(3, "Thread-3", 3)


# Start new Threads

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()
print ("Exiting Main Thread")

