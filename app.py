from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import request
from flask import jsonify
import json
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///loginits.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        ip_client = jsonify({'ip': request.remote_addr}), 200
        result = request.form
        # return result
        return render_template('welcome.html', ip_client = request.remote_addr)
        # return ip_client
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
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
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)