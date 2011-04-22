#!/usr/bin/python

from dcms import Plugin, RstParser

class Blog(Plugin):
	name = "Blog"
	text = ""
	page_limit = 2

	def __init__(self,args=[]):
		self.posts = []
		try: 
			f = open(self.datadir + "blog", "r")
			self.populate_posts(f)
			f.close()

		except IOError, e:
			self.text = e

		if not self.text and self.posts:
			self.process_arguments(args)

	def populate_posts(self, fp):
		temppost = False	
		i = 0
		for line in fp:
			if line.startswith(":title"):
				if temppost:
					self.posts.insert(0,temppost)
				i += 1
				temppost = Post(i, line[7:])
				temppost.content += line
			elif temppost:
				temppost.content += line

		if temppost:
			self.posts.insert(0,temppost)

	def process_arguments(self, args):
		if not args:
			self.show_pages()
			return

		if args[0] == "page" and len(args) > 1:
			try:
				p = int(args[1])
				if p < 1:
					p = 1
				self.show_pages(p)
			except ValueError, e:
				self.show_pages()
		elif args[0] == "id" and len(args) > 1:
			try:
				pid = int(args[1])
				self.show_post(pid)
			except ValueError, e:
				self.show_pages()
		elif args[0] == "all":
			self.show_toc()
		else:
			self.show_pages()

	def show_pages(self, p=1):
			rst = RstParser()
			i = 0
			first = (p-1)*self.page_limit
			last = p*self.page_limit
			for post in reversed(self.posts):
				if first <= i and i < last:
					self.text += rst.parse(post.content)
				else:
					pass
				i += 1
			
			pages = (len(self.posts)+1)/self.page_limit
			self.text += """<div class="pages">Pages:<ul>"""
			if p != 1:
				self.text += '<li><a href="/blog/page/1">&lt;&lt;<a></li>'
				self.text += '<li><a href="/blog/page/'
				self.text += str(p-1)
				self.text += '">&lt;<a></li>'


			for x in range(pages+1)[1:]:
				if x == p:
					self.text += "<li><b>" + str(x) + "</b></li>"
				else:
					self.text += """<li><a href="/blog/page/"""
					self.text += str(x)
					self.text += '">' + str(x) + '</a></li>'

			if p < pages:
				self.text += '<li><a href="/blog/page/'
				self.text += str(p+1)
				self.text += '">&gt;<a></li>'
				self.text += '<li><a href="/blog/page/'
				self.text += str(pages)
				self.text += '">&gt;&gt;<a></li>'

			self.text += '<li><a href="/blog/all">all posts</a></li>'
			self.text += """</ul></div>"""

	def show_post(self, pid):
		rst = RstParser()

		if pid < 1 or pid > len(self.posts):
			self.show_pages()
			return

		self.text += rst.parse(self.posts[pid-1].content)
		self.text += """<div class="pages"><ul>"""

		if pid > 1:
			self.text += '<li><a href="/blog/id/1">&lt;&lt;</a>'
			self.text += '<li><a href="/blog/id/' + str(pid) + '">&lt;</a>'

		if pid <= len(self.posts):
			self.text += '<li><a href="/blog/id/' + str(pid+1) + '">&gt;</a>'
			self.text += '<li><a href="/blog/id/' + str(len(self.posts)+1) + '">&gt;&gt;</a>'

		self.text += '<li><a href="/blog/all">all posts</a></li>'
		self.text += """</ul></div>"""

	def show_toc(self):
		self.text += "<h2>All posts in chronologically order:</h2>"
		self.text += '<ol class="toc">'

		for post in self.posts:
			self.text += '<li><a href="/blog/id/' + str(post.pid) + '">'
			self.text += post.title + '</a></li>'

		self.text += '</ol>'

class Post:
	title = ""
	content = ""
	pid = ""

	def __init__(self, pid, title, content=""):
		self.pid = pid
		self.title = title
		self.content = content
