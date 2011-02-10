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
				"Obj1":["bilhin"], "Obj2":["ibili"], "Obj3":["bilian"],
				"Act1":["bumili"], "Act2":["magbili"], "Act3":["mabili"], "Act4":["mangbili"],
				"Loc":["bilian"], "Ben":["ibili"], "Ins":["ipambili", "ipanbili", "ipabili"], 
				"Rea":["ikabili"]
			}, 
			"Cont":{
				"Obj1":["bibilhin"], "Obj2":["ibibili"], "Obj3":["bibilian"],
				"Act1":["bibili"], "Act2":["magbibili"], "Act3":["mabibili"], "Act4":["mangbibili"],
				"Loc":["bibilian"], "Ben":["ibibili"], "Ins":["ipambibili", "ipanbibili", "ipabibili"], 
				"Rea":["ikabibili"]
			}, 
			"Prog":{
				"Obj1":["binibili"], "Obj2":["ibinibili"], "Obj3":["binibilian"],
				"Act1":["bumibili"], "Act2":["nagbibili"], "Act3":["nabibili"], 
				"Act4":["nangbibili"], "Loc":["binibilian"], "Ben":["ibinibili"], 
				"Ins":["ipinanbibili", "ipinambibili", "ipinabibili"], "Rea":["ikinabibili"]
			}, 
			"Comp":{
				"Obj1":["binili"], "Obj2":["ibinili"], "Obj3":["binilian"],
				"Act1":["bumili"], "Act2":["nagbili"], "Act3":["nabili"], "Act4":["nangbili"],
				"Loc":["binilian"], "Ben":["ibinili"], "Ins":["ipinambili", "ipinanbili", "ipinabili"], 
				"Rea":["ikinabili"]
			}, 
			"Imp":{
				"Obj1":["bili", "bilia"], "Obj2":["bilian"], "Obj3":["bilhi"],
				"Act1":["bili"], "Act2":["pagbili"], "Act4":["pangbili"]
			}
		}
	}
}

"""
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
								if r in sform:
									print "%s => %s:%s [PASS]" % (lform, r, r) 
									self.count[0] += 1
								else:
									print "%s => %s:%s [FAIL]" % (lform, sform, r)
									self.count[1] += 1
		print "%s - Passes: %d, Fails: %d, Total: %d" % (filename, self.count[0], self.count[1], self.count[0] + self.count[1])

							
					
HfstTester()
