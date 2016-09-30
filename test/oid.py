#!/usr/bin/env python

import sys
sys.path.append("../lib/site-packages")
#from ZODB.utils import p64

from ZODB import DB, FileStorage
from BTrees.IOBTree import IOBTree
from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction

class NodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NodeUtil(object):
	@staticmethod
	def int2hex(key_int):
		return '{0:016x}'.format(key_int)
	
	@staticmethod
	def int2bin(key_int):
		key_hex = NodeUtil.int2hex(key_int)
		return NodeUtil.hex2bin(key_hex)
		
	@staticmethod
	def hex2bin(key_hex):
		key_bin = ""

		i = 0
		l = None
		for e in enumerate(key_hex):
			char = e[1]
			if (i % 2 == 1):
				key_bin += chr(int(l+char, 16))
			i += 1
			l = char
			
		return key_bin
	
	@staticmethod
	def bin2int(key_bin):
		return int(str(key_bin).encode("hex"), 16)
	
	@staticmethod
	def bin2hex(key_bin):
		return str(key_bin).encode("hex")
	
class Node(Persistent):
	""" Abstract node class for a data tree """
	name     = None
	children = None
	parent   = None
	
	def __init__(self, name):
		self.name = name
		self.children = IOBTree()
	
	def __repr__(self):
		id  = self.getid("hex")
		i   = self.getid("int")
		#return "<Node " + id + " " + self.name + " " + uri  + ">"
		return "<Node [" + str(i) + "] " + self.name + ">"
		
	def append(self, child):
		if not isinstance(child, Node):
			raise NodeError("parent must be of tpye Node, got '" + type(child) + "'")
		try:
			k = self.children.maxKey()
		except:
			k = 0
	
		child.parent = self
		self.children.insert(k+1, child)
		transaction.commit()
	
	def is_root(self):
		return False
	
	def items(self):
		return self.children.items()
	
	def keys(self):
		return self.children.keys()
	
	def values(self):
		return self.children.values()
	
	def getid(self, t = "raw"): # types: raw|hex|uri
		"""get a unique identifier of this object
		
		raw
			it can be obtained as raw which will represent a zodb _p_oid
			http://zodb.readthedocs.io/en/latest/api.html#transaction.IPersistent._p_oid
		
		hex
			will return the id as hex
			
		uri
			will return an url compatible name.
			
		int
			as integer
		"""
		if t == "raw":
			return self._p_oid
		if t == "hex":
			return NodeUtil.bin2hex(self._p_oid)
		if t == "uri":
			return str(self._p_oid).encode("hex")
		if t == "int":
			return NodeUtil.bin2int(self._p_oid)
			
		raise NodeError("Unknown type")
	
class Root(Node):
	def __init__(self):
		Node.__init__(self, "root")
		
	def is_root(self):
		return True

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

if __name__ == "__main__":
	storage = FileStorage.FileStorage('data/oid.fs')
	db = DB(storage)
	conn = db.open()
	root = conn.root()
	
	try:
		items = root["items"]
	except:
		print("Initializing Database ...")
		items = root["items"] = Root()
		transaction.commit()
	
	"""
	items.append(Node("one"))
	items.append(Node("two"))
	items.append(Node("three"))
	"""
	#transaction.commit()
	
	for (k, v) in items.items():
		#print v, str(v.getid()).encode('ascii'), len(v.getid())
		#print ':'.join(x.encode('hex') for x in v.getid())
		print v
	
	item = conn.get(NodeUtil.int2bin(17))
	while item.parent != None:
		sys.stdout.write(item.name + "/")
		item = item.parent
	print item.name
	
	"""
	d = bytearray(a)
	print "'" + d + "'"
	conn.get(d[7])
	"""	
	
	db.close()
	
#
