#!/bin/bash

LIST=$1
ANALYSER=$2
HEAD=1000

if [ $# -eq 3 ]; then
	HEAD=$3;
fi

cat $LIST | head -n $HEAD | apertium-destxt | lt-proc $ANALYSER | apertium-retxt | grep '*'
