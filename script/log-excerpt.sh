#!/bin/bash

file=$1
nr=$2
nstart=`expr $nr - 100`
nend=`expr $nr + 100`

cat -n $file | sed -n $nstart,${nend}p >$file:$nr.log

