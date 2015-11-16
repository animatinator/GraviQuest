import pygame, sys
from lib import *


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GraviQuest")

music = None

level = 1
area = 1

def PlayLevel(area, level):
    global music
    
    areaname = "Area %i"%(area)
    currentLevel = Level(screen, areaname, level)
    returnval = currentLevel.MainLoop()

    if returnval == "quit":
        ShowMenu()
    elif returnval == "fail":
        PlayLevel(area, level)
    elif returnval == "win":
        level += 1
        try:
            PlayLevel(area, level)
        except:
            try:
                area += 1
                level = 1
                areaname = "Area %i"%(area)
                music.stop()
                music = pygame.mixer.Sound(os.path.join(areaname, "music.ogg"))
                areatitle = open(os.path.join(areaname, "name")).read()
                ShowTitle(screen, "Area %i"%area, areatitle, os.path.join(areaname, "bg.png"))
                music.play(-1)
                PlayLevel(area, level)
            except:
                music.stop()
                creditscreen = Credits(screen, "credits.txt")
                creditscreen.Run()
                return
    return

def ShowMenu():
    global area, level, music

    try:
        music.stop()
    except:
        pass

    music = pygame.mixer.Sound("Menu.ogg")
    music.play(-1)
    
    menubg = pygame.image.load("menubg.png").convert()
    mainmenu = Menu(screen, 
        [["New game", "new", None], ["Load game", "load", [["File 1", 1], ["File 2", 2], ["File 3", 3], ["File 4", 4]] ], ["Tutorial", "tutorial", None], ["Credits", "credits", None], ["Quit", "quit", None]],
        (400, 300), 200, 100, (100, 255, 50), (75, 150, 50), menubg, True)
    selection = mainmenu.ShowMenu()

    music.fadeout(1000)

    if selection == "new":
        area = 1
        level = 1
        areaname = "Area %i"%(area)
        music = pygame.mixer.Sound(os.path.join(areaname, "music.ogg"))
        areatitle = open(os.path.join(areaname, "name")).read()
        ShowTitle(screen, "Area %i"%area, areatitle, os.path.join(areaname, "bg.png"))
        music.play(-1)
        PlayLevel(area, level)
        ShowMenu()
    
    elif selection.find("load") != -1:
        filename = selection.replace("load", "")

        saves = open("files.gqs", "r").readlines()
        gamefile = saves[int(filename) - 1].split("-")
        area, level = gamefile

        area = int(area)
        level = int(level)
        
        areaname = "Area %i"%(area)
        music = pygame.mixer.Sound(os.path.join(areaname, "music.ogg"))
        areatitle = open(os.path.join(areaname, "name")).read()
        ShowTitle(screen, "Area %i"%area, areatitle, os.path.join(areaname, "bg.png"))
        music.play(-1)

        PlayLevel(area, level)
        
    elif selection == "tutorial":
        tutorial = Tutorial(screen)
        returnval = tutorial.MainLoop()

        if returnval == "quit":
            ShowMenu()
        elif returnval == "fail":
            ShowMenu()
        elif returnval == "win":
            ShowMenu()
    
    elif selection == "credits":
        creditscreen = Credits(screen, "credits.txt")
        creditscreen.Run()
        ShowMenu()
    
    elif selection == "quit":
        pygame.quit()
        sys.exit()

while 1:
    ShowMenu()
