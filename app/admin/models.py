#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:32:11 2023

@author: bishwa
"""

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import flash
from flask_admin.babel import gettext

#from app.base.models import User
from flask_login import current_user

class MyModelAdminUser(ModelView):
	
	column_list = ['username', 'email', 'active', 'super_user', 'enable_api']
	column_searchable_list = ['username', 'email']
	page_size = 50
	
	form_columns = column_list
	
	print(current_user)
	## Restric deletion of admin user
	def delete_model(self,model):
		if model.username == "admin" or model.super_user==1:
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

class MyModelAdminGroup(ModelView):

	column_list            = [ 'id', 'name']
	column_searchable_list = column_list
	form_columns           = ['name']
	
	page_size              = 50
	can_delete             = False 
	## allow access to the users having super_user=1 (is admin)
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False

class MyModelAdminProject(ModelView):

	column_list            = [ 'id', 'name', 'group_id']
	column_searchable_list = column_list
	form_columns           = ['name']
	
	page_size             = 50
	can_delete            = False
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
	column_searchable_list = ['pipeline', 'version', 'status', 'entry_via']
	form_columns           = ['pipeline', 'version', 'status', 'entry_via']
	
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

	"""@expose('/')
	def index(self):
		
		arg1 = 'Hello admin'
		return self.render(
		    'admin/main.html',
		    arg1=arg1
		)"""

