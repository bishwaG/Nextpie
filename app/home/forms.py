# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, validators, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Length, EqualTo

from wtforms import MultipleFileField

## validation function(s)
def validate_server(form, field):
	## hostname or ip validation
	# Regular expression pattern for a valid server name or IP address
	pattern = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$|^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'

	# Check if the input matches the pattern
	if not re.match(pattern, field.data):
		raise ValidationError('Invalid server name or IP address.')


## data load

class uploadForm(FlaskForm):
    
	#groupName    = TextField    ('Group name', id='run_name'   , validators=[DataRequired()])
	#projectName  = TextField    ('Project name', id='run_name'   , validators=[DataRequired()])
	
	workflowName        = StringField('Workflow/pipeline Name',      id='workflowName')
	workflowVer         = StringField('Workflow/pipeline Version',   id='workflowVer')
	groupName           = StringField('Research Group Name',         id='groupName')
	projectName         = StringField('Research Project Name',       id='projectName')
	
	reportFile    = FileField('Pipeline report file', validators=[
	#FileRequired(),
	FileAllowed(['txt'], 'Text file only!')
	])

	traceFiles = MultipleFileField("Trace file(s)", render_kw={'multiple': True}, validators=[DataRequired()])


class passwordChange(FlaskForm):
	
	userName        = StringField('Username',           id='run_name')
	email           = StringField('Email',              id='email', validators=[DataRequired(), Email()])
	oldPassword     = PasswordField('Old password',     id='old_pass', validators=[DataRequired()])
	newPassword     = PasswordField('New password',     id='new_pass', validators=[DataRequired()])
	confirmPassword = PasswordField('Confirm Password', id='new_pass', validators=[DataRequired()])


class APIkeyForm(FlaskForm):
	
	key      = StringField('API Key', id='key')


## For SMTP settings
class SMTPform(FlaskForm):
	
	SMTPserver = StringField('SMTP server', id='server', validators=[DataRequired(), validate_server])
	SMTPport   = IntegerField('SMTP port', id='port', validators=[DataRequired()])
	SMTPtls    = StringField('Use TLS',    id="tls",  validators=[DataRequired()])
	
	yes_no_choices = [('True', 'Yes'), ('False', 'No')]
	SMTPtls = SelectField('Use TLS',id="tls", choices=yes_no_choices, validators=[InputRequired()])
    
	#SMTPtls    = SelectField('Use TLS', choices=[('True', 'Option 1'), ('False', 'Option 2')])
	SMTPuser   = StringField('SMTP user',   id='user', validators=[DataRequired(), Email()])
	SMTPpass   = PasswordField('Password',   id='pass', validators=[DataRequired()])
	SMTPreply  = StringField('Reply to email',  id='reply', validators=[DataRequired(), Email()])
	
	


	
	
	
