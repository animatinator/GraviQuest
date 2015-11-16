import pygame


def ShowTitle(screen, title, subtitle, bgimage):
        bigfont = pygame.font.Font("mainfont.otf", 150)
        smallfont = pygame.font.Font("levelfont.ttf", 50)
        
        bg = pygame.image.load(bgimage)
        
        bigtext = bigfont.render(title, True, (0, 0, 0))
        littletext = smallfont.render(subtitle, True, (0, 0, 0))
        
        ypos = (screen.get_height()/2) - 150
        xpos = screen.get_width()/2 - bigtext.get_width()/2
        
        running = 1
        
        screen.blit(bg, (0, 0))
        screen.blit(bigtext, (xpos, ypos))
        screen.blit(littletext, (screen.get_width()/2 - littletext.get_width()/2, screen.get_height() - 200))
        pygame.display.update()
        while running:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit()
                if pygame.mouse.get_pressed()[0]:
                        running = False
