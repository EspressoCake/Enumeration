#!/usr/bin/python
import socket
from multiprocessing import Pool
from optparse import OptionParser
import sys
from tabulate import tabulate
import ipaddress
import subprocess


parser = OptionParser()
usage = "USAGE: %prog [options]"
parser.add_option("-i", type="string", help="Required Input CIDR File", dest="infile")


(options, args) = parser.parse_args()


def list_creation():
    data = []
    with open(options.infile, 'r') as file:
        for line in file.readlines():
            initial_data = (i for i in ipaddress.ip_network(u'{}'.format(line.strip())))
            data.extend(map(str, initial_data))
            file.close()
    return sorted(data, key=lambda x:tuple(map(int, x.split('.'))))


def ping_host(ip_address):
    try:
        data = subprocess.check_output('ping -c1 -W1 {0} | grep "received" 2>/dev/null'.format(ip_address), shell=True)
        if "1 received" in data:
            return [ip_address, "Alive"]
    except Exception:
        pass

if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        parser.print_help()
    else:
        ip_address = list_creation()
        pool = Pool(250)
        print "\n\nIPs In Queue: {}\n\n".format(len(ip_address))
        datapoint = pool.map(ping_host, ip_address)
        tableData = tabulate([x for x in datapoint if x is not None], headers=["IP_ADDRESS", "Status"], tablefmt="grid")
        print tableData
