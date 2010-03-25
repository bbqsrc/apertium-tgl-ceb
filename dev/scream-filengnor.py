#!/usr/bin/python
# -*- coding: utf-8 -*-
version = "0.2"

import warnings # Because deprecation sounds suck!
warnings.filterwarnings('ignore', category=DeprecationWarning)

import getopt, sys, pycurl, StringIO, html5lib #, chardet
from html5lib import treebuilders
sys.setrecursionlimit(20000) # Because spectie uses Python 2.5. That's my rationale, and I'm sticking with it.

from xml.sax.handler import ContentHandler # XML parsing modules
from xml.sax import make_parser, parseString # XML parser

class dirtyTableHandler(ContentHandler):
	pFlag = False
	dump = []
	tableCount = 0
	isTable = False
	isTd = False
	tdCount = 0
	isTr = False
	trCount = -1
	anyTag = 0
	output = ""
	predump = []
	def selectedOutput(self):
		if self.pFlag:
			self.shortOutput()	
		else:
			self.longOutput()
	def shortOutput(self):
		kgo = False
		where = 0
		for i in range(len(self.dump)):
			for j in (0,1,4):
				if self.dump[i][j].find(args) == 0:
					if self.dump[i][j][-(len(args)+1):] == args:
						kgo = True
					else:
						for k in range(10):
							if self.dump[i][j].find(str(k)+")") != -1:
								where = self.dump[i][j].find(str(k)+")") 
								if self.dump[i][j].count(" ")  == (where - len(args)) :
									kgo = True
				if kgo:
					kgo = False
					print "%s %s %s" % (self.dump[i][0], self.dump[i][1], self.dump[i][4])
					break
			
	def longOutput(self):
		long1 = 0
		long2 = 0
		long3 = 0
		for i in range(len(self.dump)):
			if len(self.dump[i][0]) > long1:
				long1 = len(self.dump[i][0])
			if len(self.dump[i][1]) > long2:
				long2 = len(self.dump[i][1])
			if len(self.dump[i][4]) > long3:
				long3 = len(self.dump[i][4])
		for i in range(len(self.dump)):
			x = [0]*5
			if i == 0:
				print "\033[4m{0:^{3}}\033[0m  \033[4m{1:^{4}}\033[0m  \033[4m{2:^{5}}\033[0m".format(self.dump[i][0], self.dump[i][1], self.dump[i][4], long1, long2, long3)
			
			for j in [0,1,4]:
				if self.dump[i][j].count("\033") > 0:
					x[j] = 13
			if i != 0:
				print "{0:<{3}}  {1:<{4}}  {2:<{5}}".format(self.dump[i][0], self.dump[i][1], self.dump[i][4], (long1+x[0]), (long2+x[1]), (long3+x[4]))	
	 
	def startElement(self, tag, attrs):
		if tag == "table":
			self.tableCount += 1
			if self.tableCount == 2:
				self.isTable = True
		elif tag == "td":
			self.isTd = True
			self.tdCount += 1
		elif tag == "tr":
			self.isTr = True
			self.trCount += 1
			#if self.trCount >= 0:
			#	self.dump.append([])
		elif tag:
			self.anyTag += 1
			if tag == "b":
				if self.output[-1:] != "-":
					self.output += " "
			

	def characters(self, content):
		if self.isTd and self.tdCount > 2:
			self.output += content.strip()

	def endElement(self, tag):
		if tag == "table":
			self.isTable = False
		elif tag == "tr":
			if self.trCount > 2:
				if not pFlag:
					for i in range(len(self.predump)):
						self.predump[i] = self.predump[i].replace(args, u"\033[34m\033[1m%s\033[0m" % args).encode("utf-8")
				else:
					for i in range(len(self.predump)):
						self.predump[i] = self.predump[i].encode("utf-8")
				self.dump.append(self.predump)
				self.predump = []
			self.isTr = False
			self.tdCount = 0
		elif tag == "td":
			if self.tdCount > 2:
				self.predump.append(self.output.strip().strip())
			self.output = ""
			self.isTd = False
		elif tag:
			self.anyTag -= 1
			if tag == "font":
				self.output += " "


url = "http://baseportal.com/cgi-bin/baseportal.pl?htx=/fileng/allsearch&list=100"
args = ''
oFlag = False
pFlag = False
oFile = ""
arglen = len(sys.argv)
x = 1
def usage():
	print "scream-filengnor.py [-o output.html] [-p] <search query>"
	print "Totally sexy FilEngNor parsing with awesome column layout!"
	exit(0)
try:
	opts, args = getopt.getopt(sys.argv[1:], "hvpo:", ['help', 'version', 'output='])
except getopt.GetoptError, err:
	print str(err)
	usage()
if args == []:
	usage()
for o, a in opts:
	if o in ("-v", "--version"):
		print version
		exit(0)
	if o in ("--help", "-h"):
		usage()
	if o in ("-o", "--output"):
		oFile = a
		oFlag = True
	if o == "-p":
		pFlag = True
	else:
		assert False, "unhandled option"
args = " ".join(args) # Sexy, sexy hacks!
pf = [	('_fullsearch==', args),
	('list=', '45000')  ]

out = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.HTTPPOST, pf)
c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5")
c.setopt(c.WRITEFUNCTION, out.write)
c.perform()
c.close()

out = out.getvalue()
x = out.find("<html>")
out = out[x:].replace("\n", "").replace("ISO-8859-1", "UTF-8")
parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("BeautifulSoup"))
soup = parser.parse(out)
out =  soup.html.table.prettify()
if oFlag:
	f = open(oFile, 'w')
	f.write(out)
	f.close()

parser = make_parser()
o = dirtyTableHandler()
if pFlag:
	o.pFlag = True
parser.setContentHandler(o)
parser.parse(StringIO.StringIO(out))
o.dump.pop(0) # Fix for random error that I cant be bothered to work out
o.dump.pop(len(o.dump)-1) # <3 half-assed cleanups
o.selectedOutput()
