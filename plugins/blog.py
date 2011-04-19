#!/usr/bin/python

from dcms import Plugin, RstParser

class Blog(Plugin):
	name = "Blog"
	text = ""

	def __init__(self,args=[]):
		rst = RstParser()
		try: 
			f = open(self.datadir + "blog", "r")
			t = f.read()
			self.text = rst.parse(t)
			f.close()
		except IOError as e:
			self.text = e

		pass

