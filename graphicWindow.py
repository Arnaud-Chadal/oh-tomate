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
        for nodeVar in nodeList :
            nbr += 1
            self.nodeList.append(graphicNode.GraphicNode(nbr*200, 200, nodeVar))



    def run(self) :
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                    for graphNode in self.nodeList :
                        if graphNode.collision.collidepoint(event.pos) :
                            self.grabbed = graphNode
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    self.grabbed = None

            self.screen.fill((0, 0, 0))
            for graphNode in self.nodeList :
                if self.grabbed == graphNode :
                    graphNode.setPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                self.screen.blit(graphNode.image, (graphNode.x, graphNode.y))
                text_surface = self.my_font.render(graphNode.nodeVar.name, False, (255, 255, 255))
                self.screen.blit(text_surface, (graphNode.x, graphNode.y))
            pygame.display.flip()
