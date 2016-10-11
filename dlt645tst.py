#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from select import select
import sys, time, re, serial, binascii

weisheng_07_ids = (
    0x04000501,
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
    0x00050100,
    0x00050200,
    0x00050300,
    0x00050400,
    0x00080000,
    0x00080100,
    0x00080200,
    0x00080300,
    0x00080400,
    0x00060000,
    0x00060100,
    0x00060200,
    0x00060300,
    0x00060400,
    0x00070000,
    0x00070100,
    0x00070200,
    0x00070300,
    0x00070400,
    0x0000FF00,
    0x01010000,
    0x01010100,
    0x01010200,
    0x01010300,
    0x01010400,
    0x01020000,
    0x01020100,
    0x01020200,
    0x01020300,
    0x01020400,
    0x01010000,
    0x01010100,
    0x01010200,
    0x01010300,
    0x01010400,
    0x01020000,
    0x01020100,
    0x01020200,
    0x01020300,
    0x01020400,
    0x03300001,
    0x03300201,
    0x03300000,
    0x03300200,
    0x0280000A,
    0x13010001,
    0x13020001,
    0x13030001,
    0x13010002,
    0x13020002,
    0x13030002,
    0x13010101,
    0x13020101,
    0x13030101,
    0x13012501,
    0x13022501,
    0x13032501,
    0x04000501,
    0x040005FF,
    0x04000801,
    0x02800001,
    0x10010002,
    0x10020002,
    0x10030002,
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
    0x04000409,
    0x0400040A,
    0x04010000,
    0x04010001,
    0x04010002,
    0x04010003,
    0x04010004,
    0x04010005,
    0x04010006,
    0x04010007,
    0x04010008,
    0x0001FF01,
    0x0002FF01,
    0x0003FF01,
    0x0004FF01,
    0x0005FF01,
    0x0008FF01,
    0x0006FF01,
    0x0007FF01,
    0x0101FF01,
    0x0102FF01,
    0x0101FF01,
    0x0102FF01,
    )

keli_07_ids = (
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
    norm = addr.rjust(12, '0')
    grouped = [int(norm[i:i + 2]) for i in range(0, len(norm), 2)]
    bcd = bytearray([e / 10 * 16 + e % 10 for e in grouped])
    bcd.reverse()
    return bcd

def mod256_sum(barry):
    return reduce(lambda x, y: x + y, barry) % 256

def is_normal_resp(ctrl):
    return ctrl & 0xc0 == 0x80

def has_next_data(ctrl):
    return ctrl & 0xe0 == 0xa0 

def is_subsequent_frame(ctrl):
    return ctrl & 0x1f == 0x12

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
    leading = bytearray()
    for i in range(leading_chars_nr):
        leading.append(0xfe)
    return leading + frame + bytearray([0x16])

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
        if is_normal_resp(state['ctrl']) and \
                is_subsequent_frame(state['ctrl']):
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

    while index < len(id_table):
        id = id_table[index]
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
        if not no_read_subsequent and len(frame) and has_next_data(ctrl) and \
                seqno < 255:
            seqno += 1
        else:
            seqno = 0
            index += 1

if __name__== '__main__':
    argp = ArgumentParser(prog='dlt645tst.py')
    argp.add_argument('device'
            , help='serial device name: for example, /dev/ttyUSB0, COM5')
    argp.add_argument('addrs', nargs='+'
            , help='one or more server addresses in decimal string, '
            'separated by space')
    argp.add_argument('-t', '--id-table'
            , default='keli'
            , help='id table name: keli, weisheng and all')
    argp.add_argument('-b', '--baud'
            , type=int
            , default=2400
            , help='baud rate')
    argp.add_argument('-e', '--err-wait'
            , type=float
            , default=3.0
            , help='error wait (n.n secs)')
    argp.add_argument('-l', '--idle-wait'
            , type=float
            , default=0.02
            , help='idle wait (n.n secs)')
    argp.add_argument('-r', '--resp-timeout'
            , type=float
            , default=3
            , help='response timeout')
    argp.add_argument('-c', '--inter-char-timeout'
            , type=float
            , default=0.05
            , help='inter char timeout (n.n secs)')
    argp.add_argument('-d', '--leading-chars'
            , type=int
            , default=2
            , help='number of leading chars in sending (default: 2)')
    argp.add_argument('-s', '--no-read-subsequent'
            , action='store_true'
            , help='not to read subsequent data')
    argp.add_argument('-n', '--iterations'
            , type=int
            , default=1
            , help='number of iterations to run')

    args = argp.parse_args()
    if args.id_table == 'keli':
        id_table = keli_07_ids
    elif args.id_table == 'weisheng':
        id_table = weisheng_07_ids
    elif args.id_table == 'all':
        id_table = keli_07_ids + weisheng_07_ids
    else:
        print 'invalid id table'
        raise SystemExit
    err_wait = args.err_wait
    idle_wait = args.idle_wait
    resp_timeout = args.resp_timeout
    inter_char_timeout = args.inter_char_timeout
    leading_chars_nr = args.leading_chars
    no_read_subsequent = args.no_read_subsequent

    seri = open_seri(args.device, args.baud)

    for i in range(args.iterations):
        for addr in args.addrs:
            print '== read meter %s' % addr
            read_from_table()

