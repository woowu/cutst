#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import serial

dlt645_97_ids = (
        0x00010100, 0x00010200,
        );

seri = None
addr = None

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

def create_read_req(id):
    frame = bytearray([0x68])
    frame += enc_addr(addr)
    frame += bytearray([0x68, 0x11, 0x04])
    for i in range(4):
        frame.append(id % 256 + 0x33)
        id /= 256
    frame.append(mod256_sum(frame))
    return bytearray([0xfe, 0xfe]) + frame + bytearray([0x16])

def open_seri(dev, baud):
    return serial.Serial(dev, baud, bytesize=8, parity='E')

def read_single_id(id):
    req = create_read_req(id)
    print '> ' + ' '.join(x.encode('hex') for x in bytes(req))
    seri.write(bytes(req))
    seri.flush()

    seri.timeout = 3
    rep = seri.read(1024)
    if len(rep):
        print '< ' + ' '.join(x.encode('hex') for x in rep)

def read_from_table():
    for id in dlt645_97_ids:
        read_single_id(id)

if __name__== '__main__':
    argp = ArgumentParser(prog='seriping.py')
    argp.add_argument('device', help='serial device name')
    argp.add_argument('addr', help='server addr in decimal string')
    argp.add_argument('-b', '--baud'
            , type=int
            , default=2400
            , help='baud rate')

    args = argp.parse_args()
    addr = args.addr
    seri = open_seri(args.device, args.baud)

    read_from_table()

