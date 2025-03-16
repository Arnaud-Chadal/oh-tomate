import pygame

class GraphicNode:

    def __init__(self, x, y, linkVar):
        self.x = x
        self.y = y
        self.nodeVar = linkVar
        self.collision = pygame.rect.Rect(x, y, 30, 30)
        self.image = pygame.image.load("./images/link.png").convert_alpha()


    def setPos(self, x, y) :
        self.x = x-15
        self.y = y-15
        self.collision.x = x-15
        self.collision.y = y-15