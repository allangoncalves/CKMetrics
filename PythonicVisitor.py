#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
from collections import OrderedDict

def get_call_name(node):
	if isinstance(node, ast.Name):
		return node.id
	elif isinstance(node, ast.Attribute):
		return node.attr
	elif isinstance(node, ast.Subscript):
		return get_call_name(node.value)

def default_dict():
		return OrderedDict([('name', ''), ('iterItems', 0), ('setDefault', 0), ('enumerate', 0), 
							('zip', 0), ('sorted', 0), ('multipleAssign', 0),('multipleReturn', 0),
							('in', 0), ('multipleComparison', 0), ('functionalIdioms', 0),
							('comprehension', 0), ('join', 0)]).copy()

class PythonicVisitor(ast.NodeVisitor):

	data = default_dict()
	total_data = data.copy()
	total_data['name'] = 'FULL PROJECT'

	def visit_Assign(self, node):
		if len(node.targets) > 1:
			self.data['multipleAssign'] += 1
			self.total_data['multipleAssign'] += 1
		else:
			if isinstance(node.targets[0], ast.Tuple) or isinstance(node.targets[0], ast.List):
					self.data['multipleAssign'] += 1
					self.total_data['multipleAssign'] += 1
		super(PythonicVisitor, self).generic_visit(node)

	def visit_If(self, node):
		if isinstance(node.test, ast.Compare) and len(node.test.ops) > 1:
			self.data['multipleComparison'] += 1
			self.total_data['multipleComparison'] += 1
		super(PythonicVisitor, self).generic_visit(node)

	def visit_ListComp(self, node):
		self.data['comprehension'] += 1
		self.total_data['comprehension'] += 1
		super(PythonicVisitor, self).generic_visit(node)
	
	def visit_SetComp(self, node):
		self.data['comprehension'] += 1
		self.total_data['comprehension'] += 1
		super(PythonicVisitor, self).generic_visit(node)
	
	def visit_DictComp(self, node):
		self.data['comprehension'] += 1
		self.total_data['comprehension'] += 1
		super(PythonicVisitor, self).generic_visit(node)
	
	def visit_GeneratorExp(self, node):
		self.data['comprehension'] += 1
		self.total_data['comprehension'] += 1
		super(PythonicVisitor, self).generic_visit(node)
	
	def visit_Call(self, node):
		name = get_call_name(node.func)
		if 'map' == name or 'filter' == name or 'reduce' == name or 'apply' == name:
			self.data['functionalIdioms'] += 1
			self.total_data['functionalIdioms'] += 1
		elif 'setdefault' == name:
			self.data['setDefault'] += 1
			self.total_data['setDefault'] += 1
		elif 'iteritems' == name:
			self.data['iterItems'] += 1
			self.total_data['iterItems'] += 1
		elif 'enumerate' == name:
			self.data['enumerate'] += 1
			self.total_data['enumerate'] += 1
		super(PythonicVisitor, self).generic_visit(node)

	def visit_For(self, node):
		if isinstance(node.iter, ast.Call):
			name = get_call_name(node.iter.func)
			if name == 'sorted':
				self.data['sorted'] += 1
				self.total_data['sorted'] += 1
			elif name == 'zip' or name == 'izip':
				self.data['zip'] += 1
				self.total_data['zip'] += 1
		super(PythonicVisitor, self).generic_visit(node)

	def visit_Assign(self, node):
		if isinstance(node.value, ast.Call):
			print node.value
			if get_call_name(node.value.func) == 'join':
				self.data['join'] += 1
				self.total_data['join'] += 1
			print 'close'
		super(PythonicVisitor, self).generic_visit(node)

	
if __name__ == "__main__":

	import os
	import glob
	import sys
	import csv

	if len(sys.argv) == 2 :
		os.chdir(sys.argv[1])

	input_files = glob.glob('./*.py')

	v = PythonicVisitor()
	idioms_list = [['FILE NAME', 'ITERITEMS', 'SETDEFAULT', 'ENUMERATE', 
					'ZIP/IZIP', 'SORTED', 'MULTIPLEASSIGN', 'MULTIPLERETURN',
					'IN', 'MULTIPLECOMPARISON', 'FUNCTIONALIDIOMS', 'COMPREHENSION',
					'JOIN']]

	for file in input_files:
		print("Opening:{}".format(file))
		with open(file, "r") as input:
			file_str  = input.read()
			root = ast.parse(file_str)
			v.data['name'] = file[2:-3]
			v.visit(root)

			idioms_list.append([value for _, value in v.data.iteritems()])
			v.data = default_dict()
	idioms_list.append([value for _, value in v.total_data.iteritems()])
	
	
	#SAVE DATA
	with open('resultado.csv', 'wt') as f:
		print idioms_list
		print 'chegous'
		writer = csv.writer(f)
		writer.writerows(idioms_list)