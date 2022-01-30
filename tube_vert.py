# Projet Flappy Bird de Julian et d'Alexandre

import pygame
from random import randint


class tube_vert:

    def __init__(self, LARGEUR, HAUTEUR, screen, numero_pillier):
        self.hauteur = HAUTEUR
        self.largeur = LARGEUR
        self.position_en_x = LARGEUR + 280*numero_pillier
        self.screen = screen
        self.ouvert = randint(HAUTEUR * 0.1, HAUTEUR * 0.9)
        self.mon_dt = 0.017
        self.vitesse = -120

    def dessiner(self):
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(
            self.position_en_x, 0, 50, self.hauteur), 0)

    def déplacer(self):
        self.position_en_x += self.vitesse * self.mon_dt
        return self.position_en_x

    def ouverture(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(
            self.position_en_x, self.ouvert, 50, 100), 0)

    def detection_colision(self, mon_x, mon_y):
        if(mon_x+25 >= self.position_en_x and mon_x < self.position_en_x+50):
            if(mon_y < self.ouvert or mon_y > self.ouvert+80):

                # Son du jeu
                hit_song = pygame.mixer.Sound("sfx_hit.wav")
                hit_song.play()

                # Gameover
                police = pygame.font.SysFont("monospace", 100)
                image_texte = police.render("GAME OVER", 1, (255, 0, 0))
                self.screen.blit(image_texte, (100, 150))

                police2 = pygame.font.SysFont("monospace", 20)
                image_texte2 = police2.render(
                    "Press ESPACE to restart", 1, (255, 0, 0))
                self.screen.blit(image_texte2, (200, 250))

                return -1
            

        return 0

    def reset(self):
        if self.position_en_x < (-50):
            self.position_en_x = 770
            self.ouvert = randint(self.hauteur * 0.1, self.hauteur * 0.9)
            point_song = pygame.mixer.Sound("sfx_point.wav")
            point_song.play()
            return 1
        return 0
