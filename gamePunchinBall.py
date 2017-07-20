#!/Users/jonathanschmutz/anaconda/bin/python
import pygame as pg
from pygame.locals import *
from constantes_PunchinBall import *
from constantesDataStream import *
import os
import sys
from subprocess import Popen, PIPE
from threading  import Thread
from sys import platform
from tempfile import TemporaryFile
outfile = 'save.txt'
# from Queue import Queue, Empty
# from subprocess import call
# import binascii
# import time
# import signal
# import numpy as np
# import pandas as pd
# import scipy as sp
# import heapq
# from scipy.interpolate import UnivariateSpline
# from scipy.interpolate import interp1d
# from scipy import signal
# import json
from requests import *
import datetime
# import math
# import time
# from pyaudio import PyAudio
from functions import *
from gamePunchinBall import *

'''background'''
screen = pg.display.set_mode((w_display, h_display), RESIZABLE)
fond = pg.image.load(image_ring).convert()
fond = pg.transform.scale( fond, (w_display, h_display))

'''Punching ball'''
punchBall = pg.image.load(punchBallImage)
punchBall = pg.transform.scale(punchBall, (250*w_display/1024, 450*h_display/576))

'''Score Bar'''
scoreBar = pg.image.load(levels_images[level]).convert_alpha()
scoreBar = pg.transform.scale(scoreBar, (90/1024*w_display, 400*h_display/576))
scoreBar = pg.transform.rotate(scoreBar, -90)
# test =pg.transform.scale(scoreBar, (90, 400))

'''Winner image'''
winImg = pg.image.load(winImg).convert_alpha()
winImg = pg.transform.scale(winImg, (700*w_display/1024, 440*h_display/576))
# punchBall = punch.set_colorkey((255,255,255))

'''Score digit '''
scoreTxt = pg.image.load(image_score)
scoreTxt = pg.transform.scale(scoreTxt, (150*w_display/1024, 50*h_display/576))
scoreDigit = pg.image.load(scoreDigitImages[0])
scoreDigit = pg.transform.scale(scoreDigit, (70*w_display/1024, 90*h_display/576))

'''Fly game'''
sky = pg.image.load(skyImage).convert()
sky = pg.transform.scale(sky, (1024*w_display/1024, 576*h_display/576))
# cloud = pg.image.load(cloudImage).convert()
# cloud = pg.image.transform(cloud, ())
plane = pg.image.load(planeImage).convert_alpha()
plane = pg.transform.scale(plane, (50, 50))
# plane = plane.set_colorkey((255, 255, 255))

'''Resting state'''
timerImage = pg.image.load(timer[0])
timerImage = pg.transform.scale(timerImage, (70*w_display/1024, 90*h_display/576))
restingImage = pg.image.load('images/restingState.png').convert()
restingStateImage = pg.transform.scale(restingImage, (w_display, h_display))

# '''Tinnitus questionnaire '''
# questionsSerie1Image = pg.image.load(questionsSerie1)
# questionsSerie1Image = pg.transform.scale(questionsSerie1Image, (w_display, h_display))

'''MAIN LOOP'''
gameOn = 1
now = datetime.datetime.now()
os.mkdir('data-'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second))
path = str('data-'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)+'/')

print '\n \n \n You are running Zeta Game on ', platform
print ' \n \n                     -----------------------------'
print '                     ------ Z E T A    A C S -----'
print '                     -----------------------------'

print '\n\n                     -------------------------------------------------------------'
print '                     -----  ________    ________   _________        .         -----'
print '                     -----         /   |               |           / \        -----'
print '                     -----        /    |               |          /   \       -----'
print '                     -----       /     |               |         /     \      -----'
print '                     -----      /      |____           |        /       \     -----'
print '                     -----     /       |               |       /_________\    -----'
print '                     -----    /        |               |      /           \   -----'
print '                     -----   /         |               |     /             \  -----'
print '                     -----  /_______   |_______        |    /               \ -----'
print '                     --------------------------------------------------------------'

print ' \n  Data will be saved here : ', path
while gameOn:

    #LOAD screen Image
    home = pg.image.load(image_home).convert() #TODO add image_home
    home = pg.transform.scale(home, (1024*w_display/1024, 576*h_display/576))
    screen.blit(home, (0,0))

    # load home menu buttons
    settings = 'Etalonnage'
    settingsSurf, settingsRect = text_objects(settings, buttonText)
    settingsRect.center = (1.*w_display/4, 3.3*h_display/4)

    gameA = 'Jeu A'
    gameASurf, gameARect = text_objects(gameA, buttonText)
    gameARect.center = (1.*w_display/2, 3.3*h_display/4)
    gameB = 'Jeu B'
    gameBSurf, gameBRect = text_objects(gameB, buttonText)
    gameBRect.center = (3.*w_display/4, 3.3*h_display/4)

    screen.blit(gameASurf, gameARect)
    screen.blit(gameBSurf, gameBRect)
    screen.blit(settingsSurf, settingsRect)
    pg.display.flip()


    # Home window loop
    while homeOn:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseHome = pg.mouse.get_pos()
                choice = whichButtonHome(mouseHome, w_display, h_display)
                if choice == 1: # 1 is for resting state
                    homeOn = 0
                    punchinBall = 0
                    fly = 0
                    restingState = 1
                    questionnaire = 0
                elif choice == 2: #  is for flying game
                    homeOn = 0
                    punchinBall = 0
                    fly = 1
                    questionnaire = 0
                    restingState = 0
                elif choice == 3: # 3 is for punchinBall
                    homeOn = 0
                    punchinBall = 1
                    fly = 0
                    restingState = 0
                    questionnaire = 0

    if punchinBall :
        sessionPB += 1

        '''launch node process'''
        if platform == 'darwin': # mac
            processPB = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
        elif platform == 'linux' or platform == 'linux2': #linux
            processPB = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for LINUX

        queuePB = Queue()
        threadPB = Thread(target=enqueue_output, args=(processPB.stdout, queuePB))
        threadPB.daemon = True
        threadPB.start()
        bufferPB = []

        '''Position everything on the screen'''
        screen.blit(scoreTxt, (670, 30))
        screen.blit(fond, (0, 0))
        screen.blit(punchBall, (350*w_display/1024, -5*h_display/576))
        screen.blit(scoreBar, (317*w_display/1024, 460*h_display/576))
        screen.blit(scoreDigit, (800*w_display/1024, 30*h_display/576))
        pg.display.flip()
        # punch_noise = pg.mixer.Sound("songs/punch.ogg") # TODO resolve the MemoryError due to pg.mixer.Sound

    if fly:
        '''launch node process'''
        if platform == 'darwin': # mac
            processF = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
        elif platform == 'linux' or platform == 'linux2': #linux
            processF = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for LINUX

        queueF = Queue()
        threadF = Thread(target=enqueue_output, args=(processF.stdout, queueF))
        threadF.daemon = True # kill all on exit
        threadF.start()
        # Chargement du fond
        bufferF = []
        sessionF += 1
        '''Position everything on the screen'''
        screen.blit(sky, (0, 0))
        # screen.blit(cloud, (800*w_display/1024, 100*h_display/576))
        # screen.blit(plane, (300*w_display/1024, 200*h_display/576))
        screen.blit(plane, ( 5.* w_display / 12, 1. * h_display / 5))
        # screen.blit(scoreBar, (317, 460))
        # screen.blit(scoreDigit, (800, 30))
        # screen.blit(test, (317, 460))
        pg.display.flip()

    if restingState:
        sessionRS += 1
        if platform == 'darwin': # mac
            processRS = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
        elif platform == 'linux' or platform == 'linux2': #linux
            processRS = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for LINUX

        '''launch node process'''
        queueRS = Queue()
        threadRS = Thread(target=enqueue_output, args=(processRS.stdout, queueRS))
        threadRS.daemon = True
        threadRS.start()

        bufferRS = []
        band_alphaRS_ch1 = []
        band_alphaRS_ch2 = []
        band_alphaRS_ch3 = []
        band_alphaRS_ch4 = []

        band_deltaRS_ch1 = []
        band_deltaRS_ch2 = []
        band_deltaRS_ch3 = []
        band_deltaRS_ch4 = []

        screen.blit(restingStateImage, (0,0))
        displayNumber(0, screen, 'down')
        pg.display.flip()

    if questionnaire:

        screen.blit(questionsSerie1Image, (0,0))
        pg.display.flip()
        # questionText = pg.font.Font('freesansbold.ttf',15)
        smallText = pg.font.Font("freesansbold.ttf",15)
        question = questions[0]
        textQSurf, textQRect = text_objects(question, smallText)
        textQRect.center = (1.*w_display/2, 29)
        screen.blit(textQSurf, textQRect)


        for nb in range(11):


            # TextSurf, TextRect = text_objects("question serie 1", questionText)
            # TextRect.center = ((display_width/2),(display_height/2))
            # gameDisplay.blit(TextSurf, TextRect)

            # pg.draw.rect(screen, (218, 227, 243), (1.*w_display/12*(nb+1),58,1.*w_display/12*(nb+2),75))
            pg.draw.rect(screen, (255, 255, 255), (1.*w_display/13*(nb+1),58,1.*w_display/13,20))
            text =  "{}%".format(nb)
            textSurf, textRect = text_objects(text, smallText)
            textRect.center = ( 1. * w_display/13*(nb+1) + 1.*w_display/13/2, 58 + 10 )
            screen.blit(textSurf, textRect)

        pg.display.update()

        # sec = sec + 1
        # print sec

    while punchinBall:

        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(path, sessionPB, 'PB', saved_bufferPB_ch1, saved_bufferPB_ch2, saved_bufferPB_ch3, saved_bufferPB_ch4)
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    saveAllChannelsData(path, sessionPB, 'PB', saved_bufferPB_ch1, saved_bufferPB_ch2, saved_bufferPB_ch3, saved_bufferPB_ch4)
                    punchinBall = 0
                    saved_bufferPB_ch1 = []
                    saved_bufferPB_ch2 = []
                    saved_bufferPB_ch3 = []
                    saved_bufferPB_ch4 = []

            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0
                    processPB.terminate() # terminates the node process to close connection with openBCI
                    np.save(outfilePBCH2)
                    bufferPB = []
                    cpt = 0
                    queuePB.queue.clear()
                    saveAllChannelsData(path, sessionPB, 'PB', saved_bufferPB_ch1, saved_bufferPB_ch2, saved_bufferPB_ch3, saved_bufferPB_ch4)

                    saved_bufferPB_ch1 = []
                    saved_bufferPB_ch2 = []
                    saved_bufferPB_ch3 = []
                    saved_bufferPB_ch4 = []


        try:
            while cpt < buffersize * nb_channels :
                bufferPB.append(queuePB.get_nowait())
                saved_bufferPB.append(queuePB.get_nowait())
                cpt += 1

            bufferPB_array = np.asarray(bufferPB)

            dataPB[0, :] = bufferPB_array[ind_channel_1]
            dataPB[1, :] = bufferPB_array[ind_channel_2]
            dataPB[2, :] = bufferPB_array[ind_channel_3]
            dataPB[3, :] = bufferPB_array[ind_channel_4]

            saved_bufferPB_ch1.append(dataPB[0, :])
            saved_bufferPB_ch2.append(dataPB[1, :])
            saved_bufferPB_ch3.append(dataPB[2, :])
            saved_bufferPB_ch4.append(dataPB[3, :])

            fdataPB[0, :] = filter_data(dataPB[0, :], fs_hz)
            fdataPB[1, :] = filter_data(dataPB[1, :], fs_hz)
            fdataPB[2, :] = filter_data(dataPB[2, :], fs_hz)
            fdataPB[3, :] = filter_data(dataPB[3, :], fs_hz)

            bandmean_alphaPB = np.zeros(nb_channels)
            bandmax_alphaPB = np.zeros(nb_channels)
            bandmin_alphaPB = np.zeros(nb_channels)

            bandmean_deltaPB = np.zeros(nb_channels)
            bandmax_deltaPB = np.zeros(nb_channels)
            bandmin_deltaPB = np.zeros(nb_channels)

            for channel in range(4):
                bandmean_alphaPB[channel] = extract_freqbandmean(200, fs_hz, fdataPB[channel,:], freqMaxAlpha-2, freqMaxAlpha+2)
                bandmean_deltaPB[channel] = extract_freqbandmean(200, fs_hz, fdataPB[channel,:], 3, 4)

            ''' Get the mean, min and max of the last result of all channels'''
            newMean_alphaPB = np.average(bandmean_alphaPB) #mean of the 4 channels, not the best metric I guess
            newMean_deltaPB = np.average(bandmean_deltaPB)

            ''' increment the mean, min and max arrays of the freqRange studied'''
            mean_array_uvPB.append(newMean_alphaPB)

            if len(mean_array_uvPB) != 0:
                deltaPB = np.amax(mean_array_uvPB) - np.min(mean_array_uvPB)
            if len(mean_array_uvPB) == 0:
                deltaPB = 0
            # print "new Mean of 4 channels", newMean_alphaPB
            # print "Max - Min ", deltaPB

            if deltaPB == 0:
                level = 0

            if deltaPB !=0:
                level = int(math.floor(7*(newMean_alphaPB-np.min(mean_array_uvPB))/deltaPB))

            if level == 7:
                scorePB = scorePB + 1
                # punch_noise.play()
                scoreDigit = pg.image.load(scoreDigitImages[scorePB]).convert()
                scoreDigit = pg.transform.scale(scoreDigit, (70*w_display/1024, 90*h_display/576))
                screen.blit(fond, (0, 0))
                screen.blit(scoreDigit, (800*w_display/1024, 30*h_display/576))
                screen.blit(winImg, (100*w_display/1024, 100*h_display/576))

            if level != 7:
                scoreBar = pg.image.load(levels_images[level]).convert_alpha()
                scoreBar = pg.transform.scale(scoreBar, (90*w_display/1024, 400*h_display/576))
                scoreBar = pg.transform.rotate(scoreBar, -90)
                screen.blit(fond, (0, 0))
                screen.blit(punchBall, (350*w_display/1024,-5*h_display/576))
                screen.blit(scoreBar, (317*w_display/1024, 460*h_display/576))
                screen.blit(scoreDigit, (800*w_display/1024, 30*h_display/576))

            print "level", level
            pg.display.update()
            cpt = 0
            bufferPB = []

        except Empty:
            continue # do stuff
        else:
            str(bufferPB)
            #sys.stdout.write(char)

    while fly:

        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(path, sessionF, 'F', saved_bufferF_ch1, saved_bufferF_ch2, saved_bufferF_ch3, saved_bufferF_ch4)
                bufferF = []
                saved_bufferF_ch1 = []
                saved_bufferF_ch2 = []
                saved_bufferF_ch3 = []
                saved_bufferF_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    saveAllChannelsData(path, sessionF, 'F', saved_bufferF_ch1, saved_bufferF_ch2, saved_bufferF_ch3, saved_bufferF_ch4)
                    bufferF = []
                    saved_bufferF_ch1 = []
                    saved_bufferF_ch2 = []
                    saved_bufferF_ch3 = []
                    saved_bufferF_ch4 = []
                    fly = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0
                    processF.terminate()
                    queueF.queue.clear()
                    saveAllChannelsData(path, sessionF, 'F', saved_bufferF_ch1, saved_bufferF_ch2, saved_bufferF_ch3, saved_bufferF_ch4)
                    bufferF = []
                    saved_bufferF_ch1 = []
                    saved_bufferF_ch2 = []
                    saved_bufferF_ch3 = []
                    saved_bufferF_ch4 = []
                    cpt = 0
        try:
            while cpt < buffersize * nb_channels:
                bufferF.append(queueF.get_nowait())
                cpt += 1

            bufferF_array = np.asarray(bufferF)

            dataF[0, :] = bufferF_array[ind_channel_1]
            dataF[1, :] = bufferF_array[ind_channel_2]
            dataF[2, :] = bufferF_array[ind_channel_3]
            dataF[3, :] = bufferF_array[ind_channel_4]
            saved_bufferF_ch1.append(dataF[0, :])
            saved_bufferF_ch2.append(dataF[1, :])
            saved_bufferF_ch3.append(dataF[2, :])
            saved_bufferF_ch4.append(dataF[3, :])

            fdataF[0, :] = filter_data(dataF[0, :], fs_hz)
            fdataF[1, :] = filter_data(dataF[1, :], fs_hz)
            fdataF[2, :] = filter_data(dataF[2, :], fs_hz)
            fdataF[3, :] = filter_data(dataF[3, :], fs_hz)

            bandmean_alphaF = np.zeros(nb_channels)
            bandmax_alphaF = np.zeros(nb_channels)
            bandmin_alphaF = np.zeros(nb_channels)

            bandmean_deltaF = np.zeros(nb_channels)
            bandmax_deltaF = np.zeros(nb_channels)
            bandmin_deltaF = np.zeros(nb_channels)

            for channel in range(4):
                bandmean_alphaF[channel] = extract_freqbandmean(200, fs_hz, fdataF[channel,:], freqMaxAlpha-2, freqMaxAlpha+2)
                bandmean_deltaF[channel] = extract_freqbandmean(200, fs_hz, fdataF[channel,:], 3, 4)

            ''' Get the mean, min and max of the last reslt of all channels'''
            newMean_alphaF = np.average(bandmean_alphaF)  # mean of the 4 channels, not the best metric I guess
            mean_array_uvF.append(newMean_alphaF)
            maxAlphaF = np.amax(mean_array_uvF)
            minAlphaF = np.min(mean_array_uvF)

            if newMean_alphaF == maxAlphaF:
                newPosy = minDisplayY

            elif newMean_alphaF == minAlphaF:
                newPosy = maxDisplayY

            else:
                a = (maxDisplayY - minDisplayY) * 1. / (minAlphaF - maxAlphaF)
                b = maxDisplayY - minAlphaF * a
                newPosy = a * newMean_alphaF + b

            scoreF = scoreF + flyScore(newPosy)

            deltaPosy = 1. * (newPosy - oldPosy) / steps
            screen.blit(sky, (0, 0))
            # print newPosy
            # screen.blit(plane, (, oldPosy + deltaPosy * steps))
            screen.blit(plane, (5. * w_display / 12, newPosy))
            displayNumber(math.floor(scoreF), screen, 'down')
            # screen.blit(scoreImg, ())
            # print oldPosy, newPosy
            # pg.time.delay(400)

            pg.display.flip()

            # print "new Mean of 4 channels", newMean_alpha, maxAlpha, minAlpha

            # scoreBar = pg.image.load(levels_images[level]).convert_alpha()
            # scoreBar = pg.transform.scale(scoreBar, (90, 400))
            # scoreBar = pg.transform.rotate(scoreBar, -90)

        except Empty:
            continue  # do stuff
        else:
            str(bufferF)
            # sys.stdout.write(char)

        pg.display.update()
        oldPosy = newPosy
        cpt = 0
        saved_bufferF.append(bufferF)
        bufferF = []

    while restingState:
        # pg.time.Clock().tick(30)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(path, sessionRS, 'RS', saved_bufferRS_ch1, saved_bufferRS_ch2, saved_bufferRS_ch3, saved_bufferRS_ch4)
                saved_bufferRS_ch1 = []
                saved_bufferRS_ch2 = []
                saved_bufferRS_ch3 = []
                saved_bufferRS_ch4 = []

                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    saveAllChannelsData(path, sessionRS, 'RS', saved_bufferRS_ch1, saved_bufferRS_ch2, saved_bufferRS_ch3, saved_bufferRS_ch4)
                    saved_bufferRS_ch1 = []
                    saved_bufferRS_ch2 = []
                    saved_bufferRS_ch3 = []
                    saved_bufferRS_ch4 = []
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0
                    # print band_alphaRS_ch1
                    processRS.terminate()
                    queueRS.queue.clear()
                    bufferRS = []

        if sec == restingStateDuration :
            # np.zeros(nb_freq_alpha)
            band_alphaRS_ch1 = np.asarray(band_alphaRS_ch1)
            band_alphaRS_ch2 = np.asarray(band_alphaRS_ch2)
            band_alphaRS_ch3 = np.asarray(band_alphaRS_ch3)
            band_alphaRS_ch4 = np.asarray(band_alphaRS_ch4)
            # print 'band_alphaRS_ch1', band_alphaRS_ch1
            # print 'band_alphaRS_ch1[:, 0]', np.average(band_alphaRS_ch1[:,0])
            freqMaxAlphaCh1 = getfreqmax(band_alphaRS_ch1, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh2 = getfreqmax(band_alphaRS_ch2, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh3 = getfreqmax(band_alphaRS_ch3, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh4 = getfreqmax(band_alphaRS_ch4, 'alpha', nb_freq_alpha)
            freqMaxAlpha = int(np.average([freqMaxAlphaCh1, freqMaxAlphaCh2, freqMaxAlphaCh3, freqMaxAlphaCh4]))

            saveAllChannelsData(path, sessionRS, 'RS', saved_bufferRS_ch1, saved_bufferRS_ch2, saved_bufferRS_ch3, saved_bufferRS_ch4)
            saved_bufferRS_ch1 = []
            saved_bufferRS_ch2 = []
            saved_bufferRS_ch3 = []
            saved_bufferRS_ch4 = []


            print 'fin de la seance de reglage', freqMaxAlpha
            processRS.terminate()
            queueRS.queue.clear()
            bufferRS = []
            restingState = 0
            homeOn = 1

        elif sec < restingStateDuration:

            try:
                while cpt < buffersize * nb_channels:
                    bufferRS.append(queueRS.get_nowait())
                    cpt += 1

                bufferRS_array = np.asarray(bufferRS)

                dataRS[0, :] = bufferRS_array[ind_channel_1]
                dataRS[1, :] = bufferRS_array[ind_channel_2]
                dataRS[2, :] = bufferRS_array[ind_channel_3]
                dataRS[3, :] = bufferRS_array[ind_channel_4]
                saved_bufferRS_ch1.append(dataRS[0, :])
                saved_bufferRS_ch2.append(dataRS[1, :])
                saved_bufferRS_ch3.append(dataRS[2, :])
                saved_bufferRS_ch4.append(dataRS[3, :])

                fdataRS[0, :] = filter_data(dataRS[0, :], fs_hz)
                fdataRS[1, :] = filter_data(dataRS[1, :], fs_hz)
                fdataRS[2, :] = filter_data(dataRS[2, :], fs_hz)
                fdataRS[3, :] = filter_data(dataRS[3, :], fs_hz)

                band_alphaRS_ch1.append(extract_freqband(200, fs_hz, fdataRS[0,:], 6, 13)[0])
                band_alphaRS_ch2.append(extract_freqband(200, fs_hz, fdataRS[1,:], 6, 13)[0])
                band_alphaRS_ch3.append(extract_freqband(200, fs_hz, fdataRS[2,:], 6, 13)[0])
                band_alphaRS_ch4.append(extract_freqband(200, fs_hz, fdataRS[3,:], 6, 13)[0])
                nb_freq_alpha = extract_freqband(200, fs_hz, fdataRS[0,:], 6, 13)[1]

                band_deltaRS_ch1.append(extract_freqband(200, fs_hz, fdataRS[0,:], 3, 4)[0])
                band_deltaRS_ch2.append(extract_freqband(200, fs_hz, fdataRS[1,:], 3, 4)[0])
                band_deltaRS_ch3.append(extract_freqband(200, fs_hz, fdataRS[2,:], 3, 4)[0])
                band_deltaRS_ch4.append(extract_freqband(200, fs_hz, fdataRS[3,:], 3, 4)[0])
                nb_freq_delta = extract_freqband(200, fs_hz, fdataRS[3,:], 3, 4)[1]

                # for channel in range(4):
                #     band_alphaRS[channel] = extract_freqband(200, fs_hz, fdataRS[channel,:], 6, 11)
                #     bandmean_deltaRS[channel] = extract_freqband(200, fs_hz, fdataRS[channel,:], 3, 4)
                # globalAlpha.append(bandmean_alphaRS)

                cpt = 0
                bufferRS = []
                displayNumber(sec, screen, 'down')
                # checkImp() # TODO  check impedances function
                pg.display.update()
                sec = sec + 1

            except Empty:
                continue  # do stuff
            else:
                str(bufferRS)
                # sys.stdout.write(char)
            # time.sleep(1)
            # pg.time.delay(993) # wait to display the next second on screen
            # print sec

    while questionnaire:
        # pg.time.Clock().tick(30)
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState = 0
            if event.type == MOUSEBUTTONUP:
                # print int(mouse[1])
                if (int(mouse[1]) >= 58) & (int(mouse[1]) <= 80 ) :
                    answers.append('question 1 in %')
                    answers.append(math.floor(1.*mouse[0]/(w_display/13)))
                    print answers

                if (int(mouse[1]) >= 58) & (int(mouse[1]) <= 80 ) :
                    answers.append('question 2 in %')
                    answers.append(math.floor(1.*mouse[0]/(w_display/13)))
                    print answers

                if (int(mouse[1]) >= 58) & (int(mouse[1]) <= 80 ) :
                    answers.append('question 3 in %')
                    answers.append(math.floor(1.*mouse[0]/(w_display/13)))
                    print answers

        pg.display.update()
