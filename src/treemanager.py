import gameglobals
import time

class AnimationTimer:

	def __init__(self):
		self.frame = 0
		self.maxFrame = 15

	def update(self):
		if (self.frame < self.maxFrame):
			self.frame += 1

	def reset(self):
		self.frame = 0


class EdgeLine:

	def __init__(self, position, animationTimer, fromNode, toNode):
		self.fromPosition = list(position)
		self.fromOriginalPosition = list(position)
		self.fromTargetPosition = list(position)
		self.toPosition = list(position)
		self.toOriginalPosition = list(position)
		self.toTargetPosition = list(position)

		self.animationTimer = animationTimer
		self.fromNode = fromNode
		self.toNode = toNode

	def update(self):
		for i in range (0,2):
			diff = self.fromTargetPosition[i] - self.fromOriginalPosition[i]
			diff *= self.animationTimer.frame
			diff //= self.animationTimer.maxFrame
			self.fromPosition[i] = self.fromOriginalPosition[i] + diff

			diff = self.toTargetPosition[i] - self.toOriginalPosition[i]
			diff *= self.animationTimer.frame
			diff //= self.animationTimer.maxFrame
			self.toPosition[i] = self.toOriginalPosition[i] + diff


	def reverse(self):
		temp = self.fromPosition
		self.fromPosition = self.toPosition
		self.toPosition = temp

		temp = self.fromOriginalPosition
		self.fromOriginalPosition = self.toOriginalPosition
		self.toOriginalPosition = temp

		temp = self.fromTargetPosition
		self.fromTargetPosition = self.toTargetPosition
		self.toTargetPosition = temp

		temp = self.fromNode
		self.fromNode = self.toNode
		self.toNode = temp

	def switchFromNode(self, newNode):
		self.fromNode = newNode

	def switchToNode(self, newNode):
		self.toNode = newNode

	def reposition(self):
		for i in range (0,2):
			self.fromOriginalPosition[i] = self.fromPosition[i]
			self.fromTargetPosition[i] = self.fromNode.position[i]
			self.toOriginalPosition[i] = self.toPosition[i]
			self.toTargetPosition[i] = self.toNode.position[i]



class NodeCircle:

	def __init__(self, position, size, animationTimer, index):
		self.position = list(position)
		self.originalPosition = list(position)
		self.targetPosition = list(position)
		self.animationTimer = animationTimer
		self.radius = size
		self.index = index
		self.renderedText = None
		self.renderedBalance = None

	def update(self):
		for i in range (0,2):
			diff = self.targetPosition[i] - self.originalPosition[i]
			diff *= self.animationTimer.frame
			diff //= self.animationTimer.maxFrame
			self.position[i] = self.originalPosition[i] + diff

	def relocate(self, targetPosition):
		for i in range (0,2):
			self.originalPosition[i] = self.position[i]
			self.targetPosition[i] = targetPosition[i]


class TreeNode:
	def __init__(self, data, parent, left, right, index):
		self.data = data
		self.parent = parent
		self.left = left
		self.right = right
		self.index = index
		self.position = [0,0]
		self.treeWidth = 0
		self.parentEdge = None
		self.balance = 0

	def assignParentEdge(self, parentEdge):
		self.parentEdge = parentEdge


class Tree:
	middleWidth = 15
	halfCircleWidth = 25
	circleSize = 20
	yDisplacement = 45

	def __init__(self):
		self.root = None
		self.animationTimer = AnimationTimer()
		self.nodeCircles = []
		self.edgeLines = []
		self.treeNodes = []
		self.height = 0

	def update(self):
		self.animationTimer.update()
		for nodeCircle in self.nodeCircles:
			nodeCircle.update()
		for edgeLine in self.edgeLines:
			edgeLine.update()

	def valueOf(self, nodeCircle):
		return self.treeNodes[nodeCircle.index].data
	
	def balanceOf(self, nodeCircle):
		return self.treeNodes[nodeCircle.index].balance

	def size(self):
		return len(self.treeNodes)

	def createNewEdge(self, fromNode, toNode):
		edgeLine = EdgeLine(fromNode.position, self.animationTimer, fromNode, toNode)
		toNode.assignParentEdge(edgeLine)
		self.edgeLines.append(edgeLine)


	def createNewNode(self, data, parent, left, right):
		index = len(self.treeNodes)
		if (parent == None):
			position = [0,0]
		else:
			position = parent.position

		node = TreeNode(data, parent, left, right, index)
		nodeCircle = NodeCircle(position, self.circleSize, self.animationTimer, index)

		self.treeNodes.append(node)
		self.nodeCircles.append(nodeCircle)

		return node

	def indexOf(self, data):
		for i in range (0,len(self.treeNodes)):
			if self.treeNodes[i].data == data:
				return i
		return None

	def indexRemove(self, index):
		last = len(self.treeNodes)-1
		if gameglobals.player.isSelected(index):
			gameglobals.player.relocate(self.treeNodes[index].parent)

		if (index == last):
			self.nodeCircles.pop()
			self.treeNodes.pop()
		else:
			self.treeNodes[index] = self.treeNodes.pop()
			self.nodeCircles[index] = self.nodeCircles.pop()
			self.treeNodes[index].index = index
			self.nodeCircles[index].index = index

	def remove(self, data):
		index = self.indexOf(data)
		self.removeByIndex(index)
		self.generatePositions()

	def removeByIndex(self, index):
		node = self.treeNodes[index]
		if node.left == None: 
			if node == self.root:
				self.root = node.right
			else:
				if (node.parent.right == node):
					node.parent.right = node.right
				else:
					node.parent.left = node.right
				self.edgeLines.remove(node.parentEdge)

			if node.right != None: 
				node.right.parent = node.parent
				if (node.parent == None):
					self.edgeLines.remove(node.right.parentEdge)
				else:
					node.right.parentEdge.switchFromNode(node.parent)
			self.indexRemove(index)

		elif node.right == None:
			if node == self.root:
				self.root = node.left
			else:
				if (node.parent.right == node):
					node.parent.right = node.left
				else:
					node.parent.left = node.left
				self.edgeLines.remove(node.parentEdge)

			node.left.parent = node.parent
			if (node.parent == None):
				self.edgeLines.remove(node.left.parentEdge)
			else:
				node.left.parentEdge.switchFromNode(node.parent)
			self.indexRemove(index)

		else: 
			successor = self.inorderSuccessor(node)
			self.reassignData(node, successor.data)
			self.removeByIndex(successor.index)


	def inorderSuccessor(self, node):
		current = node.right
		while current.left != None:
			current = current.left
		return current


	def reassignData(self, node, data):
		node.data = data
		self.nodeCircles[node.index].renderedText = None


	def add(self, data):
		if (self.root == None):
			self.root = self.createNewNode(data, None, None, None)
		else:
			self.root = self.addRecursive(None, self.root, data)
		self.generatePositions()

	def addRecursive(self, parent, node, data):
		if (node == None):
			newNode = self.createNewNode(data, parent, None, None)
			self.createNewEdge(parent, newNode)
			return newNode

		if (data < node.data):
			node.left = self.addRecursive(node, node.left, data)
			return node
		elif (data > node.data):
			node.right = self.addRecursive(node, node.right, data)
			return node
		else:
			return node


	def rotateRight(self, node):
		if (node.left == None):
			return

		node.left.parentEdge.reverse()
		parentEdge = node.parentEdge
		node.parentEdge = node.left.parentEdge

		if (node.parent == None):
			self.root = node.left
		else:
			parentEdge.switchToNode(node.left)
			if (node.parent.left == node):
				node.parent.left = node.left
			else: 
				node.parent.right = node.left
			
		node.left.parent = node.parent
		node.left.parentEdge = parentEdge
		
		if (node.left.right != None):
			node.left.right.parentEdge.switchFromNode(node)
			node.left.right.parent = node

		node.parent = node.left
		node.left = node.left.right
		node.parent.right = node
		self.generatePositions()

	def rotateLeft(self, node):
		if (node.right == None):
			return

		node.right.parentEdge.reverse()
		parentEdge = node.parentEdge
		node.parentEdge = node.right.parentEdge

		if (node.parent == None):
			self.root = node.right
		else:
			parentEdge.switchToNode(node.right)
			if (node.parent.right == node):
				node.parent.right = node.right
			else:
				node.parent.left = node.right
			
		node.right.parent = node.parent
		node.right.parentEdge = parentEdge
		
		if (node.right.left != None):
			node.right.left.parentEdge.switchFromNode(node)
			node.right.left.parent = node

		node.parent = node.right
		node.right = node.right.left
		node.parent.left = node
		self.generatePositions()


	def printInOrder(self):
		output = self.inOrderToString(self.root)
		print(output)

	def inOrderToString(self, node):
		if (node == None):
			return ""
		else:
			return self.inOrderToString(node.left) + " " + \
				str(self.nodeCircles[node.index].targetPosition) + " " + self.inOrderToString(node.right) 

	def recomputeBalancesUpdateHeight(self):
		self.height = self.computeBalanceReturnHeight(self.root)

	def computeBalanceReturnHeight(self, node):
		if (node == None): return 0
		leftHeight = self.computeBalanceReturnHeight(node.left)
		rightHeight = self.computeBalanceReturnHeight(node.right)
		self.updateBalance(node, rightHeight - leftHeight)
		
		return 1 + max(leftHeight, rightHeight)

	def updateBalance(self, node, newBalance):
		if (newBalance != node.balance):
			node.balance = newBalance
			self.nodeCircles[node.index].renderedBalance = None

	def generateTreeWidth(self, node):
		if (node == None): return self.halfCircleWidth

		node.treeWidth = self.middleWidth + \
			self.generateTreeWidth(node.left) + self.generateTreeWidth(node.right)

		return node.treeWidth

	def generatePositionLeft(self, node, parent):
		if (node == None): return

		distance = self.middleWidth
		if (node.right == None):
			distance += self.halfCircleWidth
		else:
			distance += node.right.treeWidth

		node.position[0] = parent.position[0] - distance
		node.position[1] = parent.position[1] + self.yDisplacement

	def generatePositionRight(self, node, parent):
		if (node == None): return

		distance = self.middleWidth
		if (node.left == None):
			distance += self.halfCircleWidth
		else:
			distance += node.left.treeWidth
			
		node.position[0] = parent.position[0] + distance
		node.position[1] = parent.position[1] + self.yDisplacement

	def generatePositionsRecurse(self, node):
		if (node == None): return

		self.generatePositionLeft(node.left, node)
		self.generatePositionRight(node.right, node)
		self.generatePositionsRecurse(node.left)
		self.generatePositionsRecurse(node.right)

	def generatePositions(self):
		if self.root == None: return
		self.recomputeBalancesUpdateHeight()
		self.generateTreeWidth(self.root)
		self.root.position = [0,0]
		self.generatePositionsRecurse(self.root)
		self.updatePositions()

	def updatePositions(self):
		self.animationTimer.reset()
		for i in range (0,len(self.treeNodes)):
			self.nodeCircles[i].relocate(self.treeNodes[i].position)
		for edgeLine in self.edgeLines:
			edgeLine.reposition()

	def imbalance(self, node):
		absBalance = abs(node.balance)
		return absBalance 

	def totalImbalance(self):
		maxImbalance = 0
		for node in self.treeNodes:
			if self.imbalance(node) > maxImbalance:
				maxImbalance = self.imbalance(node)
		return maxImbalance


def initialise():
	gameglobals.tree = Tree()


def update():
	gameglobals.tree.update()

