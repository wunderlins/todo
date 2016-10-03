#!/usr/bin/env python

""" """

from db import *

class Note(Node):
	team = {
		"r": [],
		"a": [],
		"s": [],
		"c": [],
		"i": [],
	}

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
	
	db = db("../test/data/oid.fs")
	items = db.get_root()
	
	"""
	items.append(Node("one"))
	items.append(Node("two"))
	items.append(Node("three"))
	"""
	
	"""
	d = db.get(NodeUtil.int2bin(7))
	k = db.get_key(d)
	d.parent.children.pop(k)
	transaction.commit()
	"""
	
	#db.remove(db.get(NodeUtil.int2bin(31)))
	
	#print k
	
	"""
	d = db.get(NodeUtil.int2bin(7))
	for (k, v) in d.parent.items():
		if d == v:
			print k, d
	"""
	
	"""
	for (k, v) in items.items():
		#print v, str(v.getid()).encode('ascii'), len(v.getid())
		#print ':'.join(x.encode('hex') for x in v.getid())
		print v, v.has_children()
	"""
	
	traverse(items)
	
	n = db.get(NodeUtil.int2bin(5))
	print n.team
	
	#n = Note("test")
	#items.append(n)
	
	#item = db.get(NodeUtil.int2bin(17))
	#print item.uri()
	
	#i = db.get(NodeUtil.int2bin(9))
	#i.append(Node("eleven"))
	
	"""
	d = bytearray(a)
	print "'" + d + "'"
	conn.get(d[7])
	"""	
	
	db.close()
	
#
