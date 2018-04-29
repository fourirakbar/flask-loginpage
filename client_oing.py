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

    #delete iptables yg berfungsi mengarahkan ke halaman login
    iptables1 = 'iptables -D FORWARD -s '+input_json.split("|")[1]+' -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT'
    iptables2 = 'iptables -D FORWARD -s '+input_json.split("|")[1]+' -p tcp -d 10.151.36.130 --dport 4000 -j ACCEPT'
    iptables3 = 'iptables -t nat -D PREROUTING -p tcp -s '+input_json.split("|")[1]+' --dport 80 -j DNAT --to 10.151.36.130:4000'
    iptables4 = 'iptables -t nat -D POSTROUTING -s '+input_json.split("|")[1]+' -p tcp -d 10.151.36.130 --dport 4000 -j MASQUERADE'

    os.system(iptables1)
    time.sleep(1)
    os.system(iptables2)
    time.sleep(1)
    os.system(iptables3)
    time.sleep(1)
    os.system(iptables4)

    print "done delete rules iptables"
    #update di tabel iptables_login, set status sudah berhasil login = true
    query = "UPDATE iptables_login SET flag_iptables_login = 1 WHERE ip_iptables_login = '%s'" % (input_json.split("|")[1])
    cursor.execute(query)
    db.commit()

    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]
    

    writenew = str(input_json)

    with open("data.txt", "wb") as fo:
        fo.write(str(writenew))      

    subprocess.call(["python", "docker_oing.py"])

    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

