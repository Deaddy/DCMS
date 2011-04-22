#!/usr/bin/python

import cgi
import cgitb
import os
import imp
from sys import argv,stderr


cgitb.enable()

pluginDir = "plugins/"
dataDir = "data/"

class Dcms():
	content = ""

	def __init__(self):
		self.path = os.environ["PATH_INFO"]
		self.loadPlugins()
		self.processUrl()
		self.loadNavigation()

		print "Content-type: text/html"
		print ""
		print """ <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<link rel="stylesheet" type="text/css" href="style.css" />
<html>
	<head><title>Deaddy.net</title></head>
	<body>
"""
		print "<div class=\"navigation\">", self.navigation, "</div>"
		print "<div class=\"main\">", self.content, "</div>"
		print """
</body></html>
"""

	def processUrl(self):
		self.arguments = self.path.strip("/").split("/")

		if self.arguments:
			for plugin in self.plugins:
				if self.arguments[0].lower() == plugin.name.lower():
					c = plugin(self.arguments[1:])
					self.content = c.getContent()
					break

		else:
			return "Hello, World!"

	def loadPlugins(self):
		self.plugins = []
		pluginFiles = filter(lambda x: x[-3:] == ".py", os.listdir(pluginDir))
		for fn in pluginFiles:
			f = fn[:-3]
			clsname = f[0].upper() + f[1:]
			info = imp.find_module(f, [pluginDir])
			module = imp.load_module(f, info[0], info[1], info[2])
			info[0].close()
			cls = getattr(module, clsname)
			self.plugins.append(cls)

	def loadNavigation(self):
		self.navigation = """
<h1>Contents</h1>
<ul>"""
		for plugin in self.plugins:
			self.navigation += "<li><a href=\""
			self.navigation += plugin.name.lower()
			self.navigation += "\">"
			self.navigation += plugin.name
			self.navigation += "</a></li>"
		self.navigation += "</ul>"

	

class RstParser():
	
	def parse(self, text):
		string = ""
		for line in text.split("\n"):
			if line and line[0] == ":":
				string += "<h2>"
				string += line[1:]
				string += "</h2>"
			else:
				string += line

		return string

class Plugin():
	name = None
	text = None
	datadir = dataDir

	def __init__(self, args=[]): pass
	
	def getContent(self): return self.text

class News(Plugin):
	name = "News"
	text = "default"

if __name__=="__main__":
	cms = Dcms()
