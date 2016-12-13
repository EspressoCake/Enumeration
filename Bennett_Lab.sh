#!/bin/bash

> /etc/resolv.conf
echo "nameserver 10.11.1.220" > /etc/resolv.conf

for i in {1..254}; do
    host -l 10.11.1.$i | grep -v "not found" | awk 'BEGIN{FS="."}{print $4"."$3"."$2"."$1$6}' | sed 's/arpa domain name pointer/ is/g'; done

