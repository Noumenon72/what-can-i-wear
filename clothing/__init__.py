import datetime

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# import config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('clothing.config')
app.config.from_pyfile('configinst.py')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

from clothing import app
from models import Garment, Event
from flask import render_template, abort, request, redirect

@app.route('/')
def show_entry_page():
    return render_template("index.html")

@app.route('/garments/')
def list_garments():
    session = Session()
    garments = session.query(Garment).all()
    session.commit()
    #return render_template('permissions.html', user=author)
    return "<html>*{}*: {}<BR> {}".format(len(garments), "hi", "I hate sissy")

@app.route('/events/')
def list_events():
    bob = 'change me to refresh flask '
    session = Session()
    events = session.query(Event).all()

    session.commit()
    return render_template('events.html', events=events)

@app.route('/garments/<int:garment_id>/events/', methods=['GET'])
def list_events_for_garment(garment_id):
    session = Session()
    wears, garments = list()
    res = session.query(Event, Garment)\
        .filter(Event.garment_id == Garment.garment_id)\
        .filter_by(garment_id=garment_id).all()
    if len(res):
        (wears, garments) = list(zip(*res))
    else:
        abort(404)
    return render_template('wears.html', garment_id=garment_id, garment_name=garments[0].name, events=wears)

@app.route('/events/new', methods=['POST'])
def add_event():
    session = Session()
    event = Event()
    event.garment_id = request.form['garment_id']
    event.event_type = request.form['event_type']
    event.event_date = datetime.datetime.strptime(request.form['event_date'], '%Y-%m-%d')
    session.add(event)
    session.commit()
    return redirect('/events/')