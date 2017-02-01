# job desc line:
# <runner name> <log_port> <iterations> [arg1] [arg2] ...
# supported runner:
# dlmsauto, dlt645
#
# Examples:
# dlt645 2120 100 /dev/tts7 -n500 -tweisheng 0
#

dlt645tst.py 2220 0 /dev/tts7 -n100 -tsky -d4 -s 0
dlt645tst.py 2221 0 /dev/tts9 -n100 -tsky -d4 -s 0
dlt645tst.py 2222 0 /dev/tts11 -n100 -tsky -d4 -s 0
dlt645tst.py 2223 0 /dev/tts13 -n100 -tsky -d4 -s 0
dlt645tst.py 2224 0 /dev/tts15 -n100 -tsky -d4 -s 0
dlt645tst.py 2225 0 /dev/tts17 -n100 -tsky -d4 -s 0
dlt645tst.py 2226 0 /dev/tts19 -n100 -tsky -d4 -s 0
dlt645tst.py 2227 0 /dev/tts21 -n100 -tsky -d4 -s 0
dlt645tst.py 2228 0 /dev/tts23 -n100 -tsky -d4 -s 0

xdlms2 2229 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts6 3067 21234567 9600 2 
xdlms2 2230 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts8 3068 21234567 9600 2 
xdlms2 2231 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts10 3069 21234567 9600 2 
xdlms2 2232 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts12 3070 21234567 9600 2 
xdlms2 2233 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts14 3071 21234567 9600 2 
xdlms2 2234 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts16 3072 21234567 9600 2 
xdlms2 2235 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts18 1164 21234567 9600 2 
xdlms2 2236 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts20 1165 21234567 9600 2 
xdlms2 2237 0 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops 100 --aa-lifetime 60 /dev/tts22 1166 21234567 9600 2 

