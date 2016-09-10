from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# import config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('clothing.config')
app.config.from_pyfile('configinst.py')

import views

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

from clothing import app
from models import Garment, Image, MatchRating, Event
from sqlalchemy.orm.exc import NoResultFound
from flask import render_template, abort, request, url_for, redirect

@app.route('/')
@app.route('/garments/')
def list_garments():
    session = Session()
    garments = session.query(Garment).all()
    session.commit()
    #return render_template('permissions.html', user=author)
    return "<html>*{}*: {}<BR> {}".format(len(garments), "hi", "I hate sissy")
