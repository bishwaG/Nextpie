# Import necessary WTForms modules
from wtforms import StringField, validators, BooleanField
from wtforms.validators import DataRequired
from flask_admin.form import BaseForm

# Create a custom form class inheriting from BaseForm
class MyModelFormGroup(BaseForm):
	name = StringField('Name', validators=[DataRequired()])  # Define the 'name' field


class MyModelFormProject(BaseForm):
	name = StringField('Name', validators=[DataRequired()])  # Define the 'name' field
	

class MyModelFormUser(BaseForm):
	username       = StringField('Username', validators=[DataRequired()])  # Define the 'name' field
	email          = StringField('Email', validators=[DataRequired(), validators.Email()])
	#key            = StringField('API Key', validators=[DataRequired()], render_kw={"disabled": True} )
	key            = StringField('API Key', validators=[DataRequired()])
	#is_active      = StringField('Active', validators=[DataRequired()])
	
	is_active      = BooleanField('Active', default=False, render_kw={"class": "custom-switch"})
	is_su          = BooleanField('Super user', default=False, render_kw={"class": "custom-switch"})
	is_api_enabled = BooleanField('Enable API', default=False, render_kw={"class": "custom-switch"})
	
	
