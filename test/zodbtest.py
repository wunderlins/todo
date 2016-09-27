#!/usr/bin/env python

import sys
sys.path.append("../lib/site-packages")

from ZODB import DB, FileStorage
from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction

class Node(Persistent):
	"""Node"""
	
	def __repr__(self):
		return "<Node [" + str(self._id) + "] " + self.name + ">"
	
	def append(self, node):
		self.children.append(node)
		ix = [i for i,x in enumerate(self.children) if x == node][0]
		self.children[ix]._id = ix 
		self._p_changed = 1 # important to use this on lists
	
	def __init__(self, name):
		self._id = None
		
		self.name = name
		self.desc = ""
		self.prio = 0
		self.due = None # datetime
		self.done = False
		
		# raci
		self.responsible = []
		self.accountable = []
		self.support     = []
		self.consulted   = []
		self.informed    = []
		
		self.parent      = None # parent path
		
		self.children    = [] # list of Node objects


if __name__ == "__main__":
	storage = FileStorage.FileStorage('data/note.fs')
	db = DB(storage)
	connection = db.open()
	root = connection.root()
	
	try:
		root["nodes"]
	except:
		print "Initializing Database ..."
		root["nodes"] = Node("root")
		transaction.commit()
	
	nodes = root["nodes"]
	
	nodes.append(Node("Test 1"))
	nodes.append(Node("Test 2"))
	nodes.append(Node("Test 4"))
	
	transaction.commit()
	
	for e in nodes.children:
		print e
