#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
			parentName = self.get_call_name(n)
			#print(parentName)
			if str(parentName) not in self.superclasses:
				self.superclasses[parentName] = [node.name]
			elif node.name not in self.superclasses[parentName]:
				self.superclasses[parentName].append(node.name)

		

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
		if len(node.bases) == 0:#classe sem Pai
			self.superclasses['Object'].append(node.name)
			self.superclasses[node.name] = []
			#print(self.superclasses['Object'])
		else:
			for n in node.bases:
				parentName = self.get_call_name(n)
				if parentName not in self.superclasses['Object']:#caso em que não foi encontrado (ainda) uma definição para a classe pai
					self.superclasses['Object'].append(parentName)#adiciona o pai aos filhos diretos de Object
					self.superclasses[parentName] = [node.name]#cria a lista de filhos
				else:#definição para a classe pai foi encontrada
					self.superclasses[parentName].append(node.name)
					if node.name in self.superclasses['Object']:#encontrado uma classe pai definida, classe filha não pode ser filha direta de Object
						self.superclasses['Object'].remove(node.name)
			if node.name not in self.superclasses:
				self.superclasses[node.name] = [] 

class BodyVisitor(ast.NodeVisitor):

	complexity = 1

	def helper(self, node):
		self.complexity += 1
		super(BodyVisitor, self).generic_visit(node)

	def visit_IfExp(self, node):
		self.complexity += 1

	def visit_If(self, node):
		self.helper(node)		

	def visit_For(self, node):
		self.helper(node)

	def visit_While(self, node):
		self.helper(node)

	def visit_Break(self, node):
		self.complexity += 1

	def visit_Continue(self, node):
		self.complexity += 1

	def visit_Try(self, node):
		self.helper(node)

	def visit_TryFinally(self, node):
		self.helper(node)

	def visit_TryExcept(self, node):
		self.helper(node)

	def visit_ExceptHandler(self, node):
		self.helper(node)

	def visit_With(self, node):
		self.helper(node)

	def visit_withitem(self, node):
		self.helper(node)

	def visit_Lambda(self, node):
		super(BodyVisitor, self).generic_visit(node)

class WMCVisitor(ast.NodeVisitor):
	
	classes = {}
	bodyvisitor = BodyVisitor()

	def visit_ClassDef(self, node):
		super(WMCVisitor, self).generic_visit(node)
		self.classes[node.name] = self.bodyvisitor.complexity
		self.bodyvisitor.complexity = 0

	def visit_FunctionDef(self, node):
		self.bodyvisitor.complexity +=1
		super(BodyVisitor, self.bodyvisitor).generic_visit(node)
	

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
	        v = WMCVisitor()
	        v.visit(root)
	        print v.classes