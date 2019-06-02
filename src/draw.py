import gameglobals
import pygame
import pygame.font
pygame.font.init()


class Graphics:

	def __init__(self):
		self.background = pygame.image.load("../img/bggraphic.png")
		bgRect = self.background.get_rect()
		self.bgHalfSize = [bgRect[2]//2, bgRect[3]//2]

		self.node_unselected = pygame.image.load("../img/node.png")
		self.node_selected = pygame.image.load("../img/nodeSelected.png")
		nodeRect = self.node_selected.get_rect()
		self.nodeHalfSize = nodeRect[2]//2

		self.nodeGlow = pygame.image.load("../img/nodeglow.png")
		nodeGlowRect = self.nodeGlow.get_rect()
		self.nodeGlowHalfSize = nodeGlowRect[2]//2

		self.text_operations = None
		self.text_operations_value = None
		self.text_treeSize = None
		self.text_treeSize_value = None
		self.text_treeHeight = None
		self.text_treeHeight_value = None

		self.nextText = None


	def gameOver(self, isVictory):
		if isVictory:
			self.gameOverMessage = pygame.image.load("../img/victory.png")
		else:
			self.gameOverMessage = pygame.image.load("../img/defeat.png")

		messageRect = self.gameOverMessage.get_rect()
		self.messageHalfSize = [messageRect[2]//2, messageRect[3]//2]


offset = [gameglobals.size[0]//2, gameglobals.size[1]*5//11]
balanceYOffset = 30
normalColours = False

font = pygame.font.SysFont(None, 24)
statsFont = pygame.font.SysFont(None, 20)
opsFont = pygame.font.SysFont(None, 22)


def drawOther(): return None


def uninitialise():
	global graphics, drawOther
	graphics = None
	normalColours = False
	def drawOther(): return None


def initialise():
	global normalColours, graphics
	global BACKGROUND_COLOUR, NODE_TEXT_COLOUR
	global TEXT_COLOUR, LINE_COLOUR

	graphics = Graphics()

	normalColours = True
	BACKGROUND_COLOUR = 0, 0, 0
	NODE_TEXT_COLOUR = 255, 64, 0
	TEXT_COLOUR = 255, 255, 255
	LINE_COLOUR = 255, 255, 255


def drawGameFrame():
	screen = gameglobals.screen

	screen.fill(BACKGROUND_COLOUR)

	global graphics, drawOther
	bgPosition = [gameglobals.cameraCenter[0]*2//7 + offset[0] - graphics.bgHalfSize[0],
               gameglobals.cameraCenter[1]//2 + offset[1] - graphics.bgHalfSize[1]]
	screen.blit(graphics.background, bgPosition)

	drawGameScene()
	drawGameOverMessage()
	drawOther()

	pygame.display.flip()


def drawGameScene():
	screen = gameglobals.screen
	global offset, font, balanceYOffset, graphics

	center = [gameglobals.cameraCenter[0] + offset[0],
           gameglobals.cameraCenter[1] + offset[1]]

	for edgeLine in gameglobals.tree.edgeLines:
		fromPos = [center[0] + edgeLine.fromPosition[0],
                    center[1] + edgeLine.fromPosition[1]]
		toPos = [center[0] + edgeLine.toPosition[0],
                    center[1] + edgeLine.toPosition[1]]
		pygame.draw.line(screen, LINE_COLOUR, fromPos, toPos, 3)

	for nodeCircle in gameglobals.tree.nodeCircles:
		balance = gameglobals.tree.balanceOf(nodeCircle)

		position = [center[0] + nodeCircle.position[0],
                    center[1] + nodeCircle.position[1]]

		if (abs(balance) >= 2):
			circlePos = [position[0] - graphics.nodeGlowHalfSize,
                            position[1] - graphics.nodeGlowHalfSize]
			image = graphics.nodeGlow
			screen.blit(image, circlePos)
			if (abs(balance) > 2):
				screen.blit(image, circlePos)

		circlePos = [position[0] - graphics.nodeHalfSize,
                    position[1] - graphics.nodeHalfSize]
		if gameglobals.player.isSelected(nodeCircle.index):
			image = graphics.node_selected
		else:
			image = graphics.node_unselected
		screen.blit(image, circlePos)

		if (nodeCircle.renderedText == None):
			nodeCircle.renderedText = font.render(
				str(gameglobals.tree.valueOf(nodeCircle)), True, NODE_TEXT_COLOUR)
		textPos = [position[0]-nodeCircle.renderedText.get_width()//2,
                    position[1]-nodeCircle.renderedText.get_height()//2]
		screen.blit(nodeCircle.renderedText, textPos)

		if (nodeCircle.renderedBalance == None):
			nodeCircle.renderedBalance = font.render(str(balance), True, TEXT_COLOUR)
		textPos = [position[0]-nodeCircle.renderedBalance.get_width()//2,
                    position[1]-nodeCircle.renderedBalance.get_height()//2 - balanceYOffset]
		screen.blit(nodeCircle.renderedBalance, textPos)


def drawGameOverMessage():
	if not gameglobals.gameStats.gameOver:
		return
	global graphics
	screen = gameglobals.screen
	size = gameglobals.size
	position = [size[0]//2 - graphics.messageHalfSize[0],
             size[1]//2 - graphics.messageHalfSize[1]]
	screen.blit(graphics.gameOverMessage, position)
