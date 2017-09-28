#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Visitors import *
from DITTree import *
import sys, glob, json

class Examiner():

	nocVisitor = NOCVisitor()
	ditVisitor = DITVisitor()
	wmcVisitor = WMCVisitor()
	root = ast.AST()
	directories = []
	tree = DITTree()

	def getDirectories(self, projectFolder):
		os.chdir(projectFolder)
		for directory, folderName, file in os.walk("."):
			for name in file:
				if name.endswith(".py"):
					self.directories.append(os.path.join(directory, name))

	def getAST(self, directory):
		with open(directory, "r") as input:
			# reads the content of this file
			file_str  = input.read()
			# parses the content of this file
			self.root = ast.parse(file_str)

	def WMC(self):
		print self.wmcVisitor.classes


	def NOC(self):
		with open("NOC_","w") as input:
			input.write(json.dumps(self.nocVisitor.superclasses, ensure_ascii=False, indent=4))

	def DIT(self):		
		aux = self.ditVisitor.superclasses['Object']
		self.tree.add('Object')
		self.treeADD(aux, 'Object')
		print self.tree

	def runMetrics(self):
		for file in self.directories:
			print("Opening file:{}".format(file))
			with open(file, "r") as input:
				self.getAST(file)
				self.nocVisitor.visit(self.root)
				self.ditVisitor.visit(self.root)
				self.wmcVisitor.visit(self.root)
		self.DIT()
		self.WMC()
		self.NOC()

	def treeADD(self, children, father):
		if children.__len__()==0:
			return None
		else:
			for child in children:
				self.tree.add(child, father)
				self.treeADD(self.ditVisitor.superclasses[child], child)


if __name__ == "__main__" :
	detector = Examiner()
	if len(sys.argv) >=2:
		detector.getDirectories(sys.argv[1])
	else:
		detector.getDirectories('.')

	detector.runMetrics()


'''
print 'Object depth: {}'.format(detector.tree.depth('Object'))
print 'NodeVisitor depth: {}'.format(detector.tree.depth('NodeVisitor'))
print 'Examiner depth: {}'.format(detector.tree.depth('Examiner'))
'''

