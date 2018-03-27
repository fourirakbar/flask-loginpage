import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///loginits.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("5114100001","abctesting")
session.add(user)
 
user = User("5114100002","abctesting")
session.add(user)
 
user = User("5114100003","abctesting")
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()