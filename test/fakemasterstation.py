#!/usr/bin/env python

import os, pty

from six import int2byte, byte2int, iterbytes, PY3

if PY3:
    def byte2int(x):
        try:
            return x[0]
        except TypeError:
            return x


class FakeMasterStation(object):
    
    def __init__(self):
        master, slave = pty.openpty()
        s_name = os.ttyname(slave)
        print("FakeMasterStation port: %s" % s_name)
        self.master = master
        self.slave = slave
        self.port = s_name

    def read(self):
        cmd = os.read(self.master,32)
        print("=> %s" % ' '.join(hex(byte2int(c)) for c in cmd))
        if cmd == b'\xfe\x46\x00\x46':
            os.write(self.master, b'\xfe\x66\x01\xd2\x39') # version 2.10
        elif cmd == b'\xfe\x59\x00\x59':
            os.write(self.master, b'\xfe\x70\x00\x70') # send Ok
        elif cmd == b'\xfe\x58\x00\x58':
            os.write(self.master, b'\xfe\x70\x00\x70') # send Ok
            #os.write(self.master, b'\xfe\x78\x01\x01\x7a') # send COM err
        elif cmd[0:3] == b'\xfe\x41\x06':
            os.write(self.master, b'\xfe\x70\x00\x70') # send Ok


if __name__ == "__main__":
    fms = FakeMasterStation()
    print('Reading...')
    while True:
        fms.read()

