#!/usr/bin/python
import ast
import os

class NOCVisitor(ast.NodeVisitor):

	superclasses = {}

	def visit_ClassDef(self, node):
		for n in node.bases:
			print(n.attr)
			if str(n.attr) not in self.superclasses:
				self.superclasses[n.attr] = [node.name]
			elif node.name not in self.superclasses[n.attr]:
				self.superclasses[n.attr].append(node.name)

	def printDict(self):
		print(self.superclasses)
		

class DITVisitor(ast.NodeVisitor):
	
	superclasses = {'Object': []}

	def visit_ClassDef(self, node):
		if len(node.bases) == 0:
			if node.name not in self.superclasses['Object']:
				self.superclasses['Object'].append(node.name)
				self.superclasses[node.name] = []
				print(self.superclasses['Object'])
		else:
			for n in node.bases:
				if n.attr not in self.superclasses['Object']:
					self.superclasses['Object'].append(n.attr)
					self.superclasses[n.attr] = [node.name]
				else:
					if node.name not in self.superclasses[n.attr]:
						self.superclasses[n.attr].append(node.name)
					if node.name in self.superclasses['Object']:
						self.superclasses['Object'].remove(n.attr)
				self.superclasses[node.name] = []



				'''if str(n.attr) not in self.superclasses:
					self.superclasses[n.attr] = [node.name]
					self.superclasses['Object'].append(node.name)
				elif node.name not in self.superclasses[n.attr]:
					self.superclasses[n.attr].append(node.name)
				'''

if __name__ == "__main__":
    
    import glob
    import sys
    

    if len(sys.argv) == 2 :
    	os.chdir(sys.argv[1])
    input_files = glob.glob('./*.py')

    for file in input_files:
        print("Opening:{}".format(file))
        with open(file, "r") as input:
    		# reads the content of this file
        	file_str  = input.read()

	        # parses the content of this file
	        root = ast.parse(file_str)

	        # visits the Abstract Syntax Tree
	        v = NOCVisitor()
	        v.visit(root)
	        v.printDict()