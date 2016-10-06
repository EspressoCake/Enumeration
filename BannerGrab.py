#!/usr/bin/python

import socket
import sys
import os
from tabulate import tabulate
from optparse import OptionParser
import ipaddress

parser = OptionParser()
usage = "USAGE: %prog [options]"
parser.add_option("-i", type="string", help="Required Input CIDR File", dest="infile")
parser.add_option("-n", type="int", help="Required Port To Scan", dest="port")
parser.add_option("-s", type="string", help="Required Banner String", dest="banner")
parser.add_option("-f", type="string", help="Optional Output File", dest="outfile")
parser.add_option("-v", action="store_true", help="Display Tabulated Data To Standard Output", dest="verbose")

(options, args) = parser.parse_args()

table = []

def banner_grab(IP, PORT):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((IP, PORT))
        banner=s.recv(20)
        if options.banner in banner:
            table.append([IP,PORT,banner])
            s.close()
        else:
            s.close()
    except:
        return

def main():
    if len(sys.argv[1:]) == 0:
        parser.print_help()
    if not all((options.port, options.banner, options.infile)):
        parser.error("Please Supply All Required Arguments!")
    if options.infile:
        os.system("clear")
        with open(options.infile, 'r') as file:
            for line in file.readlines():
                net = ipaddress.ip_network(u'{}'.format(line.strip()))
                print "Beginning Network With CIDR Notation:", line.strip()
                for i in net:
                    banner_grab(line, options.port)
                file.close()
            print
    if options.outfile:
        with open(options.outfile, "w") as file:
            file.write(tabulate(table, headers=["IP_ADDRESS","PORT","SOFTWARE"]))
    if options.verbose:
        print tabulate(table, headers=["IP_ADDRESS","PORT","SOFTWARE"])


if __name__ == "__main__":
    main()

