#!/bin/sh

p=120
while true; do
    now=`date +%s`
    t=`expr $now / $p \* $p`
    270 6 1 13 $t 1
    sleep 30
done

