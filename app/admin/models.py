#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:32:11 2023

@author: bishwa
"""
import logging

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import flash
from flask_admin.babel import gettext

#from app.base.models import User
from flask_login import current_user

from app.base.models import User

## forms
from app.admin.forms import MyModelFormGroup
from app.admin.forms import MyModelFormProject
from app.admin.forms import MyModelFormUser

logging.basicConfig(level=logging.DEBUG)

class MyModelAdminUser(ModelView):
	form = MyModelFormUser
	
	column_list = ['username', 'email', 'key', 'active', 'super_user', 'enable_api']
	column_searchable_list = ['username', 'email']
	page_size = 50
	
	form_columns = ['username', 'email', 'key', 'active', 'super_user', 'enable_api']
	
	print(current_user)
	## Restric deletion of admin user
	def delete_model(self,model):
		if model.username == "admin":
			flash(gettext("Deletion of default administrator is not allowed."), 'error')
			self.session.rollback()
			return False
		elif  model.super_user==1:	
			flash(gettext("Deletion of an administrator is not allowed."), 'error')
			self.session.rollback()
			return False
		else:
			self.on_model_delete(model)
			self.session.flush()
			self.session.delete(model)
			self.session.commit()
			return True
			
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False
	
	def on_model_change(self, form, model, is_created):	
		if model.username == "admin" and (not bool(form.is_active.data)) :
			flash(gettext("Deactivating the default administrator is not allowed."), 'error')
			self.session.rollback()
			return False
			
		elif model.username == "admin" and (not bool(form.is_su.data)) :
			flash(gettext("Removing super-user privilege of the default administrator is not allowed."), 'error')
			self.session.rollback()
			return False
			
		else:
			# Update the model with the values from the form (checkboxes will be saved as 1/0)
			model.active = bool(form.is_active.data)
			model.super_user = bool(form.is_su.data)
			model.enable_api = bool(form.is_api_enabled.data)
			return True
		
	# Dynamically set the default value of `is_active` based on the existing record in the database
	def on_form_prefill(self, form, id):
		#logging.debug("Inside _on_model_get()")
		model = self.get_one(id)
		if model:
			form.is_active.data = bool(model.active)
			form.is_su.data = bool(model.super_user)
			form.is_api_enabled.data = bool(model.enable_api)
			#logging.debug(f"Prefill form - Active: {form.is_active.data}, Super User: {form.is_su.data}, Enable API: {form.is_api_enabled.data}")
        
	## create records
	def create_model(self, form):
		try:
			# Validate form before saving
			if form.validate():
			
				is_active = 1 if form.is_active.data else 0
				is_su = 1 if form.is_su.data else 0
				is_api_enabled = 1 if form.is_api_enabled.data else 0
				
				new_record = super(MyModelAdminUser, self).create_model(form)
				self.session.commit()
				return new_record
			else:
				flash("Form validation failed", "error")
				return None
		except Exception as e:
			self.session.rollback()
			flash(f"Error saving record: {str(e)}", "error")
			return None
	

	
class MyModelAdminGroup(ModelView):
	form = MyModelFormGroup
	column_list            = [ 'id', 'name']
	column_searchable_list = column_list
	form_columns           = ['name']
	
	page_size              = 50
	can_delete             = False
	can_create             = False
	
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False

class MyModelAdminProject(ModelView):
	form = MyModelFormProject
	column_list            = [ 'id', 'name', 'group_id']
	column_searchable_list = column_list
	form_columns           = ['name']
	
	page_size             = 50
	can_delete            = False
	can_create            = False
	form_excluded_columns = ['id', 'group_id']
	
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False

class MyModelAdminRun(ModelView):

	column_list            = [ 'id', 'pipeline', 'version', 'submitted', 
	                           'completed', 'trace_file', 'run_count', 
	                           'run_time_hr', 'read_TB','write_TB', 
	                           'memory_GB', 'status', 'entry_via',
	                           'project_id']
	column_searchable_list = ['pipeline', 'version', 'entry_via', 'status']
	form_columns           = ['pipeline', 'version']
	
	page_size              = 50
	
	form_excluded_columns  = ['id', 'project_id']
	
	can_delete             = False
	can_create             = False
	
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False

		
class MyModelAdminProcess(ModelView):
	
	column_searchable_list = ['task_id', 'hash', 'native_id', 'name', 'status', 'exit']
	
	form_columns = []
	can_edit     = False
	can_delete   = False
	can_create   = False
	
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False
		




from flask_admin import expose, AdminIndexView

class DashboardView(AdminIndexView):

	def is_visible(self):
		# This view won't appear in the menu structure
		return False


