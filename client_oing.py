from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
import os
import time
import mysql.connector
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)
db = mysql.connector.connect(user='taoing', password='fourir96akbar', host='10.151.36.134', database='ta_container')
cursor = db.cursor(buffered=True)

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print "masuk fungsi"

    input_json = request.get_json(force=True)

    iptables1 = 'iptables -I FORWARD 1 -s '+input_json.split("|")[1]+' -j ACCEPT' 
    iptables2 = 'iptables -t nat -I PREROUTING 1 -s '+input_json.split("|")[1]+' -j ACCEPT'
    iptables3 = 'iptables -t nat -I POSTROUTING 1 -o wlp3s0 -j MASQUERADE -s '+input_json.split("|")[1]+''

    os.system(iptables1)
    time.sleep(1)
    os.system(iptables2)
    time.sleep(1)
    os.system(iptables3)
    time.sleep(1)

    readdata = open("data.txt", "r")
    boi = readdata.read().split("|")
    print boi[2]
    print len(boi)

    if len(boi) == 1:
        def_port = 49152
    else:
        old_port = boi[2]
        def_port = int(old_port) + 1

    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]
    print 'YOUR PORT:', def_port
    
    writenew = str(input_json) + "|" + str(def_port)

    with open("data.txt", "wb") as fo:
        fo.write(str(writenew))      

    subprocess.call(["python", "docker_oing.py"])
    print "sukses"
    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

