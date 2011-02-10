#!/usr/bin/python

from subprocess import *
import os
import sys

def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
           not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None


filename = "tgl-gen.fst"

tests = {
	"bili":{
		"V":{
			"Inf":{
				"Obj1":"bilhin", "Obj2":"ibili", "Obj3":"bilian",
				"Act1":"bumian", "Act2":"magbili", "Act3":"mabili", "Act4":"mangbili",
				"Loc":"bilian", "Ben":"ibili", "Ins":"ipanbili", "Rea":"ikabili"
			}#, 
		}
	}
}

"""
			"Cont":{
				"Obj1":"bili", "Obj2":"bili", "Obj3":"bili",
				"Act1":"bili", "Act2":"bili", "Act3":"bili", "Act4":"bili",
				"Loc":"bili", "Ben":"bili", "Ins":"bili", "Rea":"bili"
			}, 
			"Prog":{
				"Obj1":"bili", "Obj2":"bili", "Obj3":"bili",
				"Act1":"bili", "Act2":"bili", "Act3":"bili", "Act4":"bili",
				"Loc":"bili", "Ben":"bili", "Ins":"bili", "Rea":"bili"
			}, 
			"Comp":{
				"Obj1":"bili", "Obj2":"bili", "Obj3":"bili",
				"Act1":"bili", "Act2":"bili", "Act3":"bili", "Act4":"bili",
				"Loc":"bili", "Ben":"bili", "Ins":"bili", "Rea":"bili"
			}, 
			"Imp":{
				"Obj1":"bili", "Obj2":"bili", "Obj3":"bili",
				"Act1":"bili", "Act2":"bili", "Act3":"bili", "Act4":"bili",
				"Loc":"bili", "Ben":"bili", "Ins":"bili", "Rea":"bili"
			}
"""
class HfstTester:
	def __init__(self):
		self.count = [0, 0]
		if not whereis("hfst-lookup"):
			print "Cannot find hfst-lookup. Check $PATH."
			sys.exit()
		self.run()

	def test(self, l, r):
		pass

	def run(self):
		for lemma in tests.keys():
			for v in tests[lemma].keys():
				for form in tests[lemma][v].keys():
					for focus in tests[lemma][v][form].keys():
						lform = "%s+%s+%s+%s" % (lemma, v, form, focus)
						sform = tests[lemma][v][form][focus]
						p1 = Popen(['echo', lform], stdout=PIPE)
						p2 = Popen(['hfst-lookup', filename], stdin=p1.stdout, stdout=PIPE)
						p1.stdout.close()
						res = p2.communicate()[0].split('\n')
						for i in res:
							if i.strip() != '':
								r = i.split('\t')[1].strip()
								if sform == r:
									print "%s => %s:%s [PASS]" % (lform, sform, r) 
									self.count[0] += 1
								else:
									print "%s => %s:%s [FAIL]" % (lform, sform, r)
									self.count[1] += 1
		print "%s - Passes: %d, Fails: %d" % (filename, self.count[0], self.count[1])

							
					
HfstTester()
