#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from select import select
import serial
import re
import time

dlt645_97_ids = (
        0x00010100, 0x00010200,
        );

seri = None
addr = None
err_wait = 3.0
idle_wait = 0.02

def open_seri(dev, baud):
    return serial.Serial(dev, baud, bytesize=8, parity='E')

def enc_addr(addr):
    i = 0
    result = bytearray()
    for d in addr.rjust(12, '0'):
        if i / 2 * 2 == i:
            result.append(int(d) * 16)
        else:
            result[-1] = result[-1] + int(d)
        i += 1
    result.reverse()
    return result

def mod256_sum(barry):
    return reduce(lambda x, y: x + y, barry) % 256

def timestamp():
    msecs = str(int(time.time() * 1000))
    return msecs[0:-3] + '.' + msecs[-3:]

def create_read_req(id):
    frame = bytearray([0x68])
    frame += enc_addr(addr)
    frame += bytearray([0x68, 0x11, 0x04])
    for i in range(4):
        frame.append(id % 256 + 0x33)
        id /= 256
    frame.append(mod256_sum(frame))
    return bytearray([0xfe, 0xfe]) + frame + bytearray([0x16])

def recv_frame():
    frame = bytearray()
    status = 0
    len = 0

    # quick and dirty checking
    seri.timeout = 0
    s = 'opening_tag'
    while True:
        readable, _, _, = select([seri], [], [], 3)
        if not readable: return (None, status)

        c = seri.read(1)
        frame.append(c)
        c = ord(c)
        #print s, hex(c)

        if s == 'opening_tag':
            if c == 0x68:
                s = 'second_tag'
            continue
        if s == 'second_tag':
            if c == 0x68:
                s = 'status'
            continue
        if s == 'status':
            status = c
            s = 'length'
            continue
        if s == 'length':
            len = c
            s = 'data'
            continue
        if s == 'data':
            len -= 1
            if not len:
                s = 'chksum'
            continue
        if s == 'chksum':
            s = 'end_tag'
            continue
        if s == 'end_tag':
            break
    return (frame, status)

def read_single_id(id):
    req = create_read_req(id)
    print timestamp() + \
            ' > ' + ' '.join(x.encode('hex') for x in bytes(req))
    seri.write(bytes(req))
    seri.flush()
    return recv_frame()

def read_from_table():
    for id in dlt645_97_ids:
        for retries in range(3):
            frame, status = read_single_id(id)
            if frame and len(frame):
                print timestamp() + \
                        ' < ' + ' '.join(x.encode('hex') for x in bytes(frame))
            if frame and status == 0x91: 
                time.sleep(idle_wait)
                break
            time.sleep(err_wait)

if __name__== '__main__':
    argp = ArgumentParser(prog='seriping.py')
    argp.add_argument('device', help='serial device name')
    argp.add_argument('addr', help='server addr in decimal string')
    argp.add_argument('-b', '--baud'
            , type=int
            , default=2400
            , help='baud rate')
    argp.add_argument('-w', '--err-wait'
            , type=float
            , default=3.0
            , help='error wait')
    argp.add_argument('-l', '--idle-wait'
            , type=float
            , default=0.02
            , help='idle wait')

    args = argp.parse_args()
    addr = args.addr
    err_wait = args.err_wait
    seri = open_seri(args.device, args.baud)

    read_from_table()

