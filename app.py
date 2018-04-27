import redis
import mysql.connector
# import MySQLdb
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
db = mysql.connector.connect(user='taoing', password='fourir96akbar', host='10.151.36.38', database='coba')
cursor = db.cursor(buffered=True)
cursor2 = db.cursor(buffered=True)
cursor3 = db.cursor(buffered=True)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        result = request.form
        return render_template('welcome.html', ip_client = request.remote_addr, result = result)

@app.route('/hello')
def hello():
    return redirect("/", code=302)

 
@app.route('/login', methods=['POST'])
def do_admin_login():
    print ("fungsi 1")
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    POST_IP = str(request.remote_addr)
    
    Session = sessionmaker(bind=engine)
    s = Session()
    print "====="
    # query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    query = "SELECT * FROM database_nrp WHERE nrp = '%s' AND password = '%s'" % (POST_USERNAME, POST_PASSWORD)
    print "This is query: "+query
    cursor.execute(query)
    print "Done execute query"
    hasil = cursor.fetchall()
    # cursor.close()
    print hasil
    # result = query.first()
    print "sebelum if"
    if hasil:
        print "masuk if"
        sql = "SELECT * FROM testing WHERE nrp = '%s'" % POST_USERNAME
        cursor.execute(sql)
        response = cursor.fetchall()
        # cursor.close()
        # sql = "SELECT * FROM testing WHERE nrp = '%s'" % POST_USERNAME
        # response = cursor.execute(sql)
        print response
        print "----"
        if response:
            print "Sudah ada di db"
            # results = cursor.fetchall()
            # # cursor.close()
            # if results:
            #     print "NRP sudah digunakan"
            #     for row in results:
            #         print "Masuk for"
            #         print row[2]
        else:
            print "Belum ada di db"
            sql_insert = """INSERT INTO testing(nrp, ip) VALUES ('%s', '%s')""" % (POST_USERNAME, POST_IP)
            print "This is sql_insert: "+sql_insert
            cursor2.execute(sql_insert)
            # cursor2.close()
            db.commit()
            # try:
            #     print "masuk try untuk insert"
                
            # except:
            #     print "ga masuk try untuk insert"
            #     db.rollback()
            # db.close()
            print "done insert"

            session['logged_in'] = True
            ip_client = POST_USERNAME + "|" + request.remote_addr
            
            print "masuk: "+ip_client
            res = requests.post('http://10.151.36.38:5000/tests/endpoint', headers={'content-type': 'application/json'}, json=ip_client)
            print res
            print "done boi"

    else:
        print "Data tidak ada di database"
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