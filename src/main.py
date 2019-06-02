import sys
import pygame
import keyinput
import treemanager
import draw
import playercontrol
import gameglobals
import cameracontrols
import gamecontrol
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
			else:
				keyinput.keyPress(event.key)


def initialiseGame(args, mode):
	uninitialiseMenu()

	global inMenu, frame
	inMenu = False
	frame = 0

	draw.initialise()
	gameglobals.player = playercontrol.PlayerControl()
	treemanager.initialise()
	playercontrol.initialise()
	cameracontrols.initialise()

	if mode == 0:
		gamecontrol.initialiseStart(args[0], args[1])
	elif mode == 1:
		gamecontrol.initialiseTutorial()
		draw.initialiseTutorial()


def uninitialiseGame():
	draw.uninitialise()


def uninitialiseMenu():
	menudraw.uninitialise()


def gameUpdate():
	global frame
	treemanager.update()
	cameracontrols.cameraUpdate()
	gamecontrol.update(frame)
	frame += 1

	if gameglobals.gameStats.gameExited:
		initialiseMenu()


def initialiseMenu():
	uninitialiseGame()

	global inMenu
	inMenu = True
	menudraw.initialise()
	menucontrol.initialise(lambda rate, size: initialiseGame([rate, size], 0),
                        None,
                        lambda: initialiseGame(None, 1))


def menuUpdate():
	menucontrol.update()


def main():
	global inMenu
	initialiseMenu()
	while 1:
		eventRead()
		if inMenu:
			menuUpdate()
		else:
			gameUpdate()

		if inMenu:
			menudraw.drawMenuFrame()
		else:
			draw.drawGameFrame()
		pygame.time.delay(20)


main()
