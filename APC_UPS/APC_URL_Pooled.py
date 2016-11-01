#!/usr/bin/python

import requests
from tabulate import tabulate
from multiprocessing import Pool
import sys
import os

IP_ADDRESS = []

def create_list():
    with open(sys.argv[1], 'r') as file:
        for line in file.readlines():
            IP_ADDRESS.append(line.strip())
        file.close()
    return sorted(IP_ADDRESS, key=lambda x:tuple(map(int, x.split('.'))))

def request(URL):
    data = requests.get("http://" + URL + "/", verify=False, allow_redirects=True)
    if "Protected" in data.text:
        return [URL, "Protected Resource, False Positive"]
    else:
        try:
            datapoint = {'login_username':'device', 'login_password':'apc'}
            postRequest = requests.post("http://" + URL + "/Forms/login1", data=datapoint, allow_redirects=True)
            if "Invalid User Name or Password." in postRequest.text:
                return [URL, "Invalid Credentials, Changed From Default"]
            elif "Someone is currently logged into the" in postRequest.text:
                return [URL, "Couldn't attempt a login, someone is currently logged in."]
            else:
                return [URL, "Default Credentials Valid"]
                requests.get((postRequest.url).replace('home.htm', 'logout.htm'))
        except Exception, e:
            pass

if __name__ == '__main__':
    ip_Addr = create_list()
    pool = Pool(150)
    datapoint = pool.map(request, ip_Addr)
    print tabulate([x for x in datapoint if x is not None], headers=['URL', 'Status'])
