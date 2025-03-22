import pygame
import pygame.mixer_music
import button
import graphicWindow
from random import randint

class Main:
    def __init__(self) -> None:
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.logoImage = pygame.image.load("./images/logoProjetAutomate.png").convert_alpha()
        self.logoImage = pygame.transform.scale(self.logoImage, (876, 192))
        self.music = pygame.mixer_music.load("./src/music.mp3")
        self.toggleMusic = 1
        self.toggleSfx = 1

        self.creditList = [self.my_font.render("Mangeur de cartes graphiques : Alexis Demont", True, (255, 255, 255)),
        self.my_font.render("Créateur de souvenirs : Arnaud Chadal (c moi)", True, (255, 255, 255)),
        self.my_font.render("Rongeur anonyme : Louis-Marie Fort", True, (255, 255, 255)),
        self.my_font.render("The one who knocks : Mathis Desbonnet", True, (255, 255, 255)),
        self.my_font.render("CEO of fun: Unix (the cat)", True, (255, 255, 255)),
        self.my_font.render("Special Thanks : Arnaud Heilmann", True, (255, 255, 255)),]

        self.splashTextList = [self.my_font.render("C'est en se tournant vers la lumière que l'on laisse l'ombre derrière soit - Arnaud", True, (255, 255, 255)),
                               self.my_font.render("LM's Quote", True, (255, 255, 255)),
                               self.my_font.render("Baptiste's Quote", True, (255, 255, 255)),
                               self.my_font.render("Alexei's Quote", True, (255, 255, 255))]
        
        self.splashText = self.splashTextList[randint(0, len(self.splashTextList)-1)]


        self.toggleSfxButton = button.Button(
            1750, 880, 150, 80
        )

        self.toggleMusicButton = button.Button(
            1750, 980, 150, 80
        )

        self.createBlankButton = button.Button(
            710, 500, 500, 80
        )

        self.loadButton = button.Button(
            710, 600, 500, 80
        )
        self.buttonList = [self.toggleSfxButton, self.toggleMusicButton, self.createBlankButton, self.loadButton]


    def run(self) :
        pygame.mixer_music.play(-1)
        while self.running:
            self.screen.fill((50, 50, 50))
            for i in range(len(self.creditList)):
                self.screen.blit(self.creditList[i], (10, 850+i*35))
            self.screen.blit(self.logoImage, (522, 50))

            self.screen.blit(self.splashText, (525, 250))

            if self.toggleSfx :
                self.toggleSfxButton.drawButton(self.screen, "Sfx On")
            else : self.toggleSfxButton.drawButton(self.screen, "Sfx Off")
            if self.toggleMusic :
                self.toggleMusicButton.drawButton(self.screen, "Music On")
            else : self.toggleMusicButton.drawButton(self.screen, "Music Off")
            self.createBlankButton.drawButton(self.screen, "Blank")
            self.loadButton.drawButton(self.screen, "Load")
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for button in self.buttonList:
                            if button.rect.collidepoint(event.pos):
                                match self.buttonList.index(button) :
                                    case 0 :
                                        self.toggleSfx = not self.toggleSfx
                                        break
                                    case 1 :
                                        self.toggleMusic = not self.toggleMusic
                                        pygame.mixer_music.set_volume(self.toggleMusic)
                                        break

                                    case 2 :
                                        self.running = False
                                        graphicWindow.Main(False, self.toggleMusic, self.toggleSfx).run()
                                        break

                                    case 3 :
                                        self.running = False
                                        graphicWindow.Main(True, self.toggleMusic, self.toggleSfx).run()
                                        break
                                