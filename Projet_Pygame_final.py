# Projet Flappy Bird de Julian et d'Alexandre

import os
from math import sqrt

import pygame
from tube_vert import *

os.chdir("GitHub\Flappy-Bird-L1\Projet_Pygame_final.py")

# Ce qu'on doit faire :
# - L'oiseau tombe
# - La chute est accélérée
# - Pour contre la chute, le joueur peut cliquer
# - Détection de collision
# - Système de score
# - Chute uniformément accéléré
# - Modification de la " vitesse de chute" par l'écoute d'évènement
# - Gestion d'obstacle ( mouvement/ génération)

# Des plus:
# - Esthétique
# - Système d'écran titre
# - Evolution comportement jeu
# - Son
# - High-score
# - Hall-of-Fame

successes, failures = pygame.init()
largeur, hauteur = 720, 480

pygame.display.set_caption("Flappy Bird")  # Nom de la page de jeu
screen = pygame.display.set_mode((largeur, hauteur))  # Taille de l'écran

clock = pygame.time.Clock()
FPS = 60

mon_x, mon_y = ((largeur - 25) // 6, (hauteur - 25) // 2)  # Position
mon_dx_sur_dt, mon_dy_sur_dt = 0, 0  # Vitesse
mon_d2x_sur_dt2, mon_d2y_sur_dt2 = 0, 0  # Accélération


Vitesse = FPS
Acceleration = 240
Amortissement_max = 0.05
mon_amortissement_x, mon_amortissement_y = Amortissement_max, Amortissement_max


couleur = pygame.color.Color(255, 255, 255)

pilier = tube_vert(largeur, hauteur, screen, 0)
pilier2 = tube_vert(largeur, hauteur, screen, 1)
pilier3 = tube_vert(largeur, hauteur, screen, 2)

# Son du jeu
wing_song = pygame.mixer.Sound("sfx_wing.wav")


# ajouter l'image flappy
flappy = pygame.image.load("flappy.png").convert_alpha()
flappy = pygame.transform.smoothscale(flappy, (30, 30))  # redimensionner


def dessiner_flappy():
    screen.blit(flappy, (mon_x - flappy.get_width() //
                         4, mon_y - flappy.get_height() // 8))


hightscore = 0
score = 0
running = 0


while running >= 0:

    # physique
    mon_dt = clock.tick(FPS)/1000

    mon_dx_sur_dt += mon_d2x_sur_dt2*mon_dt - mon_amortissement_x * \
        mon_dx_sur_dt  # On calcul la vitesse par rapport à l'accélération * temps
    mon_dy_sur_dt += mon_d2y_sur_dt2*mon_dt - mon_amortissement_y*mon_dy_sur_dt

    mon_x += mon_dx_sur_dt*mon_dt  # On calcul la position à partir de la vitesse * temps
    mon_y += mon_dy_sur_dt*mon_dt

    pilier.déplacer()
    pilier2.déplacer()
    pilier3.déplacer()

    # Anti sortie d'écran
    if mon_y < 0:
        mon_y = 0
    if mon_y > hauteur - 25:
        mon_y = hauteur - 25
        mon_d2y_sur_dt2=0

    # Evolution comportement Jeu
    Acceleration = 240 + 240*(score/10)
    print(Acceleration)

    # Application Gravité
    # mon_d2y_sur_dt2 += sqrt(Acceleration/(50-score))**2 #jeu évolutif, sqrt et **2 pour avoir toujours un valeur positif même avec un score au dessus de 50
    # Problème division par 0 quand score = 50
    mon_d2y_sur_dt2 += Acceleration/(50)
    mon_amortissement_y = Amortissement_max

    # dessin
    screen.fill(couleur)

    score += int(pilier.reset())
    score += int(pilier2.reset())
    score += int(pilier3.reset())

    pilier.dessiner()
    pilier2.dessiner()
    pilier3.dessiner()

    pilier.ouverture()
    pilier2.ouverture()
    pilier3.ouverture()

    dessiner_flappy()
    running += pilier.detection_colision(mon_x, mon_y)
    running += pilier2.detection_colision(mon_x, mon_y)
    running += pilier3.detection_colision(mon_x, mon_y)

    police = pygame.font.SysFont("monospace", 20)
    score_texte = police.render(
        ("HightScore :"+str(hightscore)+" Score :"+str(score)), 1, (255, 0, 0))
    screen.blit(score_texte, (0, 0))

    pygame.display.flip()

    # traitement des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mon_dy_sur_dt -= 200
            mon_d2y_sur_dt2 = 0
            mon_y += mon_dy_sur_dt*mon_dt
            wing_song.play()

        if event.type == pygame.KEYDOWN:  # Touche enclencher
            mon_d2y_sur_dt2 = 0
            mon_amortissement_y = 0

            if event.key == pygame.K_ESCAPE:  # Touche echap
                pygame.quit()

            if event.key == pygame.K_SPACE:
                mon_dy_sur_dt -= 200
                mon_d2y_sur_dt2 = 0
                mon_y += mon_dy_sur_dt*mon_dt
                wing_song.play()

            if event.key == pygame.K_d:
                running = 1000  # God mode

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                mon_d2y_sur_dt2 = 0
                mon_amortissement_y = Amortissement_max

    while running < 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Touche echap
                    pygame.quit()

                if event.key == pygame.K_SPACE:  # Fonction Restart
                    pilier = tube_vert(largeur, hauteur, screen, 0)
                    pilier2 = tube_vert(largeur, hauteur, screen, 1)
                    pilier3 = tube_vert(largeur, hauteur, screen, 2)
                    mon_y = largeur//2
                    mon_dy_sur_dt = 0
                    mon_d2y_sur_dt2 = 0
                    running = True

                    if score > hightscore:
                        hightscore = score
                    Acceleration = 240
                    score = 0

# pygame.quit()
