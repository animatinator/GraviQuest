import pygame, sys, math, random


clock = pygame.time.Clock()

class Firework():
    def __init__(self, parent, screen, position, num, colour):
        self.parent = parent
        self.screen = screen
        self.rootpos = position
        self.colour = colour
        self.particles = []
        self.startinglife = 100
        self.life = self.startinglife
        
        spacing = (math.pi * 2.0) / num
        for i in range(num):
            angle = (math.pi - (float(i) * spacing)) % (2.0 * math.pi)
            xvel = math.cos(angle) * 2.0
            yvel = math.sin(angle) * 2.0
            velocity = [xvel, yvel]
            newparticle = [[0, 0], velocity]
            self.particles.append(newparticle)

    def Redraw(self):
        if self.life > 0:
            # Fade out the colour as the firework's life expends
            colourval = float(self.life) / float(self.startinglife)
            colour = (colourval * self.colour[0], colourval * self.colour[1], colourval * self.colour[2])
            for i in range(len(self.particles)):
                # Get the position and velocity of the current particle
                pos = self.particles[i][0]
                vel = self.particles[i][1]
                # Add gravity to the vertical velocity, and add a tiny random velocity to the horizontal velocity
                vel[0] += random.randrange(-10, 10) * 0.01
                vel[1] += 0.1
                # Update the position
                pos[0] += vel[0]
                pos[1] += vel[1]
                # Update the current particle
                self.particles[i] = [pos, vel]

            for particle in self.particles:
                # Calculate the particle's absolute position
                pos = (self.rootpos[0] + particle[0][0], self.rootpos[1] + particle[0][1])
                # Draw a line
                pygame.draw.line(self.screen, colour, pos, (pos[0] + (particle[1][0] * 3.0), pos[1] + (particle[1][1] * 3.0)))
        
        self.life -= 1  # Decrement the firework's life

class TextItem():
    def __init__(self, parent, screen, text, size, strength, ypos):
        self.parent = parent
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font("mainfont.otf", size)
        self.strength = strength
        self.ypos = ypos

    def Redraw(self):
        text = self.font.render(self.text, True, (self.strength * 255, self.strength * 255, self.strength * 255))
        x = (self.screen.get_width() - text.get_width()) / 2
        y = self.ypos + self.parent.scrollroot
        self.screen.blit(text, (x, y))

class Credits():
    def __init__(self, screen, textfile):
        self.screen = screen
        self.textlines = open(textfile, "r").readlines()
        self.textitems = []

        self.xl = 80
        self.large = 60
        self.medium = 45
        self.small = 30

        currenty = 0

        for line in self.textlines:
            line = line.replace("\n", "")
            line = line.replace("[D]", "David Barker")
            line = line.replace("[J]", "James Raymond")

            if line.find("[XL]") != -1:
                line = line.replace("[XL]", "")
                newtext = TextItem(self, self.screen, line, self.xl, 1.0, currenty)
                self.textitems.append(newtext)
            elif line.find("[LARGE]") != -1:
                line = line.replace("[LARGE]", "")
                newtext = TextItem(self, self.screen, line, self.large, 0.9, currenty)
                self.textitems.append(newtext)
            elif line.find("[MEDIUM]") != -1:
                line = line.replace("[MEDIUM]", "")
                newtext = TextItem(self, self.screen, line, self.medium, 0.6, currenty)
                self.textitems.append(newtext)
            elif line.find("[SMALL]") != -1:
                line = line.replace("[SMALL]", "")
                newtext = TextItem(self, self.screen, line, self.small, 0.5, currenty)
                self.textitems.append(newtext)
            else:
                newtext = TextItem(self, self.screen, line, self.small, 0.5, currenty)
                self.textitems.append(newtext)
            
            currenty += 60

        self.height = currenty

        self.scrollroot = self.screen.get_height()
        self.scrollspeed = 2
        
        self.showcopyright = False
        self.tinyfont = pygame.font.Font(None, 16)
        self.copytext = self.tinyfont.render("Copyright ExeSoft 2009, all rights reserved.", True, (100, 100, 100))
        self.copyx = (self.screen.get_width() - self.copytext.get_width()) / 2

        self.fireworks = []
        
        self.bg = pygame.image.load("creditsbg.png").convert()
        self.bgpos = 0

    def Run(self):
        running = True
        pygame.mixer.music.load("GraviQuest.ogg")
        pygame.mixer.music.play(-1)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            self.Update()
            self.Redraw()

            pygame.display.update()
            clock.tick(30)

        pygame.mixer.music.fadeout(1000)

    def Update(self):
        # Normal scrolling
        if self.scrollroot > (self.screen.get_height() - self.height) - 100:
            self.scrollroot -= self.scrollspeed

        # Slow down as the end approaches
        elif self.scrollroot > (self.screen.get_height() / 2) - self.height:
            self.scrollroot -= (self.scrollspeed / 2)

        # Stop with the final text centred
        else:
            self.showcopyright = True

        # Decide whether or not to add a new firework (randomly)
        if random.randint(0, 30) == 8:
            xpos = random.randint(0, self.screen.get_width())
            ypos = random.randint(0, self.screen.get_height())
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            self.fireworks.append(Firework(self, self.screen, [xpos, ypos], 30, (r, g, b)))

        self.bgpos -= 1
        if self.bgpos < -self.bg.get_width():
            self.bgpos = 0

    def Redraw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.bg, (self.bgpos, 0))
        if self.bgpos < - (self.bg.get_width() - self.screen.get_width()):
            self.screen.blit(self.bg, (self.bgpos + self.bg.get_width(), 0))

        for item in self.fireworks:
            item.Redraw()

        for item in self.textitems:
            item.Redraw()

        if self.showcopyright:
            self.screen.blit(self.copytext, (self.copyx, self.screen.get_height() - 50))
