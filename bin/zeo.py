#!/usr/bin/env python

import sys, os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(basedir, "../lib/site-packages")))
sys.path.insert(0, os.path.realpath(os.path.join(basedir, "../lib/site-packages/ZEO")))
print "\n".join(sys.path)

#from ZEO import *
import runzeo
#print sys.argv
runzeo.main(sys.argv[1:])
