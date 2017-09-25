#!/usr/bin/python
import ast
import os

class NOCVisitor(ast.NodeVisitor):

	superclasses = {}

	def get_call_name(self, node):
		if isinstance(node, ast.Name):
			return node.id
		elif isinstance(node, ast.Attribute):
			return node.attr
		else:
			raise NotImplementedError("Could not extract call-name from node: " + str(node))

	def visit_ClassDef(self, node):
		for n in node.bases:
			fatherName = self.get_call_name(n)
			#print(fatherName)
			if str(fatherName) not in self.superclasses:
				self.superclasses[fatherName] = [node.name]
			elif node.name not in self.superclasses[fatherName]:
				self.superclasses[fatherName].append(node.name)

	def printDict(self):
		print(self.superclasses)
		

class DITVisitor(ast.NodeVisitor):
	
	superclasses = {'Object': []}

	def get_call_name(self, node):
		if isinstance(node, ast.Name):
			print 'Name'
			return node.id
		elif isinstance(node, ast.Attribute):
			print 'Attribute'
			return node.attr
		else:
			raise NotImplementedError("Could not extract call-name from node: " + str(node))

	def visit_ClassDef(self, node):
		if len(node.bases) == 0:
			if node.name not in self.superclasses['Object']:
				self.superclasses['Object'].append(node.name)
				self.superclasses[node.name] = []
				#print(self.superclasses['Object'])
		else:
			for n in node.bases:
				fatherName = self.get_call_name(n)
				if fatherName not in self.superclasses['Object']:
					self.superclasses['Object'].append(fatherName)
					self.superclasses[fatherName] = [node.name]
				else:
					if node.name not in self.superclasses[fatherName]:
						self.superclasses[fatherName].append(node.name)
					if node.name in self.superclasses['Object']:
						self.superclasses['Object'].remove(fatherName)
				self.superclasses[node.name] = []

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