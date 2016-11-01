#!/usr/bin/python

import requests
from tabulate import tabulate
from multiprocessing import Pool
import sys
import os

blankArray = []
IP_ADDRESS = []

def create_list():
    with open(sys.argv[1], 'r') as file:
        for line in file.readlines():
            IP_ADDRESS.append(line.strip())
        file.close()
    return IP_ADDRESS

def request(URL):
    data = requests.get("http://" + URL + "/", verify=False, allow_redirects=True)
    if "Protected" in data.text:
        blankArray.append([URL, "Protected Resource, False Positive"])
    else:
        try:
            datapoint = {'login_username':'device', 'login_password':'apc', }
            postRequest = requests.post("http://" + URL + "/Forms/login1", data=datapoint, allow_redirects=True)
            if "Invalid User Name or Password." in postRequest.text:
                blankArray.append([URL, "Invalid Credentials, Changed From Default"])
            elif "Someone is currently logged into the" in postRequest.text:
                blankArray.append([URL, "Couldn't attempt a login, someone is currently logged in."])
            else:
                blankArray.append([URL, "Default Credentials Valid"])
                requests.get((postRequest.url).replace('home.htm', 'logout.htm'))
        except Exception, e:
            blankArray.append([URL, "ERROR"])

if __name__ == '__main__':
    ip_Addr = create_list()
    os.system('clear')
    for item in ip_Addr:
        print "Attepting URL:", item
        request(item)
        os.system('clear')
    print tabulate(blankArray, headers=['URL', 'Status'])
