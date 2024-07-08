from app.home.models import Group, Project, Run
from app import db
from flask import jsonify
from sqlalchemy import extract, func
from wtforms.validators import Regexp
from wtforms import StringField
import datetime

class Analysis:
    
	## Fetch all rows from Group tables
	@staticmethod
	def get_all_groups():
		# list for serialization
		a = []
		
		#query = Group.query.filter(Group.name.like("%")).all()
		query = Group.query.all()
		[a.append(i.toJSON()) for i in query]
		return jsonify(a)
	
	## Fetch all rows from Projects
	def get_all_projects():
		# list for serialization
		a = []
		
		#query = Group.query.filter(Group.name.like("%")).all()
		query = Project.query.all()
		[a.append(i.toJSON()) for i in query]
		return jsonify(a)
	
	
	## Fetch data footprint by year
	def get_footprint_by_year():
		this_year = datetime.datetime.now().year
		# Execute the query to get the sum of write_TB for each year
		query_this_year = db.session.query(extract('year', Run.submitted).label('year'),func.sum(Run.write_TB)+" TB").group_by(extract('year', Run.submitted)).all()
		return jsonify(query_this_year)
		
	## Fetch data footprint by month for a given year
	def get_footprint_by_month(year):
		## mapping number to month
		month_names = {
		1: 'January', 2: 'February', 3: 'March', 4: 'April',
		5: 'May', 6: 'June', 7: 'July', 8: 'August',
		9: 'September', 10: 'October', 11: 'November', 12: 'December'
		}
    
		## query
		query_this_year = db.session.query(extract('year', Run.submitted).label('year'),extract('month', Run.submitted).\
		label('month'),func.sum(Run.write_TB).\
		label('total_write_TB')).\
		filter(extract('year', Run.submitted) == year).\
		group_by(extract('year', Run.submitted),extract('month', Run.submitted)).all()
		
		# Format the result with month names instead of numbers
		result = [
		{
		'year': row.year,
		'month': month_names[row.month],  # Convert month number to month name
		'total_write_TB': row.total_write_TB
		} 
		for row in query_this_year]
		
		return jsonify(result)	
	
	## Fetch runs by year
	def get_runs(year):
		
		if year:
		
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
			    filter(extract('year', Run.submitted) == year).all()
		else:
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
			    filter(Run.id.like("%")).all()

		## serialize query to be able to convert to JSON
		a = []
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
