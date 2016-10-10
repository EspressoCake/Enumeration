#!/usr/bin/python
import socket
from multiprocessing import Pool
from optparse import OptionParser
import sys
from tabulate import tabulate
import ipaddress


parser = OptionParser()
usage = "USAGE: %prog [options]"
parser.add_option("-i", type="string", help="Required Input CIDR File", dest="infile")
parser.add_option("-n", type="int", help="Required Port To Scan", dest="port")
parser.add_option("-s", type="string", help="Required Banner String", dest="banner")
parser.add_option("-f", type="string", help="Optional Output File", dest="outfile")

(options, args) = parser.parse_args()


def list_creation():
    data = []
    with open(options.infile, 'r') as file:
        for line in file.readlines():
            initial_data = (i for i in ipaddress.ip_network(u'{}'.format(line.strip())))
            data.extend(map(str, initial_data))
            file.close()
    return sorted(data, key=lambda x:tuple(map(int, x.split('.'))))


def grab_banner(ip_address):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip_address, options.port))
        banner = s.recv(1024)
        s.close()
        if options.banner in banner:
            return [ip_address, banner.strip()]
    except Exception:
        pass

if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        parser.print_help()
    if not all((options.port, options.banner, options.infile)):
        parser.error("Please Supply All Required Arguments!")
    else:
        ip_address = list_creation()
        pool = Pool(1500)
        print "\n\nIPs In Queue: {}\n\n".format(len(ip_address))
        datapoint = pool.map(grab_banner, ip_address)
        tableData = tabulate([x for x in datapoint if x is not None], headers=["IP_ADDRESS", "Banner"], tablefmt="grid")
        if options.outfile:
            with open(options.outfile, 'w') as outfile:
                outfile.write(tableData)
                outfile.close()
        else:
            print tableData

