import pygame, sys, math, os
from level import *
from infobox import *

clock = pygame.time.Clock()


class InfoPoint(pygame.sprite.Sprite):
    def __init__(self, parent, pos, number):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.rect = pygame.Rect(pos, (50, 50))
        self.number = number
        self.unused = True

class Tutorial(Level):
    def __init__(self, screen):
        Level.__init__(self, screen, "Area 0", 1)
        self.leveltext = self.mainfont.render("Tutorial level", True, (0, 0, 0))
        self.pausetip = pygame.image.load(os.path.join("Area 0", "pausetip.png"))
        self.Redraw()

    def LoadLevel(self):
        Level.LoadLevel(self)
        self.infopoints = pygame.sprite.Group()

        for y, row in enumerate(self.levelgrid):
            for x, item in enumerate(row):
                if item[0] != 0:
                    if type(item[0]) == type(0):  # Check to see if the item is an integer
                        # If so, create an InfoPoint object for it
                        newpoint = InfoPoint(self, (x*self.tilesize, y*self.tilesize), item[0])
                        self.levelgrid[y][x][1] = newpoint
                        self.infopoints.add(newpoint)
                    elif item[0] == "S":  # Create an InfoPoint for the start of the level
                        newpoint = InfoPoint(self, (x*self.tilesize, y*self.tilesize), 0)
                        self.infopoints.add(newpoint)
                        

    def Update(self):
        Level.Update(self)
        infohits = pygame.sprite.spritecollide(self.character.sprite, self.infopoints, False)

        if infohits:
            infopoint = infohits[0]
            
            if infopoint.unused:
                number = infopoint.number
                infopoint.unused = False
                infobox = InfoBox(self.screen, number, self.screen.copy())
                sound = pygame.mixer.Sound("Info.ogg")
                sound.play(0)
                infobox.MainLoop()
                self.needsdrawn = True

    def Redraw(self):
        Level.Redraw(self)
        self.screen.blit(self.pausetip, (0, 0))
        pygame.display.update(self.pausetip.get_rect())
