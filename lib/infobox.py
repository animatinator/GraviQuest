import pygame, sys, os

clock = pygame.time.Clock()


class InfoBox():
    def __init__(self, screen, number, bg):
        self.screen = screen
        self.number = number
        self.bg = bg
        self.image = pygame.image.load(os.path.join("Area 0", "%i.png" % self.number))

    def Redraw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.image, (self.screen.get_width() - self.image.get_width(), self.screen.get_height() - self.image.get_height()))

    def MainLoop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False

            self.Redraw()

            pygame.display.update()
            clock.tick(30)
