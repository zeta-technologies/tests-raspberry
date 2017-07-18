# coding=utf-8
import pygame as pg
from pygame.locals import *
from constantes_PunchinBall import *
from constantesDataStream import *
import sys
from subprocess import Popen, PIPE
from threading  import Thread
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
# import datetime
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

'''launch node process'''
process = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE)
# process = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE)
queue = Queue()
thread = Thread(target=enqueue_output, args=(process.stdout, queue))
thread.daemon = True # kill all on exit
thread.start()
#try:
#    pipe = subprocess.Popen('sudo node openBCIDataStream.js', stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
#except Exception as e:
#     logging.error(str(e))
#queue = Queue()
#thread = Thread(target=enqueue_output, args=(pipe.stdout, queue))
#thread.daemon = True # kill all on exit
#thread.start()

'''REsting state'''
timerImage = pg.image.load(timer[0])
timerImage = pg.transform.scale(timerImage, (70*w_display/1024, 90*h_display/576))
# restingStateImage = pg.image.load(restingState)
# restingStateImage = pg.transform.scale(restingStateImage, (w_display, h_display))

'''Tinnitus questionnaire '''
questionsSerie1Image = pg.image.load(questionsSerie1)
questionsSerie1Image = pg.transform.scale(questionsSerie1Image, (w_display, h_display))

'''MAIN LOOP'''
continuer = 1
while continuer:

    #LOAD screen Image
    home = pg.image.load(image_home).convert() #TODO add image_home
    home = pg.transform.scale(home, (1024*w_display/1024, 576*h_display/576))
    screen.blit(home, (0,0))
    # load home menu buttons
    gameA = 'Jeu A'
    gameASurf, gameARect = text_objects(gameA, buttonText)
    gameARect.center = (1.*w_display/4, 3.3*h_display/4)
    gameB = 'Jeu B'
    gameBSurf, gameBRect = text_objects(gameB, buttonText)
    gameBRect.center = (1.*w_display/2, 3.3*h_display/4)
    settings = 'Reglages'
    settingsSurf, settingsRect = text_objects(settings, buttonText)
    settingsRect.center = (1.*w_display/4*3, 3.3*h_display/4)

    screen.blit(gameASurf, gameARect)
    screen.blit(gameBSurf, gameBRect)
    screen.blit(settingsSurf, settingsRect)
    pg.display.flip()

    # booleans for each window
    punchinBall = 0
    homeOn = 1
    fly = 0
    restingState = 0
    questionnaire = 0

    # Home window loop
    while homeOn:
        pg.time.Clock().tick(30)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseHome = pg.mouse.get_pos()
                choice = whichButtonHome(mouseHome, w_display, h_display)
                if choice == 1: # 1 is for punchinBall game
                    homeOn = 0
                    punchinBall = 1
                    fly = 0
                    restingState = 0
                    questionnaire = 0
                elif choice == 2: #  is for flying game
                    homeOn = 0
                    punchinBall = 0
                    fly = 1
                    questionnaire = 0
                    restingState = 0
                elif choice == 3: # 3 is for resting state
                    homeOn = 0
                    punchinBall = 0
                    fly = 0
                    restingState = 1
                    questionnaire = 0

                # elif :
                #     homeOn = 0
                #     punchinBall = 0
                #     fly = 0
                #     restingState = 0
                #     questionnaire = 1

    if punchinBall :
        # Chargement du fond

        '''Position everything on the screen'''
        screen.blit(scoreTxt, (670, 30))
        screen.blit(fond, (0, 0))
        screen.blit(punchBall, (350*w_display/1024, -5*h_display/576))
        screen.blit(scoreBar, (317*w_display/1024, 460*h_display/576))
        screen.blit(scoreDigit, (800*w_display/1024, 30*h_display/576))
        # screen.blit(test, (317, 460))
        pg.display.flip()
        # punch_noise = pg.mixer.Sound("songs/punch.ogg") # TODO resolve the MemoryError due to pg.mixer.Sound


        # Génération d'un niveau à partir d'un fichier
        # game = Game(gameChoice) # TODO create Game class
        # game.generer()
        # game.afficher(screen)
        #
        # # Création de  Kong
        # gauge = Level("images/dk_droite.png", "images/dk_gauche.png",
        #            "images/dk_haut.png", "images/dk_bas.png", niveau) # TODO create Level class

    if fly:
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
        # timerImage = pg.image.load(timer[]).convert()
        screen.blit(restingStateImage, (0,0))
        screen.blit(timerImage, (0,0))
        pg.display.flip()
        # sec = sec + 1
        # print sec

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

        pg.time.Clock().tick(30)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    punchinBall = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0
        try:
            while cpt < buffersize * nb_channels :
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

                OPB1_fdata[0, :] = filter_data(OPB1_data[0, :], fs_hz)
                OPB1_fdata[1, :] = filter_data(OPB1_data[1, :], fs_hz)
                OPB1_fdata[2, :] = filter_data(OPB1_data[2, :], fs_hz)
                OPB1_fdata[3, :] = filter_data(OPB1_data[3, :], fs_hz)

                # OPB1_bandmean_delta = np.zeros(nb_channels)
                OPB1_bandmean_alpha = np.zeros(nb_channels)

                OPB1_bandmax_alpha = np.zeros(nb_channels)
                OPB1_bandmin_alpha = np.zeros(nb_channels)

                for channel in range(4):
                    OPB1_bandmean_alpha[channel] = extract_freqbandmean(200, fs_hz, OPB1_fdata[channel,:], 6, 11)
                    # OPB1_bandmean_delta[channel] = extract_freqbandmean(200, fs_hz, OPB1_data[channel,:], 1, 4)

                ''' Get the mean, min and max of the last result of all channels'''
                newMean_alpha = np.average(OPB1_bandmean_alpha) #mean of the 4 channels, not the best metric I guess
                # newMean_delta = np.average(OPB1_bandmean_delta)
                # ratio = newMean_alpha / newMean_delta
                # print 'ratio', ratio
                ''' increment the mean, min and max arrays of the freqRange studied'''
                OPB1_mean_array_uv.append(newMean_alpha)

                if len(OPB1_mean_array_uv) != 0:
                    delta = np.amax(OPB1_mean_array_uv) - np.min(OPB1_mean_array_uv)  # Calculate delta before or after adding newMean_alpha?
                if len(OPB1_mean_array_uv) == 0:
                    delta = 0
                print "new Mean of 4 channels", newMean_alpha
                print "Max - Min ", delta

                if delta == 0:
                    level = 0

                if delta !=0:
                    level = int(math.floor(7*(newMean_alpha-np.min(OPB1_mean_array_uv))/delta)) #we dont take the newMean

                if level == 7:
                    score = score + 1
                    # punch_noise.play()
                    scoreDigit = pg.image.load(scoreDigitImages[score]).convert()
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
                buffer_1 = []

        except Empty:
            continue # do stuff
        else:
            str(buffer_1)
            #sys.stdout.write(char)

    while fly:

        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    fly = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0
        try:

            newPosy = mainNeuro(screen, sky, plane, queue, buffer_1, OPB1_data, oldPosy)  # function that move the bird according to the metric


        except Empty:
            continue  # do stuff
        else:
            str(buffer_1)
            # sys.stdout.write(char)

        pg.display.update()
        oldPosy = newPosy
        cpt = 0
        buffer_1 = []

    while restingState:
        # pg.time.Clock().tick(30)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    punchinBall = 0
                    fly = 0
                    restingState = 0
                    questionnaire = 0

        # time.sleep(1)
        pg.time.delay(990)
        # print sec
        if sec >= 100:
            timerSec = pg.image.load(timer[int(str(sec)[2])]).convert()
            timerSec = pg.transform.scale(timerSec, (70*w_display/1024, 90*h_display/576))
            timerDiz = pg.image.load(timer[int(str(sec)[1])]).convert()
            timerDiz = pg.transform.scale(timerDiz, (70*w_display/1024, 90*h_display/576))
            timerCen = pg.image.load(timer[int(str(sec)[0])]).convert()
            timerCen = pg.transform.scale(timerCen, (70*w_display/1024, 90*h_display/576))
            screen.blit(timerSec, (230*w_display/1024, 0*h_display/576))
            screen.blit(timerDiz, (115*w_display/1024, 0*h_display/576))
            screen.blit(timerCen, (0, 0))

        elif sec < 10:
            timerSec = pg.image.load(timer[int(str(sec)[0])]).convert()
            timerSec = pg.transform.scale(timerSec, (70*w_display/1024, 90*h_display/576))

            screen.blit(timerSec, (0, 0))

        elif sec >= 10 & sec < 100:
            timerSec = pg.image.load(timer[int(str(sec)[1])]).convert()
            timerSec = pg.transform.scale(timerSec, (70*w_display/1024, 90*h_display/576))
            timerDiz = pg.image.load(timer[int(str(sec)[0])]).convert()
            timerDiz = pg.transform.scale(timerDiz, (70*w_display/1024, 90*h_display/576))

            screen.blit(timerSec, (115*w_display/1024, 0*h_display/576))
            screen.blit(timerDiz, (0, 0*h_display/576))


        # timerSec = pg.image.load(timer[sec%10]).convert()
        # timerDiz = pg.image.load(timer[int(math.floor(sec/10))%100]).convert()
        # timerCen = pg.image.load(timer[int(math.floor(sec/100))]).convert()
        # checkImp() # TODO write check impedances function

        pg.display.update()
        sec = sec + 1

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
