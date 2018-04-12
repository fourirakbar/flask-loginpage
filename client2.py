from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)
print "boi"
@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print "masuk fungsi"

    readdata = open("data.txt", "r")
    boi = readdata.read().split("|")
    print boi[2]
    print len(boi)

    if len(boi) == 1:
        def_port = 9001    
    else:
        old_port = boi[2]
        def_port = int(old_port) + 1
        print "This is old port: "+str(old_port)
    
    print "This is def port: "+str(def_port)
    input_json = request.get_json(force=True) 
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

