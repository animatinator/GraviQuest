import pygame, sys, math
from minimenu import *


clock = pygame.time.Clock()

class Menu():
    def __init__(self, screen, items, centrepos, circlewidth, circleheight, frontcolour, backcolour, bgimage = None, scrollbg = False, drawglow = False):
        self.screen = screen
        self.running = False
        self.returnval = None

        self.mainfont = pygame.font.Font(None, 60)
        
        self.items = items
        self.InitItemAngles()
        self.highlighted = 0

        self.centrepos = centrepos
        self.circlewidth = float(circlewidth)
        self.circleheight = float(circleheight)
        self.scalefactorrange = 0.5

        self.frontcolour, self.backcolour = frontcolour, backcolour

        if bgimage == None:
            self.drawbg = False
        else:
            self.drawbg = True
            self.bgimage = bgimage
        self.scrollbg = scrollbg
        
        self.bgrootpos = 0

        self.glow = pygame.image.load("glow.png").convert_alpha()

        self.mousepos = self.centrepos

    def InitItemAngles(self):
        spacing = (math.pi * 2.0) / len(self.items)

        for index, item in enumerate(self.items):
            self.items[index].append((math.pi - (float(index) * spacing)) % (2.0 * math.pi))

    def ShowMenu(self):
        self.running = True
        
        while self.running:
            self.mousepos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # If the item has no submenu
                        if self.items[self.highlighted][2] == None:
                            self.returnval = self.items[self.highlighted][1]
                            self.running = False
                        # If there is a submenu
                        else:
                            submenu = MiniMenu(self.screen, self.items[self.highlighted][2], self.mousepos, (100, 100, 100), (200, 200, 200), (0, 0, 0), self.screen.copy())
                            returnval = submenu.ShowMenu()
                            
                            if returnval != None:
                                self.returnval = "%s%s" % (str(self.items[self.highlighted][1]), str(returnval))
                                self.running = False

            self.Update()
            self.Redraw()

            clock.tick(30)

        return self.returnval

    def SetBackground(self, image):
        self.drawbg = True
        self.bgimage = image

    def Update(self):
        speed = (float(self.mousepos[0] - self.centrepos[0]) / 2500.0)
        if speed > 0.1:
            speed = 0.1
        
        for item in self.items:
            item[3] = (item[3] + speed) % (math.pi * 2.0)

        nearestval  = 2.0
        
        for index, item in enumerate(self.items):
            distval = math.cos(item[3])
            
            if distval < nearestval:
                nearestval = distval
                self.highlighted = index

        if self.drawbg and self.scrollbg:
            self.bgrootpos -= 1
            
            if self.bgrootpos < -self.bgimage.get_width():
                self.bgrootpos = 0

    def Redraw(self):
        if self.drawbg:
            image = self.bgimage
            if self.scrollbg:
                self.screen.blit(image, (self.bgrootpos, 0 - ((image.get_height() - self.screen.get_height()) / 2)))
                if self.bgrootpos < ((-image.get_width()) + self.screen.get_width()):
                    self.screen.blit(image, (self.bgrootpos + image.get_width(), 0 - ((image.get_height() - self.screen.get_height()) / 2)))
            else:
                self.screen.blit(image, (0 - ((image.get_width() - self.screen.get_width()) / 2), 0 - ((image.get_height() - self.screen.get_height()) / 2)))
        else:
            self.screen.fill((0, 0, 0))

        for index, item in enumerate(self.items):
            if index == self.highlighted:  # The highlighted item will be drawn last
                pass
            else:
                xpos = self.centrepos[0] + int(self.circlewidth * math.sin(item[3]))
                ypos = self.centrepos[1] - int(self.circleheight * math.cos(item[3]))

                colourval = 0.5 * (1.0 - math.cos(item[3]))
                r = self.backcolour[0] + int(colourval * float(self.frontcolour[0] - self.backcolour[0]))
                g = self.backcolour[1] + int(colourval * float(self.frontcolour[1] - self.backcolour[1]))
                b = self.backcolour[2] + int(colourval * float(self.frontcolour[2] - self.backcolour[2]))

                text = self.mainfont.render(item[0], True, (r, g, b))

                scalefactor = 1.0 - (self.scalefactorrange * math.cos(item[3]))
                text = pygame.transform.smoothscale(text, (int(text.get_width() * scalefactor), int(text.get_height() * scalefactor)))
                
                self.screen.blit(text, (xpos - (text.get_width() / 2.0), ypos - (text.get_height() / 2.0)))

        item = self.items[self.highlighted]
        
        xpos = self.centrepos[0] + int(self.circlewidth * math.sin(item[3]))
        ypos = self.centrepos[1] - int(self.circleheight * math.cos(item[3]))

        colourval = 0.5 * (1.0 - math.cos(item[3]))
        r = self.backcolour[0] + int(colourval * float(self.frontcolour[0] - self.backcolour[0]))
        g = self.backcolour[1] + int(colourval * float(self.frontcolour[1] - self.backcolour[1]))
        b = self.backcolour[2] + int(colourval * float(self.frontcolour[2] - self.backcolour[2]))

        text = self.mainfont.render(item[0], True, (r, g, b))

        scalefactor = 1.0 - (self.scalefactorrange * math.cos(item[3]))
        text = pygame.transform.smoothscale(text, (int(text.get_width() * scalefactor), int(text.get_height() * scalefactor)))

        self.screen.blit(self.glow, (xpos - (self.glow.get_width() / 2.0), ypos - (self.glow.get_height() / 2.0)))
        self.screen.blit(text, (xpos - (text.get_width() / 2.0), ypos - (text.get_height() / 2.0)))

        
        pygame.display.update()
