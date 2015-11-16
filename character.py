import pygame


# Rotations
DOWN = 0
LEFT = 1
UP = 2
RIGHT = 3

class Character(pygame.sprite.Sprite):
    def __init__(self, parent, pos):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        
        self.images = self.LoadImages("chartest.png")
        self.rotimages = self.images  # Copies of the original images, rotated to fit the character's current orientation
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.oldabsrect = self.rect

        self.velocity = [0.0, 0.0]
        self.maxspeedx = 8
        self.jumpspeed = 23#15
        self.rotation = DOWN
        self.canfall = True
        self.jumptriggered = False
        self.jumping = False

    def LoadImages(self, imagefile):
        rawimg = pygame.image.load(imagefile)
        images = []
        
        for i in range(0, rawimg.get_width() / self.parent.tilesize):
            # Chop off images to the right of the current one
            rect = rawimg.get_rect()
            rect.width = ((rawimg.get_width() / self.parent.tilesize) - i) * self.parent.tilesize
            rect.height = 0
            rect.x = (i+1) * self.parent.tilesize
            image = pygame.transform.chop(rawimg, rect)
            # Chop off images to the left of the current one
            rect = rawimg.get_rect()
            rect.width = i * self.parent.tilesize
            rect.height = 0
            image = pygame.transform.chop(image, rect).convert_alpha()
            
            images.append(image)

        return images

    def GetSide(self, block):
        if self.rotation == UP or self.rotation == DOWN:
            distx = self.rect.centerx - block.rect.centerx
            disty = (self.rect.centery - block.rect.centery) / 2.0
        else:
            distx = (self.rect.centerx - block.rect.centerx) / 2.0
            disty = self.rect.centery - block.rect.centery

        if distx < 0:
            if disty < 0:
                if (abs(disty) < abs(distx)): return "left"
                elif (abs(distx) < abs(disty)): return "top"
            elif disty > 0:
                if (abs(disty) < abs(distx)): return "left"
                elif (abs(distx) < abs(disty)): return "bottom"
            else: return "left"
        elif distx > 0:
            if disty < 0:
                if (abs(disty) < abs(distx)): return "right"
                elif (abs(distx) < abs(disty)): return "top"
            elif disty > 0:
                if (abs(disty) < abs(distx)): return "right"
                elif (abs(distx) < abs(disty)): return "bottom"
            else: return "right"
        else:
            if disty < 0: return "top"
            elif disty > 0: return "bottom"

    def GetGridPos(self):
        # When standing upright
        if self.rotation == DOWN:
            leftgridline = (self.rect.left / self.parent.tilesize) * self.parent.tilesize
            if abs(self.rect.left - leftgridline) > 0:  # If the character is mostly in the right grid box
                xpos = self.rect.right / self.parent.tilesize
            else:
                xpos = self.rect.left / self.parent.tilesize
                
            bottomgridline = ((self.rect.top + self.parent.tilesize) / self.parent.tilesize) * self.parent.tilesize
            if abs(self.rect.top - bottomgridline) > 0:  # If the character is still partly in the top grid box
                ypos = self.rect.top / self.parent.tilesize
            else:
                ypos = (self.rect.top + self.parent.tilesize) / self.parent.tilesize

        # When falling to the left
        elif self.rotation == LEFT:
            rightgridline = ((self.rect.left + self.parent.tilesize) / self.parent.tilesize) * self.parent.tilesize
            if abs((self.rect.left + self.parent.tilesize) - rightgridline) > 0:  # If the character is still partly in the right grid box
                xpos = (self.rect.left + self.parent.tilesize) / self.parent.tilesize
            else:
                xpos = self.rect.left / self.parent.tilesize
                
            bottomgridline = ((self.rect.top + self.parent.tilesize) / self.parent.tilesize) * self.parent.tilesize
            if abs(self.rect.top - bottomgridline) > abs((self.rect.top + self.parent.tilesize) - bottomgridline):  # If the character is mostly in the top grid box
                ypos = self.rect.top / self.parent.tilesize
            else:
                ypos = (self.rect.top + self.parent.tilesize) / self.parent.tilesize

        # When upside-down
        elif self.rotation == UP:
            leftgridline = (self.rect.left / self.parent.tilesize) * self.parent.tilesize
            if abs(self.rect.left - leftgridline) > 0:  # If the character is mostly in the right grid box
                xpos = self.rect.right / self.parent.tilesize
            else:
                xpos = self.rect.left / self.parent.tilesize

            topgridline = ((self.rect.top + self.parent.tilesize) / self.parent.tilesize) * self.parent.tilesize
            if abs((self.rect.top + self.parent.tilesize) - topgridline) > 0:  # If the character is still partly in the bottom grid box
                ypos = (self.rect.top + self.parent.tilesize) / self.parent.tilesize
            else:
                ypos = self.rect.top / self.parent.tilesize

        # When falling to the right
        elif self.rotation == RIGHT:
            leftgridline = ((self.rect.left + (self.parent.tilesize * 2)) / self.parent.tilesize) * self.parent.tilesize
            if abs((self.rect.left + self.parent.tilesize) - leftgridline) > 0:  # If the character is still partly in the left grid box
                xpos = self.rect.left / self.parent.tilesize
            else:
                xpos = (self.rect.left + self.parent.tilesize) / self.parent.tilesize
                
            bottomgridline = ((self.rect.top + self.parent.tilesize) / self.parent.tilesize) * self.parent.tilesize
            if abs(self.rect.top - bottomgridline) > abs((self.rect.top + self.parent.tilesize) - bottomgridline):  # If the character is mostly in the top grid box
                ypos = self.rect.top / self.parent.tilesize
            else:
                ypos = (self.rect.top + self.parent.tilesize) / self.parent.tilesize

        return (xpos, ypos)

    def Rotate(self, direction):
        if direction == "right":
            if self.rotation < RIGHT:
                self.rotation += 1
            else:
                self.rotation = DOWN

        elif direction == "left":
            if self.rotation > DOWN:
                self.rotation -= 1
            else:
                self.rotation = RIGHT

        temprect = self.rect.move(0, 0)

        if self.rotation == DOWN or self.rotation == UP:
            temprect.width = self.parent.tilesize
            temprect.height = self.parent.tilesize * 2
        
        elif self.rotation == LEFT or self.rotation == RIGHT:
            temprect.width = self.parent.tilesize * 2
            temprect.height = self.parent.tilesize

        if temprect != self.rect:
            oldrect = temprect.move(0, 0)
            oldrect.width = temprect.right - self.rect.left
            oldrect.height = self.rect.bottom - temprect.top
            self.oldabsrect = oldrect

        self.rect = temprect

        # Rotate all the images to fit the new orientation
        self.rotimages = []
        
        for image in self.images:
            self.rotimages.append(pygame.transform.rotate(image, -(90 * self.rotation)))

    def Reset(self):
        self.rotimages = self.images
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = self.parent.startpos
        self.oldabsrect = self.rect

    def Update(self):
        if self.canfall:
            if self.parent.gravitydir == DOWN:
                self.velocity[1] += self.parent.gravity
            elif self.parent.gravitydir == LEFT:
                self.velocity[0] -= self.parent.gravity
            elif self.parent.gravitydir == UP:
                self.velocity[1] -= self.parent.gravity
            elif self.parent.gravitydir == RIGHT:
                self.velocity[0] += self.parent.gravity
        else:
            if self.parent.gravitydir == UP or self.parent.gravitydir == DOWN:
                self.velocity[1] = 0  # Vertical gravity
            else:
                self.velocity[0] = 0  # Horizontal gravity
            self.jumping = False

        if self.parent.gravitydir == UP or self.parent.gravitydir == DOWN:
            horizontalaxis = 0
            verticalaxis = 1
        else:
            horizontalaxis = 1
            verticalaxis = 0

        if self.parent.gravitydir == DOWN or self.parent.gravitydir == LEFT:
            positivemotion = 1
        else:
            positivemotion = -1
            
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if (self.velocity[horizontalaxis] * positivemotion) > 0 and self.jumping == False:
                self.image = self.rotimages[5]
            else:
                self.image = self.rotimages[1]
            if ((self.velocity[horizontalaxis] * positivemotion) > (-self.maxspeedx) * positivemotion and (self.rotation == DOWN or self.rotation == LEFT)) or (((self.velocity[horizontalaxis] * positivemotion) > self.maxspeedx * positivemotion) and (self.rotation == UP or self.rotation == RIGHT)):
                self.velocity[horizontalaxis] -= 1 * positivemotion
            else:
                self.velocity[horizontalaxis] = (-self.maxspeedx) * positivemotion
                
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            if (self.velocity[horizontalaxis] * positivemotion) < 0 and self.jumping == False:
                self.image = self.rotimages[4]
            else:
                self.image = self.rotimages[2]
            if (((self.velocity[horizontalaxis] * positivemotion) < (self.maxspeedx * positivemotion)) and (self.rotation == DOWN or self.rotation == LEFT)) or (((self.velocity[horizontalaxis] * positivemotion) < (-self.maxspeedx) * positivemotion) and (self.rotation == UP or self.rotation == RIGHT)):
                self.velocity[horizontalaxis] += 1 * positivemotion
            else:
                self.velocity[horizontalaxis] = self.maxspeedx * positivemotion

        else:
            if (self.velocity[horizontalaxis] * positivemotion) < 0 and self.jumping == False:
                self.image = self.rotimages[4]
                self.velocity[horizontalaxis] += 1 * positivemotion
            elif (self.velocity[horizontalaxis] * positivemotion) > 0 and self.jumping == False:
                self.image = self.rotimages[5]
                self.velocity[horizontalaxis] -= 1 * positivemotion
            else:
                if self.jumping:
                    self.image = self.rotimages[3]
                else:
                    self.image = self.rotimages[0]

        if self.jumptriggered:
            self.jumptriggered = False
            if not self.jumping:
                self.canfall = True
                self.jumping = True
                if verticalaxis == 1:
                    self.velocity[verticalaxis] = (-self.jumpspeed) * positivemotion
                else:
                    self.velocity[verticalaxis] = self.jumpspeed * positivemotion

        self.rect.left += self.velocity[0]
        self.rect.top += self.velocity[1]

    def Redraw(self):
        self.parent.dirtyrects.append(self.oldabsrect)
        absrect = self.rect.move(0, 0)  # Makes a copy of the position rect
        absrect.left -= self.parent.camerapos[0]
        absrect.top -= self.parent.camerapos[1]
        self.parent.screen.blit(self.image, absrect)
        self.parent.dirtyrects.append(absrect)
        self.oldabsrect = absrect
