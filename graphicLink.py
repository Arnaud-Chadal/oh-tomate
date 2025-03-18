import pygame
from math import cos, sin, atan2, acos, sqrt, pow, pi


class GraphicLink:

    def __init__(self, linkVar, nodeVar):
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.linkVar = linkVar
        self.nodeVar = nodeVar
        self.image = pygame.image.load("./images/link.png").convert_alpha()
        self.image2 = pygame.image.load("./images/linkClick.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.isClicked = False
        self.collision = self.image.get_rect()
        self.rad = 0

    # Problème : l'objet link ne connait pas la position du noeud de destination puisque la transition contient un node et pas un graphicNode ----> Solved !
    # idée : utiliser le cos et sin pour faire tourner la flèche autour du noeud quand on le déplace ----> Solved !
    def draw(self, screen, rectArrowDrawed):
        self.calculateDeltaImage()
        if self.isClicked:
            imageRotate = pygame.transform.rotate(self.image2, self.rad * 180 / pi)
        else:
            imageRotate = pygame.transform.rotate(self.image, self.rad * 180 / pi)
        
        self.collision = imageRotate.get_rect(center=self.rect.center)
        self.collision.x = (-(32 + 15) * cos(-self.rad)) + self.linkVar[1].x + 15
        self.collision.y = (-(32 + 15) * sin(-self.rad)) + self.linkVar[1].y + 15
        self.rect = imageRotate.get_rect(center=self.rect.center)
        test = 0
        while (self.collision.collidelist(rectArrowDrawed) != -1 and test < 1000):
            self.rad = self.rad + 0.01
            if self.isClicked:
                imageRotate = pygame.transform.rotate(self.image2, self.rad * 180 / pi)
            else:
                imageRotate = pygame.transform.rotate(self.image, self.rad * 180 / pi)
            
            self.collision = imageRotate.get_rect(center=self.rect.center)
            self.collision.x = (-(32 + 15) * cos(-self.rad)) + self.linkVar[1].x + 15
            self.collision.y = (-(32 + 15) * sin(-self.rad)) + self.linkVar[1].y + 15
            self.rect = imageRotate.get_rect(center=self.rect.center)
            test += 1
        #pygame.draw.rect(screen, (255, 0, 0), self.collision)
        if (self.nodeVar.nodeVar.name != self.linkVar[1].nodeVar.name):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (self.nodeVar.x + 32, self.nodeVar.y + 32),
                (self.collision.x + 15, self.collision.y + 15),
                5,
            )
            text_surface = self.my_font.render(self.linkVar[0], False, (255, 255, 255))
            screen.blit(
                text_surface,
                (
                    self.nodeVar.x + (self.collision.x - self.nodeVar.x) / 2,
                    self.nodeVar.y + (self.collision.y - self.nodeVar.y) / 2,
                ),
            )
        else:
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (self.collision.x + 15, self.collision.y + 15),
                (self.collision.x + 100 - (200*cos(self.rad)), self.collision.y + 15 + (200*sin(self.rad))),
                5,
            )
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (self.collision.x + 100 - (200*cos(self.rad)), self.collision.y + 15 + (200*sin(self.rad))),
                (self.nodeVar.x + 32, self.nodeVar.y + 32),
                5,
            )
            text_surface = self.my_font.render(self.linkVar[0], False, (255, 255, 255))
            screen.blit(
                text_surface,
                (self.collision.x + 100 - (200*cos(self.rad)), self.collision.y + 15 + (200*sin(self.rad))),
            )

        screen.blit(
            imageRotate,
            (
                (-(32 + 15) * cos(-self.rad)) + self.linkVar[1].x + 15,
                (-(32 + 15) * sin(-self.rad)) + self.linkVar[1].y + 15,
            ),
        )

    def calculateDeltaImage(self):
        if (
            (
                sqrt(
                    pow((self.linkVar[1].x - self.nodeVar.x), 2)
                    + (pow((self.linkVar[1].y - self.nodeVar.y), 2))
                )
                / 1000000
            )
            * 1000000
        ) == 0:
            return 0
        value = (
            ((self.linkVar[1].x) - (self.nodeVar.x))
            / (
                (
                    sqrt(
                        pow((self.linkVar[1].x - self.nodeVar.x), 2)
                        + (pow((self.linkVar[1].y - self.nodeVar.y), 2))
                    )
                    / 1000000
                )
                * 1000000
            )
            / 10000
        ) * 10000
        if (value >= 1 or value <= -1):
            return
        self.rad = acos(value)
        if self.nodeVar.y < self.linkVar[1].y:
            self.rad = -self.rad
