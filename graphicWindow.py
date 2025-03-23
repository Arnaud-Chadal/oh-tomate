import pygame
import graphicNode
import graphicLink
import node
import button
import automate
from math import pi, cos, sin
import time
import gc
import pygame.mixer_music
import random


class Main:
    def __init__(self, importMenu, musicOn, sfxOn) -> None:
        pygame.font.init()
        pygame.mixer.init()
        self.music = pygame.mixer_music.load("./src/music.mp3")
        pygame.mixer_music.set_volume(0.7)
        self.shii = pygame.mixer.Sound("./src/shii.mp3")
        self.wouu = pygame.mixer.Sound("./src/wouu.mp3")
        self.sarkozyChatSound = pygame.mixer.Sound("./src/sarkozychat.mp3")
        self.sarkozyChatSound.set_volume(10)
        self.standardisationSound = pygame.mixer.Sound("./src/standardisation.mp3")
        self.determinisationSound = pygame.mixer.Sound("./src/determinisation.mp3")
        self.complementationSoud = pygame.mixer.Sound("./src/complementation.mp3")
        self.minimisationSoud = pygame.mixer.Sound("./src/minimisation.mp3")
        self.completionSound = pygame.mixer.Sound("./src/completion.mp3")
        self.importExportSound = pygame.mixer.Sound("./src/importExport.mp3")
        self.checkWordSound = pygame.mixer.Sound("./src/checkWord.mp3")
        self.clocSound = []
        for i in range(9):
            self.clocSound.append(
                pygame.mixer.Sound("./src/cloc" + str(i + 1) + ".mp3")
            )
        self.musicOn = musicOn
        self.sfxOn = sfxOn

        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.playingSound = False
        self.screen = pygame.display.set_mode((1920, 1080))
        self.image = pygame.image.load("./images/verySeriousImage.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (756, 1008))
        self.running = True
        self.createBlankAutomate(3)
        self.alphabet = self.automate.alphabet
        self.nodeAddressToGraphicNodeAddress = {}
        self.graphicNodeToNodeAddress = {}
        self.nodeList = []
        self.linkList = []
        self.clicked = None
        self.grabbed = None
        self.dragLink = None
        self.openImportMenu = importMenu
        self.menuX = 0
        self.menuY = 1080
        self.importMenuX = 0
        self.importMenuY = 6
        self.transitionMenuX = 1920
        self.transitionMenuY = 0
        self.determineButton = button.Button(
            self.menuX + 70, self.menuY + 100 - 30, 200, 80
        )
        self.minimButton = button.Button(
            self.menuX + 320, self.menuY + 100 - 30, 200, 80
        )
        self.standaButton = button.Button(
            self.menuX + 570, self.menuY + 100 - 30, 200, 80
        )
        self.completeButton = button.Button(
            self.menuX + 820, self.menuY + 100 - 30, 200, 80
        )
        self.complementButton = button.Button(
            self.menuX + 1070, self.menuY + 100 - 30, 200, 80
        )
        self.importExportButton = button.Button(
            self.menuX + 1375, self.menuY + 100 - 30, 220, 80
        )
        self.checkWordButton = button.Button(
            self.menuX + 1645, self.menuY + 100 - 30, 200, 80
        )
        self.buttonImportTab = []
        for buttonNumber in range(44):
            self.buttonImportTab.append(button.Button(660, 20, 600, 100))
        self.buttonUp = button.Button(660, 20, 600, 100)
        self.buttonDown = button.Button(660, 960, 600, 100)
        self.buttonClose = button.Button(20, 20, 100, 100)
        self.buttonNewBlank = button.Button(1650, 20, 250, 100)
        self.exportButton = button.Button(1650, 960, 250, 100)
        self.clock = pygame.time.Clock()
        self.countDownSelectLetter = 0
        self.countDownSelectState = 0
        self.xMousePos, self.yMousePos = pygame.mouse.get_pos()
        nbr = 0
        for graphNode in self.automate.nodeList:
            graphicNo = graphicNode.GraphicNode(nbr * 200, 50 * nbr, graphNode)
            self.nodeList.append(graphicNo)
            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
            self.graphicNodeToNodeAddress[graphicNo] = graphNode
            nbr += 1
        nbr = 0
        for graphNode in self.automate.nodeList:
            self.linkList.append([])
            for link in graphNode.linkList:
                self.linkList[nbr].append(
                    graphicLink.GraphicLink(
                        [link[0], self.nodeAddressToGraphicNodeAddress[link[1]]],
                        self.nodeList[nbr],
                    )
                )
            nbr += 1

    def drawTransitionMenu(self):
        my_font = pygame.font.SysFont("Comic Sans MS", 15)
        barMenuRect = pygame.rect.Rect(
            self.transitionMenuX - 5, self.transitionMenuY + 20, 10, 700
        )
        menuRect = pygame.rect.Rect(
            self.transitionMenuX, self.transitionMenuY + 20, 650, 700
        )
        if barMenuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ) or menuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ):
            if self.transitionMenuX > 1320:
                self.transitionMenuX -= 40
                if not self.playingSound and self.sfxOn:
                    self.shii.play()
                    self.playingSound = True
        else:
            if self.transitionMenuX < 1920:
                self.transitionMenuX += 40
                if not self.playingSound and self.sfxOn:
                    self.wouu.play()
                    self.playingSound = True
        if (
            barMenuRect.collidepoint(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
            or menuRect.collidepoint(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
            and (self.transitionMenuX == 1320 or self.transitionMenuX == 1920)
        ):
            self.playingSound = False
        pygame.draw.rect(self.screen, (0, 0, 0), menuRect)
        pygame.draw.rect(self.screen, (0, 0, 255), barMenuRect)
        # self.screen.blit(
        #     self.my_font.render("Menu", False, (255, 255, 255)),
        #     (self.menuX + 30, self.menuY + 30),
        # )
        string = self.automate.printTransitionTables()
        for groupsNumber in range(len(string)):
            for lineNumber in range(len(string[groupsNumber])):
                textToRender = my_font.render(
                    string[groupsNumber][lineNumber], 0, (255, 255, 255)
                )
                self.screen.blit(
                    textToRender,
                    (
                        self.transitionMenuX + 30,
                        self.transitionMenuY
                        + 20
                        + lineNumber * 30
                        + sum([len(group) for group in string[:groupsNumber]]) * 30,
                    ),
                )

    def drawMenu(self):
        barMenuRect = pygame.rect.Rect(self.menuX, self.menuY - 10, 1920, 10)
        menuRect = pygame.rect.Rect(self.menuX, self.menuY, 1920, 500)
        verySeriousRect = pygame.rect.Rect(self.menuX + 1910, self.menuY + 190, 10, 10)
        if verySeriousRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ):
            self.screen.blit(self.image, (300, 0))
            if not pygame.mixer.Channel(0).get_busy() and self.sfxOn :
                pygame.mixer.Channel(0).play(self.sarkozyChatSound)
        else:
            self.sarkozyChatSound.stop()
        if barMenuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ) or menuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ):
            if self.menuY > 880:
                self.menuY -= 40
                if not self.playingSound and self.sfxOn:
                    self.shii.play()
                    self.playingSound = True
        else:
            if self.menuY < 1080:
                self.menuY += 40
                if not self.playingSound and self.sfxOn:
                    self.wouu.play()
                    self.playingSound = True
        if (
            barMenuRect.collidepoint(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
            or menuRect.collidepoint(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
            and (self.menuY == 880 or self.menuY == 1080)
        ):
            self.playingSound = False
        pygame.draw.rect(self.screen, (0, 0, 0), menuRect)
        pygame.draw.rect(self.screen, (255, 0, 0), barMenuRect)
        # self.screen.blit(
        #     self.my_font.render("Menu", False, (255, 255, 255)),
        #     (self.menuX + 30, self.menuY + 30),
        # )
        self.standaButton = button.Button(
            self.menuX + 70, self.menuY + 100 - 30, 200, 80
        )
        self.determineButton = button.Button(
            self.menuX + 320, self.menuY + 100 - 30, 200, 80
        )
        self.completeButton = button.Button(
            self.menuX + 570, self.menuY + 100 - 30, 200, 80
        )
        self.minimButton = button.Button(
            self.menuX + 820, self.menuY + 100 - 30, 200, 80
        )
        self.complementButton = button.Button(
            self.menuX + 1070, self.menuY + 100 - 30, 200, 80
        )
        self.importExportButton = button.Button(
            self.menuX + 1375, self.menuY + 100 - 30, 220, 80
        )
        self.checkWordButton = button.Button(
            self.menuX + 1645, self.menuY + 100 - 30, 200, 80
        )
        self.standaButton.drawButton(self.screen, "Standardize")
        self.determineButton.drawButton(self.screen, "Determinize")
        self.completeButton.drawButton(self.screen, "Complete")
        self.minimButton.drawButton(self.screen, "Minimize")
        self.complementButton.drawButton(self.screen, "Complement")
        pygame.draw.rect(
            self.screen, (160, 160, 160), (self.menuX + 1320, self.menuY + 10, 5, 180)
        )
        self.importExportButton.drawButton(self.screen, "Import/Export")
        self.checkWordButton.drawButton(self.screen, "Check Word")

    def importAutomate(self, fileNumber):
        file = open("./automates/automateTest" + str(fileNumber) + ".txt", "r")
        fullAlphabet = "abcdefghijklmnopqrstuvwxyz"

        fileLines = []
        isAsynchronous = False
        for line in file:
            fileLines.append(line.rstrip())
            if (not isAsynchronous) and "&" in line:
                isAsynchronous = True

        alphabet = [fullAlphabet[i] for i in range(int(fileLines[0]))]
        allautos = [[], [], [], [], []]

        # EXTRACTION DES AUTOS DEPUIS LE FICHIER TXT
        counter = 0
        index = -1
        for line in fileLines[1:]:
            if counter == 0:
                index += 1
                counter = int(line)
            else:
                allautos[index].append(line)
                counter -= 1

        automateNameToObject = {}

        # SPLIT DES AUTOS
        for groupOfautos in allautos:
            for autoNumber in range(len(groupOfautos)):
                groupOfautos[autoNumber] = groupOfautos[autoNumber].split(";")
                if len(groupOfautos[autoNumber]) == 1:
                    groupOfautos[autoNumber].append([])
                elif len(groupOfautos[autoNumber]) == 2:
                    groupOfautos[autoNumber][1] = groupOfautos[autoNumber][1].split(",")
                    numberOfTransitions = len(groupOfautos[autoNumber][1])
                    for transitionNumber in range(numberOfTransitions):
                        groupOfautos[autoNumber][1][transitionNumber] = groupOfautos[
                            autoNumber
                        ][1][transitionNumber].split("/")

        nodeTab = []
        for groupNumber in range(len(allautos)):
            for auto in allautos[groupNumber]:
                isAlreadyHere = False
                newNode = node.Node(auto[0], False, False)
                if groupNumber == 0:
                    newNode.isInit = True
                    nodeTab.append(newNode)
                if groupNumber == 1:
                    newNode.isLast = True
                    nodeTab.append(newNode)
                if groupNumber == 2:
                    newNode.isInit = newNode.isLast = True
                    nodeTab.append(newNode)
                if groupNumber == 3:
                    for n in nodeTab:
                        if auto[0] == n.getName():
                            isAlreadyHere = True
                            n.setBin(True)
                    if isAlreadyHere == False:
                        nodeTab.append(newNode)
                if groupNumber == 4:
                    nodeTab.append(newNode)
                if not isAlreadyHere:
                    automateNameToObject[auto[0]] = newNode

        for group in allautos:
            for auto in group:
                currentNode = automateNameToObject[auto[0]]
                for link in auto[1]:
                    currentNode.addLinkToLinkList(
                        [link[0], automateNameToObject[link[1]]]
                    )

        self.automate = automate.Automate(alphabet, nodeTab, isAsynchronous)
        self.alphabet = self.automate.alphabet
        self.nodeAddressToGraphicNodeAddress = {}
        self.graphicNodeToNodeAddress = {}
        self.nodeList = []
        self.linkList = []
        nbr = 0
        for graphNode in self.automate.nodeList:
            graphicNo = graphicNode.GraphicNode(nbr * 200, 50 * nbr, graphNode)
            self.nodeList.append(graphicNo)
            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
            self.graphicNodeToNodeAddress[graphicNo] = graphNode
            nbr += 1
        nbr = 0
        for graphNode in self.automate.nodeList:
            self.linkList.append([])
            for link in graphNode.linkList:
                self.linkList[nbr].append(
                    graphicLink.GraphicLink(
                        [link[0], self.nodeAddressToGraphicNodeAddress[link[1]]],
                        self.nodeList[nbr],
                    )
                )
            nbr += 1

    def createBlankAutomate(self, numberOfLetter):
        alphabet = ["a", "b", "c"]

        nodeTab = []

        self.automate = automate.Automate(alphabet, nodeTab, False)
        self.alphabet = self.automate.alphabet
        self.nodeAddressToGraphicNodeAddress = {}
        self.graphicNodeToNodeAddress = {}
        self.nodeList = []
        self.linkList = []

    def importMenu(self):
        self.screen.fill((50, 50, 50))
        self.buttonUp.drawButton(self.screen, "Up")
        self.buttonDown.drawButton(self.screen, "Down")
        self.buttonClose.drawButton(self.screen, "Close")
        self.buttonNewBlank.drawButton(self.screen, "Create blank")
        if len(self.automate.nodeList) > 0:
            self.exportButton.drawButton(self.screen, "Export")

        space = 0
        for b in self.buttonImportTab[self.importMenuX : self.importMenuY]:
            b.rect.y = 180 + space * 120
            b.drawButton(self.screen, "Automate " + str(self.importMenuX + space + 1))
            space += 1

    def checkWord(self):
        self.screen.fill((50, 50, 50))
        bigFont = pygame.font.SysFont("Comic Sans MS", 120)
        bigTextWaitingFullScreen = bigFont.render(
            "Waiting for input...", 0, (255, 255, 255)
        )
        bigTextPleaseAnswerConsoleFullScreen = bigFont.render(
            "Write a word in the terminal", 0, (255, 255, 255)
        )
        bigTextPleaseAnswerConsoleFullScreenNext = bigFont.render(
            "then press enter !", 0, (255, 255, 255)
        )
        self.screen.blit(
            bigTextWaitingFullScreen, (0, 0), bigTextWaitingFullScreen.get_rect()
        )
        self.screen.blit(
            bigTextPleaseAnswerConsoleFullScreen,
            (0, bigTextWaitingFullScreen.get_rect().height + 50),
            bigTextPleaseAnswerConsoleFullScreen.get_rect(),
        )
        self.screen.blit(
            bigTextPleaseAnswerConsoleFullScreenNext,
            (
                0,
                bigTextPleaseAnswerConsoleFullScreen.get_rect().height
                + 20
                + bigTextWaitingFullScreen.get_rect().height,
            ),
            bigTextPleaseAnswerConsoleFullScreenNext.get_rect(),
        )
        pygame.display.flip()
        textInput = input("Saisir le texte : ")
        if self.automate.recognize(textInput):
            self.screen.fill((50, 50, 50))
            bigFont = pygame.font.SysFont("Comic Sans MS", 120)
            bigTextWaitingFullScreen = bigFont.render(
                "The word " + textInput, 0, (255, 255, 255)
            )
            bigTextPleaseAnswerConsoleFullScreen = bigFont.render(
                "IS recognized !!! Congrats", 0, (255, 255, 255)
            )
            bigTextPleaseAnswerConsoleFullScreenNext = bigFont.render(
                "Continue in the terminal", 0, (255, 255, 255)
            )
            self.screen.blit(
                bigTextWaitingFullScreen, (0, 0), bigTextWaitingFullScreen.get_rect()
            )
            self.screen.blit(
                bigTextPleaseAnswerConsoleFullScreen,
                (0, bigTextWaitingFullScreen.get_rect().height + 50),
                bigTextPleaseAnswerConsoleFullScreen.get_rect(),
            )
            self.screen.blit(
                bigTextPleaseAnswerConsoleFullScreenNext,
                (
                    0,
                    bigTextPleaseAnswerConsoleFullScreen.get_rect().height
                    + 20
                    + bigTextWaitingFullScreen.get_rect().height,
                ),
                bigTextPleaseAnswerConsoleFullScreenNext.get_rect(),
            )
            pygame.display.flip()
            input("Press enter to continue")
        else:
            self.screen.fill((50, 50, 50))
            bigFont = pygame.font.SysFont("Comic Sans MS", 120)
            bigTextWaitingFullScreen = bigFont.render(
                "The word " + textInput, 0, (255, 255, 255)
            )
            bigTextPleaseAnswerConsoleFullScreen = bigFont.render(
                "is NOT recognized....", 0, (255, 255, 255)
            )
            bigTextPleaseAnswerConsoleFullScreenNext = bigFont.render(
                "Continue in the terminal", 0, (255, 255, 255)
            )
            self.screen.blit(
                bigTextWaitingFullScreen, (0, 0), bigTextWaitingFullScreen.get_rect()
            )
            self.screen.blit(
                bigTextPleaseAnswerConsoleFullScreen,
                (0, bigTextWaitingFullScreen.get_rect().height + 50),
                bigTextPleaseAnswerConsoleFullScreen.get_rect(),
            )
            self.screen.blit(
                bigTextPleaseAnswerConsoleFullScreenNext,
                (
                    0,
                    bigTextPleaseAnswerConsoleFullScreen.get_rect().height
                    + 20
                    + bigTextWaitingFullScreen.get_rect().height,
                ),
                bigTextPleaseAnswerConsoleFullScreenNext.get_rect(),
            )
            pygame.display.flip()
            input("Press enter to continue")

    def run(self):
        pygame.mixer_music.play(-1)
        while self.running:
            pygame.mixer_music.set_volume(0.7*self.musicOn)
            self.screen.fill((50, 50, 50))
            # Check des events

            if self.openImportMenu == 0:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for graphNode in self.nodeList:
                            if graphNode.collision.collidepoint(event.pos):
                                self.grabbed = graphNode
                                self.clicked = graphNode
                                if self.sfxOn :
                                    self.clocSound[random.randint(0, 8)].play()
                        for groups in self.linkList:
                            for link in groups:
                                link.isClicked = False
                                if (
                                    link.collision.collidepoint(event.pos)
                                    and self.grabbed == None
                                ):
                                    counterSelectLetter = self.alphabet.index(
                                        link.linkVar[0]
                                    )
                                    link.isClicked = True
                                    self.clicked = link
                                    self.grabbed = link
                        if self.determineButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.determinisationSound.stop()
                                self.determinisationSound.play()
                            self.automate.toDetermine()
                            self.nodeAddressToGraphicNodeAddress = {}
                            self.graphicNodeToNodeAddress = {}
                            self.nodeList = []
                            self.linkList = []
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                graphicNo = graphicNode.GraphicNode(
                                    nbr * 200, 50 * nbr, graphNode
                                )
                                self.nodeList.append(graphicNo)
                                self.nodeAddressToGraphicNodeAddress[graphNode] = (
                                    graphicNo
                                )
                                self.graphicNodeToNodeAddress[graphicNo] = graphNode
                                nbr += 1
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                self.linkList.append([])
                                for link in graphNode.linkList:
                                    self.linkList[nbr].append(
                                        graphicLink.GraphicLink(
                                            [
                                                link[0],
                                                self.nodeAddressToGraphicNodeAddress[
                                                    link[1]
                                                ],
                                            ],
                                            self.nodeList[nbr],
                                        )
                                    )
                                nbr += 1
                        elif self.minimButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.minimisationSoud.stop()
                                self.minimisationSoud.play()
                            self.automate.toMinimize()
                            self.nodeAddressToGraphicNodeAddress = {}
                            self.graphicNodeToNodeAddress = {}
                            self.nodeList = []
                            self.linkList = []
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                graphicNo = graphicNode.GraphicNode(
                                    nbr * 200, 50 * nbr, graphNode
                                )
                                self.nodeList.append(graphicNo)
                                self.nodeAddressToGraphicNodeAddress[graphNode] = (
                                    graphicNo
                                )
                                self.graphicNodeToNodeAddress[graphicNo] = graphNode
                                nbr += 1
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                self.linkList.append([])
                                for link in graphNode.linkList:
                                    self.linkList[nbr].append(
                                        graphicLink.GraphicLink(
                                            [
                                                link[0],
                                                self.nodeAddressToGraphicNodeAddress[
                                                    link[1]
                                                ],
                                            ],
                                            self.nodeList[nbr],
                                        )
                                    )
                                nbr += 1
                            self.automate.printTransitionTables()
                        elif self.standaButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.standardisationSound.stop()
                                self.standardisationSound.play()
                            self.automate.toStandardize()
                            self.nodeAddressToGraphicNodeAddress = {}
                            self.graphicNodeToNodeAddress = {}
                            self.nodeList = []
                            self.linkList = []
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                graphicNo = graphicNode.GraphicNode(
                                    nbr * 200, 50 * nbr, graphNode
                                )
                                self.nodeList.append(graphicNo)
                                self.nodeAddressToGraphicNodeAddress[graphNode] = (
                                    graphicNo
                                )
                                self.graphicNodeToNodeAddress[graphicNo] = graphNode
                                nbr += 1
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                self.linkList.append([])
                                for link in graphNode.linkList:
                                    self.linkList[nbr].append(
                                        graphicLink.GraphicLink(
                                            [
                                                link[0],
                                                self.nodeAddressToGraphicNodeAddress[
                                                    link[1]
                                                ],
                                            ],
                                            self.nodeList[nbr],
                                        )
                                    )
                                nbr += 1
                        elif self.completeButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.completionSound.stop()
                                self.completionSound.play()
                            self.automate.toComplete()
                            self.nodeAddressToGraphicNodeAddress = {}
                            self.graphicNodeToNodeAddress = {}
                            self.nodeList = []
                            self.linkList = []
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                graphicNo = graphicNode.GraphicNode(
                                    nbr * 200, 50 * nbr, graphNode
                                )
                                self.nodeList.append(graphicNo)
                                self.nodeAddressToGraphicNodeAddress[graphNode] = (
                                    graphicNo
                                )
                                self.graphicNodeToNodeAddress[graphicNo] = graphNode
                                nbr += 1
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                self.linkList.append([])
                                for link in graphNode.linkList:
                                    self.linkList[nbr].append(
                                        graphicLink.GraphicLink(
                                            [
                                                link[0],
                                                self.nodeAddressToGraphicNodeAddress[
                                                    link[1]
                                                ],
                                            ],
                                            self.nodeList[nbr],
                                        )
                                    )
                                nbr += 1
                        elif self.complementButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.complementationSoud.stop()
                                self.complementationSoud.play()
                            self.automate.toComplement()
                            self.nodeAddressToGraphicNodeAddress = {}
                            self.graphicNodeToNodeAddress = {}
                            self.nodeList = []
                            self.linkList = []
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                graphicNo = graphicNode.GraphicNode(
                                    nbr * 200, 50 * nbr, graphNode
                                )
                                self.nodeList.append(graphicNo)
                                self.nodeAddressToGraphicNodeAddress[graphNode] = (
                                    graphicNo
                                )
                                self.graphicNodeToNodeAddress[graphicNo] = graphNode
                                nbr += 1
                            nbr = 0
                            for graphNode in self.automate.nodeList:
                                self.linkList.append([])
                                for link in graphNode.linkList:
                                    self.linkList[nbr].append(
                                        graphicLink.GraphicLink(
                                            [
                                                link[0],
                                                self.nodeAddressToGraphicNodeAddress[
                                                    link[1]
                                                ],
                                            ],
                                            self.nodeList[nbr],
                                        )
                                    )
                                nbr += 1
                        elif self.importExportButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.importExportSound.stop()
                                self.importExportSound.play()
                            self.openImportMenu = True
                        elif self.checkWordButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            if self.sfxOn :
                                self.checkWordSound.stop()
                                self.checkWordSound.play()
                            self.checkWord()
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.clicked = self.grabbed
                        self.grabbed = None
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        for graphNode in self.nodeList:
                            if graphNode.collision.collidepoint(event.pos):
                                self.dragLink = graphNode
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        if self.dragLink == None:
                            nextName = "0"
                            biggestNumber = -1
                            for n in self.automate.nodeList:
                                if biggestNumber < int(n.name):
                                    biggestNumber = int(n.name)
                            if biggestNumber != -1:
                                nextName = str(biggestNumber + 1)
                            newNode = node.Node(nextName, False, False)
                            self.automate.nodeList.append(newNode)
                            newGraphicNode = graphicNode.GraphicNode(
                                pygame.mouse.get_pos()[0],
                                pygame.mouse.get_pos()[1],
                                newNode,
                            )
                            self.nodeList.append(newGraphicNode)
                            self.nodeAddressToGraphicNodeAddress[newNode] = (
                                newGraphicNode
                            )
                            self.graphicNodeToNodeAddress[newGraphicNode] = newNode
                            print(self.automate)
                        else:
                            collideNode = None
                            for graphNode in self.nodeList:
                                if graphNode.collision.collidepoint(event.pos):
                                    collideNode = graphNode
                            if collideNode != None:
                                groupIndex = None
                                for groupsNumber in range(len(self.linkList)):
                                    for link in self.linkList[groupsNumber]:
                                        if self.dragLink == link.nodeVar:
                                            groupIndex = groupsNumber
                                if groupIndex != None:
                                    self.linkList[groupIndex].append(
                                        graphicLink.GraphicLink(
                                            ["a", collideNode], self.dragLink
                                        )
                                    )
                                    self.dragLink.nodeVar.linkList.append(
                                        ["a", collideNode.nodeVar]
                                    )
                                    for link in self.linkList[groupIndex]:
                                        print(link.linkVar)
                                elif groupIndex == None:
                                    self.linkList.append([])
                                    self.linkList[-1].append(
                                        graphicLink.GraphicLink(
                                            ["a", collideNode], self.dragLink
                                        )
                                    )
                                    self.dragLink.nodeVar.linkList.append(
                                        ["a", collideNode.nodeVar]
                                    )
                                    print(self.linkList[-1])
                                    for link in self.linkList[-1]:
                                        print(link.linkVar)
                            self.dragLink = None

                rectArrowDrawed = []
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RIGHT] and self.clicked == None:
                    for graphNode in self.nodeList:
                        graphNode.x -= 10
                        graphNode.collision.x += 10
                if keys[pygame.K_LEFT] and self.clicked == None:
                    for graphNode in self.nodeList:
                        graphNode.x += 10
                        graphNode.collision.x -= 10
                if keys[pygame.K_DOWN] and self.clicked == None:
                    for graphNode in self.nodeList:
                        graphNode.y -= 10
                        graphNode.collision.y += 10
                if keys[pygame.K_UP] and self.clicked == None:
                    for graphNode in self.nodeList:
                        graphNode.y += 10
                        graphNode.collision.y -= 10

                if self.countDownSelectLetter > 0:
                    self.countDownSelectLetter -= 1
                if self.countDownSelectState > 0:
                    self.countDownSelectState -= 1

                if self.dragLink != None:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (self.dragLink.x + 32, self.dragLink.y + 32),
                        (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                        5,
                    )

                for linkGroup in self.linkList:
                    for links in linkGroup:
                        links.draw(self.screen, rectArrowDrawed)
                        rectArrowDrawed.append(links.collision)
                        if keys[pygame.K_DELETE] and self.clicked == links:
                            linkGroup.remove(links)
                            gc.collect()
                            realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                            linkToDelete = links.linkVar
                            linkToDelete[1] = self.graphicNodeToNodeAddress[
                                linkToDelete[1]
                            ]
                            realNode.linkList.remove(links.linkVar)
                            gc.collect()
                        if (
                            keys[pygame.K_UP]
                            and self.clicked == links
                            and self.countDownSelectLetter == 0
                        ):
                            self.countDownSelectLetter = int(self.clock.get_time())
                            lettersAvailable = self.alphabet.copy()
                            if lettersAvailable != []:
                                counterSelectLetter += 1
                                realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                                linkToModifyLetter = links.linkVar.copy()
                                linkToModifyLetter[1] = self.graphicNodeToNodeAddress[
                                    linkToModifyLetter[1]
                                ]
                                realNode.linkList[
                                    realNode.linkList.index(linkToModifyLetter)
                                ][0] = lettersAvailable[
                                    counterSelectLetter % len(lettersAvailable)
                                ]
                                links.linkVar[0] = lettersAvailable[
                                    counterSelectLetter % len(lettersAvailable)
                                ]
                            else:
                                print("All letters already used !")
                        if (
                            keys[pygame.K_DOWN]
                            and self.clicked == links
                            and self.countDownSelectLetter == 0
                        ):
                            self.countDownSelectLetter = int(self.clock.get_time())
                            lettersAvailable = self.alphabet.copy()
                            if lettersAvailable != []:
                                counterSelectLetter -= 1
                                realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                                linkToModifyLetter = links.linkVar.copy()
                                linkToModifyLetter[1] = self.graphicNodeToNodeAddress[
                                    linkToModifyLetter[1]
                                ]
                                realNode.linkList[
                                    realNode.linkList.index(linkToModifyLetter)
                                ][0] = lettersAvailable[
                                    counterSelectLetter % len(lettersAvailable)
                                ]
                                links.linkVar[0] = lettersAvailable[
                                    counterSelectLetter % len(lettersAvailable)
                                ]
                            else:
                                print("All letters already used !")

                # Affichage des noeuds
                for graphNode in self.nodeList:
                    if self.grabbed == graphNode:
                        graphNode.setPos(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        )
                    if self.clicked == graphNode:
                        if bool(graphNode.nodeVar.isInit) and not bool(
                            graphNode.nodeVar.isLast
                        ):
                            self.screen.blit(
                                graphNode.image[0][1], (graphNode.x, graphNode.y)
                            )
                        elif (
                            not bool(graphNode.nodeVar.isInit)
                            and bool(graphNode.nodeVar.isLast)
                            and not bool(graphNode.nodeVar.bin)
                        ):
                            self.screen.blit(
                                graphNode.image[1][1], (graphNode.x, graphNode.y)
                            )
                        elif (
                            bool(graphNode.nodeVar.isInit)
                            and bool(graphNode.nodeVar.isLast)
                            and not bool(graphNode.nodeVar.bin)
                        ):
                            self.screen.blit(
                                graphNode.image[2][1], (graphNode.x, graphNode.y)
                            )
                        elif bool(graphNode.nodeVar.bin) and not bool(
                            graphNode.nodeVar.isLast
                        ):
                            self.screen.blit(
                                graphNode.image[3][1], (graphNode.x, graphNode.y)
                            )
                        elif bool(graphNode.nodeVar.bin) and bool(
                            graphNode.nodeVar.isLast
                        ):
                            self.screen.blit(
                                graphNode.image[4][1], (graphNode.x, graphNode.y)
                            )
                        else:
                            self.screen.blit(
                                graphNode.image[5][1], (graphNode.x, graphNode.y)
                            )
                    else:
                        if graphNode.nodeVar.isInit and not graphNode.nodeVar.isLast:
                            self.screen.blit(
                                graphNode.image[0][0], (graphNode.x, graphNode.y)
                            )
                        elif (
                            not graphNode.nodeVar.isInit
                            and graphNode.nodeVar.isLast
                            and not graphNode.nodeVar.bin
                        ):
                            self.screen.blit(
                                graphNode.image[1][0], (graphNode.x, graphNode.y)
                            )
                        elif (
                            graphNode.nodeVar.isInit
                            and graphNode.nodeVar.isLast
                            and not graphNode.nodeVar.bin
                        ):
                            self.screen.blit(
                                graphNode.image[2][0], (graphNode.x, graphNode.y)
                            )
                        elif graphNode.nodeVar.bin and not graphNode.nodeVar.isLast:
                            self.screen.blit(
                                graphNode.image[3][0], (graphNode.x, graphNode.y)
                            )
                        elif graphNode.nodeVar.bin and graphNode.nodeVar.isLast:
                            self.screen.blit(
                                graphNode.image[4][0], (graphNode.x, graphNode.y)
                            )
                        else:
                            self.screen.blit(
                                graphNode.image[5][0], (graphNode.x, graphNode.y)
                            )
                    text_surface = self.my_font.render(
                        graphNode.nodeVar.name, False, (0, 0, 0)
                    )
                    self.screen.blit(text_surface, (graphNode.x + 15, graphNode.y + 15))
                    if keys[pygame.K_DELETE] and self.clicked == graphNode:
                        realNode = self.graphicNodeToNodeAddress[graphNode]
                        self.automate.nodeList.remove(realNode)
                        gc.collect()
                        if realNode in self.automate.nodeInitList:
                            self.automate.nodeInitList.remove(realNode)
                            gc.collect()
                        if realNode in self.automate.nodeLastList:
                            self.automate.nodeLastList.remove(realNode)
                            gc.collect()
                        i = 0
                        j = 0
                        while i < len(self.linkList):
                            while j < len(self.linkList[i]):
                                if self.linkList[i][j].linkVar[1] == graphNode:
                                    self.linkList[i].remove(self.linkList[i][j])
                                    gc.collect()
                                else:
                                    j += 1
                            if (
                                self.linkList[i] != []
                                and self.linkList[i][0].nodeVar == graphNode
                            ):
                                self.linkList.remove(self.linkList[i])
                                gc.collect()
                            else:
                                i += 1
                        self.nodeList.remove(graphNode)
                        gc.collect()
                    if (
                        keys[pygame.K_UP]
                        and self.clicked == graphNode
                        and self.countDownSelectState == 0
                    ):
                        self.countDownSelectState = self.clock.get_time()
                        realNode = self.graphicNodeToNodeAddress[graphNode]
                        stateNode = (
                            int(realNode.isInit) * 4
                            + int(realNode.isLast) * 2
                            + int(realNode.bin)
                        )
                        if stateNode == 4:
                            newState = stateNode + 2
                        elif stateNode == 6:
                            newState = 0
                        else:
                            newState = stateNode + 1
                        realNode.isInit = int("{:03b}".format(newState)[0])
                        realNode.isLast = int("{:03b}".format(newState)[1])
                        realNode.bin = int("{:03b}".format(newState)[2])
                        self.automate.updateInitAndLastNodeList()
                    if (
                        keys[pygame.K_DOWN]
                        and self.clicked == graphNode
                        and self.countDownSelectState == 0
                    ):
                        self.countDownSelectState = self.clock.get_time()
                        realNode = self.graphicNodeToNodeAddress[graphNode]
                        stateNode = (
                            int(realNode.isInit) * 4
                            + int(realNode.isLast) * 2
                            + int(realNode.bin)
                        )
                        if stateNode == 0:
                            newState = 6
                        elif stateNode == 6:
                            newState = 4
                        else:
                            newState = stateNode - 1
                        realNode.isInit = int("{:03b}".format(newState)[0])
                        realNode.isLast = int("{:03b}".format(newState)[1])
                        realNode.bin = int("{:03b}".format(newState)[2])

                self.drawMenu()
                self.drawTransitionMenu()

            else:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.buttonClose.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            self.openImportMenu = False
                        elif (
                            self.buttonDown.rect.collidepoint(
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            )
                            and self.importMenuY < 44
                        ):
                            self.importMenuY += 1
                            self.importMenuX += 1
                        elif (
                            self.buttonUp.rect.collidepoint(
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                            )
                            and self.importMenuX > 0
                        ):
                            self.importMenuY -= 1
                            self.importMenuX -= 1
                        elif self.buttonNewBlank.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            self.createBlankAutomate(3)
                            self.openImportMenu = False
                        elif self.exportButton.rect.collidepoint(
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        ):
                            self.automate.saveToFile("textAutomateAlexis")
                        else:
                            for button in self.buttonImportTab:
                                if button.rect.collidepoint(
                                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                                ):
                                    self.importAutomate(
                                        self.buttonImportTab.index(button) + 1
                                    )
                                    self.openImportMenu = False
                    # elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                    # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                    # elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:

                self.importMenu()

            pygame.display.flip()
            self.clock.tick(60)
