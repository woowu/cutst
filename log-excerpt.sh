#!/bin/bash

file=$1
nr=$2
nstart=`expr $nr - 500`
nend=`expr $nr + 500`

cat -n $file | sed -n $nstart,${nend}p >$file.$nr

