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
cursor2 = db.cursor(buffered=True)

gw_device = netifaces.gateways()['default'][netifaces.AF_INET][1]
array_ip_source = []
tmp_sourceIP = []
flag=0
counter = 1

while True:
    print "Percobaan ke = "+str(counter)
    rawSocket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
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

    #kalo IP source sama IP dest nya bener
    if destinationIP != "10.151.36.134" and destinationIP != "10.151.36.255" and destinationIP != "255.255.255.255" and sourceIP != "10.151.36.1" and sourceIP != "127.0.0.1" and sourceIP != "10.151.36.3" and sourceIP != "10.151.36.12" and sourceIP != "10.151.36.5":
        print "Masuk if dengan IP: "+sourceIP

        #dicek, apakah IP tersebut sudah dibuatkan container / belum (ada di tabel container apa enggak)
        query = "SELECT * FROM container WHERE name_container = '%s'" % (sourceIP)
        query_cursor = cursor.execute(query)
        hasil = cursor.fetchall()

        #kalo belum dibuatkan container / belum ada di tabel container        
        if hasil:
            print "Sudah dibuatkan container"
        else:
            #cek apakah user tersebut sudah login / belum. dilihat dari flag di tabel iptables_login
            query2 = "SELECT flag_iptables_login FROM iptables_login WHERE ip_iptables_login = '%s'" % (sourceIP)
            print query2
            cursor2.execute(query2)
            hasil2 = cursor2.fetchall()

            if hasil2 and sourceIP == "10.151.36.70":
                #jika sudah diarahkan ke halaman login. dicek ip tersebut sudah login / belum
                str_hasil2 = str(hasil2)
                print str_hasil2.split("(")[1].split(",")

                if str_hasil2.split("(")[1].split(",")[0] == "0":
                    print "ip tersebut sudah diarahkan ke halaman login, tetapi belum login"

                elif str_hasil2.split("(")[1].split(",")[0] == "1":
                    print "ip tersebut sudah berhasil login"

            elif sourceIP == "10.151.36.70":

                print "Mulai diarahkan ke halaman login. IP SRC: "+sourceIP+" dan IP DST: "+destinationIP

                iptables1 = 'iptables -A FORWARD -s '+sourceIP+' -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT'
                iptables2 = 'iptables -A FORWARD -s '+sourceIP+' -p tcp -d 10.151.36.130 --dport 4000 -j ACCEPT'
                iptables3 = 'iptables -t nat -A PREROUTING -p tcp -s '+sourceIP+' --dport 80 -j DNAT --to 10.151.36.130:4000'
                iptables4 = 'iptables -t nat -A POSTROUTING -s '+sourceIP+' -p tcp -d 10.151.36.130 --dport 4000 -j MASQUERADE'

                os.system(iptables1)
                time.sleep(1)
                os.system(iptables2)
                time.sleep(1)
                os.system(iptables3)
                time.sleep(1)
                os.system(iptables4)             

                print "Selesai dibuatkan iptables untuk membuka halaman login. Tulis di tabel iptables_login"

                sql_insert = """INSERT INTO iptables_login(ip_iptables_login, flag_iptables_login) VALUES ('%s', '%s')""" % (sourceIP, 0)
                cursor.execute(sql_insert)
                db.commit()

                print "Selesai dituliskan di tabel iptables_login"        

    counter = counter + 1
    print "buyar bos"
    print "========="
    flag = 0
    time.sleep(1)