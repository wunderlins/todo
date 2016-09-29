#!/usr/bin/env python

import sys
sys.path.append("../lib/site-packages")
#from ZODB.utils import p64

from ZODB import DB, FileStorage
from BTrees.IOBTree import IOBTree
from ZODB.PersistentMapping import PersistentMapping
from persistent import Persistent
import transaction

class Node(Persistent):
	def __init__(self, name):
		self.name = name

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
			return str(self._p_oid).encode("hex")
		if type == "int":
			return int(str(self._p_oid).encode("hex"), 16)
			
		raise NodeError("Unknown type")

def add(branch, item):
	try:
		k = branch.maxKey()
	except:
		k = 0
	
	branch.insert(k+1, item)
	transaction.commit()
	return item

if __name__ == "__main__":
	storage = FileStorage.FileStorage('data/note.fs')
	db = DB(storage)
	connection = db.open()
	root = connection.root()
	
	try:
		items = root["items"]
	except:
		print("Initializing Database ...")
		items = root["items"] = IOBTree()
		transaction.commit()
	
	add(items, Node("one"))
	add(items, Node("two"))
	add(items, Node("tree"))
	
	#transaction.commit()
	
	for (k, v) in items.items():
		print k, v.getid("int"), v.name
	
	db.close()
