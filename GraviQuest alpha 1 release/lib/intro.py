import pygame

def showTitle(screen, text, size = None, pos = None):
	if size != None:
		bigfont = pygame.font.Font("mainfont.otf", size)
	else:
		bigfont = pygame.font.Font("mainfont.otf", 50)
	
	smallfont = pygame.font.Font("mainfont.otf", 15)
	
	bg = pygame.image.load("DisplayAreaBg.png")
	
	bigtext = bigfont.render(text, True, (0, 0, 0))
	
	littletext = smallfont.render("Click anywhere to continue", True, (0, 0, 0))
	
	ypos = screen.get_height()/2
	
	if pos != None:
		if pos == "centre":
			xpos = screen.get_width()/2 - bigtext.get_width()/2
		elif pos == "left":
			xpos = 20
		elif pos == "right":
			xpos = screen.get_width()-bigtext.get_width()-20
		else:
			xpos = screen.get_width()/2 - bigtext.get_width()/2
	else:
		xpos = screen.get_width()/2 - bigtext.get_width()/2
	
	running = 1
	
	screen.blit(bg, (0, 0))
	screen.blit(bigtext, (xpos, ypos))
	screen.blit(littletext, (screen.get_width()/2 - littletext.get_width()/2, screen.get_height() - 50))
	pygame.display.update()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		if pygame.mouse.get_pressed()[0]:
			running = False
