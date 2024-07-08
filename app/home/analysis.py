from datetime import date
from app import db
from app.home.models import Group, Project, Run
from sqlalchemy import extract, func, distinct
from itertools import chain
from flask import jsonify

class Analysis:

	@staticmethod
	def get_monthly_run_status(year, status):

		this_year  = year

		query = db.session.query(extract('month', Run.submitted), func.count(Run.status)).\
		group_by(extract('month', Run.submitted)).\
		filter(extract('year', Run.submitted) == this_year, Run.status==status).all()

		month_list = []
		for mth in range(1,13):
			val=0
			for record in query:
				if mth == record[0]:
					val=record[1]
					continue
			#print(mth,val)
			month_list.append(val)


		return {"name":status,"data":month_list}
	
	
	@staticmethod
	def get_monthly_run_counts(year):

		this_year  = year
		query = db.session.query(extract('month', Run.submitted)).\
		filter(extract('year', Run.submitted) == this_year).all()

		## unlist
		data = list(chain(*query) )

		## count occurances for each month
		month_list = []
		for i in range(1,13):
			month_list.append(data.count(i))

		return {"name":"Year "+str(this_year),"data":month_list}
	
	def get_yearly_runs_by_workflows():
		query=db.session.query(extract('year', Run.submitted), func.count(Run.pipeline), Run.pipeline).\
		group_by(Run.pipeline).all()
		
		return query
		
	
	@staticmethod
	def get_monthly_disk(year):
		this_year  = year
		query = db.session.query(extract('month', Run.submitted), func.sum(Run.write_TB)).\
		group_by(extract('month', Run.submitted)).\
		filter(extract('year', Run.submitted) == this_year).all()

		## fromat data for ag-grid
		month_list = []
		for i in range(1,13):
			val=0
			for record in query:
				if i == record[0]:
					val=record[1]
					continue
			month_list.append( round(val, 2))

		return {"name":"Year "+str(this_year),"data":month_list}

	@staticmethod
	def get_monthly_memory(year):
		this_year  = year
		query = db.session.query(extract('month', Run.submitted), func.sum(Run.memory_GB)).\
		group_by(extract('month', Run.submitted)).\
		filter(extract('year', Run.submitted) == this_year).all()

		## fromat data for ag-grid
		month_list = []
		for i in range(1,13):
			val=0
			for record in query:
				if i == record[0]:
					val=record[1]
					continue
			month_list.append( round(val, 2))

		return {"name":"Year "+str(this_year),"data":month_list}

	@staticmethod
	def get_monthly_projects(year):
		this_year  = year

		query = db.session.query(extract('month', Run.submitted), func.count(distinct(Run.project_id))).\
		group_by(extract('month', Run.submitted)).\
		filter(extract('year', Run.submitted) == this_year).all()

		month_list = []
		for mth in range(1,13):
			val=0
			for record in query:
				if mth == record[0]:
					val=record[1]
					continue
			#print(mth,val)
			month_list.append(val)


		return {"name":"Year "+str(this_year),"data":month_list}
