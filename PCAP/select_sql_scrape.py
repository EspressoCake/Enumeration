#!/usr/bin/python

import dpkt
import string
import sys


def read():
    test = []
    f = open(sys.argv[1], "r")
    pcap = dpkt.pcap.Reader(f)

    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        data = filter(lambda x: x in string.printable, str(eth.data))
        test.append(data.split())

    for items in test:
        if "SELECT" in items:
            dataformat = items.index("SELECT")
            print "\r\n{0}".format(' '.join(items[dataformat:]))

read()

