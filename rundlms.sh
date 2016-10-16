#!/bin/sh

t=0
p=120
while true; do
    now=`date +%s`
    t=`expr $now / $p \* $p`
    270 6 1 13 $t 1
    sleep 1
done
