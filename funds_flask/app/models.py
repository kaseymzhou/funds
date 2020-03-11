from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Catalog(db.Model):
    __tablename__ = 'catalog'
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),nullable=False)

class Sbi(db.Model):
    __tablename__ = 'subclass_investment'
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cid = db.Column(db.Integer,db.ForeignKey('catalog.id'))
    name = db.Column(db.String(30),nullable=False)
    # catalog_id = db.relationship('Catalog', backref='catalogs')
    funds_fk = db.relationship("Funddetails", backref="funddetails")

class Sbr(db.Model):
    __tablename__ = 'subclass_risk'
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cid = db.Column(db.Integer,db.ForeignKey('catalog.id'))
    name = db.Column(db.String(30),nullable=False)
    funds_fk_r = db.relationship("Funddetails", backref="funddetails_r")

class Sbm(db.Model):
    __tablename__ = 'subclass_management'
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cid = db.Column(db.Integer,db.ForeignKey('catalog.id'))
    name = db.Column(db.String(30),nullable=False)
    funds_fk_m = db.relationship("Funddetails", backref="funddetails_m")

class Funddetails(db.Model):
    __tablename__ = 'funds_details'
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),nullable=False)
    fid = db.Column(db.String(30),nullable=False)
    risk = db.Column(db.Integer,db.ForeignKey('subclass_risk.id'))
    iclass = db.Column(db.Integer,db.ForeignKey('subclass_investment.id'))
    management = db.Column(db.Integer,db.ForeignKey('subclass_management.id'))
    # risk_id = db.relationship('Sbr', backref='risks')
    # iclass_id = db.relationship('Sbi', backref='iclasss')
    # management_id = db.relationship('Sbm', backref='managements') #　managements.management_id.name