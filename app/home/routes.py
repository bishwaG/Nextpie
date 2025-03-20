from pathlib import Path

from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify, Response, session
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from collections import Counter

from itertools import chain
from app.home.models import Group, Project, Run, Process
from app.base.models import User, Settings
import numpy as np
import re
import json
import random

@blueprint.route('/index')
@login_required
def index():
	return render_template('index.html', segment='index', title="Dashboard")


## LOAD DATA ===================================================================
from .forms import uploadForm
@blueprint.route('/upload')
@login_required
def load_data():
	loadForm = uploadForm(meta={'csrf': False})
	return render_template('upload-data.html',
	    segment='upload',
	    title="Upload Data",
	    form=loadForm)

#
# ░██████╗███████╗████████╗████████╗██╗███╗░░██╗░██████╗░░██████╗
# ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗░██║██╔════╝░██╔════╝
# ╚█████╗░█████╗░░░░░██║░░░░░░██║░░░██║██╔██╗██║██║░░██╗░╚█████╗░
# ░╚═══██╗██╔══╝░░░░░██║░░░░░░██║░░░██║██║╚████║██║░░╚██╗░╚═══██╗
# ██████╔╝███████╗░░░██║░░░░░░██║░░░██║██║░╚███║╚██████╔╝██████╔╝
# ╚═════╝░╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═════╝░
## SETTIGNGS ===================================================================
from .forms import passwordChange, APIkeyForm, SMTPform
from flask import flash, request
from app.base.util import hash_pass
from app.base.util import verify_pass
@blueprint.route('/settings', methods=['GET','POST'])
@login_required
def change_passsword():
	pwdForm  = passwordChange(request.form, meta={'csrf': True})
	keyForm  = APIkeyForm(request.form, meta={'csrf': True})
	smtpForm = SMTPform(request.form, meta={'csrf': True})

	## prefill text field with username
	username = session["username"]
	pwdForm.userName._name = username
	
	user = User.query.filter_by(username=username).first()
	pwdForm.email.data = user.email
	
	## is super user
	isAdmin = user.super_user
	
	## prefill SMTP fields
	settings = Settings.query.filter_by(name="SMTP_SERVER").first()
	smtpForm.SMTPserver.data = settings.value
	## port
	settings = Settings.query.filter_by(name="SMTP_PORT").first()
	smtpForm.SMTPport.data = settings.value
	##tls
	settings = Settings.query.filter_by(name="SMTP_USE_TLS").first()
	smtpForm.SMTPtls.data = settings.value
	## user
	settings = Settings.query.filter_by(name="SMTP_USERNAME").first()
	smtpForm.SMTPuser.data = settings.value
	## password
	settings = Settings.query.filter_by(name="SMTP_PASSWORD").first()
	smtpForm.SMTPpass.data = settings.value
	## reply to
	settings = Settings.query.filter_by(name="REPLY_EMAIL").first()
	smtpForm.SMTPreply.data = settings.value
	
	
	## reset all the fileds
	#for i in ["SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD", "REPLY_EMAIL"]:
	#	settings = Settings.query.filter_by(name=i).first()
	#	settings.value=""
	#	db.session.commit()
	
	
	## If submit button is pressed
	if 'submit1' in request.form:
		
		## when old password is provided and email provide is new
		
		
		## when password is changed
		
		if pwdForm.newPassword.data != "" or pwdForm.confirmPassword.data !="":
			if len(pwdForm.newPassword.data) < 6:
				flash("Minimum password length is 6.")
			if pwdForm.newPassword.data != pwdForm.confirmPassword.data:
				flash("Confirmed password did not match.")
		## when new email is provide
		elif pwdForm.newPassword.data == "" and pwdForm.confirmPassword.data =="" and pwdForm.email.data !="":
			## get user
			user = User.query.filter_by(username=username).first()
			## update email
			if not verify_pass( pwdForm.oldPassword.data, user.password):
				flash("Wrong current password")
			else:
				user.email = request.form['email']
				db.session.commit()
				
				pwdForm.email.data = user.email
				
				flash("Saved successfully!")
		else:
			user = User.query.filter_by(username=username).first()

			## check if old possword is correct
			if not verify_pass( pwdForm.oldPassword.data, user.password):
				flash("Wrong current password")
			else:
				user.set_password(pwdForm.newPassword.data)
				user.email = request.form['email']
				db.session.commit()
				flash("Saved successfully!")
	
	## if SMTP for is submitted
	if 'submit3' in request.form:
	
		setting_rows = [
		{"SMTP_SERVER":   request.form['SMTPserver']},
		{"SMTP_PORT":     request.form['SMTPport']},
		{"SMTP_USE_TLS":  request.form['SMTPtls']},
		{"SMTP_USERNAME": request.form['SMTPuser']},
		{"SMTP_PASSWORD": request.form['SMTPpass']},
		{"REPLY_EMAIL":   request.form['SMTPreply']}]
		
		
		
		# Update the database rows
		for row in setting_rows:
			for key, value in row.items():
				## get the row first
				settings = Settings.query.filter_by(name=key).first()
				
				## update it
				settings.value = value
				
				print(settings.name, settings.value)
				db.session.commit()
		flash("Updated successfully!")
		
		## postfill SMTP fields
		settings = Settings.query.filter_by(name="SMTP_SERVER").first()
		smtpForm.SMTPserver.data = settings.value
		## port
		settings = Settings.query.filter_by(name="SMTP_PORT").first()
		smtpForm.SMTPport.data = settings.value
		##tls
		settings = Settings.query.filter_by(name="SMTP_USE_TLS").first()
		smtpForm.SMTPtls.data = settings.value
		## user
		settings = Settings.query.filter_by(name="SMTP_USERNAME").first()
		smtpForm.SMTPuser.data = settings.value
		## password
		settings = Settings.query.filter_by(name="SMTP_PASSWORD").first()
		smtpForm.SMTPpass.data = settings.value
		## reply to
		settings = Settings.query.filter_by(name="REPLY_EMAIL").first()
		smtpForm.SMTPreply.data = settings.value
	
	
	## render template
	return render_template('settings.html',
	    segment='settings',
	    title="Settings",
	    pwd_form=pwdForm,
	    key_form=keyForm,
	    smtp_form=smtpForm,
	    user_is_admin=isAdmin)

## -----------------------------------------------------------------------------
@blueprint.route('/users', methods=['GET','POST'])
@login_required
def crud_users():
	
	## render template
	return render_template('users.html',
	    segment='users',
	    title="Users")


@blueprint.route('/get-users', methods=['GET','POST'])
@login_required
def get_users():
	
	if request.method == 'POST':
		
		return jsonify({ 'username':'test'})
		
	elif request.method == 'GET':
		
		this_year = date.today().year
		
		#query = Process.query.filter(extract('year', Process.submit) == this_year).all()
		## Join three tables
		query = db.session.query(Project,Run,Process).\
		    add_columns(
		    Process.hash,
		    Process.status,
		    Process.exit,
		    Process.submit,
		    Process.duration,
		    Process.realtime,
		    Process.cpu,
		    Process.peak_rss,
		    Process.peak_vmem,
		    Process.rchar,
		    Process.wchar,
		    ).\
		    filter(Process.run_id==Run.id,
		           Run.project_id==Project.id
		           #,extract('year', Run.submitted) == this_year
		           ).all()

		## serialize query to be able to convert to JSON
		a = []
		for i in query:


			a.append({"project_name":str(i[0]),
			    "run_id"       :int(str(i[1])),
			    "process_name" :str(i[2]),
			    "hash"         :str(i[3]),
			    "status"       :str(i[4]),
			    "exit"         :str(i[5]),
			    "submitted"    :str(i[6].strftime("%d/%m/%Y")),
			    "duration"     :str(i[7].strftime("%H:%M:%S.%f")),
			    "realtime"     :str(i[8].strftime("%H:%M:%S.%f")),
			    "cpu"          :0 if i[9] == "-" else float(i[9].split("%")[0]),
			    "peak_rss_mb"  :Utils.toMB( i[10] ),
			    "peak_vmem_mb" :Utils.toMB( i[11] ),
			    "rchar_mb"     :Utils.toMB( i[12] ),
			    "wchar_mb"     :Utils.toMB( i[13].strip() )
			    })

		#return jsonify(a)
		
		b = {"data":a}
		return jsonify(b)

## Generate an API key
import jwt
import datetime
@blueprint.route('/key/<username>', methods=['GET','POST'])
@login_required
def generate_key(username):

	user = User.query.filter_by(username=username).first()

	if not user:
		return "User " + username + " does not exist."

	if session["username"] != username:
		return "Logged in user is different than provided."
	if not user.enable_api:
		return "User does not have API access."
	else:
		## generate api key
		x = {"key": username,
		     "exp":datetime.datetime.utcnow() +
		           datetime.timedelta(minutes=30)}
		key = jwt.encode(x,
			         user.password,
			         algorithm="HS256")
		key = key[-30:]

		user.key = key
		db.session.commit()

		return jsonify(key)


# ██╗███╗░░██╗██████╗░██╗░░░██╗████████╗  ██████╗░░█████╗░████████╗░█████╗░
# ██║████╗░██║██╔══██╗██║░░░██║╚══██╔══╝  ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
# ██║██╔██╗██║██████╔╝██║░░░██║░░░██║░░░  ██║░░██║███████║░░░██║░░░███████║
# ██║██║╚████║██╔═══╝░██║░░░██║░░░██║░░░  ██║░░██║██╔══██║░░░██║░░░██╔══██║
# ██║██║░╚███║██║░░░░░╚██████╔╝░░░██║░░░  ██████╔╝██║░░██║░░░██║░░░██║░░██║
# ╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚═════╝░░░░╚═╝░░░  ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝
## submit DATA from /load ======================================================
import os
from config import Config
from app import app
from app.home.utils import Utils, Misc
from werkzeug.utils import secure_filename

@blueprint.route('/submit-data', methods=['GET','POST'])
@login_required
## Uses static funtions from Utils class (./utils.py)
def submit_data():
	uploadForm1  = uploadForm(request.form, meta={'csrf': True})
	
	path = app.config['UPLOAD_FOLDER']

	if request.method == 'POST':
		
		#return jsonify({"message":"Reply", "response":"success"})
		
		## check if the upload filder exists
		if not os.path.exists(path):
			#return jsonify(response="fail",reason="Upload folder does not exist in the server.")
			return jsonify({"message":"Upload folder does not exist in the server.", "response":"error"})

		## check if the foler has write access
		is_readable = os.access(path, os.R_OK)
		is_writable = os.access(path, os.W_OK)
		if not is_readable:
			#return jsonify(response="fail",reason="The upload folder does not have read access in the server.")
			return jsonify({"message":"The upload folder does not have read access in the server.", "response":"error"})
		if not is_writable:
			#return jsonify(response="fail",reason="The upload folder does not have write access in the server.")
			return jsonify({"message":"The upload folder does not have write access in the server.", "response":"error"})

		## make upload folder empty
		for f in Path(path).glob('*'):
			try:
				f.unlink()
			except OSError as e:
				print("Error: %s : %s" % (f, e.strerror))
				
		## get input values
		## these are sent via javascript form_data form
		## form_data.append should be used if more fields are needed to add
		workflow_name = request.form.get('workflowName')
		workflowVer = request.form.get('workflowVer')
		groupName = request.form.get('groupName')
		projectName = request.form.get('projectName')
		
		"""return jsonify(response="test",reason=
		  "worfklow: " + str(workflow_name) +
		  ", version: " + str(workflowVer) +
		  ", group: " + str(groupName) + 
		  ", project name: " + str(projectName))"""
		
		
		## if group and project empty generate randomly.
		rnd_group_proj = False
		if not groupName or not projectName:
			groupName         = Misc.gen_groupName()
			projectName       = Misc.gen_projectName()
			rnd_group_proj    = True
			
		"""return jsonify(response="test",reason=
		  "worfklow: " + str(workflow_name) +
		  ", version: " + str(workflowVer) +
		  ", group: " + str(groupName) + 
		  ", project name: " + str(projectName))"""
		
		projGroupVer = [groupName, projectName, workflow_name, workflowVer]

		## for trace files  --------------------------------------------
		files = request.files.getlist('traceFile[]')
		fileList=[]
		for file in files:
			if file and files:
				filename = secure_filename(file.filename)

				## check extension
				if not Utils.checkExt( filename,app.config['UPLOAD_EXTENSIONS']) :
					#return jsonify(response="fail",reason="File type is not allowed. Only .txt allowed.")
					return jsonify({"message":"File type is not allowed. Only .txt allowed.", "response":"error"})
				file.save(os.path.join(path, filename))
				fileList.append(filename)
			else:
				#return jsonify(response="fail",reason="No file part.")
				return jsonify({"message":"No file part.", "response":"error"})

		## process report file -----------------------------------------
		if 'reportFile' not in request.files and (workflow_name == "" or workflowVer == ""):
			#return jsonify(response="fail",reason="Provide either workflow detailes (workflow name and version) or a pipeline report file.")
			return jsonify({"message":"Provide either workflow detailes (workflow name and version) or a pipeline report file.", "response":"error"})
		
		if 'reportFile' in request.files:
			file = request.files['reportFile']
			filename = secure_filename(file.filename)

			## check extension
			if not Utils.checkExt( filename,app.config['UPLOAD_EXTENSIONS']) :
					#return jsonify(response="fail",reason="File type is not allowed. Only .txt allowed.")
					return jsonify({"message":"File type is not allowed. Only .txt allowed.", "response":"error"})

			## save file
			file.save(os.path.join(path, filename))

			## parse report file -------------------------------------------
			## Returns projectname, group name and pipeline version
			projGroupVer = Utils.parseReportFile(os.path.join(path, filename))
		
			if projGroupVer[3] == "":
				#return jsonify(response="fail", reason="Can not extract workflow version. Make sure that your report file contains ' WORKFLOW-NAME v0.0.1' in the second line.")
				return jsonify({"message":"Can not extract workflow version. Make sure that your report file contains ' WORKFLOW-NAME v0.0.1' in the second line.", "response":"error"})

			if projGroupVer[2] == "":
				#return jsonify(response="fail", reason="Can not extract workflow name. Make sure that your report file contains ' WORKFLOW-NAME v0.0.1' in the second line.")
				return jsonify({"message":"Can not extract workflow name. Make sure that your report file contains ' WORKFLOW-NAME v0.0.1' in the second line.", "response":"error"})

			if projGroupVer[1] == "":
				#return jsonify(response="fail", reason="Can not extract project name. Make sure that your report file contains 'Run Name: ' follwed by project name in any line.")
				return jsonify({"message":"Can not extract project name. Make sure that your report file contains 'Run Name: ' follwed by project name in any line.", "response":"error"})

			if projGroupVer[0] == "":
				#return jsonify(response="fail", reason="Can not extract group name. Make sure that your report file contains 'Group: ' follwed by group name in any line.")
				return jsonify({"message":"Can not extract group name. Make sure that your report file contains 'Group: ' follwed by group name in any line.", "response":"error"})
			
		## ['research_group_A', 'test_run_poj_1', 'RNAseq', '2.0.1']
		print(projGroupVer)
		
		#return jsonify(projGroupVer)
		## parse Trace.txt files ---------------------------------------
		return jsonify( Utils.parseTraceFiles(metadataList=projGroupVer, 
		   uploadDir=app.config['UPLOAD_FOLDER'], 
		   actionSource="GUI", 
		   random_group_proj=rnd_group_proj))



## ============================================================================
# ██████╗░░█████╗░████████╗░█████╗░██████╗░░█████╗░░██████╗███████╗
# ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
# ██║░░██║███████║░░░██║░░░███████║██████╦╝███████║╚█████╗░█████╗░░
# ██║░░██║██╔══██║░░░██║░░░██╔══██║██╔══██╗██╔══██║░╚═══██╗██╔══╝░░
# ██████╔╝██║░░██║░░░██║░░░██║░░██║██████╦╝██║░░██║██████╔╝███████╗
# ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝

## Databse search
@blueprint.route('/db-<table>', methods=['GET','POST'])
@login_required
def db_search_page(table):
	return render_template("db-"+table+".html",
	    segment="db-"+table,
	    title=table.title())

from datetime import date
from sqlalchemy import extract
@blueprint.route('/db-fetch/<table>', methods=['GET', 'POST'])
def db_search(table):

	this_year = date.today().year

	## list for serialization
	a = []

	## Fetch for Group table
	if table=="Group":
		query = Group.query.filter(Group.name.like("%")).all()
		[a.append(i.toJSON()) for i in query]
		return jsonify(a)

	## Fetch from Project table
	elif table =="Project":
		query = Project.query.join(Group, Group.id==Project.group_id).\
		  add_columns(Project.id,Project.name, Group.name, Group.id).all()

		for i in query:
			a.append({"id":str(i[1]),
			    "name":str(i[2]),
			    "group_name"  :str(i[3]),
			    "group_id"    :str(i[4])
			    })

		return jsonify(a)

	## Fetch from Run table
	elif table == "Run":
		#query = Run.query.join(Project, Project.id==Run.project_id).\
		query = Run.query.join(Project, Project.id==Run.project_id).\
		  add_columns(Run.id,
		    Run.pipeline,
		    Run.version,
		    Run.submitted,
		    Run.completed,
		    Run.run_time_hr,
		    Run.read_TB,
		    Run.write_TB,
		    Run.memory_GB,
		    Run.status,
		    Run.entry_via,
		    Project.name).\
		    filter(Run.id.like("%")).filter(Run.run_time_hr.isnot(None)).all()
		    #filter(extract('year', Run.submitted) == this_year).all()

		## serialize query to be able to convert to JSON
		#a = []
		for i in query:
			a.append({"id":str(i[1]),
			    "workflow"    :str(i[2]),
			    "version"     :str(i[3]),
			    "submited"    :str(i[4].strftime("%d/%m/%Y")),
			    "completed"   :str(i[5].strftime("%d/%m/%Y")),
			    "run_time_hr" :float(i[6]),
			    "read_TB"     :float(i[7]),
			    "write_TB"    :float(i[8]),
			    "memory_GB"   :float(i[9]),
			    "status"      :str(i[10]),
			    "entry_via"   :str(i[11]),
			    "project_name":str(i[12])
			    })

		return jsonify(a)

	## Fetch from Process table
	elif table == "Process":
		#query = Process.query.filter(extract('year', Process.submit) == this_year).all()
		## Join three tables
		query = db.session.query(Project,Run,Process).\
		    add_columns(
		    Process.hash,
		    Process.status,
		    Process.exit,
		    Process.submit,
		    Process.duration,
		    Process.realtime,
		    Process.cpu,
		    Process.peak_rss,
		    Process.peak_vmem,
		    Process.rchar,
		    Process.wchar,
		    ).\
		    filter(Process.run_id==Run.id,
		           Run.project_id==Project.id
		           #,extract('year', Run.submitted) == this_year
		           ).all()

		## serialize query to be able to convert to JSON
		#a = []
		for i in query:


			a.append({"project_name":str(i[0]),
			    "run_id"       :int(str(i[1])),
			    "process_name" :str(i[2]),
			    "hash"         :str(i[3]),
			    "status"       :str(i[4]),
			    "exit"         :str(i[5]),
			    "submitted"    :str(i[6].strftime("%d/%m/%Y")),
			    "duration"     :str(i[7].strftime("%H:%M:%S.%f")),
			    "realtime"     :str(i[8].strftime("%H:%M:%S.%f")),
			    "cpu"          :0 if i[9] == "-" else float(i[9].split("%")[0]),
			    "peak_rss_mb"  :Utils.toMB( i[10] ),
			    "peak_vmem_mb" :Utils.toMB( i[11] ),
			    "rchar_mb"     :Utils.toMB( i[12] ),
			    "wchar_mb"     :Utils.toMB( i[13].strip() )
			    })

		return jsonify(a)

	else:
		return "Invalid table", 401



##==============================================================================
#
# ██████╗░░█████╗░░██████╗██╗░░██╗██████╗░░█████╗░░█████╗░██████╗░██████╗░
# ██╔══██╗██╔══██╗██╔════╝██║░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
# ██║░░██║███████║╚█████╗░███████║██████╦╝██║░░██║███████║██████╔╝██║░░██║
# ██║░░██║██╔══██║░╚═══██╗██╔══██║██╔══██╗██║░░██║██╔══██║██╔══██╗██║░░██║
# ██████╔╝██║░░██║██████╔╝██║░░██║██████╦╝╚█████╔╝██║░░██║██║░░██║██████╔╝
# ╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░
##==============================================================================
@blueprint.route('/info/<action>', methods=['GET','POST'])
@login_required
def get_info(action):

	##
	if action =="db":
		groups    = Group.query.count()
		projects  = Project.query.count()
		runs      = Run.query.count()
		processes = Process.query.count()

		return jsonify([{"groups": groups,
		                "projects": projects,
		                "runs": runs,
		                "processes": processes}])

	if action =="this-year-runs":

		this_year  = date.today().year
		this_month = date.today().month
		last_month = this_month - 1
		last_year  = this_year - 1

		## Runs of this year and last year
		this_year_runs  = Run.query.filter(extract('year', Run.completed) == this_year).count()
		last_year_runs  = Run.query.filter(extract('year', Run.completed) == last_year ).count()
		if last_year_runs == 0:
			last_year_runs = 1
		year_per_change = Utils.per_change(this_year_runs, last_year_runs)

		## Runs of this month and last month
		this_month_runs = Run.query.filter(extract('month', Run.completed) == this_month).count()
		if last_month <0:
			last_month_runs =0
		else:
			last_month_runs = Run.query.filter(extract('month', Run.completed) == last_month ).count()
		if last_month_runs == 0:
			last_month_runs = 1
		month_per_change = Utils.per_change(this_month_runs, last_month_runs)

		## Data footprint this year and last year
		query_this_year = db.session.query(extract('year', Run.submitted), func.sum(Run.write_TB)).\
		  group_by(extract('year', Run.submitted)).\
		  filter(extract('year', Run.submitted) == this_year).all()

		query_last_year = db.session.query(extract('year', Run.submitted), func.sum(Run.write_TB)).\
		  group_by(extract('year', Run.submitted)).\
		  filter(extract('year', Run.submitted) == last_year).all()

		## handle empty query
		if len(query_this_year) !=0:
			this_year_footprint = query_this_year[0][1]
		else:
			this_year_footprint = 0
		if len(query_last_year) !=0:
			last_year_footprint = query_last_year[0][1]
		else:
			last_year_footprint = 0

		footprint_per_change = Utils.per_change(this_year_footprint, last_year_footprint)

		return jsonify({"runs_this_year":round(this_year_runs,2),
		    "year_percent_change":round(year_per_change, 2),
		    "runs_this_month": round(this_month_runs,2),
		    "month_percent_change": round(month_per_change,2),
		     "footprint_this_year": round(this_year_footprint,2),
			 "footprint_percent_change": round(footprint_per_change,2)
		    })
		"""
		return jsonify({"runs_this_year":20,
		                "year_percent_change":800,
		                "runs_this_month": 5,
		                "month_percent_change":-50,
						"footprint_this_year":500,
						"footprint_percent_change": 50
		                })
		"""


	if action == "workflows":
		query = Run.query.with_entities(Run.pipeline, Run.version).distinct().all()

		a = []

		if len( query) != 0:
			for i in query:
				a.append({"name":i[0],"version":i[1]})

			return jsonify(a)

##==============================================================================
#
# ░█████╗░███╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗░██████╗██╗░██████╗
# ██╔══██╗████╗░██║██╔══██╗██║░░░░░╚██╗░██╔╝██╔════╝██║██╔════╝
# ███████║██╔██╗██║███████║██║░░░░░░╚████╔╝░╚█████╗░██║╚█████╗░
# ██╔══██║██║╚████║██╔══██║██║░░░░░░░╚██╔╝░░░╚═══██╗██║░╚═══██╗
# ██║░░██║██║░╚███║██║░░██║███████╗░░░██║░░░██████╔╝██║██████╔╝
# ╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═════╝░╚═╝╚═════╝░
##==============================================================================
## Analysis pages ==============================================================
@blueprint.route('/stats-run', methods=['GET','POST'])
@login_required
def run_stats():
	return render_template("stats-run.html",
	                       segment='stats-run',
	                       title="Run")

@blueprint.route('/stats-proc', methods=['GET','POST'])
@login_required
def proc_stats():
	return render_template("stats-proc.html",
	                       segment='stats-proc',
	                       title="Process")

@blueprint.route('/stats-gp', methods=['GET','POST'])
@login_required
def gp_stats():
	return render_template("stats-gp.html",
	                       segment='stats-gp',
	                       title="Group & Projects")

## Action ----------------------------------------------------------------------
from sqlalchemy import func, distinct
from sqlalchemy.sql.expression import null
from app import db
import numpy as np
@blueprint.route('/analysis/<action>/<workflow>/<version>', methods=['GET','POST'])
@login_required
def get_process(action,workflow,version):

	if action == "get-process-runtime":
		query = db.session.query(Run,Process).\
		    add_columns(Process.id, Process.realtime).\
		    filter( (Run.pipeline==workflow) & (Run.version==version) & (Run.id==Process.run_id)).\
		    all()

	elif action == "get-process-memory":
		query = db.session.query(Run,Process).\
		    add_columns(Process.id, Process.peak_rss).\
		    filter( (Run.pipeline==workflow) & (Run.version==version) & (Run.id==Process.run_id)).\
		    all()
	elif action == "get-process-read":
		query = db.session.query(Run,Process).\
		    add_columns(Process.id, Process.rchar).\
		    filter( (Run.pipeline==workflow) & (Run.version==version) & (Run.id==Process.run_id)).\
		    all()
	elif action == "get-process-write":
		query = db.session.query(Run,Process).\
		    add_columns(Process.id, Process.wchar).\
		    filter( (Run.pipeline==workflow) & (Run.version==version) & (Run.id==Process.run_id)).\
		    all()
	else:
		return jasonify({"message":"Invalid action"}),404

	## return empty if query is empty
	if not len(query):
		return ""

	## remove (sample) from process name
	new_query=[]
	proc_names = []
	for i in query:
		new_query.append([i[0], str(i[1]).split(" ")[0],
				  i[2], i[3] ])
		proc_names.append(str(i[1]).split(" ")[0])

	##take only unique process names
	proc_names = list( set(proc_names) )

	## loop by proc_names
	box_data_list = []
	for proc_name in proc_names:
		## empty list for different resource matrices
		mat_list = []
		## get proc_name from new_query
		for x in new_query:
			if proc_name == x[1] and action == "get-process-runtime":
				run_time  =x[3]
				run_time_hr  = run_time.hour +  run_time.minute/60 + run_time.second/(60*60)
				mat_list.append(run_time_hr)
				#print(x[1],x[3])
			if proc_name == x[1] and action == "get-process-memory":
				mat_list.append( float(Utils.toMB(x[3]))/1024)
			if proc_name == x[1] and action == "get-process-read":
				mat_list.append( float(Utils.toMB(x[3]))/2024)
			if proc_name == x[1] and action == "get-process-write":
				mat_list.append( float(Utils.toMB(x[3].strip("\n")))/1024)
		## Calculate min, max, q1, q3 and median
		quantiles = Utils.calc_quantiles(mat_list)
		box_data_list.append([proc_name,
		                      quantiles[0],
		                      quantiles[1],
		                      quantiles[2],
		                      quantiles[3],
		                      quantiles[4]])


	## return boxplot data
	return jsonify(box_data_list)

## Periodic (monthly/yearly) data

from app.home.analysis import Analysis
@blueprint.route('/analysis/<timely>/<action>', methods=['GET','POST'])
@login_required
def get_monthly(timely, action):

	this_year = date.today().year

	if timely == "monthly" and action == "runs":
		## Monthly counts of this year
		this_year_count = Analysis.get_monthly_run_counts(this_year)
		last_year_count = Analysis.get_monthly_run_counts(this_year -1)

		return jsonify([this_year_count, last_year_count])


	if timely == "monthly" and action == "disk":

		this_year_disk = Analysis.get_monthly_disk(this_year)
		last_year_disk = Analysis.get_monthly_disk(this_year-1)
		return jsonify([this_year_disk,last_year_disk])

	if timely == "monthly" and action == "memory":

		this_year_mem = Analysis.get_monthly_memory(this_year)
		last_year_mem = Analysis.get_monthly_memory(this_year-1)
		return jsonify([this_year_mem,last_year_mem])

	if timely == "monthly" and action == "status":
		this_year_comp = Analysis.get_monthly_run_status(this_year, status="COMPLETED")
		this_year_fail = Analysis.get_monthly_run_status(this_year, status="FAILED")

		return jsonify([this_year_comp,this_year_fail])

	if timely == "monthly" and action == "projects":
		this_year_proj = Analysis.get_monthly_projects(this_year)
		last_year_proj = Analysis.get_monthly_projects(this_year-1)

		return jsonify([this_year_proj,last_year_proj])
		
	if timely == "yearly" and action == "runs":
		query = Analysis.get_yearly_runs_by_workflows()
		
		return jsonify(query)

@blueprint.route('/analysis/<action>', methods=['GET','POST'])
@login_required
def get_p_status(action):

	## GROUP & Project
	## Holistic alluvial plot
	if action == "get-proj-pipe-run":

		## pipeline-version-count
		pipe_ver = Run.query.with_entities(Run.pipeline,Run.version,
		          func.count(Run.version)).group_by(Run.pipeline,Run.version).all()

		pipe_status = Run.query.with_entities(Run.pipeline,Run.status,
		          func.count(Run.status)).group_by(Run.pipeline,Run.status).all()

		version_status = Run.query.with_entities(Run.version,Run.status,
		            func.count(Run.status),null()).group_by(Run.version,Run.status).all()

		## For project-pipeline-count
		pipe_proj = db.session.\
		    query(Run.pipeline, func.count(distinct(Run.project_id))).\
		    group_by(Run.pipeline).\
		    all()

		## add "Project" at the front of pipe_proj elements
		pipe_proj_count=[]
		for i in range(len(pipe_proj)):
			tmp = list(pipe_proj[i])
			tmp.insert(0, "Project")
			pipe_proj_count.append( tmp)


		#return jsonify( pipe_proj_count + proc)
		return jsonify(pipe_proj_count + pipe_status)


############################################################################################################################
	if action == "runtime-process-count":
		
		query = Run.query.join(Process, Run.id==Process.run_id).\
		    group_by(Run.id).\
		    add_columns(Run.id, Run.pipeline, Run.run_time_hr, func.count(Process.id), Run.memory_GB ).all()
		
		main_list = []
		
		for j in query:
			#main_list.append({"workflow":   j[1], 
			#                  "runtime_hr": j[2],
			#                  "processes":  j[3] })
			
			
			main_list.append( [j[3], j[5], j[4]] )
			
		return jsonify(main_list)

	## Circos plot in stats-gp.html page
	if action == "get-per-group-workflow-runs":
		query = db.session.query(Group, Run).filter(Group.id==Project.group_id, Project.id==Run.project_id).group_by(Group.name, Run.pipeline).add_columns(Run.pipeline, func.count(Run.id)).all()

		main_list = []

		for j in query:	
			
			main_list.append( [ str(j[2]) , str(j[0]), int(j[3]) ] )
			
		return jsonify(main_list)

	if action == "get-per-group-workflow-runs-runtime":
		#query = db.session.query(Group, Run).filter(Group.id==Project.group_id, Project.id==Run.project_id).group_by(Group.name).add_columns(Run.pipeline, func.count(Run.id), func.sum(Run.run_time_hr)).all()
		
		
		query = db.session.query(Group, Run).\
		  filter(Group.id == Project.group_id, Project.id == Run.project_id).\
		  filter(Run.run_time_hr.isnot(None)).\
		  group_by(Group.name).\
		  add_columns(Run.pipeline, func.count(Run.id), func.sum(Run.run_time_hr)).\
		  all()
		
		main_list = []
		## (test_group, 102, 'Test-workflow', 1, 0.1)
		## group: test_group
		## Workflow run count: 1
		## Total runtime: 0.1
		for j in query:	
			
			main_list.append( [ str(j[0]) , j[3], round( j[4],2) ] )
			
		return jsonify(main_list)
		
############################################################################################################################>

	## for workflow by processes count bubble plot
	if action == "get-process-count-in-workflow":
	
		query = db.session.query(Run.pipeline, func.count(Process.id)).\
		filter(Run.id==Process.run_id).\
		group_by(Run.pipeline).all()
		
		pipelines = db.session.query(Run.pipeline).group_by(Run.pipeline).all()
		pipelines = list(chain(*pipelines) )
		
		main_list = []
		for i in pipelines:
			
			sub_list = []
			for j in query:
				
				
				if i in j:
					#print(i + " "+ str(j[0]) + " " + j[1] + " " + j[2])
					sub_list.append({"name": j[0], "value": j[1]})
			main_list.append({"name" : i, "data": sub_list})
		
		return jsonify(main_list)
	
	## for the bubble plot in run page
	if action == "get-detailed-runtime":
	
		query = db.session.query(Run.run_time_hr, Run.pipeline, Project.name).\
		filter(Project.id==Run.project_id).\
		order_by(Run.pipeline).all()
		
		pipelines = db.session.query(Run.pipeline).group_by(Run.pipeline).all()
		pipelines = list(chain(*pipelines) )

		"""[{
		name: 'FIMM-RNAseq',
		data: [{name: 'Project A', 22}, {name: 'Project B', 'value': 25}]
		},

		{
		name: 'RNASeqVar',
		data: [{name: 'Project X', 10}, {name: 'Project Y', 'value': 22}]
		},
		]"""

		main_list = []
		for i in pipelines:
			
			sub_list = []
			for j in query:
				
				
				if i in j:
					#print(i + " "+ str(j[0]) + " " + j[1] + " " + j[2])
					sub_list.append({"name": j[2], "value": j[0]})
			main_list.append({"name" : i, "data": sub_list})
	
		return jsonify(main_list)
	
	
	## for group size by project count in group & project page
	if action == "get-projects-in-group":
		
		query = db.session.query(Group.name, func.count(Project.name)).\
		filter(Group.id==Project.group_id).\
		group_by(Group.name).all()
		
		groups = db.session.query(Group.name).group_by(Group.name).all()
		groups = list(chain(*groups) )
		
		
		main_list = []
		for i in groups:
			
			sub_list = []
			for j in query:
				
				
				if i in j:
					#print(i + " "+ str(j[0]) + " " + j[1] + " " + j[2])
					sub_list.append({"name": j[0], "value": j[1]})
			main_list.append({"name" : i, "data": sub_list})
	
		return jsonify(main_list)
		
	## for workflow runs (events) on run page 
	if action == "get-run-events":
		## {
		## x: Date.UTC(1951, 5, 22),
		## name: 'First dogs in space',
		## label: 'First dogs in space',
		## description: 'Dezik and Tsygan were the first dogs to make a sub-orbital flight on 22 July 1951. Both dogs were recovered unharmed after travelling to a maximum altitude of 110 km.'
		## }
		
		## Join three tables
		query = db.session.query(Group,Project,Run).\
		    add_columns(
		    Run.pipeline,
		    Run.version,
		    Run.submitted,
		    ).\
		    filter(Group.id==Project.group_id,
		           Project.id==Run.project_id
		           ).all()	
		## serialize query to be able to convert to JSON
		a = []
		##  (fimm_ngs_kaarniranta, AMD_lncRNA, 1, 'FIMM-RNAseq', '2.0.7', datetime.datetime(2021, 4, 22, 9, 47, 29, 29000))
		for i in query:
			
			my_date  = i[5]
			new_date_1 = str(my_date.year) + "-" + str(my_date.month) + "-" + str(my_date.day) + " at " + str(my_date.hour) + ":" + str(my_date.minute)
			new_date_2 = my_date.timestamp() * 1000
			a.append({'x':new_date_2,
			          "name"    :str(i[3]),
			          "label":str(i[1]),
			          "description": "The workflow " + str(i[3]) + " (version " + str(i[4]) + ") was run for the project " + str(i[1]) + " from group " + str(i[0]) + " on " + new_date_1 +"."
			          })
		
		return jsonify(a)
	
	if action == "get-pipe-proc":
		## Pipeline's process status count
		proc = db.session.\
		    query(Run.pipeline, Process.status, func.count(Process.run_id)).\
		    filter(Process.run_id==Run.id).\
		    group_by(Run.pipeline,Process.status).\
		    all()

		return jsonify( proc )

	if action == "get-pipe-ver-status":

		

		ver_failed = Run.query.with_entities(Run.version,Run.status,
		            func.count(Run.status)).group_by(Run.version,Run.status).filter(Run.status=="FAILED").all()
		
		## add red color to failed ones
		ver_failed = [(*t, word) for t, word in zip(ver_failed, ["#ec5959"]*len(ver_failed))]
		
		ver_comp = Run.query.with_entities(Run.version,Run.status,
		            func.count(Run.status)).group_by(Run.version,Run.status).filter(Run.status=="COMPLETED").all()
		
		## add green color to failed ones
		ver_comp = [(*t, word) for t, word in zip(ver_comp, ["#7ae65a"]*len(ver_comp))]
		
		## pipeline version
		pipe_ver = Run.query.with_entities(Run.pipeline,Run.version,
		          func.count(Run.version)).group_by(Run.pipeline,Run.version).all()
		
		## unique pipelines
		names = {tup[0] for tup in pipe_ver}

		# Generate unique hexadecimal colors for each unique name
		random.seed(112233)
		color_dict = {name: '#' + ''.join(random.choices('0123456789ABCDEF', k=6)) for name in names}

		# Append the corresponding hexadecimal color at the end of each tuple in pipe_ver
		new_pipe_ver = [[tup[0], tup[1], tup[2], color_dict[tup[0]]] for tup in pipe_ver]
				
				
		#return jsonify( ver_failed + ver_comp + pipe_ver)
		return jsonify(new_pipe_ver + ver_comp + ver_failed)
				
	elif action == "get-run-runtime":

		## Get pipeline names
		names = Run.query.with_entities(Run.pipeline).order_by(Run.pipeline).all()
		name_list = []
		for i in names:
			if ' ' in i[0]:
				name_list.append(i[0].split(" ")[0])
			else:
				name_list.append(i[0])
		## take only unique
		name_list = list( set(name_list) )


		## Get row by names
		box_data_list = []
		for i in name_list:
			search = i+"%"
			query_res = Run.query.filter(Run.pipeline.like(search)).filter(Run.run_time_hr.isnot(None))
			runtime_list = []
			for row in query_res:
				run_time_hr    = row.run_time_hr
				runtime_list.append(run_time_hr)
				#print(row.name, Utils.toMB(row.peak_rss))

			## Calculate min, max, q1, q3 and median
			min_val = min(runtime_list)
			max_val = max(runtime_list)
			med_val = np.median(runtime_list)
			q1_val  = np.percentile(runtime_list, 25, interpolation = 'midpoint')
			q3_val  = np.percentile(runtime_list, 75, interpolation = 'midpoint')

			## keep only two decimal point
			min_val=round(min_val,2)
			max_val=round(max_val,2)
			med_val=round(med_val,2)
			q1_val=round(q1_val,2)
			q3_val=round(q3_val,2)

			box_data_list.append([i,min_val,q1_val,med_val,q3_val,max_val])
		return jsonify(box_data_list)
		#return jsonify([[760, 801, 848, 895, 965]])


	## ---------------------------------------------------------------------
	##  🇷​​​​​ 🇺​​​​🇳​​​​​​​​​​ 🇮​​​​​/🇴​​​​​
	elif "get-run-io-" in action:

		which=""
		if action.split("io-")[1] == "read":
			which = "read"
		elif action.split("io-")[1] == "write":
			which = "write"

		## Get run pipeline names
		names = Run.query.with_entities(Run.pipeline).order_by(Run.pipeline).all()
		name_list = []
		for i in names:
			if ' ' in i[0]:
				name_list.append(i[0].split(" ")[0])
			else:
				name_list.append(i[0])
		## take only unique
		name_list = list( set(name_list) )


		## Get row by names
		box_data_list = []
		for i in name_list:
			search = i+"%"
			query_res = Run.query.filter(Run.pipeline.like(search))
			my_list = []
			for row in query_res:
				if which == "read":
					my_list.append( row.read_TB)
				elif which == "write":
					my_list.append( row.write_TB)

			## Calculate min, max, q1, q3 and median
			min_val = min(my_list)
			max_val = max(my_list)
			med_val = np.median(my_list)
			q1_val  = np.percentile(my_list, 25, interpolation = 'midpoint')
			q3_val  = np.percentile(my_list, 75, interpolation = 'midpoint')

			## keep only two decimal point
			min_val=round(min_val,2)
			max_val=round(max_val,2)
			med_val=round(med_val,2)
			q1_val=round(q1_val,2)
			q3_val=round(q3_val,2)

			box_data_list.append([i,min_val,q1_val,med_val,q3_val,max_val])
		return jsonify(box_data_list)

	## ---------------------------------------------------------------------
	## 🇵​​​​​🇮​​​​​🇵​​​​​🇪​​​​​🇱​​​​​🇮​​​​​🇳​​​​​🇪​​​​​ 🇸​​​​​🇹​​​​​🇦​​​​​🇹​​​​​🇺​​​​​🇸​​​​​
	elif action == "get-pipe-status":
		query_res = Run.query.with_entities(Run.status).all()

		if(query_res):
			status=[]
			for i in query_res:
				status.append(i.status)

			## count stuffs
			count = Counter(status)

			## convert to dictionary
			dic   = dict(count)

			if "COMPLETED" in dic and "FAILED" in dic:
				return jsonify([{'name': 'FAILED','y': dic["FAILED"],},
					        {'name': 'COMPLETED','y': dic["COMPLETED"]}])
			elif "COMPLETED" in dic:
				return jsonify([{'name': 'COMPLETED','y': dic["COMPLETED"]}])
			elif "FAILED" in dic:
				return jsonify([{'name': 'FAILED','y': dic["FAILED"]}])

		else:
			return jsonify([{'name': 'COMPLETED','y': 0}])
	## ---------------------------------------------------------------------
	## 🇵​​​​​🇷​​​​​🇴​​​​​🇨​​​​​🇪​​​​ ​🇸​​🇸​​​​​ 🇸​​​​​🇹​​​​​🇦​​​​​🇹​​​​​🇺​​​​​🇸​​​​​
	elif action == "get-proc-status":
		query_res = Process.query.with_entities(Process.status).all()
		status=[]
		for i in query_res:
			status.append(i.status)

		## count stuffs
		count = Counter(status)

		## convert to dictionary
		dic   = dict(count)

		status_list = []

		if "CACHED" in dic:
			status_list.append({'name': 'CACHED','y': dic["CACHED"],})
		if "FAILED" in dic:
			status_list.append({'name': 'FAILED','y': dic["FAILED"],})
		if "COMPLETED" in dic:
			status_list.append({'name': 'COMPLETED','y': dic["COMPLETED"],})
		if "ABORTED" in dic:
			status_list.append({'name': 'ABORTED','y': dic["ABORTED"],})

		return jsonify(status_list)


	## ---------------------------------------------------------------------
	## 🇩​​​​​🇮​​​​​🇸​​​​​🇰​​​​​ 🇮​​​​​/🇴​​​​​
	## Get Disk I/O of each Run
	elif action == "get-run-io":
		query_res = Run.query.with_entities(Run.completed,
		                                    Run.read_TB,
		                                    Run.write_TB).order_by(Run.completed).filter(Run.run_time_hr.isnot(None)).all()
		csv= "Date,Disk Read,Disk Write\n"
		for i in query_res:
			dt        = str(i[0].date())
			run_read  = i[1]
			run_write = i[2]
			#print(project)
			csv       = csv + dt + "," + '%.2f' % float(run_read) + "," + 	            '%.2f' % float(run_write) + "\n"


		## Return a CSV file
		return Response(csv,
		    mimetype="text/csv",
		    headers={"Content-disposition":"attachment; filename=run-io.csv"})

	else:
		return render_template('page-404.html'), 404




# ███████╗██████╗░██████╗░░█████╗░██████╗░░██████╗
# ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
# █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝╚█████╗░
# ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗░╚═══██╗
# ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║██████╔╝
# ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═════╝░
## HTTP error redirection ======================================================
@blueprint.route('/<template>')
@login_required
def global_routing(template):

	try:

		name = template
		## check if there is extension
		if not template.endswith( '.html' ):
		    template += '.html'

		# Detect the current page
		segment = get_segment( request )

		## page title
		#title = name.capatalize()

		# Serve the file (if exists) from app/templates/FILE.html
		return render_template( template, segment=segment , title=name.title())

	except TemplateNotFound:
		return render_template('page-404.html', segment=""), 404

	except:
		return render_template('page-500.html', segment=""), 500




## segments to highlight side menu =============================================
# Helper - Extract current page name from request
def get_segment( request ):

	try:

		segment = request.path.split('/')[-1]

		if segment == '':
			segment = 'index'

		return segment

	except:
		return None
