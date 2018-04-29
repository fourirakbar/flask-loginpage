from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
import os
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)
print "boi"
@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print "masuk fungsi"

    input_json = request.get_json(force=True) 

    iptables1 = 'iptables -D FORWARD -s '+input_json.split("|")[1]+' -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT'
    iptables2 = 'iptables -D FORWARD -s '+input_json.split("|")[1]+' -p tcp -d 10.151.36.130 --dport 4000 -j ACCEPT'
    iptables3 = 'iptables -t nat -D PREROUTING -p tcp -s '+input_json.split("|")[1]+' --dport 80 -j DNAT --to 10.151.36.130:4000'
    iptables4 = 'iptables -t nat -D POSTROUTING -s '+input_json.split("|")[1]+' -p tcp -d 10.151.36.130 --dport 4000 -j MASQUERADE'

    os.system(iptables1)
    os.system(iptables2)
    os.system(iptables3)
    os.system(iptables4)

    print "done delete rules iptables"

    readdata = open("data.txt", "r")
    boi = readdata.read().split("|")
    print boi[2]
    print len(boi)

    if len(boi) == 1:
        def_port = 3128
    else:
        old_port = boi[2]
        def_port = int(old_port) + 3
        print "This is old port: "+str(old_port)
    
    print "This is def port: "+str(def_port)
    # input_json = request.get_json(force=True) 
    print request
    print "==="
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]
    print 'YOUR PORT:', str(def_port)

    writenew = str(input_json) + "|" + str(def_port)

    with open("data.txt", "wb") as fo:
        fo.write(str(writenew))

    getNRP = input_json.split("|")[0] 
    getIP = input_json.split("|")[1]        

    subprocess.call(["python", "docker_oing.py"])

    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

