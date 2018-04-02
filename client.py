from flask import Flask, render_template, request, url_for, jsonify
import docker
app = Flask(__name__)

@app.route('/')
def home():
    print "masuk home"

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

    with open("nrp.txt", "wb") as fo:
        fo.write(str(input_json))

    return home()

    return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

