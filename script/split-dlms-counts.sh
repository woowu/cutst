#!/bin/bash

ttl_errs=0
ttl_reqs=0
while (( $# )); do
    file=$1
    errs=$(grep "ERR.*unrecognized tag" $file | wc -l)
    aarq=$(grep "> 7E[0-9A-Z]\{4\}00 02[0-9A-Z]\{4\}61 [0-9A-Z]\{6\}E6 E60060" $file | wc -l)
    dlms_rd=$(grep "> 7E[0-9A-Z]\{4\}00 02[0-9A-Z]\{4\}61 [0-9A-Z]\{6\}E6 E60005" $file | wc -l)
    dlms_wr=$(grep "> 7E[0-9A-Z]\{4\}00 02[0-9A-Z]\{4\}61 [0-9A-Z]\{6\}E6 E60006" $file | wc -l)
    reqs=$((aarq + dlms_rd + dlms_wr))
    if [ $reqs -eq 0 ]; then
        echo no request found
        shift
        continue
    fi
    prob=$(bc -l <<EOF
100 * $errs / $reqs
EOF
    )
    printf "%12s: % 5d split dlms found in % 8d request (aa=% 8d rd=% 8d wr=% 8d). %%%.3f\n" \
        $(basename $file) $errs $reqs $aarq $dlms_rd $dlms_wr $prob
    #echo $file: $errs split dlms found in $reqs requests \(%$prob\)
    ttl_errs=$((ttl_errs + errs))
    ttl_aarq=$((ttl_reqs + aarq))
    ttl_rd=$((ttl_reqs + dlms_rd))
    ttl_wr=$((ttl_reqs + dlms_wr))
    ttl_reqs=$((ttl_reqs + reqs))
    shift
done
prob=$(bc -l <<EOF
100 * $ttl_errs / $ttl_reqs
EOF
)
echo == 
printf "%12s: % 5d split dlms found in % 8d request (aa=% 8d rd=% 8d wr=% 8d). %%%.3f\n" \
    total $ttl_errs $ttl_reqs $ttl_aarq $ttl_rd $ttl_wr $prob

