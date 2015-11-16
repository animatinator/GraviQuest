import pygame, sys, math, os
from character import *
from spinmenu import *
from tileloader import *


# Gravity directions
DOWN = 0
LEFT = 1
UP = 2
RIGHT = 3

clock = pygame.time.Clock()

def Distance(a, b):
    return math.sqrt((abs(b[0] - a[0])^2) + (abs(b[1] - a[1])^2))

class FloorBrick(pygame.sprite.Sprite):
    def __init__(self, parent, pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.onscreenbefore = False

    def Redraw(self):
        if self.onscreenbefore:
            self.parent.dirtyrects.append(self.oldabsrect)
        
        absrect = self.rect.move(0, 0)  # Makes a copy of the position rect
        absrect.left -= self.parent.camerapos[0]
        absrect.top -= self.parent.camerapos[1]

        if (absrect.left < self.parent.screen.get_width() and absrect.right > 0) and (absrect.top < self.parent.screen.get_height() and absrect.bottom > 0):
            self.onscreenbefore = True            
            self.parent.screen.blit(self.image, absrect)
            self.parent.dirtyrects.append(absrect)
            self.oldabsrect = absrect

class SpinBlock(pygame.sprite.Sprite):
    def __init__(self, parent, pos, spintype, image):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.spintype = spintype
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.onscreenbefore = False

    def Redraw(self):
        if self.onscreenbefore:
            self.parent.dirtyrects.append(self.oldabsrect)
        
        absrect = self.rect.move(0, 0)  # Makes a copy of the position rect
        absrect.left -= self.parent.camerapos[0]
        absrect.top -= self.parent.camerapos[1]

        if (absrect.left < self.parent.screen.get_width() and absrect.right > 0) and (absrect.top < self.parent.screen.get_height() and absrect.bottom > 0):
            self.onscreenbefore = True            
            self.parent.screen.blit(self.image, absrect)
            self.parent.dirtyrects.append(absrect)
            self.oldabsrect = absrect


class Level():
    def __init__(self, screen, folder, levelnum):
        self.screen = screen
        self.running = False
        self.returnval = None

        self.folder = folder
        self.levelnum = levelnum

        self.camerapos = [500, 0]
        self.maxcamshortdist = 250
        self.maxcamspeeds = [7, 5]  # Short distances (lesser than maxcamshortdist)
        self.maxcamspeedl = [30, 30]  # Long distances (greater than maxcamshortdist)
        self.gravity = 1.5
        self.gravitydir = DOWN
        
        self.tilesize = 50

        self.LoadImages()
        
        self.levelgrid = []
        self.floorbricks = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.character = pygame.sprite.GroupSingle()
        self.startpos = (0, 0)
        self.goalpos = (0, 0)
        self.LoadLevel()
        
        self.goalimg = pygame.image.load(os.path.join(self.folder, "goal.png")).convert_alpha()
        self.oldgoalrect = None

        self.bgimage = pygame.image.load(os.path.join(self.folder, "bg.png")).convert()
        self.dirtyrects = []
        self.needsdrawn = True

        self.mousepos = [400, 300]

    def LoadImages(self):
        images = LoadTiles(os.path.join(self.folder, "floortiles.png"), 4, 4, 16)
        ## Floor images
        # Single
        self.floorsimg = images[14]#pygame.image.load(os.path.join(self.folder, "floors.png")).convert_alpha()
        # Horizontal & vertical
        self.floorvimg = images[12]#pygame.image.load(os.path.join(self.folder, "floorv.png")).convert_alpha()
        self.floorhimg = images[13]#pygame.image.load(os.path.join(self.folder, "floorh.png")).convert_alpha()
        # Cross-piece
        self.floorximg = images[15]#pygame.image.load(os.path.join(self.folder, "floorx.png")).convert_alpha()
        # Top, bottom, left and right ends
        self.floortimg = images[0]#pygame.image.load(os.path.join(self.folder, "floort.png")).convert_alpha()
        self.floorbimg = images[1]#pygame.image.load(os.path.join(self.folder, "floorb.png")).convert_alpha()
        self.floorlimg = images[2]#pygame.image.load(os.path.join(self.folder, "floorl.png")).convert_alpha()
        self.floorrimg = images[3]#pygame.image.load(os.path.join(self.folder, "floorr.png")).convert_alpha()
        # Topleft, topright, bottomleft and bottomright corners
        self.floortlimg = images[4]#pygame.image.load(os.path.join(self.folder, "floortl.png")).convert_alpha()
        self.floortrimg = images[5]#pygame.image.load(os.path.join(self.folder, "floortr.png")).convert_alpha()
        self.floorblimg = images[6]#pygame.image.load(os.path.join(self.folder, "floorbl.png")).convert_alpha()
        self.floorbrimg = images[7]#pygame.image.load(os.path.join(self.folder, "floorbr.png")).convert_alpha()
        # Vertical-left, vertical-right, horizontal-top and horizontal-bottom three-way connectors
        self.floorvlimg = images[8]#pygame.image.load(os.path.join(self.folder, "floorvl.png")).convert_alpha()
        self.floorvrimg = images[9]#pygame.image.load(os.path.join(self.folder, "floorvr.png")).convert_alpha()
        self.floorhtimg = images[10]#pygame.image.load(os.path.join(self.folder, "floorht.png")).convert_alpha()
        self.floorhbimg = images[11]#pygame.image.load(os.path.join(self.folder, "floorhb.png")).convert_alpha()

        # Spin-block images
        self.leftspinblockimg = pygame.image.load(os.path.join(self.folder, "lspin.png")).convert_alpha()
        self.rightspinblockimg = pygame.image.load(os.path.join(self.folder, "rspin.png")).convert_alpha()

    def LoadLevel(self):
        rawleveldata = open(os.path.join(self.folder, "%i.lvl" % self.levelnum), "r").readlines()  # Get the level data as a list of lines
    
        # Split the lines into individual items
        leveldata = []
        for line in rawleveldata:
            leveldata.append(list(line))

        for y, line in enumerate(leveldata):  # For each row
            row = []
            for x, item in enumerate(line):  # For each column in the row
                thistile = [item]  # Items in the grid consist of ["itemtype", <reference to object where possible>]
                if item == "F":  # Floor brick
                    newfloorbrick = FloorBrick(self, (x * self.tilesize, y * self.tilesize), self.floorsimg)
                    self.floorbricks.add(newfloorbrick)
                    thistile.append(newfloorbrick)
                elif item == "L":  # Left spinblock
                    newblock = SpinBlock(self, (x * self.tilesize, y * self.tilesize), "left", self.leftspinblockimg)
                    self.blocks.add(newblock)
                    thistile.append(newblock)
                elif item == "R":  # Right spinblock
                    newblock = SpinBlock(self, (x * self.tilesize, y * self.tilesize), "right", self.rightspinblockimg)
                    self.blocks.add(newblock)
                    thistile.append(newblock)
                elif item == "S":  # Character start point
                    self.startpos = (x * self.tilesize, y * self.tilesize)
                    character = Character(self, self.startpos)
                    self.character.add(character)
                    thistile.append(None)
                elif item == "G":  # Goal point
                    self.goalpos = (x * self.tilesize, y * self.tilesize)
                    thistile.append(None)
                else:  # Empty (or at least unimportant) tile
                    thistile = [0, None]

                row.append(thistile)  # Append this tile to the row
            self.levelgrid.append(row)  # Append this row to the grid

            self.SetFloorImages()

    def SetFloorImages(self):
        for block in self.floorbricks.sprites():
            surroundingblocks = self.GetSurroundingBlocks(block)
            posx = block.rect.x / self.tilesize
            posy = block.rect.y / self.tilesize
            
            numblocks = len(surroundingblocks)

            if numblocks == 0:
                block.image = self.floorsimg

            elif numblocks == 1:
                # Image is chosen based on what type of end the block is (top, bottom, left or right)
                if (posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F"):
                    block.image = self.floortimg
                elif (posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F"):
                    block.image = self.floorbimg
                elif (posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F"):
                    block.image = self.floorlimg
                elif (posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F"):
                    block.image = self.floorrimg

            elif numblocks == 2:
                # If the block is part of a horizontal line
                if ((posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F")) and ((posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F")):
                    block.image = self.floorhimg
                # If the block is part of a vertical line
                elif ((posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F")) and ((posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F")):
                    block.image = self.floorvimg
                else:  # The block is part of a corner
                    # If there is a square above
                    if (posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F"):
                        # If there is a square to the left
                        if (posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F"):
                            block.image = self.floortlimg
                        # If there is a square to the right
                        elif (posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F"):
                            block.image = self.floortrimg
                    # If there is a square below
                    elif (posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F"):
                        # If there is a square to the left
                        if (posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F"):
                            block.image = self.floortlimg
                        # If there is a square to the right
                        elif (posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F"):
                            block.image = self.floortrimg

            elif numblocks == 3:
                # If the block is part of a horizontal line
                if ((posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F")) and ((posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F")):
                    # If there is a square above
                    if (posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F"):
                        block.image = self.floorhtimg
                    # If there is a square below
                    elif (posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F"):
                        block.image = self.floorhbimg
                # If the block is part of a vertical line
                elif ((posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F")) and ((posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F")):
                        # If there is a square to the left
                        if (posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F"):
                            block.image = self.floorvlimg
                        # If there is a square to the right
                        elif (posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F"):
                            block.image = self.floorvrimg

            elif numblocks == 4:
                block.image = self.floorximg

            else:
                block.image = self.floorsimg

    def GetSurroundingBlocks(self, block):
        posx = block.rect.x / self.tilesize
        posy = block.rect.y / self.tilesize
        blocks = []

        if (posx > 0) and (self.levelgrid[posy][posx - 1][0] == "F"):
            blocks.append([posx - 1, posy])
        
        if (posy > 0) and (self.levelgrid[posy - 1][posx][0] == "F"):
            blocks.append([posx, posy - 1])

        if (posx < len(self.levelgrid[0]) - 1) and (self.levelgrid[posy][posx + 1][0] == "F"):
            blocks.append([posx + 1, posy])

        if (posy < len(self.levelgrid) - 1) and (self.levelgrid[posy + 1][posx][0] == "F"):
            blocks.append([posx, posy + 1])

        return blocks

    def GetCollisions(self):
        charpos = self.character.sprite.GetGridPos()
        potentials = []  # A list of occupied squares around the character

        if self.gravitydir == DOWN or self.gravitydir == UP:
            minx = -1
            maxx = 2
            miny = -1
            maxy = 3
        else:
            minx = -1
            maxx = 3
            miny = -1
            maxy = 2

        for xval in range(minx, maxx):  # Test from one left to one right of the character (co-ordinates are relative to the player position here)
            for yval in range(miny, maxy):  # Test from one below to one above the character
                # Get the absolute x and y grid co-ordinates for this tile
                x = charpos[0] + xval
                y = charpos[1] + yval
                try:
                    # Append 'F', 'L' and 'R' (floor and spinblocks) to the list of potential collisions
                    gridval = self.levelgrid[y][x][0]
                    if gridval == "F" or gridval == "L" or gridval == "R":
                        potentials.append(self.levelgrid[y][x])
                except:  # It seems likely that this square is off the grid
                    pass

        collisions = []
        
        for potential in potentials:  # Test for collisions between the character and objects in the potentials list
            if pygame.sprite.collide_rect(self.character.sprite, potential[1]):
                collisions.append(potential)

        return collisions

    def Rotate(self, direction):
        if direction == "right":
            if self.gravitydir < RIGHT:
                self.gravitydir += 1
            else:
                self.gravitydir = DOWN

        elif direction == "left":
            if self.gravitydir > DOWN:
                self.gravitydir -= 1
            else:
                self.gravitydir = RIGHT

        self.character.sprite.Rotate(direction)
        self.needsdrawn = True
                
    def MainLoop(self):
        self.running = True
        
        while self.running:
            self.mousepos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.returnval = "quit"
                        self.running = False

                    elif event.key == pygame.K_p:
                        currentscreen = self.screen.copy()
                        pausemenu  = Menu(self.screen,
                            [["Continue", "continue"], ["Restart level", "restart"], ["Quit game", "quit"], ["Take screenshot", "screenie"]],
                            (400, 300), 200, 100, (100, 255, 50), (75, 150, 50), currentscreen, True)
                        selection = pausemenu.ShowMenu()
                        self.needsdrawn = True

                        if selection == "quit":
                            self.returnval = "quit"

                        elif selection == "restart":
                            self.character.sprite.Reset()
                            self.gravitydir = DOWN
                            self.needsdrawn = True

                        elif selection == "screenie":
                            saved = False
                            i = 1
                            while not saved:
                                if os.path.exists("GraviQuest screenshot %i.jpg" % i):
                                    i += 1
                                else:
                                    pygame.image.save(currentscreen, "GraviQuest screenshot %i.jpg" % i)
                                    saved = True

                    elif event.key == pygame.K_UP:
                        self.character.sprite.jumptriggered = True

            self.Update()

            if self.returnval != None:  # If the return value has changed (indicates a win or fail)
                break
            
            self.Redraw()

            clock.tick(30)

        return self.returnval

    def Update(self):
        # Old mouse-based camera control
        #newcamx = self.camerapos[0] + int(float(self.mousepos[0] - (self.screen.get_width() / 2.0)) * 0.1)
        #newcamy = self.camerapos[1] + int(float(self.mousepos[1] - (self.screen.get_height() / 2.0)) * 0.1)
        #self.camerapos = [newcamx, newcamy]

        # Move the camera to keep up with the character (such that it is centre-screen), within speed limits
        camdistx = (self.character.sprite.rect.centerx - self.camerapos[0]) - (self.screen.get_width() / 2)
        camdisty = (self.character.sprite.rect.centery - self.camerapos[1]) - (self.screen.get_height() / 2)

        if abs(camdistx) > self.maxcamshortdist:
            if abs(camdistx) > self.maxcamspeedl[0]:
                camdistx = (camdistx / abs(camdistx)) * self.maxcamspeedl[0]  # Makes sure that the sign (+/-) of the speed matches that of the distance
        else:
            if abs(camdistx) > self.maxcamspeeds[0]:
                camdistx = (camdistx / abs(camdistx)) * self.maxcamspeeds[0]

        if abs(camdisty) > self.maxcamshortdist:
            if abs(camdisty) > self.maxcamspeedl[1]:
                camdisty = (camdisty / abs(camdisty)) * self.maxcamspeedl[1]
        else:
            if abs(camdisty) > self.maxcamspeeds[1]:
                camdisty = (camdisty / abs(camdisty)) * self.maxcamspeeds[1]

        self.camerapos = [self.camerapos[0] + camdistx, self.camerapos[1] + camdisty]

        # Update the character
        self.character.sprite.Update()

        # Test for collisions, and respond accordingly
        collisions = self.GetCollisions()
        
        if collisions:
            for obj in collisions:
                block = obj[1]
                side = self.character.sprite.GetSide(block)

                if side == "top":
                    self.character.sprite.rect.top = block.rect.top - self.character.sprite.rect.height
                    self.character.sprite.velocity[1] = 0
                elif side == "bottom":
                    self.character.sprite.rect.top = block.rect.top + self.tilesize
                    self.character.sprite.velocity[1] = 0
                elif side == "left":
                    self.character.sprite.rect.left = block.rect.left - self.character.sprite.rect.width
                    self.character.sprite.velocity[0] = 0
                elif side == "right":
                    self.character.sprite.rect.left = block.rect.left + self.tilesize
                    self.character.sprite.velocity[0] = 0
                else:
                    pass

                if (side == "top" and self.gravitydir == DOWN) or (side == "bottom" and self.gravitydir == UP) or (side == "left" and self.gravitydir == RIGHT) or (side == "right" and self.gravitydir == LEFT):
                    self.character.sprite.canfall = False
                    self.character.sprite.jumping = False

                # React to the player headbutting spin-blocks
                if obj[0] == "R":  # Right-spin
                    if (side == "top" and self.gravitydir == UP) or (side == "right" and self.gravitydir == RIGHT) or (side == "bottom" and self.gravitydir == DOWN) or (side == "left" and self.gravitydir == LEFT):
                        self.Rotate("right")
                elif obj[0] == "L":  # Left-spin
                    if (side == "top" and self.gravitydir == UP) or (side == "right" and self.gravitydir == RIGHT) or (side == "bottom" and self.gravitydir == DOWN) or (side == "left" and self.gravitydir == LEFT):
                        self.Rotate("left")

        # Test for whether the character should be falling
        chargridpos = self.character.sprite.GetGridPos()
        canfall = True
        if self.gravitydir == DOWN:
            try:
                if self.levelgrid[chargridpos[1] + 2][chargridpos[0]][0] != 0:
                    canfall = False
            except:  # The grid position perhaps doesn't exist - assume it is empty
                canfall = True
            if chargridpos[0] < 0:  # Prevents strange errors when the character is offscreen - it should ALWAYS fall, as the offscreen area is empty
                canfall = True
        elif self.gravitydir == LEFT:
            try:
                if self.levelgrid[chargridpos[1]][chargridpos[0] - 1][0] != 0:
                    canfall = False
            except:  # The grid position perhaps doesn't exist - assume it is empty
                canfall = True
        elif self.gravitydir == UP:
            try:
                if self.levelgrid[chargridpos[1] - 1][chargridpos[0]][0] != 0:
                    canfall = False
            except:  # The grid position perhaps doesn't exist - assume it is empty
                canfall = True
            if chargridpos[0] < 0:  # Prevents strange errors when the character is offscreen - it should ALWAYS fall, as the offscreen area is empty
                canfall = True
        elif self.gravitydir == RIGHT:
            try:
                if self.levelgrid[chargridpos[1]][chargridpos[0] + 2][0] != 0:
                    canfall = False
            except:  # The grid position perhaps doesn't exist - assume it is empty
                canfall = True
        self.character.sprite.canfall = canfall

        # If the player has fallen off the edge of the level, change the return value to 'fail' (the mainloop will then exit after this function)
        if (self.character.sprite.rect.top > (len(self.levelgrid) * self.tilesize)) or (self.character.sprite.rect.top < (0 - self.tilesize)) or (self.character.sprite.rect.left > (len(self.levelgrid[0]) * self.tilesize)) or (self.character.sprite.rect.left < (0 - self.tilesize)):
            self.returnval = "fail"

        # If the player is at the goal (allow a slight margin of error)
        if Distance(self.character.sprite.rect.topleft, self.goalpos) < 5:
            self.returnval = "win"

    def Redraw(self):
        self.screen.blit(self.bgimage, (0, 0))

        # Draw floor bricks
        for floorbrick in self.floorbricks.sprites():
            floorbrick.Redraw()

        # Draw blocks
        for block in self.blocks.sprites():
            block.Redraw()

        # Draw the goal
        goalx = self.goalpos[0] - self.camerapos[0]
        goaly = self.goalpos[1] - self.camerapos[1]

        if self.oldgoalrect:
            self.dirtyrects.append(self.oldgoalrect)

        if ((goalx + self.tilesize) > 0 and goalx < self.screen.get_width() and (goaly + (self.tilesize * 2)) > 0 and goaly < self.screen.get_height()):
            self.screen.blit(self.goalimg, (goalx, goaly))
            goalrect = pygame.Rect(goalx, goaly, self.tilesize, self.tilesize * 2)
            self.dirtyrects.append(goalrect)
            self.oldgoalrect = goalrect
        
        # Draw character
        self.character.sprite.Redraw()

        if self.needsdrawn:  # If the level has not been drawn yet:
            pygame.display.update(self.screen.get_rect())
            self.needsdrawn = False
        else:
            pygame.display.update(self.dirtyrects)
        self.dirtyrects = []
