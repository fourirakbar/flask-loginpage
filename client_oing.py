from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
import os
import time
import mysql.connector
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)
db = mysql.connector.connect(user='taoing', password='fourir96akbar', host='192.168.0.15', database='ta_container')
cursor = db.cursor(buffered=True)

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print "masuk fungsi"

    input_json = request.get_json(force=True)

    # iptables1 = 'iptables -I FORWARD 1 -s '+input_json.split("|")[1]+' -j ACCEPT' 
    # # iptables2 = 'iptables -t nat -I PREROUTING 1 -s '+input_json.split("|")[1]+' -j ACCEPT'
    # iptables3 = 'iptables -t nat -I POSTROUTING 1 -o wlp3s0 -j MASQUERADE -s '+input_json.split("|")[1]+''

    # os.system(iptables1)
    # time.sleep(1)
    # # os.system(iptables2)
    # # time.sleep(1)
    # os.system(iptables3)
    # time.sleep(1)

    readdata = open("data.txt", "r")
    check = readdata.read()
    print "IKI CHECK COK: "+check
    if check:
        print "masuk check"
        boi = check.split("|")
        print boi[2]
        print len(boi)
        old_port = boi[2]
        def_port = int(old_port) + 1
    else:
        print "ga masuk check"
        def_port = 49152

    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]
    print 'YOUR PORT:', def_port
    
    writenew = str(input_json) + "|" + str(def_port)

    with open("data.txt", "wb") as fo:
        fo.write(str(writenew))

    print "WES MARI COK"

    subprocess.call(["python", "docker_oing.py"])

    print "jancok mari cok"

    iptables1 = 'iptables -I FORWARD 1 -s '+input_json.split("|")[1]+' -j ACCEPT' 
    # iptables2 = 'iptables -t nat -I PREROUTING 1 -s '+input_json.split("|")[1]+' -j ACCEPT'
    iptables2 = 'iptables -t nat -I POSTROUTING 1 -o wlp3s0 -j MASQUERADE -s '+input_json.split("|")[1]+''
    iptables3 = 'iptables -t nat -I PREROUTING 1 -i vboxnet0 -s '+input_json.split("|")[1]+' -p tcp --dport 80 -j REDIRECT --to-ports '+str(def_port)+''
    iptables4 = 'iptables -t nat -I PREROUTING 1 -i vboxnet0 -s '+input_json.split("|")[1]+' -p tcp --dport 443 -j REDIRECT --to-ports '+str(def_port)+''

    os.system(iptables1)
    time.sleep(1)
    os.system(iptables2)
    time.sleep(1)
    os.system(iptables3)
    time.sleep(1)
    os.system(iptables4)

    print "sukses"
    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

