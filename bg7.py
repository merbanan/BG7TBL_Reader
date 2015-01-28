import serial
import time
import numpy as np
import Image
from pylab import *

hold(False)
ser = serial.Serial('/dev/ttyUSB0',57600,timeout=1)
#ser.write("\x8f\x72\x00\x8f\x72\x00\x8f\x72\x00")
#s = ser.read(10)
#ser.write("\x8f\x76\x8f\x66\x30\x30\x30\x30\x30\x30\x30\x30\x30")
#s = ser.read(10)
#ser.write("\x8f\x73\x8f\x66\x30\x30\x30\x30\x30\x30\x30\x30\x30")
#s = ser.read(10)
#ser.write("\x8f\x76\x8f\x66\x30\x30\x30\x30\x30\x30\x30\x30\x30")
#s = ser.read(10)
#ser.write("\x8f\x73\x8f\x66\x30\x30\x30\x30\x30\x30\x30\x30\x30")
#s = ser.read(10)
freq = "015000000" # 9
stepsize = "00009000" # 8
samples = "0250" # 4
print stepsize
arr = np.zeros( (1, int(samples)), np.uint8 )

import matplotlib.pyplot as plt
arr = []
bw = int(stepsize)*int(samples)*10
print "Bandwidth = " + str(bw) + " Hz"
print "Min freq = " + str(int(freq)*10)
print "Max freq = " + str(int(freq)*10 + int(bw))
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
	arr.append(sub_list)
        ax=subplot(211)
        arr2 = np.mean(arr,axis=0)
        ax.autoscale(True)
        ax.plot(X,arr2)

	ax1=subplot(212)
	ax1.imshow(arr,cmap=plt.cm.spectral) #Needs to be in row,col order
#	plt.plot(X,arr2)
        plt.savefig('./fig.jpg')


#print arr

#q = np.array(arr)
#im = Image.fromarray(q)
#im.save("/home/michael/specgram.jpeg") 


sub_list2 = [75*(float(x) / 255) for x in sub_list]
#print sub_list
#print len(sub_list)
#print sub_list2
import matplotlib.pyplot as plt
plt.plot(X,sub_list2)
plt.show()



#plt.ylabel('RSSI')
#plt.show()
