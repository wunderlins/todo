#!/usr/bin/env python

import sys
sys.path.append("../lib/site-packages")
#from ZODB.utils import p64

from ZODB import DB, FileStorage
from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction

import urllib

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
	_name_uri = ""
	
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
	
	def __init__(self, name, parent):
		
		# check if this path is already used
		if parent != None:
			#print parent.children
			"""
			for e in parent.children:
				print "-e-> %s|%s" % (name, e.name)
				if e.name == name:
					path = name
					raise NodeExeption("Node exists: %s") % name
			"""
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
		# TODO: urlencode name 
		self._name_uri = urllib.quote(name)
		#print "comitting %s" % self.name
		#self._p_changed = 1
		transaction.commit()
		
		# for debugging purpose
		#pass

	def is_root(self):
		""" check if this is the root node """
		return self._is_root
	
	def __repr__(self):
		id  = self.getid("hex")
		uri = self.getid("uri")
		return "<Node " + id + " " + self.name + " " + uri  + ">"
	
	def getid(self, type = "raw"): # types: raw|hex|uri
		"""get a unique identifier of this object
		
		raw
			it can be obtained as raw which will represent a zodb _p_oid
			http://zodb.readthedocs.io/en/latest/api.html#transaction.IPersistent._p_oid
		
		hex
			will return the id as hex
			
		uri
			will return an url compatible name.
		"""
		
		if type == "raw":
			return self._p_oid
		if type == "hex":
			return str(self._p_oid).encode("hex")
		if type == "uri":
			#return str(self._p_oid).encode("hex")
			# TODO: generate path
			stack = []
			current = self
			while True:
				# prepend name
				stack.insert(0, self._name_uri)
				if current.is_root() == True:
					break
				current = current.parent
			
			return '/'.join(stack)
			
		raise NodeError("Unknown type")
	
	def add_child(self, node):
		self.children.append(node)
		self._p_changed = 1 # important to use this on lists
		transaction.commit()
		return node
		
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
	
	n = Node("Test 1", nodes)
	nodes.add_child(n)
	nodes.add_child(Node("Test 2", nodes))
	t4 = nodes.add_child(Node("Test 4", nodes))
	nodes.add_child(Node("Test 7", t4))
	
	for e in nodes.children:
		print(e)
	
