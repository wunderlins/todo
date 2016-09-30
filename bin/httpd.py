#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Very simple HTTP server in python.

Usage::
    ./httpd.py [<port>]

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	
	def _parse_request(self):
		q = self.path.split("?")
		path = q[0]
		query = ""
		if len(q) > 1:
			query = parse_qs(q[1])
		
		return (path, query)	

	def do_GET(self):
		(path, query) = self._parse_request()
		
		print path
		print query
		
		self._set_headers()
		self.wfile.write("<html><body><h1>hi!</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		(path, query) = self._parse_request()
		# Doesn't do anything with posted data
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self._set_headers()
		self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd on port %d ...' % port
	httpd.serve_forever()

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
