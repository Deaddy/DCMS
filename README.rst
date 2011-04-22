Simple CMS in python for CGI
============================
:Author:
   Deaddy
:Licence:
   Public domain
:Dependencies:
   mod_rewrite

Usage
-----
Place directory on your webserver and add a rewrite rule that rewrites every
request, that is not an existing file to dcms.py/url, for example:
   RewriteCond /var/www/localhost/htdocs/dcms/%{REQUEST_FILENAME} !-F

   RewriteRule ^(.*)$ /dcms.py$1 [PT,QSA,L]

To test the blog move data/blog.example to data/blog
For static modules simply add a new file named like your module in the
plugindir with following contents:

#!/usr/bin/bash

from Dcms import Plugin
# uncomment if you want to use the rst-parser
# from Dcms import RstParser

class MyPlugin(Plugin):
   name = MyPlugin
   text = """my static content"

# uncomment following lines if you want to use the RstParser
#   def __init__(self, args=[]):
#      rst = RstParser()
#      self.text = rst.parse(self.text)
