#!/usr/bin/env python

import sys
sys.path.append("lib/site-packages")

from lib.db import *

if __name__ == "__main__":
	
	db = db("var/db/note.fs")
	items = db.get_root()