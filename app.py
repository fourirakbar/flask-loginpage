import redis
import MySQLdb
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import request
from flask import jsonify
import json
import os
import requests
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_socketio import SocketIO
engine = create_engine('sqlite:///loginits.db', echo=True)
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
db = MySQLdb.connect("10.151.36.38","taoing","fourir96akbar","coba")
cursor = db.cursor()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # ip_client = jsonify({'ip': request.remote_addr}), 200
        # dictToSend = {'question':json=dictToSend'what is the answer?'}
        
        # print 'response from server: ', res.text
        # dictFromServer = res.json()
        result = request.form
        # ip_client = request.remote_addr
        # ip_client = {'ip': 'request.remote_addr'}
        # res = requests.post('http://10.151.36.38:5000/test/endpoint', data=ip_client)
        # return res.text
        return render_template('welcome.html', ip_client = request.remote_addr, result = result)
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    print "fungsi 1"
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    POST_IP = str(request.remote_addr)
    
    Session = sessionmaker(bind=engine)
    s = Session()
    print "====="
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    print "sebelum if"
    if result:
        print "masuk if"
        sql = "SELECT * FROM testing WHERE nrp = '%s'" % POST_USERNAME
        print sql
        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            print results
            print "-----"
            if results:
                print "NRP sudah digunakan"
                for row in results:
                    print "Masuk for"
                    print row[2]
                    # id = row[0]
                    # nrp = row[1]
                    # ip = row[2]

                    # print "id=%s,nrp=%s,ip=%d" % (id, nrp, ip )
            else:
                sql_insert = """INSERT INTO testing(nrp, ip) VALUES ('%s', '%s')""" % (POST_USERNAME, POST_IP)
                try:
                    cursor.execute(sql_insert)
                    db.commit()
                except:
                    db.rollback()
                db.close()
                print "done insert"

                session['logged_in'] = True
                ip_client = POST_USERNAME + "|" + request.remote_addr
                # ip_client = jsonify({'ip': request.remote_addr}), 200
                print "masuk"
                res = requests.post('http://10.151.36.38:5000/tests/endpoint', headers={'content-type': 'application/json'}, json=ip_client)
            
        except:
            print "Error: unable to fetch data"

        
        print "done boi"
        # r = redis.StrictRedis(host='10.151.36.38', port=6379, db=0)

        # check_nrp = r.get(POST_USERNAME)

        # if check_nrp:
            # print "NRP sudah digunakan: "+check_nrp
        # else:
            # print "NRP belum digunakan"
            # r.set(POST_USERNAME, request.remote_addr)
    
            

            # dictToSend = {'question':'what is the answer?'}
            # res = requests.post('10.151.36.38:5000/test/endpoint', json=dictToSend)
            # print 'response from server: ', res.text
            # ductFromServer = res.json()

    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip_client = jsonify({'ip': request.remote_addr}), 200

@app.route("/query-example")
def query_exampe():
    username = request.args.get('username')
    your_ip = request.remote_addr
    return '''<h1>Your name is: {}</h1>
            <h1>Your IP is: {}</h1>'''.format(username, your_ip)

@app.route("/form-example", methods=['GET', 'POST'])
def form_example():
    return '''<form method="POST">
                  Username: <input type="text" name="username"><br>
                  Password: <input type="text" name="password"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route("/json-example", methods=['POST'])
def json_exampe():
    return 'Todo...'
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)