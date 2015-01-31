import sys
import os
import serial
import time
import numpy as np
import Image
import argparse
from pylab import *
import time
from datetime import date

parser = argparse.ArgumentParser(description='Output heatmap.py-compatible power files for BG7TBL Spec Analyzer')
parser.add_argument('output_path', metavar='TITLE', type=str,
    help='One-word-title of your job.')
slicegroup = parser.add_argument_group('Slicing',
    'Efficiently render a portion of the data. (optional)  Frequencies can take G/M/k suffixes.  Timestamps look like "YYYY-MM-DD HH:MM:SS"  Durations take d/h/m/s suffixes.')
slicegroup.add_argument('--low', dest='low_freq', default=None,
    help='Minimum frequency for scanning.')
slicegroup.add_argument('--high', dest='high_freq', default=None,
    help='Maximum frequency for scanning.')
#slicegroup.add_argument('--res', dest='res_factor', default=None,
#    help='Resolution factor. Greater than 1 results in n-range scan')
#slicegroup.add_argument('--samples', dest='samples', default=None,
#    help='Number of samples')
#slicegroup.add_argument('--stepsize', dest='stepsize', default=None,
#    help='Duration to use, stopping at the end.')
for i, arg in enumerate(sys.argv):
    if (arg[0] == '-') and arg[1].isdigit():
        sys.argv[i] = ' ' + arg
args = parser.parse_args()

#From keenard's code

def freq_parse(s):
    suffix = 1
    if s.lower().endswith('k'):
        suffix = 1e3
    if s.lower().endswith('m'):
        suffix = 1e6
    if s.lower().endswith('g'):
        suffix = 1e9
    if suffix != 1:
        s = s[:-1]
    return float(s) * suffix









low_freq = freq_parse(args.low_freq)
high_freq = freq_parse(args.high_freq)
samples = 1000

stepsize=int(((int(high_freq)-int(low_freq))/samples))
if (stepsize < 1000):
	print "Stepsize too small. Increasing frequency interval."
	stepsize=1000
	high_freq=int(low_freq)+stepsize*samples


date = datetime.datetime.now()
csvfile = date.strftime("%Y_%j__%H_%M_%S_%f")

file = open(args.output_path + '--' + csvfile + '.csv', 'w')

#today = date.fromtimestamp(time.time())
hold(False)
ser = serial.Serial('/dev/ttyUSB0',57600,timeout=1)
freq_int = int(int(low_freq)/10)


freq_str = "{0:0>9}".format(freq_int) # 9
#freq2_str = "{0:0>9}".format(freq2) # 9
#stepsize = "00011000" # 8
#freq = "013800000" # 9
stepsize_str = "{0:0>8}".format(stepsize/10) # 9

#stepsize2 = "00100000" # 8
samples_str = "{0:0>4}".format(samples) # 9
#samples = "1000" # 4
#print stepsize
arr = np.zeros( (1, samples), np.uint8 )

arr = []
bw = stepsize*samples*10
print "Bandwidth = " + str(bw) + " Hz"
print "Min freq = " + str(freq_int*10)
print "Max freq = " + str(freq_int*10 + int(bw))
print "Samples = " + str(samples)
print "Stepsize = " + str(stepsize)
X = np.linspace(freq_int*10, freq_int*10 + int(bw), samples)
print args.output_path + '--' + csvfile + '.csv'
sys.stdout.flush()
for x in range(0, 1000000):
	time.sleep(5)
	ser.write("\x8f\x78" + freq_str + stepsize_str + samples_str)
        time.sleep(12)
	t = ser.readline()

#print "please wait..."
#print s
        byte_list = map(ord,t)

	c = byte_list
	sub_list = filter(lambda a: a != 0, c)[::2]

#	sub_list = [((byte*0.191187)+-87.139634) for byte in sub_list]

	chunks=[sub_list[x:x+10] for x in xrange(0, len(sub_list), 10)]
	arr.append(sub_list)

	date = datetime.datetime.now()
	freq1 = freq_int*10
	freq2 = freq_int*10
	stepsizeline = stepsize*10
	stepsizesingle = stepsize
        for i in range (0, len(chunks), 1):
	        sub_list_str = map(str,chunks[i])
		powerstring = ", ".join(sub_list_str)
		sample_max = int(samples)
		sample_min = 1
		freq1 = (freq_int*10 + i*(stepsizeline*10))
		freq2 = ((freq_int*10) + (i+1)*(stepsizeline*10) - (stepsizesingle*10))
		string1 = date.strftime("%Y-%m-%d") + ", " + date.strftime('%H:%M:%S') + ", " + str(freq1) + ", " + str(freq2) + ", " + str(stepsize*10) + ", " + str(samples) + ", " + powerstring + "\n"
		file.write(string1)
		file.flush()


file.close()
  #      ax=subplot(211)
  #      arr2 = np.mean(arr,axis=0)
  #      ax.autoscale(True)
  #      ax.plot(X, arr2)
  #	ax1=subplot(212)
  #	r = int(freq)*10
  #	s = int(freq)*10 + int(bw)
  #	ax1.imshow(arr, cmap=plt.cm.spectral) #Needs to be in row,col order
  #      plt.savefig('./fig.jpg')

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
