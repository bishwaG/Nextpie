from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class Group(db.Model):
	__tablename__ = 'Group'
	 
	id        = db.Column(db.Integer, primary_key=True)
	name      = db.Column(db.String(64), index=True, unique=True)
	
	## one to many
	projects = relationship("Project", backref="group", cascade="all, delete")
	
	
	def __repr__(self):
        	return '{}'.format(self.name)  
	
	## function get columns in json format
	def toJSON(self):
		"""Return object data in easily serializable format"""
		return {
		    "id"       : self.id,
		    "name"     : self.name
		}
		

class Project(db.Model):
	__tablename__ = 'Project'
	 
	id        = db.Column(db.Integer(), primary_key=True)
	name      = db.Column(db.String(64), index=True, unique=True)
	
	## foreign key
	group_id  = db.Column(db.Integer, db.ForeignKey('Group.id', ondelete="CASCADE"))
	
	## one to many relationship
	runs = relationship("Run", backref="project", cascade="all, delete")
	
	def __repr__(self):
        	return '{}'.format(self.name)
	
	## function get columns in json format
	def toJSON(self):
		"""Return object data in easily serializable format"""
		return {
		    "id"       : self.id,
		    "name"     : self.name,
		    "group_id" : self.group_id
		}
	

class Run(db.Model):
	__tablename__ = 'Run'
	id          = db.Column(db.Integer(), primary_key=True)
	pipeline    = db.Column(db.String(140))
	version     = db.Column(db.String(10))
	submitted   = db.Column(db.DateTime())
	completed   = db.Column(db.DateTime())
	trace_file  = db.Column(db.String(200))
	run_count   = db.Column(db.Integer())
	run_time_hr = db.Column(db.Float())
	read_TB     = db.Column(db.Float())
	write_TB    = db.Column(db.Float())
	memory_GB   = db.Column(db.Float())
	status      = db.Column(db.String(10))
	entry_via   = db.Column(db.String(10))
	
	## foreign key
	project_id = db.Column(db.Integer(), db.ForeignKey('Project.id', ondelete="CASCADE"))
	
	## relationsip (one to many)
	processes = relationship("Process",backref="runs", cascade="all, delete")
	
	def __repr__(self):
        	return '{}'.format(self.id)
        	
	## function get object data in  json format
	def toJSON(self):
		"""Return object data in easily serializable format"""
		return {
		    "id"         : self.id,
		    "workflow"   : self.pipeline,
		    "version"    : self.version,
		    "submitted"  : self.submitted.strftime("%d/%m/%Y"),
		    "completed"  : self.completed.strftime("%d/%m/%Y"),
		    "run_time_hr": self.run_time_hr,
		    "read_TB"    : self.read_TB,
		    "write_TB"   : self.write_TB,
		    "memory_GB"  : self.memory_GB,
		    "status"     : self.status,
		    "entry_via"  : self.entry_via,
		    "project_id" : self.project_id
		}
		
class Process(db.Model):
	__tablename__ = 'Process'
	id        = db.Column(db.Integer, primary_key=True)
	task_id   = db.Column(db.String(140))
	hash      = db.Column(db.String(15))
	native_id = db.Column(db.Integer())
	name      = db.Column(db.String(250))
	status    = db.Column(db.String(20))
	exit      = db.Column(db.Integer())
	submit    = db.Column(db.DateTime())
	duration  = db.Column(db.Time())
	realtime  = db.Column(db.Time())
	cpu       = db.Column(db.String(140))
	peak_rss  = db.Column(db.String(140))
	peak_vmem = db.Column(db.String(140))	
	rchar	  = db.Column(db.String(140))
	wchar     = db.Column(db.String(140))
	
	## foreign key
	run_id = db.Column(db.Integer, db.ForeignKey('Run.id', ondelete="CASCADE"))
	
	## convert to MB
	def toGB(self,diskUsage):

		if diskUsage == 0:
			return 0
		if ' ' in diskUsage:
			amt, unit = diskUsage.split(" ")
			if unit == "B":
				return float(amt) / (1000*1000*1000)
			elif unit == "KB":
				return float(amt) / (1000*1000)
			elif unit == "MB":
				return float(amt)
			elif unit == "GB":
				return float(amt)
			elif unit == "TB":
				return float(amt)*1000
			else:
				return False
		else:
			return 0
	
	## function get object data in  json format
	def toJSON(self):
		"""Return object data in easily serializable format"""
		cpu=self.cpu.split("%")[0]
		if cpu=="-":
			cpu=0
			
		peak_rss  = self.toGB(self.peak_rss)
		peak_vmem = self.toGB(self.peak_vmem)
		rchar     = self.toGB(self.rchar)
		wchar     = self.toGB(self.wchar.strip())
		return {
		    "id"        : self.id,
		    "task_id"   : self.task_id,
		    "hash"      : self.hash,
		    "native_id" : self.native_id,
		    "name"      : self.name,
		    "status"    : self.status,
		    "exit"      : self.exit,
		    "submit"    : self.submit.strftime("%d/%m/%Y"),
		    "duration"  : self.duration.strftime("%H:%M:%S.%f"),
		    "realtime"  : self.realtime.strftime("%H:%M:%S.%f"),
		    "cpu"       : cpu,
		    "peak_rss"  : peak_rss,
		    "peak_vmem" : peak_vmem,
		    "rchar"     : rchar,
		    "wchar"     : wchar,
		    "run_id"    : self.run_id
		}
	
	def __repr__(self):
        	return '{}'.format(self.name)
	

