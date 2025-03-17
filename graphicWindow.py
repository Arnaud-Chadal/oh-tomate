import pygame
import graphicNode
import graphicLink
from math import pi, cos, sin


class Main:
    def __init__(self, nodeList) -> None:
        pygame.font.init()
        self.my_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.nodeList = []
        self.linkList = []
        self.nodeAddressToGraphicNodeAddress = {}
        self.clicked = None
        self.grabbed = None
        self.xMousePos, self.yMousePos = pygame.mouse.get_pos()
        nbr = 0
        for graphNode in nodeList:
            graphicNo = graphicNode.GraphicNode(nbr * 200, 50*nbr, graphNode)
            self.nodeList.append(graphicNo)
            self.nodeAddressToGraphicNodeAddress[graphNode] = graphicNo
            nbr += 1
        nbr = 0
        for graphNode in nodeList:
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
                                print("Oui !")
                                link.isClicked = True
                                self.clicked = link
                                self.grabbed = link
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.clicked = self.grabbed
                    self.grabbed = None
                    
            rectArrowDrawed = []

            # print(self.linkList)
            for linkGroup in self.linkList:
                for links in linkGroup:
                    # print(links.nodeVar.nodeVar.name)
                    # print("\n")
                    links.draw(self.screen, rectArrowDrawed)
                    rectArrowDrawed.append(links.collision)
            #     print("---")
            #     print("\n")
            # print("\n\n\n\n")
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
