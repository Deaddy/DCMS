#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb, os, imp, re
from sys import argv,stderr
from string import Template


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

		self.mapping = { 
				'navigation'	: self.navigation,
				'content'		: self.content,
				'description'	: self.description,
				'url'				: self.url
				}
		print self.template.safe_substitute(self.mapping)

	def processUrl(self):
		self.arguments = self.path.strip("/").split("/")

		if self.arguments and self.arguments[0]:
			self.content = "fuuu"
			if self.plugins.has_key(self.arguments[0].lower()):
				c = self.plugins[self.arguments[0].lower()](self.arguments[1:])

		else:
			c = self.plugins[self.default_plugin]()

		self.content = c.getContent()
		self.content_type = c.getContentType()
		self.description = c.getDescription()
		self.url = self.arguments[0].lower()

		if self.content_type == 'rss':
			tmpl_path = 'rss.tmpl'
		else:
			tmpl_path = 'main.tmpl'

		with open(tmpl_path, 'r') as f:
			self.template = Template(f.read())


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
				("\n(\.code)", self.__code),
				("(\ncode\.)", self.__code),
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

	def __code(self, m):
		if m.group(1) == ".code":
			return "<pre><code>"
		else:
			return "\n</code></pre>\n"

class Plugin():
	name = None
	text = None
	content_type = "html"
	datadir = dataDir
	description = ""

	def __init__(self, args=[]): pass

	def getContentType(self): return self.content_type
	
	def getContent(self): return self.text

	def getDescription(self): return self.description

if __name__=="__main__":
	cms = Dcms()
