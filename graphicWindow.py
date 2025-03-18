import pygame
import graphicNode
import graphicLink
import node
from math import pi, cos, sin


class Main:
    def __init__(self, automate) -> None:
        pygame.font.init()
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.nodeList = []
        self.linkList = []
        self.automate = automate
        self.alphabet = automate.alphabet
        self.nodeAddressToGraphicNodeAddress = {}
        self.graphicNodeToNodeAddress = {}
        self.clicked = None
        self.grabbed = None
        self.dragLink = None
        self.clock = pygame.time.Clock()
        self.countDownSelectLetter = 0
        self.xMousePos, self.yMousePos = pygame.mouse.get_pos()
        nbr = 0
        for graphNode in automate.nodeList:
            graphicNo = graphicNode.GraphicNode(nbr * 200, 50*nbr, graphNode)
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
                                counterSelectLetter = self.alphabet.index(link.linkVar[0])
                                link.isClicked = True
                                self.clicked = link
                                self.grabbed = link
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.clicked = self.grabbed
                    self.grabbed = None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for graphNode in self.nodeList:
                        if graphNode.collision.collidepoint(event.pos):
                            self.dragLink = graphNode
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    if self.dragLink == None:
                        print(self.nodeList)
                        nextName = "NewNameDefault"
                        biggestNumber = -1
                        for n in self.automate.nodeList:
                            if (biggestNumber < int(n.name)):
                                biggestNumber = int(n.name)
                        if biggestNumber != -1:
                            nextName = str(biggestNumber+1)
                        newNode = node.Node(nextName, False, False)
                        self.automate.nodeList.append(newNode)
                        newGraphicNode = graphicNode.GraphicNode(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], newNode)
                        self.nodeList.append(newGraphicNode)
                        self.nodeAddressToGraphicNodeAddress[newNode] = newGraphicNode
                        self.graphicNodeToNodeAddress[newGraphicNode] = newNode
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
                                self.linkList[groupIndex].append(graphicLink.GraphicLink(['a', collideNode], self.dragLink))
                                self.dragLink.nodeVar.linkList.append(['a', collideNode.nodeVar])
                                print(self.linkList[groupIndex])
                                for link in self.linkList[groupIndex]:
                                    print(link.linkVar)
                            elif groupIndex == None:
                                self.linkList.append([])
                                self.linkList[-1].append(graphicLink.GraphicLink(['a', collideNode], self.dragLink))
                                self.dragLink.nodeVar.linkList.append(['a', collideNode.nodeVar])
                                print(self.linkList[-1])
                                for link in self.linkList[-1]:
                                    print(link.linkVar)
                        self.dragLink = None
                
                    
            rectArrowDrawed = []
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_RIGHT] and self.clicked == None:
                for graphNode in self.nodeList:
                    graphNode.x += 10
                    graphNode.collision.x += 10
            if keys[pygame.K_LEFT] and self.clicked == None:
                for graphNode in self.nodeList:
                    graphNode.x -= 10
                    graphNode.collision.x -= 10
            if keys[pygame.K_DOWN] and self.clicked == None:
                for graphNode in self.nodeList:
                    graphNode.y += 10
                    graphNode.collision.y += 10
            if keys[pygame.K_UP] and self.clicked == None:
                for graphNode in self.nodeList:
                    graphNode.y -= 10
                    graphNode.collision.y -= 10
            
            if self.countDownSelectLetter > 0:
                self.countDownSelectLetter -= 1
                
            if self.dragLink != None:
                pygame.draw.line(self.screen, (255, 255, 255), (self.dragLink.x+32, self.dragLink.y+32), (
                        pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    ), 5)

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
                    if keys[pygame.K_UP] and self.clicked == links and self.countDownSelectLetter == 0:
                        self.countDownSelectLetter = int(self.clock.get_time())
                        lettersAvailable = self.alphabet.copy()
                        # for allNodeLinks in self.graphicNodeToNodeAddress[links.nodeVar].linkList:
                        #     if allNodeLinks[0] in lettersAvailable:
                        #         lettersAvailable.remove(allNodeLinks[0])
                        if lettersAvailable != []:
                            counterSelectLetter += 1
                            realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                            linkToModifyLetter = links.linkVar.copy()
                            linkToModifyLetter[1] = self.graphicNodeToNodeAddress[linkToModifyLetter[1]]
                            realNode.linkList[realNode.linkList.index(linkToModifyLetter)][0] = lettersAvailable[counterSelectLetter%len(lettersAvailable)]
                            links.linkVar[0] = lettersAvailable[counterSelectLetter%len(lettersAvailable)]
                        else:
                            print("All letters already used !")
                    if keys[pygame.K_DOWN] and self.clicked == links and self.countDownSelectLetter == 0:
                        self.countDownSelectLetter = int(self.clock.get_time())
                        lettersAvailable = self.alphabet.copy()
                        # for allNodeLinks in self.graphicNodeToNodeAddress[links.nodeVar].linkList:
                        #     if allNodeLinks[0] in lettersAvailable:
                        #         lettersAvailable.remove(allNodeLinks[0])
                        if lettersAvailable != []:
                            counterSelectLetter -= 1
                            realNode = self.graphicNodeToNodeAddress[links.nodeVar]
                            linkToModifyLetter = links.linkVar.copy()
                            linkToModifyLetter[1] = self.graphicNodeToNodeAddress[linkToModifyLetter[1]]
                            realNode.linkList[realNode.linkList.index(linkToModifyLetter)][0] = lettersAvailable[counterSelectLetter%len(lettersAvailable)]
                            links.linkVar[0] = lettersAvailable[counterSelectLetter%len(lettersAvailable)]
                        else:
                            print("All letters already used !")

            # Affichage des noeuds
            for graphNode in self.nodeList:
                if self.grabbed == graphNode:
                    graphNode.setPos(
                        pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    )
                if self.clicked == graphNode:
                    self.screen.blit(graphNode.image2, (graphNode.x, graphNode.y))
                else:
                    self.screen.blit(graphNode.image, (graphNode.x, graphNode.y))
                text_surface = self.my_font.render(
                    graphNode.nodeVar.name, False, (0, 0, 0)
                )
                self.screen.blit(text_surface, (graphNode.x + 15, graphNode.y + 15))

                # affichage des lignes
                # idée : afficher des arcs plutôt que des lignes pour pas que ça se superpose
                # pour ça, compter le nombre de transition d'un noeud vers un autre et donner des coefs de courbure selon ce nombre à intervalles réguliers
                # for link in graphNode.nodeVar.linkList :
                #     for graphNode2 in self.nodeList :
                #         if graphNode2.nodeVar == link[1] :
                #             pygame.draw.line(self.screen, (255, 255, 255), (graphNode.x+32, graphNode.y+32), (graphNode2.x+32, graphNode2.y+32), 5)
                #             text_surface = self.my_font.render(link[0], False, (255, 255, 255))
                #             self.screen.blit(text_surface, (graphNode.x+(graphNode2.x-graphNode.x)/2, graphNode.y+(graphNode2.y-graphNode.y)/2))

                # Affichage des flèches de transitions pour indiquer le sens
                # On ne peut pas juste afficher un sprite car il faudra pouvoir cliquer dessus si on veut supprimer la transition
                # for links in self.linkList :
                #     for link in links :
                #         link.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
