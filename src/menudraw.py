import os
import gameglobals
import pygame
import pygame.font
pygame.font.init()

BACKGROUND_COLOUR = 0, 0, 0
BUTTON_COLOUR_GLOW = 255, 255, 0
BUTTON_COLOUR_INNER = 0, 64, 255
BUTTON_COLOUR_OUTER = 0, 0, 127
WHITE = 255, 255, 255

drawMenu = [lambda screen, selection,
            renders: drawMenu_main(screen, selection, renders)]

font = pygame.font.SysFont(None, 32)


class MenuGraphics:

	def __init__(self):
		self.background = pygame.image.load(os.path.join("img", "background.png"))



graphics = None


def uninitialise():
	global graphics
	graphics = None


def initialise():
	global graphics
	graphics = MenuGraphics()


def drawMenuFrame():
	screen = gameglobals.screen
	global graphics

	screen.fill(BACKGROUND_COLOUR)
	screen.blit(graphics.background, [0, 0])

	menu = gameglobals.menu
	drawMenu[menu.currentMenu](screen, menu.currentOption(),
                            menu.optionsTextRender[menu.currentMenu])
	pygame.display.flip()


def drawMenu_main(screen, selection, renders):
	drawButton(screen, "START", 0, renders, selection)
	drawButton(screen, "TUTORIAL", 1, renders, selection)


def generateButton(message, index, renders):
	if renders[index] == None:
		renders[index] = font.render(message, True, WHITE)

	nButtons = len(renders)
	x = gameglobals.size[0]//2
	spacing = 100
	y = (gameglobals.size[1] - (nButtons-1)*spacing)//2
	y += index*spacing

	return ([x, y], renders[index])


def drawButton(screen, message, index, renders, selection):
	buttonStats = generateButton(message, index, renders)
	centerPosition = buttonStats[0]
	text = buttonStats[1]
	halfRectWidth = 150
	halfRectHeight = 35

	rect = pygame.Rect(centerPosition[0]-halfRectWidth,
                    centerPosition[1]-halfRectHeight, 2*halfRectWidth, 2*halfRectHeight)

	if (index == selection):
		pygame.draw.rect(screen, BUTTON_COLOUR_GLOW, rect.inflate(10, 10))
	pygame.draw.rect(screen, BUTTON_COLOUR_OUTER, rect)
	pygame.draw.rect(screen, BUTTON_COLOUR_INNER, rect.inflate(-5, -5))

	screen.blit(text, [centerPosition[0]-text.get_width()//2,
                    centerPosition[1]-text.get_height()//2])
