import pygame, sys
from lib import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GraviQuest")

level = 1
area = 1

def PlayLevel(area, level):
    areaname = "Area %i"%(area)
    currentLevel = Level(screen, areaname, level)
    returnval = currentLevel.MainLoop()

    if returnval == "quit":
        ShowMenu()
    elif returnval == "fail":
        showTitle(screen, "Area %i : Level %i"%(area, level), size = 50, pos = "Centre")
        PlayLevel(area, level)
    elif returnval == "win":
        level += 1
        try:
            showTitle(screen, "Area %i : Level %i"%(area, level), size = 50, pos = "Centre")
            PlayLevel(area, level)
        except:
            try:
                area += 1
                level = 1
                showTitle(screen, "Area %i : Level %i"%(area, level), size = 50, pos = "Centre")
                PlayLevel(area, level)
            except:
                creditscreen = Credits(screen, "credits.txt")
                creditscreen.Run()
                return
    return

def ShowMenu():
    global area, level
    
    menubg = pygame.image.load("menubg.png").convert()
    mainmenu = Menu(screen, 
        [["New game", "new", None], ["Load game", "load", [["File 1", 1], ["File 2", 2], ["File 3", 3], ["File 4", 4]] ], ["Instructions", "instruct", None], ["Credits", "credits", None], ["Quit", "quit", None]],
        (400, 300), 200, 100, (100, 255, 50), (75, 150, 50), menubg, True)
    selection = mainmenu.ShowMenu()

    if selection == "new":
        showTitle(screen, "Area %i : Level %i"%(area, level), size = 50, pos = "Centre")
        PlayLevel(area, level)
        ShowMenu()
    
    elif selection.find("load") != -1:
        filename = selection.replace("load", "")

        saves = open("files.gqs", "r").readlines()
        gamefile = saves[int(filename) - 1].split("-")
        area, level = gamefile

        area = int(area)
        level = int(level)

        PlayLevel(area, level)
        
    elif selection == "instruct":
        pass
    
    elif selection == "credits":
        creditscreen = Credits(screen, "credits.txt")
        creditscreen.Run()
        ShowMenu()
    
    elif selection == "quit":
        sys.exit()

while 1:
    ShowMenu()
