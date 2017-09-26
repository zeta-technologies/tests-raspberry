
import numpy as np
from subprocess import Popen, PIPE
from threading  import Thread
from subprocess import call
from constantes_PunchinBall import *

'''FREQ'''
FreqRange = 'alpha'
freqMaxAlpha = 11
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

bufferRS = []
bufferPB = []
bufferT = []

nb_channels = 4
ind_2_remove_in_buffer1 = []
ind_channel_1 = []
ind_channel_2 = []
ind_channel_3 = []
ind_channel_4 = []

ratios_ch1 = []
ratios_ch2 = []
ratios_ch3 = []
ratios_ch4 = []

mean_array_uvPB = []
mean_array_uvF = []
mean_array_uvRS = []

dataPB = np.zeros((nb_channels, buffersize))
fdataPB = np.zeros((nb_channels, buffersize))

dataF = np.zeros((nb_channels, buffersize))
fdataF = np.zeros((nb_channels, buffersize))

dataRS = np.zeros((nb_channels, buffersize, restingStateDuration)) # need to store every chunk to reprocess the ratio
fdataRS = np.zeros((nb_channels, buffersize, restingStateDuration))

''' Save buffer, to keep data records somewhere'''


saved_bufferPB = []
saved_bufferT = []
saved_bufferRS = []
saved_bufferRS_ch1 = []
saved_bufferRS_ch2 = []
saved_bufferRS_ch3 = []
saved_bufferRS_ch4 = []
saved_bufferT_ch1 = []
saved_bufferT_ch2 = []
saved_bufferT_ch3 = []
saved_bufferT_ch4 = []
saved_bufferPB_ch1 = []
saved_bufferPB_ch2 = []
saved_bufferPB_ch3 = []
saved_bufferPB_ch4 = []
sessionF = 0
sessionPB = 0
sessionRS = 0
'''for the fft '''
length = 200
NFFT = 200
fs_hz = 200
# overlap = NFFT/2 # useless for now

'''Neurofeedback loop'''
# newMean = 0 # useless now
# oldMean = 5E-13 # useless now
mean_array_alphaPB = []
mean_array_deltaPB = []
ratio_arrayPB = []

mean_array_alphaF = []
mean_array_deltaF = []
ratio_arrayF = []

mean_array_alphaRS = []
mean_array_deltaRS = []
ratio_arrayRS = []

'''reorder channels index'''
# the following loop saves the index of the buffer that are interesting, without the channel id every 0 [nb_channels]
for ind in range(0, buffersize):
    # starts at index 0 which is the number of the sample
    ind_channel_1.append(ind*4)
    ind_channel_2.append(ind*4+1)
    ind_channel_3.append(ind*4+2)
    ind_channel_4.append(ind*4+3)
