import sys
from Queue      import Queue, Empty
from subprocess import call
import binascii
import time
import signal
import scipy
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import heapq
from scipy import signal
import json
from requests import *
import datetime
import math
from time import sleep
import pygame as pg
from pyaudio import PyAudio
from constantesDataStream import *
from constantes_PunchinBall import *

def filter_data(data, fs_hz):
    '''
    filter from 2 to 50 Hz, helps remove 50Hz noise and replicates paper
    US : 60Hz, UE : 50Hz
    also helps remove the DC line noise (baseline drift)
    Wn = fc/(fs/2) is the cutoff frequency, frequency at which we lose 3dB.
    For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample. (Wn is thus in half-cycles / sample.)
    '''

    b, a = scipy.signal.butter(4, [0.5 / (fs_hz / 2.0), 44.0 / (fs_hz / 2.0)], btype='bandpass')
    # f_data = signal.lfilter(b, a, data, axis=0)
    f_data = scipy.signal.filtfilt(b ,a, data)
    # OTHER FILTERS

    # filter the data to remove DC
    # hp_cutoff_hz = 1.0
    # b1, a1 = signal.butter(2, hp_cutoff_hz / (fs_hz / 2.0), 'highpass')  # define the filter
    # ff_data = signal.lfilter(b1, a1, data, 0)  # apply along the zeroeth dimension

    # notch filter the data to remove 50 Hz and 100 Hz
    # notch_freq_hz = np.array([50.0])  # these are the center frequencies
    # for freq_hz in np.nditer(notch_freq_hz):  # loop over each center freq
    #     bp_stop_hz = freq_hz + 3.0 * np.array([-1, 1])  # set the stop band
    #     b, a = signal.butter(3, bp_stop_hz / (fs_hz / 2.0), 'bandstop')  # create the filter
    #     fff_data = signal.lfilter(b, a, f_data, 0)  # apply along the zeroeth dimension

    return f_data

def extract_freqbandmean(N, fe, signal, fmin, fmax):
    #f = np.linspace(0,fe/2,int(np.floor(N/2)))
    fftsig = abs(np.fft.fft(signal))
    # print fftsig.shape
    fftsig = fftsig[fmin:fmax]
    mean = np.mean(fftsig)
    return mean

def extract_freqbandmin(N, fe, signal, fmin, fmax):
    #f = np.linspace(0,fe/2,int(np.floor(N/2)))
    fftsig = abs(np.fft.fft(signal))
    # print fftsig.shape
    fftsig = fftsig[fmin:fmax]
    min = np.min(fftsig)
    return min

def extract_freqbandmax(N, fe, signal, fmin, fmax):
    #f = np.linspace(0,fe/2,int(np.floor(N/2)))
    fftsig = abs(np.fft.fft(signal))
    # print fftsig.shape
    fftsig = fftsig[fmin:fmax]
    max = np.amax(fftsig)
    return max

def neurofeedback_freq(array, freqMax, freqMin):
    last3 = np.average(array[-3:-1])
    max = np.amax(array)
    min = np.min(array)
    a = 1. * (freqMin - freqMax) / (max - min)
    b = freqMin - max  * a
    frequency = a * last3 + b
    return frequency

def neurofeedback_freq_arctan(array, freqMax, freqMin):
    spread_average = np.average(array[-5:-1])
    globalMean = np.average(array)
    frequency = (freqMax-freqMin)/math.pi*np.arctan(spread_average*1e9-globalMean)+freqMax-freqMin    # 1000/Pi * arctan(x-A) + 1000, gives frequency between 500 and 1500
    return frequency

def neurofeedback_volume(array, volMax, volMin):
    last = array[-1]
    max = np.amax(array)
    min = np.min(array)
    a = 1. * (volMin - volMax) / (max - min)
    b = volMin - max  * a
    volume = a * last + b
    return volume

def enqueue_output(out, queue):
    while True:
        lines = out.readline()
        out.flush()
        #if lines != '\n' :
            #queue.put(float(lines))
        queue.put(float(lines))
            #print queue

def sine_tone(freq, duration, bitrate):
    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = bitrate #number of frames per second/frameset.

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    FREQUENCY = freq #Hz, waves per second, 261.63=C4-note.
    LENGTH = duration #seconds to play sound

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''
    # print (type(FREQUENCY))

    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA += chr(int(math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128))
    #fill remainder of frameset with silence
    for x in xrange(RESTFRAMES):
        WAVEDATA += chr(128)

    p = PyAudio()
    stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=BITRATE,
        output=True,
        )
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()

def punch(level, levels_images, fond, punch): # function that change the image and increase the level

    level = level + 1
    level_img = pg.image.load(levels_images[level-1]).convert_alpha()
    scaled_level = pg.transform.scale(level_img, (100, 440))
    screen.blit(scaled_level, (700, 100))
    punch_noise.play()
    screen.blit(fond, (0, 0))
    screen.blit(punch, (200+2*x,-9))
    time.sleep(1)

def movePunchinBall(angle, screen, scoreBar, scoreDigit, fond, image):
    animUpLeft = []
    animUpRight = []
    allAnim = []
    for i in range(angle):
        animUpLeft.append(pg.transform.rotate(image, -i))

    for i in range(angle):
        animUpRight.append(pg.transform.rotate(image, i))

    allAnim.append(animUpLeft + list(reversed(animUpLeft)) + animUpRight + list(reversed(animUpRight)))
    # print allAnim
    for j in range(len(allAnim[0])):
        screen.blit(fond, (0, 0))
        # print allAnim[0][1]
        screen.blit(allAnim[0][j], (350, -5))
        # print 1
        # sleep(0.1)
        pg.display.update()

        # screen.blit(scoreBar, (317, 460))
        # screen.blit(scoreDigit, (800, 30))


#TODO function that returns the next position in flying game
# def newPosition ( ):

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


# def whichCase(posx, posy, serie):
#     if serie == 1:
#         if posx < 67 & posx > 37  :
#
#         if posy < 75 & posy > 58 :
#
#     if serie == 2:
#         if posx < & posx >  :
#
#         if posy < & posy > :
#     if serie == 2:
#         if posx < & posx >  :
#
#         if posy < & posy > :
#     if serie == 2:
#         if posx < & posx >  :
#
#         if posy < & posy > :
#     if serie == 2:
#         if posx < & posx >  :
#
#         if posy < & posy > :
#     if serie == 2:
#         if posx < & posx >  :
#
#         if posy < & posy > :
def whichButtonHome(mouse, w_display, h_display):
    button = 0

    if (int(mouse[0]) <= 1.*w_display / 4 + 30) & (int(mouse[0]) >= 1.* w_display / 4 - 30) & (int(mouse[1]) <= h_display - 50) & (int(mouse[1]) >= h_display - 100):
        button = 1

    elif (int(mouse[0]) <= 1.* w_display / 2 + 30) & (int(mouse[0]) >= 1.*w_display / 2 - 30) & (int(mouse[1]) <= h_display - 50) & (int(mouse[1]) >= h_display - 100):
        button = 2

    elif (int(mouse[0]) <= 3.*w_display / 4 + 30) & (int(mouse[0]) >= 3.*w_display / 4 - 30) & (int(mouse[1]) <= h_display - 50) & (int(mouse[1]) >= h_display - 100):
        button = 3
    # print button
    # return 1
    return button

def whichButtonReturn(mouse, w_display, h_display):
    button = 0
    if (int(mouse[0]) <= 1.* w_display / 6) & (int(mouse[1]) <= 50):
        button = 1
    return button

def mainNeuro(queue, buffer_1, OPB1_data, oldPosy ):
    cpt = 0
    try:
        while cpt < buffersize * nb_channels:
            buffer_1.append(queue.get_nowait())
            cpt += 1
            cpt2 = 0

        while cpt2 < 1:

            cpt2 += 1
            buffer_1_array = np.asarray(buffer_1)

            OPB1_data[0, :] = buffer_1_array[ind_channel_1]
            OPB1_data[1, :] = buffer_1_array[ind_channel_2]
            OPB1_data[2, :] = buffer_1_array[ind_channel_3]
            OPB1_data[3, :] = buffer_1_array[ind_channel_4]

            OPB1_fdata[0, :] = filter_data(OPB1_data[0, :], fs_hz)
            OPB1_fdata[1, :] = filter_data(OPB1_data[1, :], fs_hz)
            OPB1_fdata[2, :] = filter_data(OPB1_data[2, :], fs_hz)
            OPB1_fdata[3, :] = filter_data(OPB1_data[3, :], fs_hz)

            # OPB1_bandmean_delta = np.zeros(nb_channels)
            OPB1_bandmean_alpha = np.zeros(nb_channels)

            OPB1_bandmax_alpha = np.zeros(nb_channels)
            OPB1_bandmin_alpha = np.zeros(nb_channels)

            for channel in range(4):
                OPB1_bandmean_alpha[channel] = extract_freqbandmean(200, fs_hz, OPB1_fdata[channel, :], 6, 11)
                # OPB1_bandmean_delta[channel] = extract_freqbandmean(200, fs_hz, OPB1_data[channel,:], 1, 4)

            ''' Get the mean, min and max of the last result of all channels'''
            newMean_alpha = np.average(OPB1_bandmean_alpha)  # mean of the 4 channels, not the best metric I guess
            OPB1_mean_array_uv.append(newMean_alpha)
            maxAlpha = np.amax(OPB1_mean_array_uv)
            minAlpha = np.min(OPB1_mean_array_uv)

            if newMean_alpha == maxAlpha:
                newPosy = minDisplayY
            elif newMean_alpha == minAlpha:
                newPosy = maxDisplayY
            else:
                a = 1. * (maxDisplayY-minDisplayY) / (minAlpha - maxAlpha)
                b = maxDisplayY - minAlpha * a
                newPosy = a * newMean_alpha + b
            # screen.blit(fond, (0, 0))

            deltaPosy = 1.* (newPosy - oldPosy) / steps
            screen.blit(sky, (0, 0))
            print newPosy
            # screen.blit(plane, (, oldPosy + deltaPosy * steps))
            screen.blit(plane, (5. * w_display / 12, newPosy))
            # print oldPosy, newPosy
            # pg.time.delay(400)
            pg.display.flip()

            # print "new Mean of 4 channels", newMean_alpha, maxAlpha, minAlpha

            # scoreBar = pg.image.load(levels_images[level]).convert_alpha()
            # scoreBar = pg.transform.scale(scoreBar, (90, 400))
            # scoreBar = pg.transform.rotate(scoreBar, -90)
            oldPosy = newPosy
            cpt = 0
            buffer_1 = []

    except Empty:
        # print 'ERROR : outside main try '
        return