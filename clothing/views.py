""" MOVED TO __INIT__ TO AVOID CIRCULAR IMPORT"""

"""
from clothing import app
from models import Garment, Image, MatchRating, Event
from sqlalchemy.orm.exc import NoResultFound
import __init__
from flask import render_template, abort, request, url_for, redirect

@app.route('/')
@app.route('/garments/')
def list_garments():
    session = __init__.Session()
    garment = session.query(Garment).first()
    name = garment.name
    print(name)
    session.commit()
    #return render_template('permissions.html', user=author)
    return "<html>*{}*: {}<BR> {}".format(garment.name, "hi", "I hate sissy")
"""
"""
@app.route('/users/<int:userid>/create_permission', methods=['GET', 'POST'])
def create_permission(userid):
    if request.method == 'POST':
        session = Session()
        try:
            user = session.query(User).filter_by(userid=userid).one()
        except NoResultFound as e:
            abort(500, "User {} not found".format(str(userid)))

        newperm = Permission(userid=userid, name=request.form['permission name'],
                                rule=request.form['permission rule'])
        user.permissions.append(newperm)
        session.commit()
        return redirect(url_for('list_permissions'))
    elif request.method == 'GET':
        return render_template('new_permission.html', userid=userid)
"""
