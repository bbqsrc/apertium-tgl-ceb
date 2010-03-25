#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
filename = "tgl.filengnor-output"

f = open("%s.txt" % filename, 'r') # consistency says I must use 'r'

files = {}

line = f.readline()

while line:
	for i in line.split():
		if i.find("[") >= 0:
			gram = i
			break
	gram = re.sub(r"[0-9]|\[|\]|\ |\;|\:", r"", gram)
	gram = re.sub(r"\.\,|\,\.|\.|\,|\/", r"_", gram)
	gram = gram.strip("_")
	
	if not gram in files:
		files[gram] = open("%s.%s.txt" % (filename, gram), 'w')
	
	files[gram].write(line)
	line = f.readline()

for i in files:
	files[i].close()
