import pygame


class Button:

    def __init__(self, x, y, width, height):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)

    def drawButton(self, screen, text):
        for i in range(4):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    self.rect.x - i,
                    self.rect.y - i,
                    self.rect.width + 5,
                    self.rect.height + 5,
                ),
                1,
            )
        textToRender = self.my_font.render(text, 0, (255, 255, 255))
        rectText = textToRender.get_rect()
        screen.blit(
            textToRender,
            (
                (self.rect.width / 2) - (rectText.width / 2) + self.rect.x,
                (self.rect.height / 2) - (rectText.height / 2) + self.rect.y,
            ),
        )
