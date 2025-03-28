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
        self.logoImage = pygame.image.load(
            "./images/logoProjetAutomate.png"
        ).convert_alpha()
        self.logoImage = pygame.transform.scale(self.logoImage, (876, 192))
        self.music = pygame.mixer_music.load("./src/music.mp3")
        self.toggleMusic = 1
        self.toggleSfx = 1

        self.creditList = [
            self.my_font.render(
                "Mangeur de cartes graphiques : Alexis Demont", True, (255, 255, 255)
            ),
            self.my_font.render(
                "Créateur de souvenirs : Arnaud Chadal", True, (255, 255, 255)
            ),
            self.my_font.render(
                "Rongeur anonyme : Louis-Marie Fort", True, (255, 255, 255)
            ),
            self.my_font.render(
                "The one who knocks : Mathis Desbonnet", True, (255, 255, 255)
            ),
            self.my_font.render("CEO of fun: Unix (the cat)", True, (255, 255, 255)),
            self.my_font.render(
                "Special Thanks : Arnaud Heilmann", True, (255, 255, 255)
            ),
        ]

        self.splashTextList = [
            self.my_font.render(
                "C'est en se tournant vers la lumière que l'on laisse l'ombre derrière soit - Arnaud",
                True,
                (255, 255, 255),
            ),
            self.my_font.render("Que la farce soit avec vous - Louis-Marie", True, (255, 255, 255)),
            self.my_font.render("C'est moi wesh ! - Mathis", True, (255, 255, 255)),
            self.my_font.render(
                "J'ai une toute dernière question... - Alexis", True, (255, 255, 255)
            ),
            self.my_font.render("Miaou - Unix", True, (255, 255, 255)),
            self.my_font.render(
                "De quoi de quoi de quoi ? - Arnaud Heilmann", True, (255, 255, 255)
            ),
            self.my_font.render("Avec joie - Arthur Briere", True, (255, 255, 255)),
            self.my_font.render("So ! - Danielle O'Hara ", True, (255, 255, 255)),
        ]

        self.angle = 3
        self.angleMax = 3
        self.angleSpeed = 0.01
        self.direction = 1

        self.maxZoom = 1.3
        self.minZoom = 1
        self.zoomDirection = 1
        self.zoomSpeed = 0.003
        self.zoom = 1

        self.clock = pygame.time.Clock()

        self.splashText = self.splashTextList[randint(0, len(self.splashTextList) - 1)]
        self.splashTextCopy = self.splashText

        self.toggleSfxButton = button.Button(1750, 880, 150, 80)

        self.toggleMusicButton = button.Button(1750, 980, 150, 80)

        self.createBlankButton = button.Button(710, 400, 500, 80)

        self.loadButton = button.Button(710, 500, 500, 80)

        self.loadFromCustomFileButton = button.Button(710, 600, 500, 80)

        self.quitButton = button.Button(710, 700, 500, 80)
        self.buttonList = [
            self.toggleSfxButton,
            self.toggleMusicButton,
            self.createBlankButton,
            self.loadButton,
            self.loadFromCustomFileButton,
            self.quitButton,
        ]

    def blitRotateCenter(self, image, topleft, angle):

        rotated_image = pygame.transform.rotozoom(image, angle, self.zoom)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        self.screen.blit(rotated_image, new_rect)

    def animateSplashText(self):
        self.blitRotateCenter(
            self.splashText, (960 - (self.splashText.get_width() / 2), 250), self.angle
        )

        if self.zoomDirection == 1 and self.zoom < self.maxZoom:
            self.zoom += self.zoomSpeed
        elif self.zoomDirection == 1 and self.zoom >= self.maxZoom:
            self.zoomDirection = -1
            self.zoom -= self.zoomSpeed
        elif self.zoomDirection == -1 and self.zoom > self.minZoom:
            self.zoom -= self.zoomSpeed
        elif self.zoomDirection == -1 and self.zoom <= self.minZoom:
            self.zoomDirection = 1
            self.zoom += self.zoomSpeed

        if self.direction == 1 and self.angle < self.angleMax:
            self.angle += self.angleSpeed
        elif self.direction == 1 and self.angle >= self.angleMax:
            self.direction = -1
            self.angle -= self.angleSpeed
        elif self.direction == -1 and self.angle > -self.angleMax:
            self.angle -= self.angleSpeed
        elif self.direction == -1 and self.angle <= -self.angleMax:
            self.direction = 1
            self.angle += self.angleSpeed

    def run(self):
        pygame.mixer_music.play(-1)
        while self.running:
            self.screen.fill((50, 50, 50))
            for i in range(len(self.creditList)):
                self.screen.blit(self.creditList[i], (10, 850 + i * 35))
            self.screen.blit(self.logoImage, (522, 50))

            if self.toggleSfx:
                self.toggleSfxButton.drawButton(self.screen, "Sfx On")
            else:
                self.toggleSfxButton.drawButton(self.screen, "Sfx Off")
            if self.toggleMusic:
                self.toggleMusicButton.drawButton(self.screen, "Music On")
            else:
                self.toggleMusicButton.drawButton(self.screen, "Music Off")
            self.createBlankButton.drawButton(self.screen, "Blank")
            self.loadButton.drawButton(self.screen, "Load")
            self.loadFromCustomFileButton.drawButton(
                self.screen, "Load From Custom File"
            )
            self.quitButton.drawButton(self.screen, "Quit")
            self.animateSplashText()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttonList:
                        if button.rect.collidepoint(event.pos):
                            match self.buttonList.index(button):
                                case 0:
                                    self.toggleSfx = not self.toggleSfx
                                    break
                                case 1:
                                    self.toggleMusic = not self.toggleMusic
                                    pygame.mixer_music.set_volume(self.toggleMusic)
                                    break

                                case 2:
                                    self.running = False
                                    window = graphicWindow.Main(
                                        False, self.toggleMusic, self.toggleSfx
                                    )
                                    window.createBlankAutomate()
                                    window.run()
                                    break

                                case 3:
                                    self.running = False
                                    window = graphicWindow.Main(
                                        True, self.toggleMusic, self.toggleSfx
                                    )
                                    window.importMenu()
                                    window.run()
                                    break
                                case 4:
                                    self.running = False
                                    newGraphicWindow = graphicWindow.Main(
                                        False, self.toggleMusic, self.toggleSfx
                                    )
                                    newGraphicWindow.importAutomateFromCustomFile()
                                    newGraphicWindow.run()
                                case 5:
                                    self.running = False
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()
