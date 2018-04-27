#!/usr/bin/env python
import struct
import sys,os
import socket
import binascii
import netifaces
import mysql.connector
import socket
import requests
import time
import subprocess
import os
from scapy.all import *

db = mysql.connector.connect(user='taoing', password='fourir96akbar', host='10.151.36.134', database='ta_container')
cursor = db.cursor(buffered=True)

gw_device = netifaces.gateways()['default'][netifaces.AF_INET][1]
array_ip_source = []
tmp_sourceIP = []
flag=0
# with open('ipsrc.txt') as baca:
#     for line in baca:
#         print "This is line: "+line
#         if 'str' in line:
#             print "something good"
#             break

# sniff = sniff(iface='wlp3s0')
# print sniff.summary()
counter = 1
while True:
    print "Percobaan ke = "+str(counter)
    rawSocket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
    #ifconfig eth0 promisc up
    receivedPacket=rawSocket.recv(2048)

    #Ethernet Header...
    ethernetHeader=receivedPacket[0:14]
    ethrheader=struct.unpack("!6s6s2s",ethernetHeader)
    destinationIP= binascii.hexlify(ethrheader[0])
    sourceIP= binascii.hexlify(ethrheader[1])
    protocol= binascii.hexlify(ethrheader[2])

    # print "Destination: " + destinationIP
    # print "Source: " + sourceIP
    # print "Protocol: "+ protocol

    #IP Header... 
    ipHeader=receivedPacket[14:34]
    ipHdr=struct.unpack("!12s4s4s",ipHeader)
    destinationIP=socket.inet_ntoa(ipHdr[2])
    sourceIP=socket.inet_ntoa(ipHdr[1])

    readdata = open("ipsrc.txt", "r")
    subnetajk = sourceIP.split(".")
    
    if subnetajk[0] == "10" and subnetajk[1] == "151" and subnetajk[2] == "36":
        if destinationIP != "10.151.36.134" and destinationIP != "10.151.36.255" and destinationIP != "255.255.255.255" and sourceIP != "10.151.36.1" and sourceIP != "127.0.0.1" and sourceIP != "10.151.36.3" and sourceIP != "10.151.36.12" and sourceIP != "10.151.36.5":
            print "Start with: "+sourceIP

            if not array_ip_source:
                print "Masuk array kosong"
                array_ip_source.append(sourceIP)
                flag = 1
            else:
                for i in array_ip_source:
                    print "Iki i: "+i
                    if sourceIP in array_ip_source:
                        continue
                    else:
                        print "Tambah mbut"    
                        array_ip_source.append(sourceIP)
                    

    for data in array_ip_source:
        query = "SELECT * FROM container WHERE name_container = '%s'" % (data)        
        cursor.execute(query)
        hasil = cursor.fetchall()
        print hasil
        if hasil:
            print "ada ing"
        else:
            # diarahin ke halaman login
            # iptables -t nat -D PREROUTING -i wlp3s0 -s 10.151.36.37 -p tcp --dport 80 -j REDIRECT --to-ports 4000
            print "Masuk else dengan IP: "+sourceIP+ " dan destination IP: "+destinationIP
            print "xxxxx"
            print tmp_sourceIP
            print "xxxxx"
            if flag == 1 and sourceIP == "10.151.36.70":
                print "flag = 1 bosku: "+sourceIP
                # string_iptables = 'iptables -t nat -A PREROUTING -i wlp3s0 -s '+sourceIP+' -p tcp --dport 80 -j REDIRECT --to-ports 4000'
                # string_iptables = 'iptables -t nat -A PREROUTING -i wlp3s0 -s '+sourceIP+' -p tcp --dport 80 -j REDIRECT --to-destination 10.151.36.130:4000/hello'

                iptables1 = 'iptables -A FORWARD -s '+sourceIP+' -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT'
                iptables2 = 'iptables -A FORWARD -s '+sourceIP+' -p tcp -d 10.151.36.130 --dport 4000 -j ACCEPT'
                iptables3 = 'iptables -t nat -A PREROUTING -p tcp -s '+sourceIP+' --dport 80 -j DNAT --to 10.151.36.130:4000'
                iptables4 = 'iptables -t nat -A POSTROUTING -s '+sourceIP+' -p tcp -d 10.151.36.130 --dport 4000 -j MASQUERADE'

                os.system(iptables1)
                os.system(iptables2)
                os.system(iptables3)
                os.system(iptables4)

                tmp_sourceIP.append(sourceIP)

            
            else:
                print "boi"
                # if sourceIP in tmp_sourceIP:
                #     print "set iptables now!!"
                #     # string_iptables = 'iptables -t nat -A PREROUTING -i wlp3s0 -s '+sourceIP+' -p tcp --dport 80 -j REDIRECT --to-ports 4000'
                #     iptables1 = 'iptables -A FORWARD -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT'
                #     iptables2 = 'iptables -A FORWARD -p tcp -d 10.151.36.130 --dport 4000 -j ACCEPT'
                #     iptables3 = 'iptables -t nat -A PREROUTING -p tcp -s '+sourceIP+' --dport 80 -j DNAT --to 10.151.36.130:4000'
                #     iptables4 = 'iptables -t nat -A POSTROUTING -p tcp -d 10.151.36.130 --dport 4000 -j MASQUERADE'

                #     os.system(iptables1)
                #     os.system(iptables2)
                #     os.system(iptables3)
                #     os.system(iptables4)
                #     tmp_sourceIP.append(sourceIP)
        

    counter = counter + 1
    print "buyar bos"
    print "========="
    flag = 0
    time.sleep(3)