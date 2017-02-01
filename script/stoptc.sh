#!/bin/bash

echo "stop dlt645tst"
for pid in \
    `ps -Cpython -opid,command |grep dlt645tst.py |grep -v grep |sed -n 's/^\s*\([0-9]\+\)\s\+python.*$/\1/p'`; do
    echo killing $pid
    kill $pid
done

echo "stop dlms tests"
for pid in \
    `ps -eF |grep rundlms |grep -v grep |sed -n 's/^root\s\+\([0-9]\+\)\s\+.*$/\1/p'`; do
    echo killing $pid
    kill $pid
done
killall xdlms >/dev/null 2>&1
killall xdlms2 >/dev/null 2>&1

echo "stop testcase-*.sh"
for pid in \
    `ps -eF |grep testcase |grep -v grep |sed -n 's/^root\s\+\([0-9]\+\)\s\+.*$/\1/p'`; do
    echo killing $pid
    kill $pid
done

killall xdlms >/dev/null 2>&1
killall xdlms2 >/dev/null 2>&1

echo "kill nc, cut, logger"
killall nc >/dev/null 2>&1
killall socat >/dev/null 2>&1
killall cut >/dev/null 2>&1
killall logger >/dev/null 2>&1

