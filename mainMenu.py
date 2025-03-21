import pygame
import pygame.mixer_music
import button
import graphicWindow

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

        self.creditList = [self.my_font.render("Automaton player : Alexis Demont", True, (255, 255, 255)),
        self.my_font.render("Créateur de souvenirs : Arnaud Chadal", True, (255, 255, 255)),
        self.my_font.render("Directeur financier : Louis-Marie Fort", True, (255, 255, 255)),
        self.my_font.render("The one who knocks : Mathis Desbonnet", True, (255, 255, 255)),
        self.my_font.render("CEO of fun: Unix (the cat)", True, (255, 255, 255)),
        self.my_font.render("Special Thanks : Arnaud Heilmann", True, (255, 255, 255)),]

        self.toggleSfxButton = button.Button(
            1700, 800 - 30, 200, 80
        )

        self.toggleMusicButton = button.Button(
            1700, 900 - 30, 200, 80
        )

        self.createBlankButton = button.Button(
            850, 500, 200, 80
        )

        self.loadButton = button.Button(
            850, 600, 200, 80
        )
        self.buttonList = [self.toggleSfxButton, self.toggleMusicButton, self.createBlankButton, self.loadButton]


    def run(self) :
        pygame.mixer_music.play(-1)
        while self.running:
            self.screen.fill((50, 50, 50))
            for i in range(len(self.creditList)):
                self.screen.blit(self.creditList[i], (10, 850+i*30))
            self.screen.blit(self.logoImage, (522, 150))
            self.toggleSfxButton.drawButton(self.screen, "Sfx")
            self.toggleMusicButton.drawButton(self.screen, "Music")
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

                                        break

                                    case 3 :
                                        self.running = False
                                        graphicWindow.Main(True, self.toggleMusic).run()
                                        break
                                