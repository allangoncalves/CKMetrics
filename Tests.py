import unittest
from DITTree import *

class TreeTests(unittest.TestCase):

	def setUp(self):
		self.tree = DITTree()
		self.tree.add(10)
		self.tree.add(20, 10)
		self.tree.add(30, 10)
		self.tree.add(50, 20)
		self.tree.add(40, 20)
		self.tree.add(70, 20)
		self.tree.add(78, 70)
		self.tree.add(11, 30)

	def test_tree_add(self):
		self.assertEqual(self.tree.__str__(), '10(20(50(),40(),70(78())),30(11()))')

	def test_tree_notFoundException(self):
		self.assertRaises(NodeNotFoundException, self.tree.depth, 555)

	def test_tree_length(self):
		self.assertEqual(self.tree.length(), 8)

if __name__ == '__main__':
	unittest.main()