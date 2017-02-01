#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import sys, threading, subprocess, time, socket, signal

log_server = "10.86.201.53"

runners = []
killed = False

def get_timestamp():
    secs = time.time()
    return time.strftime("%y-%m-%dT%H:%M:%S"
            , time.localtime(int(secs))) \
            + '.%03d' % int((secs % 1) * 1000)

def conn_log_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((log_server, port))
    return sock;

def gen_runner(name, log_port, iterations, args):
    sys.stdout.write('starting runner %s\n' % name)
    logsink = conn_log_server(log_port)
    i = 0
    while (iterations == 0 or i < iterations) \
            and not killed:
        time.sleep(1)
        logsink.send(get_timestamp() + ' %s iteration %d\n' % (name, i))
        p = subprocess.Popen([name] + args
                , stdout=subprocess.PIPE
                , stderr=subprocess.STDOUT)
        while True:
            output = p.stdout.readline()
            if not output or killed:
                p.terminate()
                break
            logsink.send(output)
        i += 1
    logsink.send(get_timestamp() + ' %s ended\n' % name)
    logsink.close()

def dispatch_script_line(line):
    runners.append(Test_job(line))

def run_test():
    for r in runners:
        r.start()
    for r in runners:
        r.join()

class Test_job(threading.Thread):
    def __init__(self, job_desc):
        threading.Thread.__init__(self)
        self.job_desc = job_desc
    def run(self):
        # job desc line:
        # <runner name> <log_port> <iterations> ...
        toks = self.job_desc.split()
        runner = toks[0]
        log_port = int(toks[1])
        iterations = int(toks[2])
        args = toks[3:]
        gen_runner(runner, log_port, iterations, args)

if __name__== '__main__':
    argp = ArgumentParser(prog='runtest.py')
    argp.add_argument('script')
    args = argp.parse_args()

    for line in open(args.script):
        norm = line.strip()
        if not norm: continue
        if norm[0] == '#': continue
        dispatch_script_line(norm)
    run_test()

