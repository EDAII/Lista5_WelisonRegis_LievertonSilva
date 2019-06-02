import gameglobals
from enum import IntEnum


class MenuScreen(IntEnum):
	main = 0
	mode_start = 1


class MenuVars:
	numOptions = [2, 0]

	def __init__(self):
		self.currentOptions = [0]*len(self.numOptions)
		self.buttonOperations = self.defineButtonOperations()
		self.backOperations = self.defineBackOperations()
		self.currentMenu = MenuScreen.main
		self.optionsTextRender = self.generateEmptyArray()

	def generateEmptyArray(self):
		numMenus = len(self.numOptions)
		arr = [[]]*numMenus
		for i in range(0, numMenus):
			arr[i] = [None]*self.numOptions[i]
		return arr

	def defineButtonOperations(self):
		operations = self.generateEmptyArray()

		operations[0][0] = lambda: start_start(60, 20)
		operations[0][1] = lambda: start_tutorial()

		# operations[1][0] = lambda : start_start(90, 20)
		# operations[1][1] = lambda : start_start(80, 30)
		# operations[1][2] = lambda : start_start(70, 40)
		# operations[1][3] = lambda : start_start(60, 80)

		return operations

	def defineBackOperations(self):
		operations = [MenuScreen.main]*len(self.numOptions)

		return operations

	def currentOption(self):
		return self.currentOptions[self.currentMenu]

	def goToMenu(self, toMenu):
		self.currentMenu = toMenu

	def goDown(self):
		self.currentOptions[self.currentMenu] += 1
		if self.currentOptions[self.currentMenu] >= self.numOptions[self.currentMenu]:
			self.currentOptions[self.currentMenu] = 0

	def goUp(self):
		self.currentOptions[self.currentMenu] -= 1
		if self.currentOptions[self.currentMenu] < 0:
			self.currentOptions[self.currentMenu] = self.numOptions[self.currentMenu]-1

	def enter(self):
		operation = self.buttonOperations[self.currentMenu][self.currentOptions[self.currentMenu]]
		if operation != None:
			operation()

	def goBack(self):
		self.goToMenu(self.backOperations[self.currentMenu])


start_start = None
start_construction = None
start_tutorial = None


def initialise(startStartFunction, constructionStartFunction, tutorialStartFunction):
	global start_start, start_endless, start_construction, start_tutorial
	start_start = startStartFunction
	start_construction = constructionStartFunction
	start_tutorial = tutorialStartFunction

	gameglobals.menu = MenuVars()


def update():
	pass
