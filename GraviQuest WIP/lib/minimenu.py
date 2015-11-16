import pygame


clock = pygame.time.Clock()


class MiniMenu():
    def __init__(self, screen, items, position, textcolour, highlightcolour, boxcolour, background):
        self.screen = screen
        self.running = False
        self.returnval = None

        self.finalrect = pygame.Rect(position[0], position[1], 0, 0)
        self.rect = self.finalrect.move(0, 0)
        self.scale = 0.0

        self.textcolour = textcolour
        self.highlightcolour = highlightcolour
        self.boxcolour = boxcolour

        self.background = background

        self.mainfont = pygame.font.Font("levelfont.ttf", 30)

        self.items = items
        self.highlighted = None

        self.InitMenu()

    def InitMenu(self):
        maxwidth = 0
        totalheight = 0
        
        for i, item in enumerate(self.items):
            text = self.mainfont.render(item[0], True, self.textcolour)
            self.items[i].append(text)

            width = text.get_width()
            height = text.get_height()
            
            if width > maxwidth:
                maxwidth = width
            
            totalheight += height

        self.finalrect.width = maxwidth
        self.finalrect.height= totalheight

    def Redraw(self):
        self.screen.blit(self.background, (0, 0))
        
        pygame.draw.rect(self.screen, self.boxcolour, self.rect)

        curheight = 0
        
        for i, item in enumerate(self.items):
            ypos = self.rect.top + (curheight * self.scale)
            curheight += item[2].get_height()
            pos = (self.rect.left, ypos)

            if i == self.highlighted:
                newitem = self.mainfont.render(item[0], True, self.highlightcolour)
                self.screen.blit(newitem, pos)
            else:
                self.screen.blit(item[2], pos)
        
        pygame.display.update(self.rect)

    def Update(self):
        if self.scale < 1.0:
            self.scale += 0.1

        if self.scale > 1.0:
            self.scale = 1.0

        self.rect = self.finalrect.move(0, 0)
        self.rect.height *= self.scale

    def ShowMenu(self):
        self.running = True
        
        while self.running:
            self.mousepos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if self.rect.collidepoint(self.mousepos):
                        for i, item in enumerate(self.items):
                            rect = item[2].get_rect()
                            rect.left, rect.top = self.rect.topleft
                            rect.top += rect.height * i
                            
                            if rect.collidepoint(self.mousepos):
                                self.highlighted = i
                                
                    else:
                        self.highlighted = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left-click
                    if event.button == 1:
                        if self.highlighted == None:
                            self.returnval = None
                            self.running = False
                            
                        else:
                            self.returnval = self.items[self.highlighted][1]
                            self.running = False

            self.Update()
            self.Redraw()

            clock.tick(30)

        return self.returnval
