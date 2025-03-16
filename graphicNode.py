import pygame

class GraphicNode:

    def __init__(self, x, y, nodeVar):
        self.x = x
        self.y = y
        self.nodeVar = nodeVar
        self.image = pygame.image.load("./images/circle.png").convert_alpha()
        self.collision = pygame.rect.Rect(x, y, 128, 128)

    def setPos(self, x, y) :
        self.x = x
        self.y = y
        self.collision.x = x
        self.collision.y = y