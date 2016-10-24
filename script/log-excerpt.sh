#!/bin/bash

basename=$1
nr=$2
nstart=`expr $nr - 100`
nend=`expr $nr + 100`

cat -n $basename.log | sed -n $nstart,${nend}p >$basename:$nr.log

