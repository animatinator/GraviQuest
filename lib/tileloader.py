import pygame


def LoadTiles(image, x, y, num):
        imgs = []
        try:
                image.get_width()
        except:
                image = pygame.image.load(image).convert_alpha()
        
        imagedim = image.get_width(), image.get_height()
        tiledim = imagedim[0]/x, imagedim[1]/y
        
        for slicey in xrange(y):
                for slicex in xrange(x):
                        workingimage = pygame.transform.chop(image, (0, 0, tiledim[0] * slicex, tiledim[1] * slicey))
                        workingimage = pygame.transform.chop(workingimage, (tiledim[0], tiledim[1], workingimage.get_width(), workingimage.get_height()))
                        
                        imgs.append(workingimage)
        
        del image, imagedim, tiledim

        return imgs
