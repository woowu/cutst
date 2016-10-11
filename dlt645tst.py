#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from select import select
import sys, time, re, serial, binascii

dlt645_07_ids = (
    0x00010000,
    0x00010100,
    0x00010200,
    0x00010300,
    0x00010400,
    0x00020000,
    0x00020100,
    0x00020200,
    0x00020300,
    0x00020400,
    0x00030000,
    0x00030100,
    0x00030200,
    0x00030300,
    0x00030400,
    0x00040000,
    0x00040100,
    0x00040200,
    0x00040300,
    0x00040400,
    0x00050000,
    0x00080000,
    0x00060000,
    0x00070000,
    0x00010001,
    0x01010000,
    0x01020000,
    0x03300001,
    0x03300201,
    0x03300200,
    0x02010100,
    0x02010200,
    0x02010300,
    0x02020100,
    0x02020200,
    0x02020300,
    0x02030000,
    0x02030100,
    0x02030200,
    0x02030300,
    0x02040000,
    0x02040100,
    0x02040200,
    0x02040300,
    0x02060000,
    0x02060100,
    0x02060200,
    0x02060300,
    0x04000101,
    0x04000102,
    0x04000501,
    0x04000409,
    0x0400040A,
    0x04010001,
    )

seri = None

def open_seri(dev, baud):
    return serial.Serial(dev, baud, bytesize=8, parity='E', timeout=0)

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

def is_normal_resp(ctrl):
    return ctrl & 0xc0 == 0x80

def has_next_data(ctrl):
    return ctrl & 0xe0 == 0xa0 

def timestamp():
    msecs = str(int(time.time() * 1000))
    return msecs[0:-3] + '.' + msecs[-3:]

def print_packet(packet, dir):
    while len(packet):
        print timestamp() + \
                ' %s ' % dir + ' '.join(binascii.hexlify(x)
                        for x in packet[:16])
        packet = packet[16:]
    sys.stdout.flush() # in case stdout is piped

def create_read_req(id, seqno):
    frame = bytearray([0x68])
    frame += enc_addr(addr)
    if seqno == 0:
        frame += bytearray([0x68, 0x11, 0x04])
    else:
        frame += bytearray([0x68, 0x12, 0x05])
    for i in range(4):
        frame.append((id % 256 + 0x33) % 256)
        id /= 256

    # Keli considers seqno as not part of data
    if seqno > 0:
        frame.append(seqno % 256)

    frame.append(mod256_sum(frame))
    return bytearray([0xfe, 0xfe]) + frame + bytearray([0x16])

def recv_frame():
    def opening_tag_on_char(state, c):
        state['frame'].append(c)
        if ord(c) == 0x68:
            return second_tag_on_char
        else:
            return opening_tag_on_char

    def second_tag_on_char(state, c):
        state['frame'].append(c)
        if ord(c) == 0x68:
            return ctrl_on_char
        else:
            return second_tag_on_char

    def ctrl_on_char(state, c):
        state['frame'].append(c)
        state['ctrl'] = ord(c)
        return length_on_char

    def length_on_char(state, c):
        state['frame'].append(c)
        state['data_len'] = ord(c)
        return data_on_char

    def data_on_char(state, c):
        state['frame'].append(c)
        state['data_len'] -= 1
        if state['data_len'] > 0:
            return data_on_char
        if has_next_data(state['ctrl']):
            return seqno_on_char
        else:
            return chksum_on_char

    def seqno_on_char(state, c):
        state['frame'].append(c)
        state['seqno'] = ord(c)
        return chksum_on_char

    def chksum_on_char(state, c):
        state['frame'].append(c)
        return closing_tag_on_char

    def closing_tag_on_char(state, c):
        state['frame'].append(c)
        return None

    state = {'frame': bytearray(), 'ctrl': 0, 'seqno': 0}
    resp_timeout = 3
    inter_char_timeout = 0.05

    # quick and dirty checking
    #
    handler = opening_tag_on_char
    while True:
        if len(state['frame']):
            timeout = inter_char_timeout
        else:
            timeout = resp_timeout
        readable, _, _, = select([seri], [], [], timeout)
        if not readable:
            return (state['frame'], state['ctrl'], state['seqno'])

        handler = handler(state, seri.read(1))
        if not handler: break
    return (state['frame'], state['ctrl'], state['seqno'])

def read_single_id(id, seqno):
    req = create_read_req(id, seqno)
    print_packet(bytes(req), '>')
    seri.write(bytes(req))
    seri.flush()
    return recv_frame()

def read_from_table():
    index = 0
    seqno = 0

    while index < len(dlt645_07_ids):
        id = dlt645_07_ids[index]
        for retries in range(3):
            frame, ctrl, _ = read_single_id(id, seqno)
            if len(frame):
                print_packet(bytes(frame), ' ')
            else:
                continue

            if is_normal_resp(ctrl): 
                time.sleep(idle_wait)
                break
            else:
                time.sleep(err_wait)
        if len(frame) and has_next_data(ctrl) and seqno < 255:
            seqno += 1
        else:
            seqno = 0
            index += 1

if __name__== '__main__':
    argp = ArgumentParser(prog='dlt645tst.py')
    argp.add_argument('device', help='serial device name')
    argp.add_argument('addrs', nargs='+'
            , help='one or more server address in decimal string')
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
    err_wait = args.err_wait
    idle_wait = args.idle_wait
    seri = open_seri(args.device, args.baud)

    for addr in args.addrs:
        print '== read meter %s' % addr
        read_from_table()

