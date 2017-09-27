#!/usr/bin/python
# coding=utf-8

import pygame as pg
from pygame.locals import *
from constantes_PunchinBall import *
# from constantesDataStream import *
import os
import sys
import signal
from subprocess import Popen, PIPE
from subprocess import call
from threading  import Thread
from sys import platform
from tempfile import TemporaryFile
from requests import *
import datetime
from functions import *
import os, binascii
from colour import Color

'''background'''
screen = pg.display.set_mode((w_display, h_display), RESIZABLE)
fond = pg.image.load(image_ring).convert()
fond = pg.transform.scale( fond, (w_display, h_display))

'''Punching ball'''
punchBall = pg.image.load(punchBallImage)
punchBall = pg.transform.scale(punchBall, (int(math.floor(0.244 * w_display)), int(math.floor(0.78*h_display))))

'''Score Bar'''
scoreBar = pg.image.load(levels_images[level]).convert_alpha()
scoreBar = pg.transform.scale(scoreBar, (int(math.floor(0.088*w_display)), int(math.floor(0.69*h_display))))
scoreBar = pg.transform.rotate(scoreBar, -90)
# test =pg.transform.scale(scoreBar, (90, 400))

'''Winner image'''
winImg = pg.image.load(winImg).convert_alpha()
winImg = pg.transform.scale(winImg, (int(math.floor(0.68*w_display)), int(math.floor(0.76*h_display))))
# punchBall = punch.set_colorkey((255,255,255))

'''Score digit '''
scoreTxt = pg.image.load(image_score)
scoreTxt = pg.transform.scale(scoreTxt, (int(math.floor(0.15*w_display)), int(math.floor(h_display*0.087))))
scoreDigit = pg.image.load(scoreDigitImages[0])
scoreDigit = pg.transform.scale(scoreDigit, (int(math.floor(0.068*w_display)), int(math.floor(0.156*h_display))))

'''training game'''
sky = pg.image.load(skyImage).convert()
sky = pg.transform.scale(sky, (w_display, h_display))
# cloud = pg.image.load(cloudImage).convert()
# cloud = pg.image.transform(cloud, ())
plane = pg.image.load(planeImage).convert_alpha()
plane = pg.transform.scale(plane, (50, 50))
red = Color("red")
colors = list(red.range_to(Color("green"), 100))
# plane = plane.set_colorkey((255, 255, 255))

'''Resting state'''
timerImage = pg.image.load(timer[0])
timerImage = pg.transform.scale(timerImage, (int(math.floor(0.068*w_display)), int(math.floor(0.156*h_display))))
restingImage = pg.image.load('images/restingState.png').convert()
restingStateImage = pg.transform.scale(restingImage, (w_display, h_display))

'''Tinnitus questionnaire '''
questionImage1 = pg.image.load(questionImage1Path)
questionImage1 = pg.transform.scale(questionImage1, (w_display, h_display))
questionImage2 = pg.image.load(questionImage2Path)
questionImage2 = pg.transform.scale(questionImage2, (w_display, h_display))

'''sleep'''
sleepImage = pg.image.load(sleepImgPath).convert()
sleepImage = pg.transform.scale(sleepImage, (w_display, h_display))

'''End Session IMG'''
endSessionImg = pg.image.load(endSessionImg)
endSessionImg = pg.transform.scale(endSessionImg, (w_display, h_display))

'''MAIN LOOP'''
gameOn = 1
now = datetime.datetime.now()
randomId = binascii.b2a_hex(os.urandom(15)) #id is 30 characters long
sessionName = str(str(now.month)+'_'+str(now.day)+'_'+str(now.minute)+'_'+str(randomId))

'''Loop that reads the text file sessionsNames, and check if the randomId has already been chosen in this folder'''
if os.path.isfile('sessionsNames.txt'):
    sessionsNames = open('sessionsNames.txt', 'r')
    sessionsNamesLines = sessionsNames.readlines()
    for i in range(len(sessionsNamesLines)):
        if randomId == sessionsNamesLines[i][-30:] :
            randomId = binascii.b2a_hex(os.urandom(15))
            sessionName = str(str(now.month)+'_'+str(now.day)+'_'+str(now.minute)+'_'+str(randomId))
    sessionsNames.close()
    sessionsNames = open('sessionsNames.txt', 'a+')

else :
    sessionsNames = open('sessionsNames.txt', 'a+')

sessionsNames.write(sessionName +'\n' )
sessionsNames.close()

'''check if the directory /data already exists'''
if not os.path.isdir('data'):
    os.mkdir('data')

'''create the paths and folders for the new session'''
if not os.path.isdir('data/'+sessionName):
    os.mkdir('data/'+sessionName)
    os.mkdir('data/'+sessionName+'/training-data')
    os.mkdir('data/'+sessionName+'/RS1-data')
    os.mkdir('data/'+sessionName+'/RS2-data')
    os.mkdir('data/'+sessionName+'/Saving-data')
    os.mkdir('data/'+sessionName+'/Sleep-data')
    pathT = str('data/'+sessionName+'/training-data/')
    pathS = str('data/'+sessionName+'/saving-data/')
    pathRS1 = str('data/'+sessionName+'/RS1-data/')
    pathRS2 = str('data/'+sessionName+'/RS2-data/')
    pathSleep = str('data/'+sessionName+'/Sleep-data/')



print '\n \n \n You are running Zeta Game on ', platform
print ' \n \n                     -----------------------------\n                     ------ Z E T A    A C S -----\n                     -----------------------------'
print '\n\n                     --------------------------------------------------------------\n                     -----  ________    ________   _________        .         -----\n                     -----         /   |               |           / \        -----\n                     -----        /    |               |          /   \       -----\n                     -----       /     |               |         /     \      -----\n                     -----      /      |____           |        /       \     -----\n                     -----     /       |               |       /_________\    -----\n                     -----    /        |               |      /           \   -----\n                     -----   /         |               |     /             \  -----\n                     -----  /_______   |_______        |    /               \ -----\n                     --------------------------------------------------------------'
print ' \n  Data will be saved here : ', pathRS2, pathRS1, pathT, pathS

'''MAIN LOOP'''

while gameOn:

    #LOAD screen Image
    home = pg.image.load(image_home).convert() #TODO add image_home
    home = pg.transform.scale(home, (w_display, h_display))
    screen.blit(home, (0,0))

    # load home menu buttons
    # settings = 'Lancer la session'
    # settingsSurf, settingsRect = text_objects(settings, buttonText)
    # settingsRect.center = (3.*w_display/10, 3.3*h_display/4)

    # launchTraining = 'Lancer la session'
    # launchTrainingSurf, launchTrainingRect = text_objects(launchTraining, buttonText)
    # launchTrainingRect.center = (2.*w_display/5, 3.3*h_display/4)

    nextStep = 'Etape suivante ICI'
    nextStepSurf, nextStepRect = text_objects(nextStep, buttonTextHuge)
    nextStepRect.center = (4.*w_display/10, 1.*h_display/4)

    progression = 'Progression'
    progressionSurf, progressionRect = text_objects(progression, buttonText)
    progressionRect.center = (4.*w_display/5, 3.3*h_display/4)

    # screen.blit(launchTrainingSurf, launchTrainingRect)

    pg.display.flip()


    # Home window loop
    while homeOn:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP and not(sessionEnded):
                mouseHome = pg.mouse.get_pos()
                choice = whichButtonHomePatient(mouseHome, w_display, h_display)

                if choice == 1: #  start training with RS1
                    homeOn = 0
                    training = 0
                    restingState1 = 1
                    restingState2 = 0
                    sleep = 0
                    saving = 0
                elif choice == 2: # saving of 1:30 of EEG
                    homeOn = 0
                    training = 0
                    restingState1 = 0
                    restingState2 = 0
                    sleep = 0
                    saving = 1
                elif choice == 3: #  is for sleep session, starts and stops when he decides
                    homeOn = 0
                    training = 0
                    restingState1 = 0
                    restingState2 = 0
                    sleep = 1
                    saving = 0

        if sessionEnded :
            progressionMetricSurf, progressionMetricRect = text_objects(progressionMetric, buttonText)
            progressionMetricRect.center = (1.*w_display/2, 1.*h_display/2)
            screen.blit(endSessionImg, (0,0))
            screen.blit(progressionMetricSurf, progressionMetricRect)
            pg.display.flip()

    if restingState1:
        print "RESTINGSTATE1"
        if platform == 'darwin' and sessionRS == 0: # mac
            process = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()
        elif platform == 'linux' or platform == 'linux2' and sessionRS == 0: #linux
            process = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE, preexec_fn=os.setsid) # for LINUX
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()

        sessionRS += 1
        secRS1 = 0
        bufferRS1 = []
        band_alphaRS1_ch1 = []
        band_alphaRS1_ch2 = []
        band_alphaRS1_ch3 = []
        band_alphaRS1_ch4 = []
        band_deltaRS1_ch1 = []
        band_deltaRS1_ch2 = []
        band_deltaRS1_ch3 = []
        band_deltaRS1_ch4 = []
        screen.blit(restingStateImage, (0,0))
        displayNumber(0, screen, 'timeRSV011')
        pg.display.flip()
        queue.queue.clear()

    if training:
        print "TRAINING"
        sessionF += 1
        bufferT = []
        screen.blit(sky, (0, 0))
        pg.display.flip()
        queue.queue.clear()

    if restingState2:
        print "RESTINGSTATE2"
        sessionRS += 1
        secRS2 = 0
        bufferRS2 = []
        band_alphaRS2_ch1 = []
        band_alphaRS2_ch2 = []
        band_alphaRS2_ch3 = []
        band_alphaRS2_ch4 = []
        band_deltaRS2_ch1 = []
        band_deltaRS2_ch2 = []
        band_deltaRS2_ch3 = []
        band_deltaRS2_ch4 = []
        screen.blit(restingStateImage, (0,0))
        displayNumber(0, screen, 'timeRSV011')
        pg.display.flip()
        queue.queue.clear()

    if saving:
        print "SAVING"
        if platform == 'darwin' and sessionRS == 0: # mac
            process = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()
        elif platform == 'linux' or platform == 'linux2' and sessionRS == 0: #linux
            process = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE, preexec_fn=os.setsid) # for LINUX
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()

        secS = 0
        bufferS = []
        band_alphaS_ch1 = []
        band_alphaS_ch2 = []
        band_alphaS_ch3 = []
        band_alphaS_ch4 = []
        band_deltaS_ch1 = []
        band_deltaS_ch2 = []
        band_deltaS_ch3 = []
        band_deltaS_ch4 = []
        screen.blit(restingStateImage, (0,0))
        displayNumber(0, screen, 'timeRSV011')
        pg.display.flip()
        queue.queue.clear()

    if sleep :
        print "SLEEP"
        if platform == 'darwin' and sessionRS == 0: # mac
            process = Popen(['/usr/local/bin/node', 'openBCIDataStream.js'], stdout=PIPE) # for MAC
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()
        elif platform == 'linux' or platform == 'linux2' and sessionRS == 0: #linux
            process = Popen(['sudo', '/usr/bin/node', 'openBCIDataStream.js'], stdout=PIPE, preexec_fn=os.setsid) # for LINUX
            '''launch node process'''
            queue = Queue()
            thread = Thread(target=enqueue_output, args=(process.stdout, queue))
            thread.daemon = True
            thread.start()

        secSleep = 0
        bufferSleep = []
        band_alphaSleep_ch1 = []
        band_alphaSleep_ch2 = []
        band_alphaSleep_ch3 = []
        band_alphaSleep_ch4 = []
        band_deltaSleep_ch1 = []
        band_deltaSleep_ch2 = []
        band_deltaSleep_ch3 = []
        band_deltaSleep_ch4 = []
        screen.blit(sleepImage, (0,0))
        displayNumber(0, screen, 'timeSleep')
        pg.display.flip()
        queue.queue.clear()

    while restingState1:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(pathRS1, sessionRS, 'RS', saved_bufferRS1_ch1, saved_bufferRS1_ch2, saved_bufferRS1_ch3, saved_bufferRS1_ch4)
                saved_bufferRS1_ch1 = []
                saved_bufferRS1_ch2 = []
                saved_bufferRS1_ch3 = []
                saved_bufferRS1_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState1 = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    training = 0
                    restingState1 = 0
                    bufferRS1 = []
                    queue.queue.clear()
                    saveAllChannelsData(pathRS1, sessionRS, 'RS', saved_bufferRS1_ch1, saved_bufferRS1_ch2, saved_bufferRS1_ch3, saved_bufferRS1_ch4)
                    saved_bufferRS1_ch1 = []
                    saved_bufferRS1_ch2 = []
                    saved_bufferRS1_ch3 = []
                    saved_bufferRS1_ch4 = []

        if secRS1 == restingStateDuration :
            # np.zeros(nb_freq_alpha)
            band_alphaRS1_ch1 = np.asarray(band_alphaRS1_ch1)
            band_alphaRS1_ch2 = np.asarray(band_alphaRS1_ch2)
            band_alphaRS1_ch3 = np.asarray(band_alphaRS1_ch3)
            band_alphaRS1_ch4 = np.asarray(band_alphaRS1_ch4)
            # print 'band_alphaRS_ch1', band_alphaRS_ch1
            # print 'band_alphaRS_ch1[:, 0]', np.average(band_alphaRS_ch1[:,0])
            freqMaxAlphaCh1 = getfreqmaxband(band_alphaRS1_ch1, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh2 = getfreqmaxband(band_alphaRS1_ch2, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh3 = getfreqmaxband(band_alphaRS1_ch3, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh4 = getfreqmaxband(band_alphaRS1_ch4, 'alpha', nb_freq_alpha)

            freqMaxAlpha = int(np.average([freqMaxAlphaCh1, freqMaxAlphaCh2, freqMaxAlphaCh3, freqMaxAlphaCh4]))

            for chunk in range(restingStateDuration):
                ratios_ch1.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS1[0,:, chunk], freqMaxAlphaCh1-2, freqMaxAlphaCh1+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS1[0,:, chunk], 3, 4)[0])))
                ratios_ch2.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS1[1,:, chunk], freqMaxAlphaCh2-2, freqMaxAlphaCh2+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS1[1,:, chunk], 3, 4)[0])))
                ratios_ch3.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS1[2,:, chunk], freqMaxAlphaCh3-2, freqMaxAlphaCh3+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS1[2,:, chunk], 3, 4)[0])))
                ratios_ch4.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS1[3,:, chunk], freqMaxAlphaCh4-2, freqMaxAlphaCh4+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS1[3,:, chunk], 3, 4)[0])))

            median_ratio_ch1 = np.median(ratios_ch1)
            median_ratio_ch2 = np.median(ratios_ch2)
            median_ratio_ch3 = np.median(ratios_ch3)
            median_ratio_ch4 = np.median(ratios_ch4)

            mad_ch1 = mad(ratios_ch1)
            mad_ch2 = mad(ratios_ch2)
            mad_ch3 = mad(ratios_ch3)
            mad_ch4 = mad(ratios_ch4)

            madRatioAlphaOverDelta = np.average([mad_ch4, mad_ch3, mad_ch2, mad_ch1])
            medianratioAlphaoverDelta = np.average([median_ratio_ch1, median_ratio_ch2, median_ratio_ch3, median_ratio_ch4])
            minRatioAlphaOverDelta = medianratioAlphaoverDelta - 3 * madRatioAlphaOverDelta
            maxRatioAlphaOverDelta = medianratioAlphaoverDelta + 3 * madRatioAlphaOverDelta

            screen.blit(nextStepSurf, nextStepRect)
            pg.display.flip()


            ''' END OF THE SESSION, WAITING FOR THE USER TO CLICK ON THE TEXT BUTTON '''
            for event in pg.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouseRS1 = pg.mouse.get_pos()
                    saveAllChannelsData(pathRS1, sessionRS, 'RS', saved_bufferRS1_ch1, saved_bufferRS1_ch2, saved_bufferRS1_ch3, saved_bufferRS1_ch4)
                    saved_bufferRS1_ch1 = []
                    saved_bufferRS1_ch2 = []
                    saved_bufferRS1_ch3 = []
                    saved_bufferRS1_ch4 = []
                    RS1choice = whichButtonHomeV2(mouseRS1, w_display, h_display)
                    if RS1choice == 3:
                        homeOn = 0
                        training = 1
                        restingState1 = 0
                        bufferRS1 = []
                        queue.queue.clear()


        elif secRS1 < restingStateDuration:
            try:
                # queue.queue.clear()
                while len(bufferRS1) < buffersize * nb_channels:
                    bufferRS1.append(queue.get_nowait())

                if len(bufferRS1) == buffersize * nb_channels:
                    # print sec
                    bufferRS1_array = np.asarray(bufferRS1)

                    dataRS1[0, :, secRS1] = bufferRS1_array[ind_channel_1]
                    dataRS1[1, :, secRS1] = bufferRS1_array[ind_channel_2]
                    dataRS1[2, :, secRS1] = bufferRS1_array[ind_channel_3]
                    dataRS1[3, :, secRS1] = bufferRS1_array[ind_channel_4]

                    saved_bufferRS1_ch1.append(dataRS1[0, :, secRS1])
                    saved_bufferRS1_ch2.append(dataRS1[1, :, secRS1])
                    saved_bufferRS1_ch3.append(dataRS1[2, :, secRS1])
                    saved_bufferRS1_ch4.append(dataRS1[3, :, secRS1])

                    fdataRS1[0, :, secRS1] = filter_data(dataRS1[0, :, secRS1], fs_hz)
                    fdataRS1[1, :, secRS1] = filter_data(dataRS1[1, :, secRS1], fs_hz)
                    fdataRS1[2, :, secRS1] = filter_data(dataRS1[2, :, secRS1], fs_hz)
                    fdataRS1[3, :, secRS1] = filter_data(dataRS1[3, :, secRS1], fs_hz)

                    band_alphaRS1_ch1.append(extract_freqband(200, fs_hz, fdataRS1[0,:, secRS1], 6, 13)[0])
                    band_alphaRS1_ch2.append(extract_freqband(200, fs_hz, fdataRS1[1,:, secRS1], 6, 13)[0])
                    band_alphaRS1_ch3.append(extract_freqband(200, fs_hz, fdataRS1[2,:, secRS1], 6, 13)[0])
                    band_alphaRS1_ch4.append(extract_freqband(200, fs_hz, fdataRS1[3,:, secRS1], 6, 13)[0])

                    nb_freq_alpha = extract_freqband(200, fs_hz, fdataRS1[0,:], 6, 13)[1]

                    band_deltaRS1_ch1.append(extract_freqband(200, fs_hz, fdataRS1[0,:, secRS1], 3, 4)[0])
                    band_deltaRS1_ch2.append(extract_freqband(200, fs_hz, fdataRS1[1,:, secRS1], 3, 4)[0])
                    band_deltaRS1_ch3.append(extract_freqband(200, fs_hz, fdataRS1[2,:, secRS1], 3, 4)[0])
                    band_deltaRS1_ch4.append(extract_freqband(200, fs_hz, fdataRS1[3,:, secRS1], 3, 4)[0])

                    nb_freq_delta = extract_freqband(200, fs_hz, fdataRS1[3,:], 3, 4)[1]

                    bufferRS1 = []
                    displayNumber(secRS1, screen, 'timeRSV011')
                    # checkImp() # TODO  check impedances function
                    pg.display.update()
                    secRS1 = secRS1 + 1

            except Empty:
                continue  # do stuff
            else:
                str(bufferRS1)
                # sys.stdout.write(char)

    while training:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(pathT, sessionF, 'F', saved_bufferT_ch1, saved_bufferT_ch2, saved_bufferT_ch3, saved_bufferT_ch4)
                bufferT = []
                saved_bufferT_ch1 = []
                saved_bufferT_ch2 = []
                saved_bufferT_ch3 = []
                saved_bufferT_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    saveAllChannelsData(pathT, sessionF, 'F', saved_bufferT_ch1, saved_bufferT_ch2, saved_bufferT_ch3, saved_bufferT_ch4)
                    bufferT = []
                    saved_bufferT_ch1 = []
                    saved_bufferT_ch2 = []
                    saved_bufferT_ch3 = []
                    saved_bufferT_ch4 = []
                    training = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    training = 0
                    restingState1 = 0
                    saveAllChannelsData(pathT, sessionF, 'F', saved_bufferT_ch1, saved_bufferT_ch2, saved_bufferT_ch3, saved_bufferT_ch4)
                    bufferT = []
                    saved_bufferT_ch1 = []
                    saved_bufferT_ch2 = []
                    saved_bufferT_ch3 = []
                    saved_bufferT_ch4 = []

        if durationSession > 0:
            try:
                while len(bufferT) < buffersize * nb_channels:

                    if len(bufferT) % int(math.floor(1.*buffersize/5)) == 0:
                        screen.blit(sky, (0,0))
                        indColor = get_ind_color(trainingScore(newPosy), 10,0, len(colors))
                        color = (colors[indColor].rgb[0]*255,colors[indColor].rgb[1]*255,colors[indColor].rgb[2]*255)
                        if (veryOldPosy + 1.*(oldPosy - veryOldPosy)/steps) <= minDisplayY + 10 :
                            positionY = minDisplayY + 10
                        elif (veryOldPosy + 1.*(oldPosy - veryOldPosy)/steps) >= maxDisplayY :
                            positionY = maxDisplayY
                        else :
                            positionY = veryOldPosy + 1.*(oldPosy - veryOldPosy)/steps

                        pg.draw.rect(screen, color , (2. * w_display / 12, positionY, 100, 10 ))
                        displayNumber(math.floor(scoreF), screen, 'scoreV011')
                        displayNumber(durationSession, screen, 'timeV011')
                        veryOldPosy += 1.*(oldPosy - veryOldPosy)/steps
                        pg.display.flip()

                    bufferT.append(queue.get_nowait())

                if len(bufferT) == buffersize * nb_channels :
                    bufferT_array = np.asarray(bufferT)

                    dataF[0, :] = bufferT_array[ind_channel_1]
                    dataF[1, :] = bufferT_array[ind_channel_2]
                    dataF[2, :] = bufferT_array[ind_channel_3]
                    dataF[3, :] = bufferT_array[ind_channel_4]

                    saved_bufferT_ch1.append(dataF[0, :])
                    saved_bufferT_ch2.append(dataF[1, :])
                    saved_bufferT_ch3.append(dataF[2, :])
                    saved_bufferT_ch4.append(dataF[3, :])

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
                    ratioF = np.zeros(nb_channels)

                    for channel in range(nb_channels):
                        bandmean_alphaF[channel] = extract_freqbandmean(200, fs_hz, fdataF[channel,:], freqMaxAlpha-2, freqMaxAlpha+2)
                        bandmean_deltaF[channel] = extract_freqbandmean(200, fs_hz, fdataF[channel,:], 3, 4)
                        ratioF[channel] = 1.* bandmean_alphaF[channel] / bandmean_deltaF[channel]

                    # maximiser alpha/delta
                    ''' Get the mean, min and max of the last reslt of all channels'''
                    newMean_alphaF = np.average(bandmean_alphaF)
                    # maxAlphaF = np.amax(mean_array_uvF)
                    # minAlphaF = np.min(mean_array_uvF)

                    medRatioF = np.median(ratioF)
                    mean_array_uvF.append(medRatioF)

                    if medRatioF == maxRatioAlphaOverDelta:
                        newPosy = minDisplayY

                    elif medRatioF == minRatioAlphaOverDelta:
                        newPosy = maxDisplayY

                    else:
                        a = (maxDisplayY - minDisplayY) * 1. / (minRatioAlphaOverDelta - maxRatioAlphaOverDelta)
                        b = maxDisplayY - minRatioAlphaOverDelta * a
                        newPosy = a * medRatioF + b

                    scoreF = scoreF + trainingScore(newPosy)
                    durationSession = durationSession -  1

            except Empty:
                continue  # do stuff
            else:
                str(bufferT)
                # sys.stdout.write(char)
            veryOldPosy = oldPosy
            oldPosy = newPosy
            saved_bufferT.append(bufferT)
            bufferT = []

        elif durationSession == 0 :
            saveAllChannelsData(pathT, sessionF, 'F', saved_bufferT_ch1, saved_bufferT_ch2, saved_bufferT_ch3, saved_bufferT_ch4)
            saved_bufferT_ch1 = []
            saved_bufferT_ch2 = []
            saved_bufferT_ch3 = []
            saved_bufferT_ch4 = []
            screen.blit(nextStepSurf, nextStepRect)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouseRS2 = pg.mouse.get_pos()
                    choiceRS2 = whichButtonHomeV2(mouseRS2, w_display, h_display)
                    if choiceRS2 == 3:
                        bufferT = []
                        durationSession = durationSessionInit
                        training = 0
                        homeOn = 1
                        restingState1 = 0
                        restingState2 = 0
                        bufferRS1 = []
                        band_alphaRS1_ch1 = []
                        band_alphaRS1_ch2 = []
                        band_alphaRS1_ch3 = []
                        band_alphaRS1_ch4 = []
                        band_deltaRS1_ch1 = []
                        band_deltaRS1_ch2 = []
                        band_deltaRS1_ch3 = []
                        band_deltaRS1_ch4 = []
                        screen.blit(restingStateImage, (0,0))
                        displayNumber(0, screen, 'timeRSV011')
                        pg.display.flip()
                        queue.queue.clear()

    while restingState2:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(pathRS2, sessionRS, 'RS', saved_bufferRS2_ch1, saved_bufferRS2_ch2, saved_bufferRS2_ch3, saved_bufferRS2_ch4)
                saved_bufferRS2_ch1 = []
                saved_bufferRS2_ch2 = []
                saved_bufferRS2_ch3 = []
                saved_bufferRS2_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState2 = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    training = 0
                    restingState2 = 0
                    questionnaire = 0
                    bufferRS2 = []
                    queue.queue.clear()
                    saveAllChannelsData(pathRS2, sessionRS, 'RS', saved_bufferRS2_ch1, saved_bufferRS2_ch2, saved_bufferRS2_ch3, saved_bufferRS2_ch4)
                    saved_bufferRS2_ch1 = []
                    saved_bufferRS2_ch2 = []
                    saved_bufferRS2_ch3 = []
                    saved_bufferRS2_ch4 = []
                    # print bufferRS

                    # print band_alphaRS_ch1

        if secRS2 == restingStateDuration :
            # np.zeros(nb_freq_alpha)
            band_alphaRS2_ch1 = np.asarray(band_alphaRS2_ch1)
            band_alphaRS2_ch2 = np.asarray(band_alphaRS2_ch2)
            band_alphaRS2_ch3 = np.asarray(band_alphaRS2_ch3)
            band_alphaRS2_ch4 = np.asarray(band_alphaRS2_ch4)
            # print 'band_alphaRS_ch1', band_alphaRS_ch1
            # print 'band_alphaRS_ch1[:, 0]', np.average(band_alphaRS_ch1[:,0])
            freqMaxAlphaCh1 = getfreqmaxband(band_alphaRS2_ch1, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh2 = getfreqmaxband(band_alphaRS2_ch2, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh3 = getfreqmaxband(band_alphaRS2_ch3, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh4 = getfreqmaxband(band_alphaRS2_ch4, 'alpha', nb_freq_alpha)

            freqMaxAlpha = int(np.average([freqMaxAlphaCh1, freqMaxAlphaCh2, freqMaxAlphaCh3, freqMaxAlphaCh4]))

            for chunk in range(restingStateDuration):
                ratios_ch1.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS2[0,:, chunk], freqMaxAlphaCh1-2, freqMaxAlphaCh1+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS2[0,:, chunk], 3, 4)[0])))
                ratios_ch2.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS2[1,:, chunk], freqMaxAlphaCh2-2, freqMaxAlphaCh2+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS2[1,:, chunk], 3, 4)[0])))
                ratios_ch3.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS2[2,:, chunk], freqMaxAlphaCh3-2, freqMaxAlphaCh3+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS2[2,:, chunk], 3, 4)[0])))
                ratios_ch4.append(1.*np.median((extract_freqband(200, fs_hz, fdataRS2[3,:, chunk], freqMaxAlphaCh4-2, freqMaxAlphaCh4+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataRS2[3,:, chunk], 3, 4)[0])))

            median_ratio_ch1 = np.median(ratios_ch1)
            median_ratio_ch2 = np.median(ratios_ch2)
            median_ratio_ch3 = np.median(ratios_ch3)
            median_ratio_ch4 = np.median(ratios_ch4)

            mad_ch1 = mad(ratios_ch1)
            mad_ch2 = mad(ratios_ch2)
            mad_ch3 = mad(ratios_ch3)
            mad_ch4 = mad(ratios_ch4)

            madRatioAlphaOverDeltaEnd = np.average([mad_ch4, mad_ch3, mad_ch2, mad_ch1])
            medianratioAlphaoverDeltaEnd = np.average([median_ratio_ch1, median_ratio_ch2, median_ratio_ch3, median_ratio_ch4])
            minRatioAlphaOverDelta = medianratioAlphaoverDelta - 3 * madRatioAlphaOverDelta
            maxRatioAlphaOverDelta = medianratioAlphaoverDelta + 3 * madRatioAlphaOverDelta

            metric = medianratioAlphaoverDeltaEnd - medianratioAlphaoverDelta
            if  metric >= 0 :
                progressionMetric = 'Progression ' + str( metric )[0] + '.' + str(metric)[2:5]
            elif metric < 0 :
                progressionMetric = 'Progression : -' + str( metric )[1] + '.' + str(metric)[3:6]

            sessionEnded = 1
            homeOn = 0
            training = 0
            restingState2 = 0
            progressionMetricSurf, progressionMetricRect = text_objects(progressionMetric, buttonText)
            progressionMetricRect.center = (1.*w_display/2, 1.*h_display/2)
            screen.blit(endSessionImg, (0,0))
            screen.blit(progressionMetricSurf, progressionMetricRect)
            pg.display.flip()

            # process.terminate()
            # call(['sudo service bluetooth restart'])
            # os.system('sudo service bluetooth restart')
            bufferRS2 = []
            queue.queue.clear()
            saveAllChannelsData(pathRS2, sessionRS, 'RS', saved_bufferRS2_ch1, saved_bufferRS2_ch2, saved_bufferRS2_ch3, saved_bufferRS2_ch4)
            saved_bufferRS2_ch1 = []
            saved_bufferRS2_ch2 = []
            saved_bufferRS2_ch3 = []
            saved_bufferRS2_ch4 = []

        elif secRS2 < restingStateDuration:
            try:
                # queue.queue.clear()
                while len(bufferRS2) < buffersize * nb_channels:
                    bufferRS2.append(queue.get_nowait())

                if len(bufferRS2) == buffersize * nb_channels:
                    # print secRS2
                    bufferRS2_array = np.asarray(bufferRS2)

                    dataRS2[0, :, secRS2] = bufferRS2_array[ind_channel_1]
                    dataRS2[1, :, secRS2] = bufferRS2_array[ind_channel_2]
                    dataRS2[2, :, secRS2] = bufferRS2_array[ind_channel_3]
                    dataRS2[3, :, secRS2] = bufferRS2_array[ind_channel_4]

                    saved_bufferRS2_ch1.append(dataRS2[0, :, secRS2])
                    saved_bufferRS2_ch2.append(dataRS2[1, :, secRS2])
                    saved_bufferRS2_ch3.append(dataRS2[2, :, secRS2])
                    saved_bufferRS2_ch4.append(dataRS2[3, :, secRS2])

                    fdataRS2[0, :, secRS2] = filter_data(dataRS2[0, :, secRS2], fs_hz)
                    fdataRS2[1, :, secRS2] = filter_data(dataRS2[1, :, secRS2], fs_hz)
                    fdataRS2[2, :, secRS2] = filter_data(dataRS2[2, :, secRS2], fs_hz)
                    fdataRS2[3, :, secRS2] = filter_data(dataRS2[3, :, secRS2], fs_hz)

                    band_alphaRS2_ch1.append(extract_freqband(200, fs_hz, fdataRS2[0,:, secRS2], 6, 13)[0])
                    band_alphaRS2_ch2.append(extract_freqband(200, fs_hz, fdataRS2[1,:, secRS2], 6, 13)[0])
                    band_alphaRS2_ch3.append(extract_freqband(200, fs_hz, fdataRS2[2,:, secRS2], 6, 13)[0])
                    band_alphaRS2_ch4.append(extract_freqband(200, fs_hz, fdataRS2[3,:, secRS2], 6, 13)[0])

                    nb_freq_alpha = extract_freqband(200, fs_hz, fdataRS2[0,:], 6, 13)[1]

                    band_deltaRS2_ch1.append(extract_freqband(200, fs_hz, fdataRS2[0,:, secRS2], 3, 4)[0])
                    band_deltaRS2_ch2.append(extract_freqband(200, fs_hz, fdataRS2[1,:, secRS2], 3, 4)[0])
                    band_deltaRS2_ch3.append(extract_freqband(200, fs_hz, fdataRS2[2,:, secRS2], 3, 4)[0])
                    band_deltaRS2_ch4.append(extract_freqband(200, fs_hz, fdataRS2[3,:, secRS2], 3, 4)[0])

                    nb_freq_delta = extract_freqband(200, fs_hz, fdataRS2[3,:], 3, 4)[1]

                    bufferRS2 = []
                    displayNumber(secRS2, screen, 'timeRSV011')
                    # checkImp() # TODO  check impedances function
                    pg.display.update()
                    secRS2 = secRS2 + 1

            except Empty:
                continue  # do stuff
            else:
                str(bufferRS2)
                # sys.stdout.write(char)

    while saving:
        # print "while saving"
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(pathS, sessionS, 'RS', saved_bufferS_ch1, saved_bufferS_ch2, saved_bufferS_ch3, saved_bufferS_ch4)
                saved_bufferS_ch1 = []
                saved_bufferS_ch2 = []
                saved_bufferS_ch3 = []
                saved_bufferS_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState1 = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    training = 0
                    restingState1 = 0
                    bufferS = []
                    queue.queue.clear()
                    saveAllChannelsData(pathS, sessionRS, 'RS', saved_bufferS_ch1, saved_bufferS_ch2, saved_bufferS_ch3, saved_bufferS_ch4)
                    saved_bufferS_ch1 = []
                    saved_bufferS_ch2 = []
                    saved_bufferS_ch3 = []
                    saved_bufferS_ch4 = []


        if secS == durationSessionSaving :
            # np.zeros(nb_freq_alpha)
            band_alphaS_ch1 = np.asarray(band_alphaS_ch1)
            band_alphaS_ch2 = np.asarray(band_alphaS_ch2)
            band_alphaS_ch3 = np.asarray(band_alphaS_ch3)
            band_alphaS_ch4 = np.asarray(band_alphaS_ch4)
            # print 'band_alphaRS_ch1', band_alphaRS_ch1
            # print 'band_alphaRS_ch1[:, 0]', np.average(band_alphaRS_ch1[:,0])
            freqMaxAlphaCh1 = getfreqmaxband(band_alphaS_ch1, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh2 = getfreqmaxband(band_alphaS_ch2, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh3 = getfreqmaxband(band_alphaS_ch3, 'alpha', nb_freq_alpha)
            freqMaxAlphaCh4 = getfreqmaxband(band_alphaS_ch4, 'alpha', nb_freq_alpha)

            freqMaxAlpha = int(np.average([freqMaxAlphaCh1, freqMaxAlphaCh2, freqMaxAlphaCh3, freqMaxAlphaCh4]))

            for chunk in range(durationSessionSaving):
                ratios_ch1.append(1.*np.median((extract_freqband(200, fs_hz, fdataS[0,:, chunk], freqMaxAlphaCh1-2, freqMaxAlphaCh1+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataS[0,:, chunk], 3, 4)[0])))
                ratios_ch2.append(1.*np.median((extract_freqband(200, fs_hz, fdataS[1,:, chunk], freqMaxAlphaCh2-2, freqMaxAlphaCh2+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataS[1,:, chunk], 3, 4)[0])))
                ratios_ch3.append(1.*np.median((extract_freqband(200, fs_hz, fdataS[2,:, chunk], freqMaxAlphaCh3-2, freqMaxAlphaCh3+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataS[2,:, chunk], 3, 4)[0])))
                ratios_ch4.append(1.*np.median((extract_freqband(200, fs_hz, fdataS[3,:, chunk], freqMaxAlphaCh4-2, freqMaxAlphaCh4+2)[0]))/np.median((extract_freqband(200, fs_hz, fdataS[3,:, chunk], 3, 4)[0])))

            median_ratio_ch1 = np.median(ratios_ch1)
            median_ratio_ch2 = np.median(ratios_ch2)
            median_ratio_ch3 = np.median(ratios_ch3)
            median_ratio_ch4 = np.median(ratios_ch4)

            mad_ch1 = mad(ratios_ch1)
            mad_ch2 = mad(ratios_ch2)
            mad_ch3 = mad(ratios_ch3)
            mad_ch4 = mad(ratios_ch4)

            madRatioAlphaOverDelta = np.average([mad_ch4, mad_ch3, mad_ch2, mad_ch1])
            medianratioAlphaoverDelta = np.average([median_ratio_ch1, median_ratio_ch2, median_ratio_ch3, median_ratio_ch4])
            minRatioAlphaOverDelta = medianratioAlphaoverDelta - 3 * madRatioAlphaOverDelta
            maxRatioAlphaOverDelta = medianratioAlphaoverDelta + 3 * madRatioAlphaOverDelta

            # screen.blit(nextStepSurf, nextStepRect)
            # pg.display.flip()
            bufferS = []
            queue.queue.clear()
            if answer2Ind == 0 :
                screen.blit(questionImage1, (0,0))
                question1 = 'Quelle est la force de votre acouphene ?'
                question1Surf, question1Rect = text_objects(question1, buttonText)
                question1Rect.center = (5. * w_display / 10, 1.*h_display/4)
                screen.blit(question1Surf, question1Rect)
                pg.display.flip()

            ''' END OF THE SESSION, WAITING FOR THE USER TO CLICK ON THE TEXT BUTTON '''
            for event in pg.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouseS = pg.mouse.get_pos()
                    saveAllChannelsData(pathS, sessionRS, 'RS', saved_bufferS_ch1, saved_bufferS_ch2, saved_bufferS_ch3, saved_bufferS_ch4)
                    saved_bufferS_ch1 = []
                    saved_bufferS_ch2 = []
                    saved_bufferS_ch3 = []
                    saved_bufferS_ch4 = []
                    sChoice = whichAnswerCliked(mouseS, w_display, h_display)
                    if sChoice == 1 or sChoice == 2 or sChoice == 3 or sChoice == 4 or sChoice == 5:
                         #open file and save the answer
                        print "level is", sChoice
                        answer1 = sChoice - 1
                        sChoice = 0
                        answer2Ind = 1
                        screen.blit(questionImage2, (0,0))
                        question2 = 'A quel point vous derange-t-il ?'
                        question2Surf, question2Rect = text_objects(question2, buttonText)
                        question2Rect.center = (5. * w_display / 10, 4.*h_display/7)
                        screen.blit(question2Surf, question2Rect)
                        pg.display.flip()
                    elif (sChoice == 11 or sChoice == 12 or sChoice == 13 or sChoice == 14 or sChoice == 15) and answer2Ind != 0 :
                         #open file and save the answer
                        print "level is", sChoice
                        answer2 = sChoice - 11
                        sChoice = 0
                        answersFile = open('answersFile.txt', 'a+')
                        answersFile.write(sessionName+ ' | Answers : Quelle est la force de votre acouphene ? '+str(answer1)+ '/4 | '+'A quel point vous derange-t-il ? ' + str(answer2) + '/4\n')
                        screen.blit(endSessionImg, (0,0))
                        pg.display.flip()

                # answersFile = open('answers.txt', 'a+')

        elif secS < durationSessionSaving:
            try:
                # queue.queue.clear()
                while len(bufferS) < buffersize * nb_channels:
                    bufferS.append(queue.get_nowait())

                if len(bufferS) == buffersize * nb_channels:

                    bufferS_array = np.asarray(bufferS)

                    dataS[0, :, secS] = bufferS_array[ind_channel_1]
                    dataS[1, :, secS] = bufferS_array[ind_channel_2]
                    dataS[2, :, secS] = bufferS_array[ind_channel_3]
                    dataS[3, :, secS] = bufferS_array[ind_channel_4]

                    saved_bufferS_ch1.append(dataS[0, :, secS])
                    saved_bufferS_ch2.append(dataS[1, :, secS])
                    saved_bufferS_ch3.append(dataS[2, :, secS])
                    saved_bufferS_ch4.append(dataS[3, :, secS])

                    fdataS[0, :, secS] = filter_data(dataS[0, :, secS], fs_hz)
                    fdataS[1, :, secS] = filter_data(dataS[1, :, secS], fs_hz)
                    fdataS[2, :, secS] = filter_data(dataS[2, :, secS], fs_hz)
                    fdataS[3, :, secS] = filter_data(dataS[3, :, secS], fs_hz)

                    band_alphaS_ch1.append(extract_freqband(200, fs_hz, fdataS[0,:, secS], 6, 13)[0])
                    band_alphaS_ch2.append(extract_freqband(200, fs_hz, fdataS[1,:, secS], 6, 13)[0])
                    band_alphaS_ch3.append(extract_freqband(200, fs_hz, fdataS[2,:, secS], 6, 13)[0])
                    band_alphaS_ch4.append(extract_freqband(200, fs_hz, fdataS[3,:, secS], 6, 13)[0])

                    nb_freq_alpha = extract_freqband(200, fs_hz, fdataS[0,:], 6, 13)[1]

                    band_deltaS_ch1.append(extract_freqband(200, fs_hz, fdataS[0,:, secS], 3, 4)[0])
                    band_deltaS_ch2.append(extract_freqband(200, fs_hz, fdataS[1,:, secS], 3, 4)[0])
                    band_deltaS_ch3.append(extract_freqband(200, fs_hz, fdataS[2,:, secS], 3, 4)[0])
                    band_deltaS_ch4.append(extract_freqband(200, fs_hz, fdataS[3,:, secS], 3, 4)[0])

                    nb_freq_delta = extract_freqband(200, fs_hz, fdataS[3,:], 3, 4)[1]

                    bufferS = []
                    displayNumber(secS, screen, 'timeRSV011')
                    # checkImp() # TODO  check impedances function
                    pg.display.update()
                    secS = secS + 1

            except Empty:
                continue  # do stuff
            else:
                str(bufferS)
                # sys.stdout.write(char)

    while sleep:
        pg.time.Clock().tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                saveAllChannelsData(pathSleep, sessionRS, 'Sleep', saved_bufferSleep_ch1, saved_bufferSleep_ch2, saved_bufferSleep_ch3, saved_bufferSleep_ch4)
                saved_bufferSleep_ch1 = []
                saved_bufferSleep_ch2 = []
                saved_bufferSleep_ch3 = []
                saved_bufferSleep_ch4 = []
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    restingState1 = 0
            elif event.type == MOUSEBUTTONUP:
                mouseReturn = pg.mouse.get_pos()
                if whichButtonReturn(mouseReturn, w_display, h_display):
                    homeOn = 1
                    training = 0
                    sleep = 0
                    restingState1 = 0
                    bufferSleep = []
                    queue.queue.clear()
                    saveAllChannelsData(pathSleep, sessionRS, 'Sleep', saved_bufferSleep_ch1, saved_bufferSleep_ch2, saved_bufferSleep_ch3, saved_bufferSleep_ch4)
                    saved_bufferSleep_ch1 = []
                    saved_bufferSleep_ch2 = []
                    saved_bufferSleep_ch3 = []
                    saved_bufferSleep_ch4 = []

        if secSleep < 9999:

            try:
                while len(bufferSleep) < buffersize * nb_channels:
                    bufferSleep.append(queue.get_nowait())

                if len(bufferSleep) == buffersize * nb_channels:
                    bufferSleep_array = np.asarray(bufferSleep)
                    dataSleep = np.zeros((nb_channels, buffersize)) # need to store every chunk to reprocess the ratio
                    fdataSleep = np.zeros((nb_channels, buffersize))

                    dataSleep[0, :] = bufferSleep_array[ind_channel_1]
                    dataSleep[1, :] = bufferSleep_array[ind_channel_2]
                    dataSleep[2, :] = bufferSleep_array[ind_channel_3]
                    dataSleep[3, :] = bufferSleep_array[ind_channel_4]

                    saved_bufferSleep_ch1.append(dataSleep[0, :])
                    saved_bufferSleep_ch2.append(dataSleep[1, :])
                    saved_bufferSleep_ch3.append(dataSleep[2, :])
                    saved_bufferSleep_ch4.append(dataSleep[3, :])

                    bufferSleep = []
                    displayNumber(secSleep, screen, 'timeSleep')
                    pg.display.update()
                    secSleep += 1
            except Empty:
                continue  # do stuff
            else:
                str(bufferSleep)
                # sys.stdout.write(char)
