#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple script to merge selenium suites tests in one suite file """

import sys
import urllib 
from lxml import html

postfix='.html'

#Format: OutputFile: [ list of suites or individual tests ]
config={
    'testsAdmin':     ['loginAdmin',      'ViewTests', 'EditTests', 'AdmUsers'],
    'testsEditor':    ['loginEditor',     'ViewTests', 'EditTests'],
    'testsAnonymous': ['ViewTests', 'NoEditTests'],
}
header="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
  <title>Merged tests</title>
</head>
<body>
<table id="suiteTable" cellpadding="1" cellspacing="1" border="1" class="selenium"><tbody>
<tr><td><b>Merged tests</b></td></tr>
"""

footer="""</tbody></table>
</body>
</html>
"""
allTests=[]
for output, suites in config.iteritems():
    for suite in suites:
        suiteContent=html.fromstring(open(suite+postfix, 'r').read())
        if suiteContent.xpath("//table[@id='suiteTable']"):
            for link in suiteContent.xpath("//a"):
                file=link.get("href")
                allTests.append({'name': link.text, 'file':file})
        elif suiteContent.xpath("/html/head[@profile='http://selenium-ide.openqa.org/profiles/test-case']"):
            allTests.append({'name': str(suiteContent.xpath("/html/head/title/text()")[0]), 'file':suite+postfix})
        else:
            sys.stderr.write("Unknown file "+suite)
    f=open(output+postfix, 'w')
    f.write(header+'\n')
    for test in allTests:
        f.write('<tr><td><a href="'+test['file']+'">'+test['name']+'</a></td></tr>'+'\n')
    f.write(footer)
    f.close();

            