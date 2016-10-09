import datetime

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, state

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

@app.route('/garments_dropdown')
def garments_dropdown():
    session = Session()
    garments = session.query(Garment)
    if not request.args.get("short_sleeves") == "true":
        garments = garments.filter(Garment.style!="polo").filter(Garment.style!="short-sleeved dress")
    garments = garments.all()
    session.commit()
    for garment in garments:
        garment.wears_since_last_wash = \
            len([event for event in garment.events if
                 event.event_date > garment.last_washed and event.event_type == 'wear'])
        garment.wears_left_till_wash = garment.wears_between_washes - garment.wears_since_last_wash
    return render_template("garments_dropdown.html", garments=garments)


@app.route('/garments/')
def list_garments():
    session = Session()
    garments = session.query(Garment).all()
    session.commit()
    return "<html>*{}*: {}<BR> {}".format(len(garments), "hi", "I hate sissy")

@app.route('/events/')
def list_events():
    bob = 'change me to refresh flask '
    session = Session()
    events = session.query(Event).all()

    session.commit()
    return render_template('events.html', events=events)

@app.route('/events/history')
def list_history():
    get = request.args.get('event_type')
    session = Session()
    events = session.query(Event).filter_by(event_type=get).all()
    session.commit()
    return render_template('events_history.html', event_type=get, events=events)


@app.route('/events/new', methods=['POST'])
def add_event():
    session = Session()
    event_date = datetime.datetime.strptime(request.form['event_date'], '%Y-%m-%d')
    for garment_id in request.form.getlist('garment_id'):
        event = Event()
        event.garment_id = garment_id
        event.event_type = request.form['event_type']
        event.event_date = event_date
        if request.form.get('event_type') == 'wear':
            session.query(Garment).filter(Garment.garment_id == garment_id) \
                .update({"last_worn": event_date}, synchronize_session='fetch')
        elif request.form.get('event_type') == 'wash':
            # TODO: if later than current last_washed
            session.query(Garment).filter(Garment.garment_id.in_(request.form.getlist('garment_id'))) \
                .update({"last_washed": event_date}, synchronize_session='fetch')
        session.add(event)
    session.commit()
    return redirect('/')


@app.route('/garments/<int:garment_id>/', methods=['GET'])
def dump_garment(garment_id):
    session = Session()
    wears = list()
    res = session.query(Garment)\
        .filter_by(garment_id=garment_id).one()
    """if len(res):
        (wears, garments) = list(zip(*res))
    else:
        abort(404)
    return render_template('wears.html', garment_id=garment_id, garment_name=garments[0].name, events=wears)"""
    return ", ".join([str(item) for item in res.__dict__.values() if item is not None and type(item) is not state.InstanceState])



@app.route('/garments/<int:garment_id>/events/', methods=['GET'])
def list_events_for_garment(garment_id):
    session = Session()
    wears = list()
    garments = list()
    res = session.query(Event, Garment)\
        .filter(Event.garment_id == Garment.garment_id)\
        .filter_by(garment_id=garment_id).all()
    if len(res):
        (wears, garments) = list(zip(*res))
    else:
        abort(404)
    return render_template('wears.html', garment_id=garment_id, garment_name=garments[0].name, events=wears)


@app.route('/recommendations')
def list_recommendations():
    priorities = request.args.getlist('priorities[]')
    session=Session()
    garments = session.query(Garment).outerjoin(Event)\
        .order_by(Garment.last_washed.desc(), Garment.type.desc())\
        .all()
    for garment in garments:
        garment.wears_since_last_wash = \
            len([event for event in garment.events if event.event_date > garment.last_washed and event.event_type == 'wear'])
        garment.wears_left_till_wash = garment.wears_between_washes - garment.wears_since_last_wash
    session.commit()
    return render_template("recommendations.html", garments = garments)