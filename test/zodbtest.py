#!/usr/bin/env python

import sys
sys.path.append("../lib/site-packages")
#from ZODB.utils import p64

from ZODB import DB, FileStorage
#from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction

#import pdb;

class NodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Person(Persistent):
	nickname = ""
	firstname = ""
	lastname = ""
	
	samaccountname = ""
	email = ""
	phone = ""
	
	def __init__(self, nickname, firstname="", lastname=""):
		self.nickname = nickname
		self.firstname = firstname
		self.lastname = lastname
	
	def __repr__(self):
		out = "<"
		if self.lastname:
			out += self.lastname
		
		if self.nickname:
			if out != "<":
				out += " "
			out += '"' + self.nickname + '"'
		
		if self.firstname:
			out += ' ' + self.firstname
		
		out += ">"
		
		return out
		#return '<%s "%s" %s>' % (self.lastname, self.nickname, self.firstname)

class Node(Persistent):
	"""Node"""
	_is_root = False
	
	parent = None
	
	name = ""
	desc = ""
	prio = 0
	due = None # datetime
	done = False
	
	# rasci
	responsible = []
	accountable = []
	support     = []
	consulted   = []
	informed    = []
	
	children    = [] # list of Node objects
	
	def is_root(self):
		return self._is_root
	
	def __repr__(self):
		#return "<Node " + self.name + "{" + str(self._p_jar[p64(0)]) + "}>"
		#pdb.set_trace()
		return "<Node " + self.name + "{" + str(self._p_oid) + "}>"
	
	def getOid(self):
		return self._p_oid
	
	def append(self, node):
		self.children.append(node)
		self._p_changed = 1 # important to use this on lists
		transaction.commit()
	
	def __init__(self, name, parent):
		# set the parent node
		self._is_root = False
		if parent == None:
			self._is_root = True
			self.parent = None # parent path
		else:
			if not isinstance(parent, Node):
				raise NodeError("parent must be of tpye Node, got '" + type(parent) + "'")
			self.parent = parent
		
		# set defaults
		self.name = name
		transaction.commit()
		
		# for debugging purpose
		#pass


if __name__ == "__main__":
	storage = FileStorage.FileStorage('data/note.fs')
	db = DB(storage)
	connection = db.open()
	root = connection.root()
	
	try:
		root["nodes"]
	except:
		print("Initializing Database ...")
		root["nodes"] = Node("root", None)
		transaction.commit()
	
	nodes = root["nodes"]
	
	nodes.append(Node("Test 1", nodes))
	nodes.append(Node("Test 2", nodes))
	nodes.append(Node("Test 4", nodes))
	
	for e in nodes.children:
		print(e)
