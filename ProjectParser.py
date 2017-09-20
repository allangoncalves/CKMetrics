from Visitors import *
import sys
import glob
import json

class Examiner():

	myVisitor = NOCVisitor()
	root = ast.AST()
	directories = []

	def getDirectories(self, projectFolder):
		os.chdir(projectFolder)
		for directory, folderName, file in os.walk("."):
			for name in file:
				if name.endswith(".py"):
					self.directories.append(os.path.join(directory, name))
		print(self.directories)

	def getAST(self, directory):
		with open(directory, "r") as input:
			# reads the content of this file
			file_str  = input.read()
			# parses the content of this file
			self.root = ast.parse(file_str)

	def NOC(self):
		for file in self.directories:
			print("Opening file:{}".format(file))
			with open(file, "r") as input:
				self.getAST(file)
				self.myVisitor.visit(self.root)
				print(self.myVisitor.superclasses)
		os.chdir(sys.argv[1])
		with open("NOC_","w") as input:
			input.write(json.dumps(detector.myVisitor.superclasses, ensure_ascii=False, indent=4))

	def DIT(self):
		pass
		



if __name__ == "__main__" :
	
	detector = Examiner()
	detector.getDirectories(sys.argv[1])
	detector.NOC()
		


