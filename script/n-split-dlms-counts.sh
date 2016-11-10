#!/bin/bash

n=$1
shift
files=$*

if [[ $n -le 0 ]]; then
    echo need to specify a 'n' > 0
    exit 1
fi
echo files=${files}

for i in $(seq $n); do
    echo counting at $(date):
    ./split-dlms-counts.sh ${files}
    sleep 600
done

