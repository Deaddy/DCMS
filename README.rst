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
