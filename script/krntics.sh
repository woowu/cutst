#!/bin/bash

grep krn_tics: - |sed -n 's/^\([^ ]\+\) krn_tics: \([0-9]\+\);.*$/\1 \2/p'
