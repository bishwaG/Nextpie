# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import datetime
import jwt
from config import Config
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, recoveryForm
from app.base.models import User

from app.base.util import verify_pass, generate_rand_passwd, hash_pass
from app import app
from app.home.utils import Misc
## for emal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@blueprint.route('/')
def route_default():
	return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	login_form = LoginForm(request.form)
	if 'login' in request.form:

		# read form data
		username = request.form['username']
		password = request.form['password']

		# Locate user
		user = User.query.filter_by(username=username).first()
		
		## check user validity
		if user is None:
			return render_template( 'accounts/login.html', 
			                        msg='Invalid user.', 
			                        form=login_form)
		
		## Check if the user is active
		if not user.is_active():
			return render_template( 'accounts/login.html', 
			                        msg='Account not activated.', 
			                        form=login_form)

		# Check the password
		if user and verify_pass( password, user.password):
			login_user(user)
			session["username"] = username
			return redirect(url_for('base_blueprint.route_default'))
		
			                        	
		# Something (user or pass) is not ok
		return render_template( 'accounts/login.html', 
		                        msg='Unable to log user in.', 
		                        form=login_form)
	
	## if user is not authenticated go to login
	if not current_user.is_authenticated:
		return render_template( 'accounts/login.html',
		                form=login_form)
	return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        password  = request.form['password']
        email     = request.form['email'   ]
        
        ## generate api key
        key = jwt.encode({"key": username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, password, algorithm="HS256") 
        key = key[-30:]
        
        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        #user = User(**request.form)
        user=User(username=username,email=email,password=password,key=key,enable_api=False)
        db.session.add(user)
        db.session.commit()
	
        return render_template( 'accounts/register.html', 
                                msg='<p>User created successfully!</p> <p>You will get an email once your account gets activated. <p><a href="/login">Login</a></p>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)


## Forgot password
from app.base.models import Settings
@blueprint.route('/recover', methods=['GET', 'POST'])
def recover():
	recovery_form = recoveryForm(request.form)
	
	if 'recover' in request.form:
		receiver_email = request.form['email']
		
		## check if email exists
		user = User.query.filter_by(email=receiver_email).first()
		if not user:
			return render_template( 'accounts/recover.html', 
			                         msg="<p>Email does not exist.</p>", form=recovery_form)
			
		else:
			
			## random password
			new_passwd = generate_rand_passwd()
			## message
			message  = "Hi,\nYou have requested a new password from Nextpie."
			message += " Below is your new password. Please change "
			message += "your password from the setting page after you "
			message += "login."
			message += "\n\n Password: " + new_passwd
			
			## generate a ransom password
			reply = Misc.send_email(receiver_email, "[Nextpie] A new password", message)
			
			## add the new password to the database			
			user = User.query.filter_by(email=receiver_email).first()
			user.password = hash_pass(new_passwd)
			db.session.commit()


			return render_template( 'accounts/recover.html', 
			                  msg="<p>"+reply+"</p>", form=recovery_form) 
				             
	return render_template( 'accounts/recover.html', form=recovery_form)



@blueprint.route('/logout')
def logout():
	logout_user()

	app.logger.info("Loggin out " + session["username"])
	session["username"] = ""

	return redirect(url_for('base_blueprint.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
