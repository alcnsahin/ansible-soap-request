#!/usr/bin/python

import urllib2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib2.Request('')
req.add_header("Content-Type", "text/xml; charset=utf-8")
response = urllib2.urlopen(req, data='', context=ctx)
print(response.read())