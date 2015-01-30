# BG7TBL_Reader
Read data from a BG7TBL Simple spectrum analyzer device

This program will read data from a BG7TBL and plot its fft and a scrolling spectrogram. In Linux Mint, you can open the fig.jpg file while it is running, so that the environment gets notified of the changes. Other linuxes probably have similar behavior. 

The default configuration is to plot the wifi band (2.4 GHz). You can change the start frequency and the other fields in the source file, but keep in mind the length of each field in ascii digits after the comment symbol.

All frequencies are multiplied by 10 behind the device. So, if you want to enter 1 GHz, enter 100,000,000 (without the commas) - which basically means 100 MHz. This is due to the internal frequency scaler.

If you want to enter 200 MHz, enter 020,000,000 (without the commas), or "020000000" in the freq field.

I designed this based on the BG7TBL Simple spectrum analyzer with range 138MHz-4.4 GHz, but devices based on the same software should work.

The step is configurable, and when finding the maximum frequency, the multiplication of the step by the number of samples is done. This must be multiplied by 10 (all frequencies are basically 10 times higher than what you input on the device), and added to the initial frequency int(freq) to get the maximum frequency.

xvfb-run is needed if you don't have access to an x-server, since I presently using some pylab routines in the source code, which is part of matplotlib.
