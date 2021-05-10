from __future__ import unicode_literals
from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from server import app

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

