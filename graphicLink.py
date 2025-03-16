import pygame
from math import cos, sin, atan2

class GraphicLink :

    def __init__(self, linkVar, nodeVar):
        self.linkVar = linkVar
        self.nodeVar = nodeVar
        self.x = nodeVar.x
        self.y = nodeVar.y
        self.collision = pygame.rect.Rect(self.x, self.y, 30, 30)
        self.image = pygame.image.load("./images/link.png").convert_alpha()

# Problème : l'objet link ne connait pas la position du noeud de destination puisque la transition contient un node et pas un graphicNode
#idée : utiliser le cos et sin pour faire tourner la flèche autour du noeud quand on le déplace
    def draw(self, screen) :
        self.x = self.nodeVar.x
        self.y = self.nodeVar.y
        dx = 100-self.x
        dy = 250-self.y
        imageRotate = pygame.transform.rotate(self.image, atan2(-dy, dx))
        screen.blit(imageRotate, (self.x, self.y))