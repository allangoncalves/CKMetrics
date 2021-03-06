#!/usr/bin/env python
# -*- coding: utf-8 -*-
class NodeNotFoundException(Exception):

	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)


class Node:

	def __init__(self, key, children=None):
		self.key = key
		self.children = children or []
	
	def __str__(self):
		return str(self.key)

class DITTree:

	def __init__(self):
		self.root = None
		self.size = 0

	def find_node(self, node, key):
		if node == None or node.key == key:
			return node		
		for child in node.children:
			return_node = self.find_node(child, key)
			if return_node: 
				return return_node
		return None

	def depth(self, key):
		node = self.find_node(self.root, key)
		if not node:
			raise NodeNotFoundException('No element was found.')
		return self.auxDepth(node) 

	def auxDepth(self, node):
		if not node.children:
			return 0

		maxdepth = []		
		
		for child in node.children:
			maxdepth.append(self.auxDepth(child)) 
		
		return 1 + max(maxdepth)

	def add(self, new_key, parent_key=None):
		new_node = Node(new_key)
		if not parent_key:
			self.root = new_node
			self.size = 1
		else:
			parent_node = self.find_node(self.root, parent_key)
			if not parent_node:
				raise NodeNotFoundException('No element was found with the informed parent key.')
			parent_node.children.append(new_node)
			self.size += 1
	
	def print_tree(self, node, str_aux):
		if node == None: return ""
		str_aux += str(node) + '('
		for child in node.children:
			end = ',' if child is not node.children[-1] else ''
			str_aux = self.print_tree(child, str_aux) + end
		str_aux += ')'
		return str_aux

	def is_empty(self):
		return self.size == 0

	def length(self):
		return self.size

	def __str__(self):
		return self.print_tree(self.root, "")