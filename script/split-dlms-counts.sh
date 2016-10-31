#!/bin/bash

ttl_errs=0
ttl_reqs=0
while (( $# )); do
    file=$1
    errs=$(grep "ERR.*unrecognized tag" $file | wc -l)
    reqs=$(grep "> 7E[0-9A-Z]\{4\}00 02[0-9A-Z]\{4\}61 [0-9A-Z]\{6\}E6 E600" $file | wc -l)
    if [ $reqs -eq 0 ]; then
        echo no request found
        exit
    fi
    prob=$(bc -l <<EOF
100 * $errs / $reqs
EOF
    )
    printf "%12s: % 5d split dlms found in % 8d request. %%%.3f\n" \
        $(basename $file) $errs $reqs $prob
    #echo $file: $errs split dlms found in $reqs requests \(%$prob\)
    ttl_errs=$((ttl_errs + errs))
    ttl_reqs=$((ttl_reqs + reqs))
    shift
done
prob=$(bc -l <<EOF
100 * $ttl_errs / $ttl_reqs
EOF
)
echo == 
printf "%12s: % 5d split dlms found in % 8d request. %%%.3f\n" \
    total $ttl_errs $ttl_reqs $prob

