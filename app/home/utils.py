import re
import os
import os.path
from datetime import datetime, time, timedelta

import glob
import pandas as pd
from app import db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import csv
import time as tt
import numpy as np
from app.home.models import Group, Project, Run, Process


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.base.models import Settings
class Misc:
	"Misc. functions"
	
	@staticmethod
	def send_email(toEmail, subject, message):

		## get SMTP details from the database
		settings = Settings.query.filter_by(name="SMTP_SERVER").first()
		smtpServer = settings.value
		## port
		settings = Settings.query.filter_by(name="SMTP_PORT").first()
		port = settings.value
		##tls
		settings = Settings.query.filter_by(name="SMTP_USE_TLS").first()
		tls = settings.value
		## user
		settings = Settings.query.filter_by(name="SMTP_USERNAME").first()
		username = settings.value
		## password
		settings = Settings.query.filter_by(name="SMTP_PASSWORD").first()
		password = settings.value
		## reply to
		settings = Settings.query.filter_by(name="REPLY_EMAIL").first()
		replyTo = settings.value
		
		if smtpServer == "" or str(port) == "" or tls == "" or username == "" or password == "" or replyTo == "":
			return("Error: SMPT server details missing.")
		
		
		FROM = replyTo
		TO = toEmail
		SUBJECT = subject
		TEXT = message

		# Prepare actual message
		# Create a MIMEText object for the email content
		email_content = MIMEMultipart()
		email_content['From']    = FROM
		email_content['To']      = TO
		email_content['Subject'] = SUBJECT
		email_content.attach(MIMEText(message, 'plain'))
		
		
		try:
			server = smtplib.SMTP(smtpServer + ":" + port)
			server.ehlo()
			server.starttls()
			server.login(username, password)
			server.sendmail(FROM, TO, email_content.as_string())
			server.close()
			return ('Successfully sent an email')
		except Exception as e:
			return("Failed to send mail.\n" + str(e))

class Utils:
	""" Calculate box plot values from a list """
	@staticmethod
	def calc_quantiles(mylist):
		## Calculate min, max, q1, q3 and median
		min_val = min(mylist)
		max_val = max(mylist)
		med_val = np.median(mylist)
		q1_val  = np.percentile(mylist, 25, interpolation = 'midpoint')
		q3_val  = np.percentile(mylist, 75, interpolation = 'midpoint')
		
		## keep only two decimal point
		min_val=round(min_val,2)
		max_val=round(max_val,2)
		med_val=round(med_val,2)
		q1_val=round(q1_val,2)
		q3_val=round(q3_val,2)
		
		return [min_val, q1_val, med_val,  q3_val, max_val]
	
	"""calculate percentage change """
	@staticmethod
	def per_change(current, previous):
		if current == previous:
			return 100.0
		try:
			return ((current - previous) / previous) * 100.0
		except ZeroDivisionError:
			return 0

        
	"Returns in MB not MiB"
	@staticmethod
	def toMB(diskUsage):

		if diskUsage == 0:
			return 0
		if ' ' in diskUsage:
			amt, unit = diskUsage.split(" ")
			if unit == "B":
				return float(amt) / (1000*1000)
			elif unit == "KB":
				return float(amt) / 1000
			elif unit == "MB":
				return float(amt)
			elif unit == "GB":
				return float(amt)*1000
			elif unit == "TB":
				return float(amt)*1000*1000
			else:
				return False
		else:
			return 0
	
	
	
	## returns a time object from a given time
	@staticmethod
	def getTimeObj(mytime):
		ms = 0 
		s  = 0
		m  = 0
		h  = 0
		d  = 0

		split = mytime.split(" ")
			
		## for ms
		idx = [i for i, item in enumerate(split) if re.search( re.compile("ms$") , item)]
		if len(idx):
			ms   = split[idx[0]]
			ms   = int( ms.replace("ms","") )
		## seconds
		idx = [i for i, item in enumerate(split) if re.search( re.compile("[0-9]s$") , item)]
		if len(idx):
			s    = split[idx[0]]
			s    = float( s.replace("s","") )
		## minutes
		idx = [i for i, item in enumerate(split) if re.search( re.compile("m$") , item)]
		if len(idx):
			m    = split[idx[0]]
			m    = int( m.replace("m","") )
		## hours
		idx = [i for i, item in enumerate(split) if re.search( re.compile("h$") , item)]
		if len(idx):
			h    = split[idx[0]]
			h    = int( h.replace("h","") )
		## days (UNUSED)
		idx = [i for i, item in enumerate(split) if re.search( re.compile("d$") , item)]
		if len(idx):
			d    = split[idx[0]]
			d    = int( d.replace("d","") )

		
		return time(int(h),int(m),int(s), int(ms))
		
		
	## function to check file extension
	@staticmethod
	def checkExt(filename, exts):
		file_ext = str.split(filename,".")[1]
		if file_ext in exts:
			return True
		else:
			return False
	
	## Function to merge more than one Trace files
	@staticmethod
	def parseReportFile(reportFile):
	
		groupName   = ""
		projectName = ""
		pipeline    = ""
		pipelineVer = ""
		
		with open(reportFile) as reader:
			line_counter=0
			for line in reader.readlines():

				## increase line counter
				line_counter += 1

				## grep pipeline name and version
				if line_counter == 2:

					pipeline    = str.split(line,"v")[0].strip()
					pipelineVer = str.split(line,"v")[1].strip()
					continue
					
				## grep run name
				if re.search("Run Name:", line):
					projectName = str.split(line,": ")[1].strip()
					continue
				
				## grep project name
				if re.search("Group:", line):
					groupName = str.split(line,": ")[1].strip()
					continue

		return [groupName, projectName, pipeline, pipelineVer]
	
	## function to parse trace files
	## Takes list [groupName, projectName, pipelineVer]
	@staticmethod
	def parseTraceFiles(metadataList, uploadDir, actionSource):
		
		## function input
		groupName   = metadataList[0]
		projectName = metadataList[1]
		pipeline    = metadataList[2]
		pipelineVer = metadataList[3]

		## remove 'v' or 'V' from version
		if "v" in pipelineVer:
			pipelineVer = pipelineVer.replace("v","")
		elif "V" in pipelineVer:
			pipelineVer = pipelineVer.replace("V", "")
		
		
		## Create a group record if does not exist
		g = ""
		groupExists = Group.query.filter_by(name=groupName).first()
		if not groupExists:
			g = Group(name=groupName)
			db.session.add(g)
			db.session.commit()
		else:
			g = groupExists
		
		## Create a project record if does not exist
		projExists = Project.query.filter_by(name=projectName).first()
		if not projExists: 
			p = Project(name=projectName, group=g)
			db.session.add(p)
			db.session.commit()
		else:
			p = projExists
		
		
		path = uploadDir
		
		## support both trace.txt and Trace.txt
		allFiles = glob.glob(os.path.join(path, "Trace.txt*"))
		if len(allFiles)==0:
			allFiles = glob.glob(os.path.join(path, "trace.txt*"))
		
		## take trace files in a loop
		fileCounter = 0
		run_exists_flag   = 0
		for traceFile in allFiles:
			fileCounter += 1
			fName, fExt = os.path.splitext(traceFile)
			fExt = fExt.replace(".","")
			count = 0
			if fExt == "txt":
				count = 1
			else:
				count = int(fExt) + 1
			
			
			print("COUNT:" + str(count))
			
			## check if record exists
			runExists = Run.query.filter_by(pipeline=pipeline, 
			                                version=pipelineVer,
			                                #run_count=count,
			                                #trace_file=os.path.basename(traceFile),
			                                submitted = Utils.checkRunFromTraceFile(traceFile, "submitted"),
			                                status = "COMPLETED",
			                                project=p).first()
			
			## Create a run record
			if not runExists:
				r = Run(pipeline=pipeline, 
					version=pipelineVer, 
					submitted=Utils.checkRunFromTraceFile(traceFile, "submitted"), 
					#completed="",
					trace_file=os.path.basename(traceFile),
					run_count=count,
					project=p,
					entry_via=actionSource)
				
				db.session.add(r)
				db.session.commit()
			else:
				r=runExists
				run_exists_flag = 1
				return {"message":"No records inserted into the database. This is a completed run.", "response":"warning"}
			
			##------------------------------------------------------
			## variables for summarizing columns from trace and adding
			## to run table
			run_status = "COMPLETED"
			submitted_list = []
			completed_list = []
			rss = 0
			disk_read = 0
			disk_write = 0
			wchar_list = []
			with open(traceFile) as reader1:
				lineCounter  = -1
				proc_exists_flag   = []
				for line in reader1.readlines():
					## skip header line
					if lineCounter >= 0:
						
						split = line.split("\t")
						
						taskID    = split[0]
						hashID    = split[1]
						native_id = split[2]
						name      = split[3]
						status    = split[4]
						exit      = split[5]
						
						#convert string to data and time object
						if(split[6] == "-"):
							continue
						submit    = datetime.strptime(split[6], "%Y-%m-%d %H:%M:%S.%f")
						duration  = Utils.getTimeObj(split[7])
						realtime  = Utils.getTimeObj(split[8])
						cpu       = split[9]
						peak_rss  = split[10]
						peak_vmem = split[11]
						rchar     = split[12]
						wchar     = split[13]
						
						## append submitted time to the list
						if status=="COMPLETED":
							submitted_list.append(submit)
							## sum rss
							rss        = rss        + Utils.toMB(peak_rss)
							disk_read  = disk_read  + Utils.toMB(rchar)
							disk_write = disk_write + Utils.toMB(wchar.rstrip("\n"))
							
							## completed = submitted + runtime
							
							completed_list.append(submit + timedelta(hours=realtime.hour, minutes=realtime.minute,seconds=realtime.second, microseconds=realtime.microsecond) )
							
						## check if completed
						if status=="FAILED":
							submitted_list.append(submit)
							completed_list.append(submit + timedelta(hours=realtime.hour, minutes=realtime.minute,seconds=realtime.second, microseconds=realtime.microsecond) )
							run_status="FAILED"
						
						if status=="ABORTED":
							submitted_list.append(submit)
							completed_list.append(submit)
							run_status="ABORTED"
						
						## check if process record exists
						procExists = Process.query.filter_by(
						            #task_id   = taskID,
						            hash      = hashID,
						            native_id = native_id,
						            status    = status ).first()
						
						
						## insert to database if the process does not exit
						if not procExists:
							proc = Process(task_id   = taskID,
								    hash      = hashID,
								    native_id = native_id,
								    name      = name,
								    status    = status,
								    exit      = exit,
								    submit    = submit,
								    duration  = duration,
								    realtime  = realtime,
								    cpu       = cpu,
								    peak_rss  = peak_rss,
								    peak_vmem = peak_vmem,
								    rchar     = rchar,
								    wchar     = wchar,
								    runs       = r)
								    
								    
							db.session.add(proc)
							db.session.commit()
							#tt.sleep(0.0005)
						
							proc_exists_flag.append(0)
							
						else:
							proc_exists_flag.append(1)
						
						## If else end
						
					
					## increase line counter
					lineCounter += 1
				
				## for loop end
			
			
			## update run table
			if len(submitted_list) !=0:
				r.submitted = min(submitted_list)
			if len(completed_list) !=0:
				r.completed = max(completed_list)
			if len(submitted_list) !=0 and len(completed_list) !=0:
				rt            = max(completed_list) - min(submitted_list)
				rt_hr         = rt.seconds/(60*60)
				r.run_time_hr = "{:.2f}".format(rt_hr)
			
			if status == "ABORTED":
				r.status    = status
				r.read_TB   = 0
				r.write_TB  = 0
				r.memory_GB = 0
			else:
				r.status    = run_status
				r.read_TB   = "{:.4f}".format(disk_read/(1000*1000))
				r.write_TB  = "{:.4f}".format(disk_write/(1000*1000))
				r.memory_GB = "{:.4f}".format(rss / 1000)
			
			## update run count
			r.run_count = r.run_count 
			
			db.session.commit() 
			
			## with end
			
		#return {"run-exists":run_exists_flag, "existant-processes": proc_exists_flag.count(1),"non-existant-processes":proc_exists_flag.count(0)}
		return {"message":"Records inserted into the database.", "response":"info"}
		
		

	## Function to check status, submitted time and completed time of a run.
	## Data is collected from trace file
	@staticmethod
	def checkRunFromTraceFile(traceFile, var):
		## Allowed variables
		allowed_var = ["status", "submitted", "completed"]
		
		## return message if above allowed values are not provided as 
		## a function parameter
		if var not in allowed_var:
			return {"message":"variable value not allowed."}
		
		## empty lists
		status_list    = []
		submitted_list = []
		completed_list = []
		
		with open(traceFile) as reader1:
				lineCounter=-1
				for line in reader1.readlines():
					## skip header line
					if lineCounter >= 0:
						
						## print line
						print("LINE:", line)
						## split by tab
						split = line.split("\t")
						
						## skip if this job was not submitted
						if(split[6] == "-"):
							continue
						
						## get jon status from 5th column
						status    = split[4]
						
						## split submitted time and get a time object
						submit    = datetime.strptime(split[6], "%Y-%m-%d %H:%M:%S.%f")
						realtime  = Utils.getTimeObj(split[8])
						
						
						## if a job is COMPLETED or CACHED 
						## append submit time to submitted list
						## append completed time to completed list
						if status=="COMPLETED" or status=="CACHED":
							submitted_list.append(submit)
							completed_list.append(submit + timedelta(hours=realtime.hour, minutes=realtime.minute,seconds=realtime.second, microseconds=realtime.microsecond) )
						
						## if a job has FAILED add 'failed' to status list
						if status=="FAILED":
							submitted_list.append(submit)
							completed_list.append(submit + timedelta(hours=realtime.hour, minutes=realtime.minute,seconds=realtime.second, microseconds=realtime.microsecond) )
							status_list.append("FAILED")
						## for aborted put submitted time = completed time
						if status=="ABORTED":
							submitted_list.append(submit)
							completed_list.append(submit)
							status_list.append("ABORTED")
						
					lineCounter += 1
		## send status (sends failed if FAILED value is found in submitted list)
		print(submitted_list)
		if var == "status":
			if "FAILED" in status_list:
				return "Run failed"
			elif "ABORTED" in status_list:
				return "Run aborted"
			else:
				return "Run completed"
		
		## returm the youngest time of a submitted job
		if var == "submitted":		
			return min(submitted_list)
		
		## return the oldest time of a completed job
		if var == "completed":
			return max(completed_list)
				
			
