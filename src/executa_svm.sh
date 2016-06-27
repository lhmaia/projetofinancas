#!/bin/bash

#arquivo="petr4.news.tend"
arquivo=$1

svm-scale -s dados/$arquivo.range dados/$arquivo.train > dados/$arquivo.scale
svm-train -s 0 -t 2 -g 0.0078125 dados/$arquivo.scale dados/$arquivo.model
svm-scale -s dados/$arquivo.range dados/$arquivo.pred > dados/$arquivo.pred.scale
svm-predict dados/$arquivo.pred.scale dados/$arquivo.model dados/$arquivo.out > dados/$arquivo.svm.out
