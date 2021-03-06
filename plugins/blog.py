#!/usr/bin/python 
from dcms import Plugin, RstParser
from string import Template
import re

CONFIG_DOMAIN = "http://deaddy.net/"

class Blog(Plugin):
	name = "Blog"
	descripton = """
A small blog about system administration, code and mathematics.
"""
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
		content_type = ''
		i = 0
		for line in fp:
			if line.startswith(":title"):
				content_type = ''
				if temppost:
					self.posts.insert(0,temppost)
				i += 1
				temppost = Post(pid=i, title = line[7:])
				temppost.text += "\n"
			if temppost and line.startswith(":date"):
				temppost.date = line[6:]
			if line.startswith(":abstract"):
				content_type = 'abstract'
			elif line.startswith(":text"):
				content_type = "text"
			elif temppost and content_type:
				temppost.__dict__[content_type] += line

		if temppost:
			self.posts.insert(0,temppost)

		# fix pids
		postcount = 1
		for post in self.posts:
			post.pid = postcount
			post.generate_clean_url()
			postcount += 1


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
				self.show_post_by_pid(pid)
			except ValueError, e:
				self.show_pages()
		elif args[0] == "all":
			self.show_toc()
		elif args[0] == "rss.xml":
			self.content_type = 'rss'
			self.show_rss()
		elif args[0] == "cleanurl":
			try:
				cleanurl = args[1]
				self.show_post_by_cleanurl(cleanurl)
			except ValueError, e:
				self.show_pages()
		else:
			self.show_pages()


	def show_rss(self):
		rst = RstParser()
		item_template_string = """
	<item>
		<title>${title}</title>
		<link>${url}</link>
		<guid>${guid}</guid>
		<pubDate>${date}</pubDate>
		<description>
		${text}
		</description>
	</item>
"""
		item_template = Template(item_template_string)
		items = []
		i = 1
		for post in self.posts:
			post_dict = {}
			post_dict['title'] = post.title
#			post_dict['text'] = rst.parse(post.text).replace("&rdquo;",
#					"&quot;").replace("&ldquo;", "&quot;")
			post_dict['text'] = post.abstract
			post_dict['date'] = post.date
			post_dict['url']	= CONFIG_DOMAIN+"blog/cleanurl/" + post.cleanurl
			post_dict['guid'] = CONFIG_DOMAIN+"blog/id/" + str(i)
			item_text = item_template.safe_substitute(post_dict)
			items.append(item_text)
			i += 1

		self.text += "\n".join(reversed(items))


	def show_pages(self, p=1):
			rst = RstParser()
			i = 0
			first = (p-1)*self.page_limit
			last = p*self.page_limit
			for post in reversed(self.posts):
				if first <= i and i < last:
					self.text += '<h2><a class="permalink" href="/blog/cleanurl/'
					self.text += post.cleanurl + '">' + post.title + '</a></h2>\n'
					self.text += "<i>" + post.date + "</i>\n"
					self.text += rst.parse(post.text)
				else:
					pass
				i += 1
			
			pages = (len(self.posts)+1)/self.page_limit
			self.text += """<div class="pages">Pages:<ul>"""
			if p != 1:
				self.text += '<li><a href="/blog/page/1">&lt;&lt;</a></li>'
				self.text += '<li><a href="/blog/page/'
				self.text += str(p-1)
				self.text += '">&lt;</a></li>'


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
				self.text += '">&gt;</a></li>'
				self.text += '<li><a href="/blog/page/'
				self.text += str(pages)
				self.text += '">&gt;&gt;</a></li>'

			self.text += '<li><a href="/blog/all">all posts</a></li>'
			self.text += '<li><a href="/blog/rss.xml">rss</a></li>'
			self.text += """</ul></div>"""


	def show_post_by_pid(self, pid):
		rst = RstParser()

		if pid < 1 or pid > len(self.posts):
			self.show_pages()
			return

		self.text += '<h2><a class="permalink" href="/blog/cleanurl/' + str(self.posts[pid-1].cleanurl) + '">'
		self.text += self.posts[pid-1].title + "</a></h2>\n"
		self.text += "<i>" + self.posts[pid-1].date + "</i>\n"
		self.text += rst.parse(self.posts[pid-1].text)
		self.text += """<div class="pages"><ul>"""

		if pid > 1:
			self.text += '<li><a href="/blog/id/1">&lt;&lt;</a></li>'
			self.text += '<li><a href="/blog/id/' + str(pid-1) + '">&lt;</a></li>'

		if pid < len(self.posts):
			self.text += '<li><a href="/blog/id/' + str(pid+1) + '">&gt;</a></li>'
			self.text += '<li><a href="/blog/id/' + str(len(self.posts)) + '">&gt;&gt;</a></li>'

		self.text += '<li><a href="/blog/all">all posts</a></li>'
		self.text += '<li><a href="/blog/rss.xml">rss</a></li>'
		self.text += """</ul></div>"""

	
	def show_post_by_cleanurl(self, url):
			rst = RstParser()
			post = filter(lambda p: url == p.cleanurl, self.posts)
			if not post:
				self.show_pages()
			else:
				self.show_post_by_pid(post[0].pid)

	def show_toc(self):
		self.text += "<h2>All posts in chronologically order:</h2>"
		self.text += '<ol class="toc">'

		for post in self.posts:
			self.text += '<li><a href="/blog/cleanurl/' + post.cleanurl + '">'
			self.text += post.title + '</a></li>'

		self.text += '</ol>'
		self.text += """<div class="pages"><a href="/blog/rss.xml">rss</a></div>"""

class Post:
	title = ""
	text = ""
	pid = ""
	abstract = ""
	date = ""
	cleanurl = ""

	def __init__(self, pid, title, text="", abstract="", date=""):
		self.pid = pid
		self.title = title
		self.generate_clean_url()
		self.text = text
		self.abstract = abstract
		self.date = date

	def generate_clean_url(self):
		"""This function generates a clean url from the pid and title, by
		removing non-alpha-numerical characters, replacing spaces by -,
		lowercasing it and prepending "pid-" to the string."""

		spaces_replaced = self.title.replace(' ', '-')
		pattern = re.compile('[^a-zA-Z0-9-]+')
		stripped = pattern.sub('', spaces_replaced)
		self.cleanurl = '-'.join([str(self.pid), stripped.lower()])
