#!/usr/bin/env python

class lexcGenerator:
	def __init__(self):
		self.lex = "Infixes"
		self.nextlex = "RegSuffixes"
		self.input = open("stems-in.txt", 'r')
		self.output = open("stems-out.txt", 'w')
		self.count = 0
		self.run()

	def run(self):
		self.output.write("LEXICON %s\n" % self.lex)
		for i in self.input:
			x = "@R.ALPH.%s@%s\t%s ;\n" % (i[0],i[1:].split(' ')[0].strip(), self.nextlex)
			self.output.write(x)
		self.input.close()
		self.output.close()


lexcGenerator()

