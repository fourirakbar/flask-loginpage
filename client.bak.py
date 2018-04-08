from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint(self):
    # index_port = index_port + 1
    # print "masuk: "+index_port
    input_json = request.get_json(force=True) 
    print request
    print "==="
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]

    with open("data.txt", "wb") as fo:
        fo.write(str(input_json))

    getNRP = input_json.split("|")[0] 
    getIP = input_json.split("|")[1]        

    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

