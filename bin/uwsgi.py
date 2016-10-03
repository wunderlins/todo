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
	port = 8020
	host = "0.0.0.0"
	
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
		print " * port: %d" % port
	
	if len(sys.argv) > 2:
		host = sys.argv[2]
		print " * host: %s" % host
	
	app.run(port=port, host=host)

if __name__ == "__main__":
	print " * Starting ..."
	main()
	
