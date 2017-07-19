# coding=utf-8
"""Constantes of ZETA Games first App"""

import pygame as pg
from pyaudio import PyAudio

# Personnalisation de la fenêtre
titre_fenetre = "ZETA GAMES"
image_icone = "images/zeta.png"
w_display = 480
h_display = 280
pg.font.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
choice = ''
# Listes des images du jeu


'''Load images, sonds libraries'''
buttonText = pg.font.Font('fonts/couture-bld.otf', 15) # font for Menu button
image_home = 'images/home.jpg'

'''Punchin Ball Game '''
punchBallImage = "images/punch3.png"
image_ring = "images/ring.png"
image_score = "images/scoretxt.png"
levels_images = ['images/level0.png', 'images/level1.png', 'images/level2.png', 'images/level3.png',
                 'images/level4.png', 'images/level5.png', 'images/level6.png']
winImg = "images/win.png"
scoreDigitImages = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
punchinballSprite = ['images/punch1.png', 'images/punch2.png', 'images/punch3.png', 'images/punch4.png',
                     'images/punch5.png', ]
scorePB = 0
level = 0
# punch_noise = pg.mixer.Sound("songs/punch.ogg")


'''Fly game'''
skyImage = 'images/beach.png' # which is a beach now
planeImage = 'images/bird.png' # which is a bird now
# skyImage = 'images/sky.png'
# planeImage = 'images/plane.jpg'
cloudImage = 'images/cloud.png'
oldPosy = 180 # initial position of the Bird
steps = 10
minDisplayY = 10 # min and max position that the bird can reach, 10px is top of the screen
maxDisplayY = 100
maxScore = 15 # score ruler is 15 max
minScore = 1
scoreF = 0

'''Resting state'''
timer = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
restingState = 'images/restingState.png'
restingStateDuration = 120 # in seconds
sec = 0

'''Navigation among the pages'''
# booleans for each window
punchinBall = 0
homeOn = 1
fly = 0
restingState = 0
questionnaire = 0

'''Tinnitus Questionnary '''
# useless for now
questionsSerie1 = 'images/questionsSerie1.png'
answers = []
questions = ['Pour quel pourcentage de votre temps éveillé \n étiez-vous conscient de vos acouphènes?','Sur une echelle de 0-10, quelle force avaient vos acouphènes ?','Vos acouphènes vous ont géné quel % de votre temps ?','À quel degré avez-vous eu le sentiment que vous pouviez contrôler vos acouphènes?','quelle facilité avez-vous eue à gérer vos acouphènes?','À quel point était-ce facile pour vous d’ignorer vos acouphènes?']
