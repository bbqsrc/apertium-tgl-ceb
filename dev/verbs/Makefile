all: tgl-gen.fst tgl-morph.fst

tgl-lexc.fst: tgl.lexc
	hfst-lexc tgl.lexc -o $@

tgl-twol.fst: tgl.twol
	hfst-twolc tgl.twol -o $@

tgl-gen.fst: tgl-lexc.fst tgl-twol.fst 
	hfst-compose-intersect -l tgl-lexc.fst tgl-twol.fst -o $@

tgl-morph.fst: tgl-gen.fst
	hfst-invert tgl-gen.fst > $@

clean: 
	rm tgl-gen.fst tgl-morph.fst tgl-twol.fst tgl-lexc.fst
