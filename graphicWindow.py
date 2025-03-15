import pygame


class Main :
    def __init__(self) -> None :
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True



    def run(self) :
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
