#!/usr/bin/python
import socket
from multiprocessing import Pool
import sys
from tabulate import tabulate
import ipaddress


def list_creation():
    data = []
    with open(sys.argv[1], 'r') as file:
        for line in file.readlines():
            initial_data = (i for i in ipaddress.ip_network(u'{}'.format(line.strip())))
            data.extend(map(str, initial_data))
            file.close()
    return sorted(data, key=lambda x:tuple(map(int, x.split('.'))))


def grab_banner(ip_address):
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((ip_address, int(sys.argv[2])))
        banner = s.recv(1024)
        s.close()
        if "cryptlib" in banner:
            return [ip_address, banner.strip()]
    except Exception:
        pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python {} CIDR_HOST_LIST PORT".format(sys.argv[0])
        sys.exit()
    else:
        ip_address = list_creation()
        pool = Pool(500)
        ip_address = list_creation()
        datapoint = pool.map(grab_banner, ip_address)
        print tabulate([x for x in datapoint if x is not None], headers=["IP_ADDRESS", "Banner"])



