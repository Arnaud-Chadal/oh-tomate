import pygame
import graphicNode
import graphicLink
import node
import button
from math import pi, cos, sin


class Main:
    def __init__(self, automate) -> None:
        pygame.font.init()
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.image = pygame.image.load("./images/verySeriousImage.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (756, 1008))
        self.running = True
        self.automate = automate
        self.alphabet = automate.alphabet
        self.nodeAddressToGraphicNodeAddress = {}
        self.graphicNodeToNodeAddress = {}
        self.nodeList = []
        self.linkList = []
        self.clicked = None
        self.grabbed = None
        self.dragLink = None
        self.menuX = 0
        self.menuY = 1080
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
        self.importButton = button.Button(
            self.menuX + 1375, self.menuY + 100 - 30, 200, 80
        )
        self.exportButton = button.Button(
            self.menuX + 1625, self.menuY + 100 - 30, 200, 80
        )
        self.clock = pygame.time.Clock()
        self.countDownSelectLetter = 0
        self.countDownSelectState = 0
        self.xMousePos, self.yMousePos = pygame.mouse.get_pos()
        nbr = 0
        for graphNode in automate.nodeList:
            graphicNo = graphicNode.GraphicNode(nbr * 200, 50 * nbr, graphNode)
            self.nodeList.append(graphicNo)
            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
            self.graphicNodeToNodeAddress[graphicNo] = graphNode
            nbr += 1
        nbr = 0
        for graphNode in automate.nodeList:
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
                self.transitionMenuX -= 30
        else:
            if self.transitionMenuX < 1920:
                self.transitionMenuX += 30
        pygame.draw.rect(self.screen, (0, 0, 0), menuRect)
        pygame.draw.rect(self.screen, (0, 0, 255), barMenuRect)
        # self.screen.blit(
        #     self.my_font.render("Menu", False, (255, 255, 255)),
        #     (self.menuX + 30, self.menuY + 30),
        # )
        string = self.automate.printTransitionTables()
        for groupsNumber in range(len(string)):
            for lineNumber in range(len(string[groupsNumber])):
                textToRender = my_font.render(string[groupsNumber][lineNumber], 0, (255, 255, 255))
                self.screen.blit(
                    textToRender,
                    (
                        self.transitionMenuX + 30,
                        self.transitionMenuY + 20 + lineNumber * 30 + sum([len(group) for group in string[:groupsNumber]]) * 30,
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
        if barMenuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ) or menuRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        ):
            if self.menuY > 880:
                self.menuY -= 30
        else:
            if self.menuY < 1080:
                self.menuY += 30
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
        self.importButton = button.Button(
            self.menuX + 1375, self.menuY + 100 - 30, 200, 80
        )
        self.exportButton = button.Button(
            self.menuX + 1625, self.menuY + 100 - 30, 200, 80
        )
        self.standaButton.drawButton(self.screen, "Standardize")
        self.determineButton.drawButton(self.screen, "Determinize")
        self.completeButton.drawButton(self.screen, "Complete")
        self.minimButton.drawButton(self.screen, "Minimize")
        self.complementButton.drawButton(self.screen, "Complement")
        pygame.draw.rect(
            self.screen, (160, 160, 160), (self.menuX + 1320, self.menuY + 10, 5, 180)
        )
        self.importButton.drawButton(self.screen, "Import")
        self.exportButton.drawButton(self.screen, "Export")

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            # Check des events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for graphNode in self.nodeList:
                        if graphNode.collision.collidepoint(event.pos):
                            self.grabbed = graphNode
                            self.clicked = graphNode
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
                            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
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
                            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
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
                            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
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
                            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
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
                            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
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
                if self.exportButton.rect.collidepoint(
                        pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    ):
                        self.automate.saveToFile("test16")
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
                        self.nodeAddressToGraphicNodeAddress[newNode] = newGraphicNode
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
                        realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                        linkToDelete = links.linkVar
                        linkToDelete[1] = self.graphicNodeToNodeAddress[linkToDelete[1]]
                        realNode.linkList.remove(links.linkVar)
                    if (
                        keys[pygame.K_UP]
                        and self.clicked == links
                        and self.countDownSelectLetter == 0
                    ):
                        self.countDownSelectLetter = int(self.clock.get_time())
                        lettersAvailable = self.alphabet.copy()
                        # for allNodeLinks in self.graphicNodeToNodeAddress[links.nodeVar].linkList:
                        #     if allNodeLinks[0] in lettersAvailable:
                        #         lettersAvailable.remove(allNodeLinks[0])
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
                        # for allNodeLinks in self.graphicNodeToNodeAddress[links.nodeVar].linkList:
                        #     if allNodeLinks[0] in lettersAvailable:
                        #         lettersAvailable.remove(allNodeLinks[0])
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
                    if bool(graphNode.nodeVar.isInit) and not bool(graphNode.nodeVar.isLast) :
                        self.screen.blit(graphNode.image[0][1], (graphNode.x, graphNode.y))
                    elif not bool(graphNode.nodeVar.isInit) and bool(graphNode.nodeVar.isLast) and not bool(graphNode.nodeVar.bin) :
                        self.screen.blit(graphNode.image[1][1], (graphNode.x, graphNode.y))
                    elif bool(graphNode.nodeVar.isInit) and bool(graphNode.nodeVar.isLast) and not bool(graphNode.nodeVar.bin) :
                        self.screen.blit(graphNode.image[2][1], (graphNode.x, graphNode.y))
                    elif bool(graphNode.nodeVar.bin) and not bool(graphNode.nodeVar.isLast) :
                        self.screen.blit(graphNode.image[3][1], (graphNode.x, graphNode.y))
                    elif bool(graphNode.nodeVar.bin) and bool(graphNode.nodeVar.isLast):
                        self.screen.blit(graphNode.image[4][1], (graphNode.x, graphNode.y))
                    else :
                        self.screen.blit(graphNode.image[5][1], (graphNode.x, graphNode.y))
                else:
                    if graphNode.nodeVar.isInit and not graphNode.nodeVar.isLast :
                        self.screen.blit(graphNode.image[0][0], (graphNode.x, graphNode.y))
                    elif not graphNode.nodeVar.isInit and graphNode.nodeVar.isLast and not graphNode.nodeVar.bin :
                        self.screen.blit(graphNode.image[1][0], (graphNode.x, graphNode.y))
                    elif graphNode.nodeVar.isInit and graphNode.nodeVar.isLast and not graphNode.nodeVar.bin :
                        self.screen.blit(graphNode.image[2][0], (graphNode.x, graphNode.y))
                    elif graphNode.nodeVar.bin and not graphNode.nodeVar.isLast :
                        self.screen.blit(graphNode.image[3][0], (graphNode.x, graphNode.y))
                    elif graphNode.nodeVar.bin and graphNode.nodeVar.isLast:
                        self.screen.blit(graphNode.image[4][0], (graphNode.x, graphNode.y))
                    else :
                        self.screen.blit(graphNode.image[5][0], (graphNode.x, graphNode.y))
                text_surface = self.my_font.render(
                    graphNode.nodeVar.name, False, (0, 0, 0)
                )
                self.screen.blit(text_surface, (graphNode.x + 15, graphNode.y + 15))
                if (keys[pygame.K_DELETE] and self.clicked == graphNode):
                    realNode = self.graphicNodeToNodeAddress[graphNode]
                    self.automate.nodeList.remove(realNode)
                    if realNode in self.automate.nodeInitList: 
                        self.automate.nodeInitList.remove(realNode)
                    if realNode in self.automate.nodeLastList:
                        self.automate.nodeLastList.remove(realNode)
                    i = 0
                    j = 0
                    while i < len(self.linkList):
                        while j < len(self.linkList[i]):
                            if self.linkList[i][j].linkVar[1] == graphNode:
                                self.linkList[i].remove(self.linkList[i][j])
                            else:
                                j += 1
                        if (self.linkList[i] != [] and self.linkList[i][0].nodeVar == graphNode):
                            self.linkList.remove(self.linkList[i])
                        else:
                            i += 1
                    self.nodeList.remove(graphNode)
                if (keys[pygame.K_UP] and self.clicked == graphNode and self.countDownSelectState == 0):
                    self.countDownSelectState = self.clock.get_time()
                    realNode = self.graphicNodeToNodeAddress[graphNode]
                    stateNode = int(realNode.isInit)*4 + int(realNode.isLast)*2 + int(realNode.bin)
                    if (stateNode == 4):
                        newState = stateNode + 2
                    elif (stateNode == 6):
                        newState = 0
                    else:
                        newState = stateNode + 1
                    realNode.isInit = int("{:03b}".format(newState)[0])
                    realNode.isLast = int("{:03b}".format(newState)[1])
                    realNode.bin = int("{:03b}".format(newState)[2])
                if (keys[pygame.K_DOWN] and self.clicked == graphNode and self.countDownSelectState == 0):
                    self.countDownSelectState = self.clock.get_time()
                    realNode = self.graphicNodeToNodeAddress[graphNode]
                    stateNode = int(realNode.isInit)*4 + int(realNode.isLast)*2 + int(realNode.bin)
                    if (stateNode == 0):
                        newState = 6
                    elif (stateNode == 6):
                        newState = 4
                    else:
                        newState = stateNode - 1
                    realNode.isInit = int("{:03b}".format(newState)[0])
                    realNode.isLast = int("{:03b}".format(newState)[1])
                    realNode.bin = int("{:03b}".format(newState)[2])

            self.drawMenu()
            self.drawTransitionMenu()
            pygame.display.flip()
            self.clock.tick(60)
