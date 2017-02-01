#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from select import select
import sys, time, re, serial, binascii, datetime

__07_demo_ids = (
    (0x04000101, 1, 0),
    (0x04000102, 1, 0),
    (0x0400040b, 1, 0),
    (0x0400040d, 1, 0),
    (0x04800001, 1, 0),
    (0x04800002, 1, 0),
    (0x04800003, 1, 0),
    (0x00010000, 1, 0),
    )

__07_simple_ids = (
   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),

   (0x00010000,1,0),
   (0x00020000,1,0),
   (0x00030000,1,0),
   (0x00040000,1,0),
   )

__07_weisheng_ids = (
   (0x04000501,1,0),
   (0x00010000,1,0),
   (0x00010100,1,0),
   (0x00010200,1,0),
   (0x00010300,1,0),
   (0x00010400,1,0),
   (0x00020000,1,0),
   (0x00020100,1,0),
   (0x00020200,1,0),
   (0x00020300,1,0),
   (0x00020400,1,0),
   (0x00030000,1,0),
   (0x00030100,1,0),
   (0x00030200,1,0),
   (0x00030300,1,0),
   (0x00030400,1,0),
   (0x00040000,1,0),
   (0x00040100,1,0),
   (0x00040200,1,0),
   (0x00040300,1,0),
   (0x00040400,1,0),
   (0x00050000,1,0),
   (0x00050100,1,0),
   (0x00050200,1,0),
   (0x00050300,1,0),
   (0x00050400,1,0),
   (0x00080000,1,0),
   (0x00080100,1,0),
   (0x00080200,1,0),
   (0x00080300,1,0),
   (0x00080400,1,0),
   (0x00060000,1,0),
   (0x00060100,1,0),
   (0x00060200,1,0),
   (0x00060300,1,0),
   (0x00060400,1,0),
   (0x00070000,1,0),
   (0x00070100,1,0),
   (0x00070200,1,0),
   (0x00070300,1,0),
   (0x00070400,1,0),
   (0x0000FF00,1,0),
   (0x01010000,1,0),
   (0x01010100,1,0),
   (0x01010200,1,0),
   (0x01010300,1,0),
   (0x01010400,1,0),
   (0x01020000,1,0),
   (0x01020100,1,0),
   (0x01020200,1,0),
   (0x01020300,1,0),
   (0x01020400,1,0),
   (0x01010000,1,0),
   (0x01010100,1,0),
   (0x01010200,1,0),
   (0x01010300,1,0),
   (0x01010400,1,0),
   (0x01020000,1,0),
   (0x01020100,1,0),
   (0x01020200,1,0),
   (0x01020300,1,0),
   (0x01020400,1,0),
   (0x03300001,1,0),
   (0x03300201,1,0),
   (0x03300000,1,0),
   (0x03300200,1,0),
   (0x0280000A,1,0),
   (0x13010001,1,0),
   (0x13020001,1,0),
   (0x13030001,1,0),
   (0x13010002,1,0),
   (0x13020002,1,0),
   (0x13030002,1,0),
   (0x13010101,1,0),
   (0x13020101,1,0),
   (0x13030101,1,0),
   (0x13012501,1,0),
   (0x13022501,1,0),
   (0x13032501,1,0),
   (0x04000501,1,0),
   (0x040005FF,1,0),
   (0x04000801,1,0),
   (0x02800001,1,0),
   (0x10010002,1,0),
   (0x10020002,1,0),
   (0x10030002,1,0),
   (0x02010100,1,0),
   (0x02010200,1,0),
   (0x02010300,1,0),
   (0x02020100,1,0),
   (0x02020200,1,0),
   (0x02020300,1,0),
   (0x02030000,1,0),
   (0x02030100,1,0),
   (0x02030200,1,0),
   (0x02030300,1,0),
   (0x02040000,1,0),
   (0x02040100,1,0),
   (0x02040200,1,0),
   (0x02040300,1,0),
   (0x02060000,1,0),
   (0x02060100,1,0),
   (0x02060200,1,0),
   (0x02060300,1,0),
   (0x04000101,1,0),
   (0x04000102,1,0),
   (0x04000409,1,0),
   (0x0400040A,1,0),
   (0x04010000,1,0),
   (0x04010001,1,0),
   (0x04010002,1,0),
   (0x04010003,1,0),
   (0x04010004,1,0),
   (0x04010005,1,0),
   (0x04010006,1,0),
   (0x04010007,1,0),
   (0x04010008,1,0),
   (0x0001FF01,1,0),
   (0x0002FF01,1,0),
   (0x0003FF01,1,0),
   (0x0004FF01,1,0),
   (0x0005FF01,1,0),
   (0x0008FF01,1,0),
   (0x0006FF01,1,0),
   (0x0007FF01,1,0),
   (0x0101FF01,1,0),
   (0x0102FF01,1,0),
   (0x0101FF01,1,0),
   (0x0102FF01,1,0),
    )

__07_keli_ids = (
    (0x00010000,2,3),
    (0x00010100,2,3),
    (0x00010200,2,3),
    (0x00010300,2,3),
    (0x00010400,2,3),
    (0x00020000,2,3),
    (0x00020100,2,3),
    (0x00020200,2,3),
    (0x00020300,2,3),
    (0x00020400,2,3),
    (0x00030000,2,3),
    (0x00030100,2,3),
    (0x00030200,2,3),
    (0x00030300,2,3),
    (0x00030400,2,3),
    (0x00040000,2,3),
    (0x00040100,2,3),
    (0x00040200,2,3),
    (0x00040300,2,3),
    (0x00040400,2,3),
    (0x00050000,2,3),
    (0x00080000,2,3),
    (0x00060000,2,3),
    (0x00070000,2,3),
    (0x00010001,2,3),
    (0x01010000,2,3),
    (0x01020000,2,3),
    (0x03300001,2,3),
    (0x03300201,2,3),
    (0x03300200,2,3),
    (0x02010100,2,3),
    (0x02010200,2,3),
    (0x02010300,2,3),
    (0x02020100,2,3),
    (0x02020200,2,3),
    (0x02020300,2,3),
    (0x02030000,2,3),
    (0x02030100,2,3),
    (0x02030200,2,3),
    (0x02030300,2,3),
    (0x02040000,2,3),
    (0x02040100,2,3),
    (0x02040200,2,3),
    (0x02040300,2,3),
    (0x02060000,2,3),
    (0x02060100,2,3),
    (0x02060200,2,3),
    (0x02060300,2,3),
    (0x04000101,2,3),
    (0x04000102,2,3),
    (0x04000501,2,3),
    (0x04000409,2,3),
    (0x0400040A,2,3),
    (0x04010001,23,0),
    )

__07_sky_ids = (
   (0x0101FF01,1,0),
   (0x0102FF01,1,0),
   (0x04000501,2,3),
   (0x00010000,1,0),
   )
 
__97_sky_ids = (
   (0xc010,1,0),
   (0xa01f,1,0),
   (0xb01f,1,0),
   (0xa02f,1,0),
   (0xc020,1,0),
   (0x9010,1,0),
   )

no_ids = ()

proto_algo_07 = {
        'id_len': 4,
        'addr_len': 6,
        'leading_char': 254,
        'opening_tag': 104,
        'closing_tag': 22,
        'complement_char': 51,
        'ctrl_read_data': 17,
        'ctrl_read_next_data': 18,
        'fr_resp_mask': 0x80,
        'fr_resp_flg_mask': 0x40,
        'fr_subsequent_ind_mask': 0x20,
        'fr_fc_mask': 0x1f,
        }

proto_algo_97 = {
        'id_len': 2,
        'addr_len': 6,
        'leading_char': 254,
        'opening_tag': 104,
        'closing_tag': 22,
        'complement_char': 51,
        'ctrl_read_data': 1,
        'ctrl_read_next_data': 18,          # FIXME
        'fr_resp_mask': 0x80,               # FIXME
        'fr_resp_flg_mask': 0x40,           # FIXME
        'fr_subsequent_ind_mask': 0x20,     # FIXME
        'fr_fc_mask': 0x1f,                 # FIXME
        }

proto_algo = proto_algo_07
mode_97 = False
last_read_counters_time = datetime.datetime(1970, 1, 1)
cu_reset_nr = 0
timeout_nr = 0
read_nr = 0
read_counters = False
read_counters_intvl = 0

def open_seri(dev, baud):
    return serial.Serial(dev, baud, bytesize=8, parity='E', timeout=0)

def timestamp():
    secs = time.time()
    return time.strftime("%y-%m-%dT%H:%M:%S"
            , time.localtime(int(secs))) + '.%03d' \
            % int((secs % 1) * 1000)

def log(line):
    print timestamp() + ' ' + line

def print_packet(packet, dir):
    width = 16
    while len(packet):
        log(' %s ' % dir + ' '.join(binascii.hexlify(x)
                        for x in packet[:width]))
        packet = packet[width:]
    sys.stdout.flush() # in case stdout is piped

def enc_addr(addr):
    if addr == '0':     # 0 means broadcase
        return bytearray([0x99] * 6)
    norm = addr.rjust(12, '0')
    grouped = [int(norm[i:i + 2]) for i in range(0, len(norm), 2)]
    return bytearray([e / 10 * 16 + e % 10 for e in reversed(grouped)])

def mod256_sum(barry):
    return reduce(lambda x, y: x + y, barry) % 256

def is_normal_resp(ctrl):
    return (ctrl & proto_algo['fr_resp_mask']) \
            and not (ctrl & proto_algo['fr_resp_flg_mask'])

def has_next_data(ctrl):
    return is_normal_resp(ctrl) and \
            (ctrl & proto_algo['fr_subsequent_ind_mask'])

def is_subsequent_frame(ctrl):
    return ctrl & proto_algo['fr_fc_mask'] == proto_algo['ctrl_read_next_data']

def create_read_req(id, seqno):
    frame = bytearray([proto_algo['opening_tag']])
    frame += enc_addr(addr)
    if seqno == 0:
        frame += bytearray([proto_algo['opening_tag']
            , proto_algo['ctrl_read_data'], proto_algo['id_len']])
    else:
        frame += bytearray([proto_algo['opening_tag']
            , proto_algo['ctrl_read_next_data'], proto_algo['id_len'] + 1])
    for i in range(proto_algo['id_len']):
        frame.append((id + proto_algo['complement_char']) % 256)
        id /= 256

    # Keli did not complement the seqno with 51
    if seqno > 0:
        frame.append(seqno % 256)

    frame.append(mod256_sum(frame))
    leading = bytearray()
    for i in range(leading_chars_nr):
        leading.append(0xfe)
    return leading + frame + bytearray([proto_algo['closing_tag']])

def recv_frame():
    def calc_mod256_chksum(frame):
        chksum = 0;
        for c in frame:
            chksum = (chksum + c) % 256
        return chksum
    def opening_tag_on_char(state, c):
        state['frame'].append(c)
        if ord(c) == proto_algo['opening_tag']:
            state['_len'] = 0
            return addr_on_char
        else:
            return opening_tag_on_char
    def addr_on_char(state, c):
        state['frame'].append(c)
        state['_len'] += 1
        if state['_len'] == proto_algo['addr_len']:
            return second_tag_on_char
        else:
            return addr_on_char
    def second_tag_on_char(state, c):
        state['frame'].append(c)
        if ord(c) == proto_algo['opening_tag']:
            return ctrl_on_char
        else:
            return None
    def ctrl_on_char(state, c):
        state['frame'].append(c)
        state['ctrl'] = ord(c)
        return length_on_char
    def length_on_char(state, c):
        state['frame'].append(c)
        state['_len'] = ord(c)
        if state['_len']:
            return data_on_char
        else:
            return chksum_on_char
    def data_on_char(state, c):
        state['frame'].append(c)
        state['_len'] -= 1
        state['data'].append(c)
        if state['_len'] > 0:
            return data_on_char
        return chksum_on_char
    def chksum_on_char(state, c):
        if calc_mod256_chksum(state['frame']) != ord(c):
            state['bad_chksum'] = True
        state['frame'].append(c)
        return closing_tag_on_char
    def closing_tag_on_char(state, c):
        state['frame'].append(c)
        if ord(c) == proto_algo['closing_tag']:
            state['completed'] = True
        return None

    state = {'frame': bytearray()
            , 'ctrl': 0, 'data': bytearray(), 'completed': False
            , 'bad_chksum': False}

    handler = opening_tag_on_char
    while True:
        if len(state['frame']):
            timeout = inter_char_timeout
        else:
            timeout = resp_timeout
        readable, _, _, = select([seri], [], [], timeout)
        if not readable:
            if not len(state['frame']):
                log('timeout')
            return state

        handler = handler(state, seri.read(1))
        if not handler: break
    state.pop('_len', None)
    return state

def read_single_id(id, seqno):
    req = create_read_req(id, seqno)
    if not no_trace:
        print_packet(bytes(req), '>')
    seri.write(bytes(req))
    seri.flush()
    return recv_frame()

def read_from_table():
    global read_nr, timeout_nr
    index = 0
    seqno = 0

    while index < len(id_table):
        entry = id_table[index]
        for r in range(entry[1] + 1):
            resp = read_single_id(entry[0], seqno)
            read_nr += 1
            if len(resp['frame']) \
                    and (not no_trace or not resp['completed']):
                print_packet(bytes(resp['frame']), ' ')
            if resp['bad_chksum']:
                log('bad chksum')
            if not len(resp['frame']):
                timeout_nr += 1
                continue

            if is_normal_resp(resp['ctrl']) or entry[2] == 0: 
                time.sleep(idle_wait)
                break
            else:
                time.sleep(entry[2])
        if not no_read_subsequent and len(resp['frame']) \
                and has_next_data(resp['ctrl']) \
                and seqno < 255:
            seqno += 1
        else:
            seqno = 0
            index += 1

def read_debug_counters():
    global last_read_counters_time

    if last_read_counters_time:
        delta = datetime.datetime.now() - last_read_counters_time
    else:
        delta = datetime.datetime.now()
    if delta.total_seconds() < read_counters_intvl:
        return

    resp = read_single_id(0x04910000, 0)
    if not len(resp['frame']): return
    if not no_trace or not resp['completed']:
        print_packet(bytes(resp['frame']), ' ')
    if len(resp['data']) != (20 + 1) * 4:
        log('error: incorrect counters resp: len=%d' % len(resp['data']))
        return
    data = resp['data'][4:] # strip the id
    decode_dl645_data(data)
    print_counters(data)
    last_read_counters_time = datetime.datetime.now()

def decode_dl645_data(data):
    for i in range(len(data)):
        m = data[i] - 0x33
        if m < 0:
            m = 256 + m
        data[i] = m

def parse_uint_be(array):
    n = 0
    for i in range(len(array)):
        n = n * 256 + array[i]
    return n

prev_krn_tics = None
prev_krn_tics_read_time = None
def print_counters(data):
    global prev_krn_tics, prev_krn_tics_read_time
    global cu_reset_nr

    mco_abort = parse_uint_be(data[:4])
    data = data[4:]
    mco_nak = parse_uint_be(data[:4])
    data = data[4:]
    mco_bcc = parse_uint_be(data[:4])
    data = data[4:]
    mco_timeout = parse_uint_be(data[:4])
    data = data[4:]
    mco_overrepeat = parse_uint_be(data[:4])
    data = data[4:]
    mco_lock_broken = parse_uint_be(data[:4])
    data = data[4:]
    mco_trans = parse_uint_be(data[:4])
    data = data[4:]
    mco_slave_reqs = parse_uint_be(data[:4])
    data = data[4:]
    mco_slave_resps = parse_uint_be(data[:4])
    data = data[4:]
    mco_master_reqs = parse_uint_be(data[:4])
    data = data[4:]
    mco_master_resps = parse_uint_be(data[:4])
    data = data[4:]
    mco_send_altered = parse_uint_be(data[:4])
    data = data[4:]
    mco_recv_altered = parse_uint_be(data[:4])
    data = data[4:]
    mco_duplex = parse_uint_be(data[:4])
    data = data[4:]
    mco_extq = parse_uint_be(data[:4])

    data = data[4:]
    dlp_sch_ddc_err = parse_uint_be(data[:4])
    data = data[4:]
    dlp_lock_broken = parse_uint_be(data[:4])
    data = data[4:]
    krn_send_lock_broken = parse_uint_be(data[:4])
    data = data[4:]
    idt = parse_uint_be(data[:4])
    data = data[4:]
    krn_tics = parse_uint_be(data[:4])

    summary = 'krn_tics: %d; ' % krn_tics
    if mco_abort:
        summary += 'mart: %d; ' % mco_abort
    if mco_nak:
        summary += 'mnak: %d; ' % mco_nak
    if mco_bcc:
        summary += 'mbcc: %d; ' % mco_bcc
    if mco_timeout:
        summary += 'mto: %d; ' % mco_timeout
    if mco_overrepeat:
        summary += 'movr: %d; ' % mco_overrepeat
    if mco_lock_broken:
        summary += 'mlb: %d; ' % mco_lock_broken
    if mco_send_altered:
        summary += 'msa: %d; ' % mco_send_altered
    if mco_recv_altered:
        summary += 'mdup: %d; ' % mco_duplex
    if mco_extq:
        summary += 'meq: %d; ' % mco_extq
    if mco_trans:
        summary += 'mtrans: %d (s: %d, %d, m: %d, %d); ' % (
                mco_trans, mco_slave_reqs, mco_slave_resps
                , mco_master_reqs, mco_master_resps)
    if dlp_lock_broken:
        summary += 'dlb: %d; ' % dlp_lock_broken
    if krn_send_lock_broken:
        summary += 'kslb: %d; ' % krn_send_lock_broken
    if idt:
        summary += 'idt: %d; ' % idt
    log(summary)

    if prev_krn_tics == None:
        prev_krn_tics = krn_tics
        prev_krn_tics_read_time = datetime.datetime.now()
        return

    delta = (datetime.datetime.now()
            - prev_krn_tics_read_time).total_seconds()
    # One sec = 200 tics in our CU
    # Times 5 giving it a margin
    if abs(krn_tics - prev_krn_tics) > (5 * delta * 200):
        log('detected CU reset!')
        cu_reset_nr += 1
        prev_krn_tics = krn_tics
        prev_krn_tics_read_time = datetime.datetime.now()

def print_statics():
    log('ttl reads=%d, timeout=%d' % (read_nr, timeout_nr))

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
    argp.add_argument('-x', '--no-trace'
            , action='store_true'
            , help='not to trace communication')
    argp.add_argument('-n', '--iterations'
            , type=int
            , default=1
            , help='number of iterations to run')
    argp.add_argument('--read-counters'
            , action='store_true'
            , help='read the debug counters (4.145.0.0)')
    argp.add_argument('--read-counters-intvl'
            , type=float
            , default=60
            , help='intvl secs to read the debug counters')

    args = argp.parse_args()
    if args.id_table == 'demo':
        id_table = __07_demo_ids
    elif args.id_table == 'keli':
        id_table = __07_keli_ids
    elif args.id_table == 'weisheng':
        id_table = __07_weisheng_ids
    elif args.id_table == 'simple':
        id_table = __07_simple_ids
    elif args.id_table == 'sky':
        id_table = __07_sky_ids
    elif args.id_table == 'all':
        id_table = __07_keli_ids + __07_weisheng_ids
    elif args.id_table == '97sky':
        id_table = __97_sky_ids
    elif args.id_table == 'empty':
        id_table = no_ids
    else:
        log('invalid id table')
        raise SystemExit
    if args.id_table[0] == '9' and args.id_table[1] == '7':
        mode_97 = True
    idle_wait = args.idle_wait
    resp_timeout = args.resp_timeout
    inter_char_timeout = args.inter_char_timeout
    leading_chars_nr = args.leading_chars
    no_trace = args.no_trace
    no_read_subsequent = args.no_read_subsequent
    if not mode_97:
        read_counters = args.read_counters
        read_counters_intvl = args.read_counters_intvl
    if mode_97:
        proto_algo = proto_algo_97

    seri = open_seri(args.device, args.baud)

    i = 0;
    while args.iterations == 0 or i < args.iterations:
        log('iteration %d' % (i + 1))
        for addr in args.addrs:
            log('read meter %s' % addr)
            read_from_table()
            if read_counters:
                read_debug_counters()
        print_statics()
        i += 1

