#!/usr/bin/python

import cgi, cgitb, os, imp, re
from sys import argv,stderr


cgitb.enable()

pluginDir = "plugins/"
dataDir = "data/"

class Dcms():
	content = ""
	default_plugin = "blog"

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
<link rel="stylesheet" type="text/css" href="/style.css" />
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

		if self.arguments and self.arguments[0]:
			self.content = "fuuu"
			if self.plugins.has_key(self.arguments[0].lower()):
				c = self.plugins[self.arguments[0].lower()](self.arguments[1:])
				self.content = c.getContent()

		else:
			c = self.plugins[self.default_plugin]()
			self.content = c.getContent()



	def loadPlugins(self):
		self.plugins = {}
		pluginFiles = filter(lambda x: x[-3:] == ".py", os.listdir(pluginDir))
		pluginFiles.sort()
		for fn in pluginFiles:
			f = fn[:-3]
			clsname = f[0].upper() + f[1:]
			info = imp.find_module(f, [pluginDir])
			module = imp.load_module(f, info[0], info[1], info[2])
			info[0].close()
			cls = getattr(module, clsname)
			self.plugins[clsname.lower()] = cls

	def loadNavigation(self):
		self.navigation = """
<h1>Contents</h1>
<ul>"""
		for plugin in self.plugins.values():
			self.navigation += "<li><a href=\""
			self.navigation += "/" + plugin.name.lower()
			self.navigation += "\">"
			self.navigation += plugin.name
			self.navigation += "</a></li>"
		self.navigation += "</ul>"

	

class RstParser():
	
	def parse(self, text):
		tokens = [
				(":title\s*([^\n]*)", self.__title),
				(":date\s*([^\n]*)", self.__date),
				("\"([^\"]+)\":\"([^\"]+)\"", self.__link),
				("\s_([^\_]+)_([^\w])", self.__italic),
				("\n(\.p)", self.__paragraph),
				("(\np\.)", self.__paragraph),
				("img:\"([^\"]+)\"", self.__img),
		]

		for token in tokens:
			text = re.sub(token[0], token[1], text)

		return text

	def __title(self, matchobject):
		return "<h2>" + matchobject.group(1) + "</h2>\n"

	def __date(self, matchobject):
		return "<i>" + matchobject.group(1) + "</i><br />\n"

	def __link(self, m):
		return "<a href=\"" + m.group(1) + "\">" + m.group(2) + "</a>"

	def __img(self, m):
		return "<br /><img src=\"" + m.group(1) + "\"/><br />" 

	def __italic(self, m):
		return " <i>" + m.group(1) + "</i>" + m.group(2)

	def __paragraph(self, m):
		if m.group(1) == ".p":
			return "<p>"
		else:
			return "\n</p>"

class Plugin():
	name = None
	text = None
	datadir = dataDir

	def __init__(self, args=[]): pass
	
	def getContent(self): return self.text

if __name__=="__main__":
	cms = Dcms()
