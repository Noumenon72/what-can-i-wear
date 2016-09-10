import os, sys
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Date
from sqlalchemy.dialects.mysql import TINYINT, TINYTEXT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()
# Base.__table_args__ = {'mysql_engine': 'MyISAM'}

""" user_permissions = Table('user_permissions', Base.metadata,
                         #Column('id', Integer, primary_key=True),
                         Column('userid', TINYINT(1), ForeignKey('users.userid')),
                         Column('permissionid', INTEGER, ForeignKey('permissions.id')))
"""
class Garment(Base):
    __tablename__ = 'garment'
    garment_id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_washed = Column(Date)
    type = Column(String(30))
    color = Column(String(30))
    texture = Column(String(30))
    seasonality = Column(String(30))
    fabric = Column(String(30))
    pattern = Column(String(30))
    weight_category = Column(Integer)
    brand = Column(String(30), default=None)
    comment = Column(String(255))
    formality_rating = Column(Integer)
    wears_between_washes = Column(Integer)
    picture_id = Column(Integer, ForeignKey('image.image_id'))
    picture = relationship('Image', backref='garment')
    # matches = relationship('MatchRating')

class Image(Base):
    __tablename__ = 'image'
    image_id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    path = Column(String(255))


class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    garment_id = Column(Integer, ForeignKey('garment.garment_id'))
    garment = relationship("Garment", backref=backref('event', order_by=event_id))
    event_date = Column(Date)
    event_type = Column(String(30))

class MatchRating(Base):
    __tablename__ = 'match_rating'
    garment_id = Column(Integer, ForeignKey('garment.garment_id'), nullable=False, primary_key=True)
    matched_garment_id = Column(Integer, ForeignKey('garment.garment_id'), nullable=False)

    match_rating = Column(Integer, default=None)
    garment = relationship("Garment", foreign_keys=[garment_id], backref="matched")
    matched_garment = relationship("Garment", foreign_keys=[matched_garment_id], backref='matched_to')