import pygame, lib

screen = pygame.display.set_mode((256, 256))

frames = lib.LoadTiles("10_Set.JPG", 5, 2, None)

clock = pygame.time.Clock()

n = 0
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
	
	screen.blit(frames[n], (0, 0))
	screen.blit(frames[n], (128, 0))
	screen.blit(frames[n], (0, 128))
	screen.blit(frames[n], (128, 128))
	
	if n < len(frames)-1:
		n += 1
	else:
		n = 0
	
	clock.tick(24)
	pygame.display.update()
