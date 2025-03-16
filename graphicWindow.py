import pygame
import graphicNode


class Main :
    def __init__(self, nodeList) -> None :
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.nodeList = []
        self.clicked = None
        self.grabbed = None
        nbr = 0
        for graphNode in nodeList :
            nbr += 1
            self.nodeList.append(graphicNode.GraphicNode(nbr*200, 200, graphNode))
            # for link in graphNode.nodeVar.linkList :
                



    def run(self) :
        while self.running : 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                    for graphNode in self.nodeList :
                        if graphNode.collision.collidepoint(event.pos) :
                            self.grabbed = graphNode
                            self.clicked = graphNode
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    self.clicked = self.grabbed
                    self.grabbed = None

            self.screen.fill((0, 0, 0))
            for graphNode in self.nodeList :
                if self.grabbed == graphNode :
                    graphNode.setPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if self.clicked == graphNode :
                    self.screen.blit(graphNode.image2, (graphNode.x, graphNode.y))
                else : self.screen.blit(graphNode.image, (graphNode.x, graphNode.y))
                text_surface = self.my_font.render(graphNode.nodeVar.name, False, (0, 0, 0))
                self.screen.blit(text_surface, (graphNode.x+15, graphNode.y+15))
                for link in graphNode.nodeVar.linkList :
                    for graphNode2 in self.nodeList :
                        if graphNode2.nodeVar == link[1] :
                            pygame.draw.line(self.screen, (255, 255, 255), (graphNode.x+32, graphNode.y+32), (graphNode2.x+32, graphNode2.y+32))
                            text_surface = self.my_font.render(link[0], False, (255, 255, 255))
                            self.screen.blit(text_surface, (graphNode.x+(graphNode2.x-graphNode.x)/2, graphNode.y+(graphNode2.y-graphNode.y)/2))
            pygame.display.flip()
