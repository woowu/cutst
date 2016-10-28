#!/bin/sh

DEBUG=
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
if [[ $DEBUG != "yes" && ! -f /ffc/cfg/config.db ]]; then
    echo no config
    exit 1
fi

if [[ $DEBUG != "yes" ]]; then
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
    if [[ -n $lp_from || -n $lp_to ]]; then
        opts+=(--no-lp-time-hist)
    fi
    echo xdlms "${opts[@]}" \
        $com_no $meter_no $baud_idx $1 1
    if [[ $DEBUG != "yes" ]]; then
        xdlms "${opts[@]}" \
            $com_no $meter_no $baud_idx $1 1
    fi
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
        [0-4])
            do_rd $acqtime "no" `expr $acqtime - 7200 + 1` $acqtime
            ;;
        [5-9])
            do_rd $acqtime "yes"
            ;;
    esac
    i=`expr $i + 1`
done

