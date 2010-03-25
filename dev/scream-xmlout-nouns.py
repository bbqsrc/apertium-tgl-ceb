#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, sys, string


try: 
	i = open(sys.argv[1])
	o = open(sys.argv[2], 'w')
except:
	print "Error."
	exit(1)

words = set()
propers = set()
line = i.readline()
while line:
	win = line.split()[0].strip()
	if win[0] in string.uppercase:
		propers.add(win)
	else:
		words.add(win)
	line = i.readline()

o.write("<!-- Nouns -->\n")
for mot in words:
	mot = "  <e lm=\"%s\"><i>%s</i><par n=\"aso__n\"/></e>\n" % (mot, mot)
	o.write(mot)

o.write("\n<!-- Proper nouns -->\n")
for mot in propers:
	mot = "  <e lm=\"%s\"><i>%s</i><par n=\"Dios__np\"/></e>\n" % (mot, mot)
	o.write(mot)

i.close()
o.close()
