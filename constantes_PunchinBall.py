# coding=utf-8
"""Constantes du jeu de Labyrinthe Donkey Kong"""

import pygame as pg
from pyaudio import PyAudio

# Paramètres de la fenêtre
nombre_sprite_cote = 15
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite

# Personnalisation de la fenêtre
titre_fenetre = "ZETA GAMES"
image_icone = "images/dk_droite.png"
w_display = 480
h_display = 280
pg.font.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
# Listes des images du jeu
image_accueil = "images/accueil.png"
image_fond = "images/fond.jpg"
image_mur = "images/mur.png"
image_depart = "images/depart.png"
image_arrivee = "images/arrivee.png"

'''Load images, sonds libraries'''
image_home = 'images/home.jpg'
punchBallImage = "images/punch3.png"
image_ring = "images/ring.jpg"
image_score = "images/scoretxt.png"
levels_images = ['images/level0.png', 'images/level1.png', 'images/level2.png', 'images/level3.png',
                 'images/level4.png', 'images/level5.png', 'images/level6.png']
winImg = "images/win.png"
scoreDigitImages = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
punchinballSprite = ['images/punch1.png', 'images/punch2.png', 'images/punch3.png', 'images/punch4.png',
                     'images/punch5.png', ]
# punch_noise = pg.mixer.Sound("songs/punch.ogg")

level = 0
score = 0

'''Fly game'''
skyImage = 'images/sky.png'
planeImage = 'images/plane.jpg'
cloudImage = 'images/cloud.png'
oldPosy = 200
steps = 10

'''resting state'''
timer = ['images/0.png', 'images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png',
                    'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
restingState = 'images/restingStateImage.png'
sec = 0


'''Tinnitus Questionnary '''
questionsSerie1 = 'images/questionsSerie1.png'
answers = []
questions = ['Pour quel pourcentage de votre temps éveillé \n étiez-vous conscient de vos acouphènes?','Sur une echelle de 0-10, quelle force avaient vos acouphènes ?','Vos acouphènes vous ont géné quel % de votre temps ?','À quel degré avez-vous eu le sentiment que vous pouviez contrôler vos acouphènes?','quelle facilité avez-vous eue à gérer vos acouphènes?','À quel point était-ce facile pour vous d’ignorer vos acouphènes?']
