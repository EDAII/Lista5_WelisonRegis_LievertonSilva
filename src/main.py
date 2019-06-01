import sys
import pygame
import keyinput
import gameglobals
import menucontrol
import menudraw
pygame.init()

inMenu = True
frame = None


def eventRead():
	global inMenu
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if (inMenu):
				keyinput.keyPressMenu(event.key)


def initialiseGame(args, mode):
	uninitialiseMenu()

	global inMenu, frame
	inMenu = False
	frame = 0

def uninitialiseMenu():
	menudraw.uninitialise()


def initialiseMenu():

	global inMenu
	inMenu = True
	menudraw.initialise()
	menucontrol.initialise(lambda rate, size: initialiseGame([rate, size], 0),
                        None,
                        lambda: initialiseGame(None, 3))


def menuUpdate():
	menucontrol.update()


def main():
	global inMenu
	initialiseMenu()
	while 1:
		eventRead()
		if inMenu:
			menuUpdate()

		if inMenu:
			menudraw.drawMenuFrame()
		pygame.time.delay(20)


main()
