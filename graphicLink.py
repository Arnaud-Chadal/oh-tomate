import pygame
from math import cos, sin, atan2

class GraphicLink :

    def __init__(self, linkVar, nodeVar):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.linkVar = linkVar
        self.nodeVar = nodeVar
        self.collision = pygame.rect.Rect(nodeVar.x+32, nodeVar.y+32, 30, 5)
        self.image = pygame.image.load("./images/link.png").convert_alpha()
        self.image2 = pygame.image.load("./images/linkClick.png").convert_alpha()

# Problème : l'objet link ne connait pas la position du noeud de destination puisque la transition contient un node et pas un graphicNode ----> Solved !
#idée : utiliser le cos et sin pour faire tourner la flèche autour du noeud quand on le déplace
    def draw(self, screen) :
        pygame.draw.line(screen, (255, 255, 255), (self.nodeVar.x+32, self.nodeVar.y+32), (self.linkVar[1].x+32, self.linkVar[1].y+32), 5)
        text_surface = self.my_font.render(self.linkVar[0], False, (255, 255, 255))
        screen.blit(text_surface, (self.nodeVar.x+(self.linkVar[1].x-self.nodeVar.x)/2, self.nodeVar.y+(self.linkVar[1].y-self.nodeVar.y)/2))
        screen.blit(self.image, (self.linkVar[1].x+32-(15*4), self.linkVar[1].y+32-12))