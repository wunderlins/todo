#!/usr/bin/env python

# library path
import sys, os
sys.path.append("../lib/site-packages")

from flask import Flask
app = Flask(__name__)

# flask config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['STATIC_FOLDER'] = os.path.realpath(os.path.join(basedir, '../www'))
#print app.config['STATIC_FOLDER']
app.config['STATIC_URL_PATH'] = "/www"
#app.config["DEBUG"] = True


"""
for e in app.config:
	print e + ": " + str(app.config[e])
"""

@app.route('/')
def hello_world():
	return 'Hello, World!'

def main():
	app.run()

if __name__ == "__main__":
	print " * Starting ..."
	main()
