#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from select import select
import time, serial, binascii

def open_seri(dev, baud):
    return serial.Serial(dev, baud, bytesize=8, parity='E', timeout=0)

def timestamp():
    msecs = str(int(time.time() * 1000))
    return msecs[0:-3] + '.' + msecs[-3:]

def print_packet(packet):
    width = 32
    while len(packet):
        print timestamp() + ' ' + \
                ' '.join(binascii.hexlify(x)
                        for x in packet[:width])
        packet = packet[width:]
    #sys.stdout.flush() # in case stdout is piped

def keep_reading():
    packet = bytearray()
    while True:
        readable, _, _, = select([seri], [], [], inter_char_timeout)
        if readable:
            packet.append(seri.read(1024))
        elif len(packet):
            print_packet(bytes(packet))
            packet = bytearray()

if __name__== '__main__':
    argp = ArgumentParser(prog='serisniff.py')
    argp.add_argument('device'
            , help='serial device name: for example, /dev/ttyUSB0, COM5')
    argp.add_argument('-b', '--baud'
            , type=int
            , default=2400
            , help='baud rate')
    argp.add_argument('-c', '--inter-char-timeout'
            , type=float
            , default=0.2
            , help='inter char timeout (n.n secs)')

    args = argp.parse_args()
    inter_char_timeout = args.inter_char_timeout

    seri = open_seri(args.device, args.baud)
    keep_reading()

