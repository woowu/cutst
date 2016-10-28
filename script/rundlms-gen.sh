#!/bin/sh

NODB=
PERIOD=120

meter_no=$1
iterations=$2

if [[ ! $meter_no -gt 0 ]]; then
    echo need meter_no
    exit 1
fi
if [[ ! $iterations -gt 0 ]]; then
    echo bad iterations
    exit 1
fi
if [[ $NODB != "yes" && ! -f /ffc/cfg/config.db ]]; then
    echo no config
    exit 1
fi

if [[ $NODB != "yes" ]]; then
    com_no=`sqlite3 /ffc/cfg/config.db "select ncomid from meterunitconfig where nmeterid=$meter_no;"`
    baud_idx=`sqlite3 /ffc/cfg/config.db "select nbaudft from meterunitconfig where nmeterid=$meter_no;"`
else
    com_no=1
    baud_idx=13
fi
if [[ ! $com_no -gt 0 ]]; then
    echo bad com_no
    exit 1
fi
if [[ ! $baud_idx -gt 0 ]]; then
    echo bad baud_idx
    exit 1
fi

do_rd() {
    acqtime=$1
    rd_reg=$2
    lp_from=$3
    lp_to=$4
    opts=(-L --brief --no-save --no-last-value)

    if [[ $rd_reg == "no" ]]; then
        opts+=(--no-reg)
    fi
    if [[ -n $lp_from ]]; then
        t="`date -d@$lp_from +"%Y-%m-%d %H:%M:%S"`"
        opts+=(--lp-from "${t}")
    fi
    if [[ -n $lp_to ]]; then
        t="`date -d@$lp_to +"%Y-%m-%d %H:%M:%S"`"
        opts+=(--lp-to "${t}")
    fi
    echo xdlms "${opts[@]}" \
        $com_no $meter_no $baud_idx $1 1
    xdlms "${opts[@]}" \
        $com_no $meter_no $baud_idx $1 1
    if [[ $? -ne 0 ]]; then
        echo "ERR: xdlms error, exit code = $?"
        sleep 200 
    fi
}

i=0
while [[ $i -lt $iterations ]]; do
    echo "iteration $i"

    acqtime=`date +%s`
    acqtime=`expr $acqtime / $PERIOD \* $PERIOD`
    c=`expr $i % 10`
    case $c in 
        [0-4])          # 50%, lp window = 2hr, no register
            do_rd $acqtime "no" `expr $acqtime - 7200 + 1` $acqtime
            ;;
        [5-6])          # 20%, lp window = 0.5hr, with register
            do_rd $acqtime "yes" `expr $acqtime - 1800 + 1` $acqtime
            ;;
        [7-9])          # 30%, random lp timewindow (<=0.5hr) 
            lp_to=`expr $acqtime + 300`
            d=`expr $RANDOM % 10 + 1`
            d=`expr $d \* 60`
            lp_to=`expr $lp_to - $d`
            d=`expr $RANDOM % 30 + 1`
            d=`expr $d \* 60`
            lp_from=`expr $lp_to - $d + 1`
            do_rd $acqtime "yes" $lp_from $lp_to
            ;;
    esac
    i=`expr $i + 1`
done

