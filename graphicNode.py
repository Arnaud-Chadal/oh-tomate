import pygame

class GraphicNode:

    def __init__(self, x, y, nodeVar):
        self.x = x
        self.y = y
        self.nodeVar = nodeVar
        self.collision = pygame.rect.Rect(x, y, 64, 64)
        self.image = [[
                pygame.image.load("./images/init.png").convert_alpha(), pygame.image.load("./images/initClick.png").convert_alpha()
            ], [
                pygame.image.load("./images/last.png").convert_alpha(), pygame.image.load("./images/lastClick.png").convert_alpha()
            ], [
                pygame.image.load("./images/initLast.png").convert_alpha(), pygame.image.load("./images/initLastClick.png").convert_alpha()
            ], [
                pygame.image.load("./images/bin.png").convert_alpha(), pygame.image.load("./images/binClick.png").convert_alpha()
            ], [
                pygame.image.load("./images/binLast.png").convert_alpha(), pygame.image.load("./images/binLastClick.png").convert_alpha()
            ], [
                pygame.image.load("./images/node.png").convert_alpha(), pygame.image.load("./images/nodeClick.png").convert_alpha()
            ]
        ]


    def setPos(self, x, y) :
        self.x = x-32
        self.y = y-32
        self.collision.x = x-32
        self.collision.y = y-32