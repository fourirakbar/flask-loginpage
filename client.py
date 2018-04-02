from flask import Flask, render_template, request, url_for, jsonify
import docker
app = Flask(__name__)

@app.route('/')
def create_container():
    print "Start create container using docker"

    file = open("data.txt", "r")
    result = file.read()
    # print "Isi file data.txt: "+result

    name_container = result.split("|")[0]
    print "Name container: "+name_container

    client = docker.from_env()

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print "masuk"
    input_json = request.get_json(force=True) 
    print request
    print "==="
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print 'NRP:', input_json.split("|")[0]
    print 'YOUR IP:', input_json.split("|")[1]

    with open("data.txt", "wb") as fo:
        fo.write(str(input_json))

    return create_container()

    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

