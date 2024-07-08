# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

from app.base.util import hash_pass

class Settings(db.Model):
	__tablename__ = 'Settings'
	
	id        = db.Column(db.Integer, primary_key=True)
	name      = db.Column(db.String(64), index=True, unique=True)
	value      = db.Column(db.String(64), index=True, unique=False)
	
class User(db.Model, UserMixin):

	__tablename__ = 'User'

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	email = Column(String, unique=True)
	password = Column(Binary)
	key=Column(String)
	active=db.Column(db.Boolean, default=False, nullable=False)
	super_user=db.Column(db.Boolean, default=False, nullable=False)
	enable_api=db.Column(db.Boolean, default=False, nullable=False)

	def __init__(self, **kwargs):
		for property, value in kwargs.items():
			# depending on whether value is an iterable or not, we must
			# unpack it's value (when **kwargs is request.form, some values
			# will be a 1-element list)
			if hasattr(value, '__iter__') and not isinstance(value, str):
				# the ,= unpack of a singleton fails PEP8 (travis flake8 test)
				value = value[0]

			if property == 'password':
				value = hash_pass( value ) # we need bytes here (not plain str)

			setattr(self, property, value)
	
	## Functions for setting password
	def set_password(self, password):
		self.password = hash_pass(password)
	
	## Fnction for checking password if supplined one is correct
	def check_password(self, password):
		return check_password_hash(self.password, password)
		
	## Dunction to check if the user is active
	def is_active(self):
		if self.active:
			return True
		else:
			return False
	## Function to check if the user is admin
	## Admin user will be redirected to /admin (in routes.py)
	def is_admin(self):
		if self.super_user:
			return True
		else:
			return False
			
	## This method tells Python how to print objects of this class, which 
	## is going to be useful for debugging.
	def __repr__(self):
		return str(self.username)


@login_manager.user_loader
def user_loader(id):
	return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
	username = request.form.get('username')
	user = User.query.filter_by(username=username).first()
	return user if user else None

