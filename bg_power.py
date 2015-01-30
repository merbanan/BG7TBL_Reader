import serial
import time
import numpy as np
import Image
from pylab import *
import time
from datetime import date

date = datetime.datetime.now()
csvfile = date.strftime("%Y%m%d-%H%M%S")
file = open(csvfile + '.csv', 'w')
#today = date.fromtimestamp(time.time())
hold(False)
ser = serial.Serial('/dev/ttyUSB0',57600,timeout=1)
#freq = "340000000" # 9
#stepsize = "00011000" # 8
freq = "013800000" # 9
stepsize = "00426220" # 8

samples = "1000" # 4
#print stepsize
arr = np.zeros( (1, int(samples)), np.uint8 )

import matplotlib.pyplot as plt
arr = []
bw = int(stepsize)*int(samples)*10
#print "Bandwidth = " + str(bw) + " Hz"
#print "Min freq = " + str(int(freq)*10)
#print "Max freq = " + str(int(freq)*10 + int(bw))
X = np.linspace(int(freq)*10, int(freq)*10 + int(bw), int(samples))
for x in range(0, 1080):
	time.sleep(5)
	ser.write("\x8f\x78" + freq + stepsize + samples)
#print "please wait..."
	time.sleep(30)
	s = ser.readline()
#print s
	byte_list = map(ord,s)
	c = byte_list
	sub_list = filter(lambda a: a != 0, c)[::2]
#	sub_list = [((byte*0.191187)+-87.139634) for byte in sub_list]
	chunks=[sub_list[x:x+10] for x in xrange(0, len(sub_list), 10)]
	arr.append(sub_list)

	date = datetime.datetime.now()
	freq1 = int(freq)*10
	freq2 = int(freq)*10
	stepsizeline = int(stepsize)*10
	stepsizesingle = int(stepsize)
        for i in range (0, len(chunks), 1):
	        sub_list_str = map(str,chunks[i])
		powerstring = ", ".join(sub_list_str)
		sample_max = int(samples)
		sample_min = 1
		freq1 = (int(freq)*10 + i*(stepsizeline*10))
		freq2 = ((int(freq)*10) + (i+1)*(stepsizeline*10) - (stepsizesingle*10))
		string1 = date.strftime("%Y-%m-%d") + ", " + date.strftime('%H:%M:%S') + ", " + str(freq1) + ", " + str(freq2) + ", " + str(int(stepsize)*10) + ", " + str(int(samples)) + ", " + powerstring
		print string1
		f.write(string1)
  #      ax=subplot(211)
  #      arr2 = np.mean(arr,axis=0)
  #      ax.autoscale(True)
  #      ax.plot(X, arr2)
  #	ax1=subplot(212)
  #	r = int(freq)*10
  #	s = int(freq)*10 + int(bw)
  #	ax1.imshow(arr, cmap=plt.cm.spectral) #Needs to be in row,col order
  #      plt.savefig('./fig.jpg')
file.close()

#print arr

#q = np.array(arr)
#im = Image.fromarray(q)
#im.save("/home/michael/specgram.jpeg") 


#sub_list2 = [75*(float(x) / 255) for x in sub_list]
#print sub_list
#print len(sub_list)
#print sub_list2
#import matplotlib.pyplot as plt
#plt.plot(X,sub_list2)
#plt.show()



#plt.ylabel('RSSI')
#plt.show()
