# coding=utf-8
"""Constantes of ZETA Games first App"""

import pygame as pg
import numpy as np
from subprocess import Popen, PIPE
from threading  import Thread
from subprocess import call

# Personnalisation de la fenêtre
titre_fenetre = "ZETA GAMES"
image_icone = "images/zeta.png"
w_display = 480
h_display = 270
pg.font.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
choice = ''
# Listes des images du jeu
'''constants for streaming loop'''
cpt = 0
cpt2 = 0
buffersize = 200 # a bit more than one second of data,

bufferRS1 = []
bufferRS2 = []
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

mean_array_uvT = []
mean_array_uvRS2 = []
mean_array_uvRS1 = []


'''Load images, sonds libraries'''
buttonText = pg.font.Font('fonts/couture-bld.otf', 15) # font for Menu button
progressionTextFont = pg.font.Font('fonts/couture-bld.otf', 5) # font for Menu button

buttonTextHuge = pg.font.Font('fonts/couture-bld.otf', 20) # font for Menu button
image_home = 'images/homev011.png'


scoreDigitImages = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']

'''training game'''
skyImage = 'images/beach.png' # which is a beach now
planeImage = 'images/bird.png' # which is a bird now
# skyImage = 'images/sky.png'
# planeImage = 'images/plane.jpg'
cloudImage = 'images/cloud.png'
oldPosy = 180 # initial position of the Bird
# steps = 10
minDisplayY = 15 # min and max position that the bird can reach, 10px is top of the screen
maxDisplayY = 220
maxScore = 15 # score ruler is 15 max
minScore = 1
scoreT = 0
steps = 1.*buffersize/40
newPosy = maxDisplayY
veryOldPosy = maxDisplayY
oldPosy = maxDisplayY
deltaPosy_1 = 1. * (newPosy - oldPosy) / steps
deltaPosy_2 = 1. * (oldPosy - veryOldPosy) / steps
scorF = 1
maxRatioAlphaOverDelta = 1
minRatioAlphaOverDelta = 0
coef_mad = 3
veryOldPosy = maxDisplayY

'''Resting state'''
timer = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
restingState = 'images/restingState.png'
restingStateDuration = 180 # in seconds
sec = 0
secRS2 = 0
secRS1 = 0
durationSessionInit =  180
durationSession = durationSessionInit
restingState1isDone = 0
endSessionImg = 'images/endSession.png'

'''Progression '''
progressionCoeff = 100 #coefficient that higher the progression metric since it's a low coeff ~ 0.001
displayedMetric = 0

'''Navigation among the pages'''
# booleans for each window
punchinBall = 0
homeOn = 1
training = 0
restingState1 = 0
restingState2 = 0
questionnaire = 0

'''Tinnitus Questionnary '''
# useless for now
questionsSerie1 = 'images/questionsSerie1.png'
answers = []
questions = ['Pour quel pourcentage de votre temps éveillé \n étiez-vous conscient de vos acouphènes?','Sur une echelle de 0-10, quelle force avaient vos acouphènes ?','Vos acouphènes vous ont géné quel % de votre temps ?','À quel degré avez-vous eu le sentiment que vous pouviez contrôler vos acouphènes?','quelle facilité avez-vous eue à gérer vos acouphènes?','À quel point était-ce facile pour vous d’ignorer vos acouphènes?']



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


''' Save buffer, to keep data records somewhere'''

saved_bufferPB = []
saved_bufferT = []
saved_bufferRS1 = []
saved_bufferRS2 = []
saved_bufferRS1_ch1 = []
saved_bufferRS1_ch2 = []
saved_bufferRS1_ch3 = []
saved_bufferRS1_ch4 = []
saved_bufferRS2_ch1 = []
saved_bufferRS2_ch2 = []
saved_bufferRS2_ch3 = []
saved_bufferRS2_ch4 = []

saved_bufferT_ch1 = []
saved_bufferT_ch2 = []
saved_bufferT_ch3 = []
saved_bufferT_ch4 = []
sessionT = 0
sessionRS1 = 0
sessionRS2 = 0
sessionEnded = 0
'''for the fft '''
length = 200
NFFT = 200
fs_hz = 200
# overlap = NFFT/2 # useless for now

'''Neurofeedback loop'''
# newMean = 0 # useless now
# oldMean = 5E-13 # useless now

mean_array_alphaF = []
mean_array_deltaF = []
ratio_arrayF = []

mean_array_alphaRS1 = []
mean_array_deltaRS1 = []
ratio_arrayRS1 = []

mean_array_alphaRS2 = []
mean_array_deltaRS2 = []
ratio_arrayRS2 = []

'''Band means for Training loop'''
bandmean_alphaT = np.zeros(nb_channels)
bandmax_alphaT = np.zeros(nb_channels)
bandmin_alphaT = np.zeros(nb_channels)

bandmean_deltaT = np.zeros(nb_channels)
bandmax_deltaT = np.zeros(nb_channels)
bandmin_deltaT = np.zeros(nb_channels)
ratioT = np.zeros(nb_channels)
'''reorder channels index'''
# the following loop saves the index of the buffer that are interesting, without the channel id every 0 [nb_lines_jsnels]
for ind in range(0, buffersize):
    ind_channel_1.append(ind*4)
    ind_channel_2.append(ind*4+1)
    ind_channel_3.append(ind*4+2)
    ind_channel_4.append(ind*4+3)
