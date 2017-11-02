import sys
from subprocess import Popen, PIPE
from threading  import Thread
from Queue      import Queue, Empty
from subprocess import call
import binascii
import time
import signal
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import heapq
from scipy import signal
import json
from requests import *
import datetime
import pygame as pg # module that allows us to play music and change the volume regarding to alpha level
import math
from pyaudio import PyAudio
from functions import *

FreqRange = 'alpha'
if FreqRange == '':
    logging.warning('No frequency passed as argument')

if FreqRange == 'alpha':
    freqRange = np.array([6, 11])
elif FreqRange == 'gamma':
    freqRange = np.array([25, 50])
elif FreqRange == 'beta':
    freqRange = np.array([12, 25])
elif FreqRange == 'theta':
    freqRange = np.array([4, 7])
elif FreqRange == 'XXII_beta':
    freqRange = np.array([15, 23])
elif FreqRange == 'XXII_gamma':
    freqRange = np.array([38, 40])

'''constants for streaming loop'''
cpt = 0
cpt2 = 0
buffersize = 200 # a bit more than one second of data,
buffer_1 = []
nb_channels = 4
ind_2_remove_in_buffer1 = []
ind_channel_1 = []
ind_channel_2 = []
ind_channel_3 = []
ind_channel_4 = []
OPB1_mean_array_uv = np.array([])
OPB1_data = np.zeros((nb_channels, buffersize))

''' Save buffer, to keep data records somewhere'''
saved_buffer = []

'''launch node process'''
process = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE)
queue = Queue()
thread = Thread(target=enqueue_output, args=(process.stdout, queue))
thread.daemon = True # kill all on exit
thread.start()


'''for the fft '''
length = 200
NFFT = 200
fs_hz = 200
# overlap = NFFT/2 # useless for now

''' Song playing'''
pg.mixer.init()
pg.mixer.music.load('afterMarianneSpace.mp3')
pg.mixer.music.set_volume(1)
pg.mixer.music.play(0)
volume = 0.5

'''Neurofeedback loop'''
# newMean = 0 # useless now
# oldMean = 5E-13 # useless now
mean_array = []
min_array =[]
max_array = []

'''reorder channels index'''
# the following loop saves the index of the buffer that are interesting, without the channel id every 0 [nb_channels]
for ind in range(0, buffersize):
    # starts at index 0 which is the number of the sample
    ind_channel_1.append(ind*4)
    ind_channel_2.append(ind*4+1)
    ind_channel_3.append(ind*4+2)
    ind_channel_4.append(ind*4+3)

'''MAIN LOOP'''
while True:
    try:
        # the first while loop builds the buffer_1 for 1 second, then it's processed by 2nd loop
        while (cpt < buffersize*nb_channels)  :
            buffer_1.append(queue.get_nowait())
            cpt += 1
            cpt2 = 0

        while cpt2 <1 :

            cpt2 += 1
            buffer_1_array = np.asarray(buffer_1)

            OPB1_data[0, :] = buffer_1_array[ind_channel_1]
            OPB1_data[1, :] = buffer_1_array[ind_channel_2]
            OPB1_data[2, :] = buffer_1_array[ind_channel_3]
            OPB1_data[3, :] = buffer_1_array[ind_channel_4]

            f_ch1 = filter_data(OPB1_data[0, :], fs_hz)
            f_ch2 = filter_data(OPB1_data[1, :], fs_hz)
            f_ch3 = filter_data(OPB1_data[2, :], fs_hz)
            f_ch4 = filter_data(OPB1_data[3, :], fs_hz)

            OPB1_bandmean = np.zeros(nb_channels)
            OPB1_bandmax = np.zeros(nb_channels)
            OPB1_bandmin = np.zeros(nb_channels)

            for channel in range(4):
                OPB1_bandmean[channel] = extract_freqbandmean(200, fs_hz, OPB1_data[channel,:], freqRange[0], freqRange[1])
                OPB1_bandmin[channel] = extract_freqbandmin(200, fs_hz, OPB1_data[channel,:], freqRange[0], freqRange[1])
                OPB1_bandmax[channel] = extract_freqbandmax(200, fs_hz, OPB1_data[channel,:], freqRange[0], freqRange[1])

            print 'CHAN1', OPB1_bandmean[0] , 'CHAN2', OPB1_bandmean[1] , 'CHAN3', OPB1_bandmean[2] , 'CHAN4', OPB1_bandmean[3]

            ''' Get the mean, min and max of the last result of all channels'''
            newMean = np.average(OPB1_bandmean)
            newMin = np.average(OPB1_bandmin)
            newMax = np.average(OPB1_bandmax)

            ''' increment the mean, min and max arrays of the freqRange studied'''
            max_array.append(newMax)
            min_array.append(newMin)
            mean_array.append(newMean)

            # BIG_Max = np.amax(max_array ) # the BIG MEAN is the global mean of the session
            # BIG_Min = np.amin(min_array )
            # print BIG_Min
            # print BIG_Max
            # VOLUME = (newMean-min(oldMean,newMean))/(max(oldMean, newMean)-min(oldMean, newMean))
            # volume = (1/math.pi*np.arctan(spread_average-(BIG_Max-BIG_Min)/2)+0.5) # 1000/Pi * arctan(x-A) + 1000, gives frequency between 500 and 1500
            #
            # volume = spread_average / BIG_Max
            # volume = (1/math.pi*np.arctan(spread_average-(BIG_Max-BIG_Min)/2)+0.5)
            ''' Volume is MAX=1 when freqRange is MIN, and volume MIN=0.3 when freqRange is MAX'''

            volume = neurofeedback_volume(mean_array, volMax=1, volMin=0.3)

            if np.invert(math.isnan(volume)): #the issue is that the first frequencies are not defined, thus are NaN float. sine_tone works only with float
                pg.mixer.music.set_volume(volume)
                print "Volume set to ", volume

            # print type(frequency)
            # pg.mixer.music.stop()
            cpt = 0
            buffer_1 = []
            saved_buffer.append([buffer_1])

#    req = Request('https://blink-detector.herokuapp.com/eegs.json')
#    req.add_header('Content-Type', 'application/json')
#
#    response = urlopen(req, json.dumps(data))

    except Empty:
        continue # do stuff
    else:

        str(buffer_1)
        #sys.stdout.write(char)
