import re
import os
import os.path
import random
import string
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
    def gen_groupName(length=12):
        while True:
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            group_name = f"group_{random_string}"
            
            ## check if group exists
            exist_group = Group.query.filter_by(name=group_name).first()
            if exist_group is None:
                return group_name
    
    @staticmethod
    def gen_projectName(length=12):
        while True:
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            project_name = f"project_{random_string}"
            
            ## check if group exists
            exist_project = Project.query.filter_by(name=project_name).first()
            if exist_project is None:
                return project_name
    
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
    
    @staticmethod
    def duration_to_min(time_str):
        time_dict = {'d': 0.0, 'h': 0.0, 'm': 0.0, 's': 0.0, 'ms': 0.0}
        if not isinstance(time_str, str):
            return 0
        parts = time_str.strip().split()

        for item in parts:
            try:
                if item.endswith('ms'):
                    time_dict['ms'] += float(item[:-2])
                else:
                    unit = item[-1]
                    if unit in time_dict:
                        time_dict[unit] += float(item[:-1])
            except (ValueError, IndexError):
                continue  # skip invalid parts

        # Convert all to total minutes
        total_minutes = (
          time_dict['d'] * 24 * 60 +    # days → minutes
          time_dict['h'] * 60 +         # hours → minutes
          time_dict['m'] +              # already in minutes
          time_dict['s'] / 60 +         # seconds → minutes
          time_dict['ms'] / 1000 / 60   # ms → seconds → minutes
        )
        return total_minutes
    
    ########################################################################
    ## returns a time object from a given time
    ########################################################################
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
        
        ## if s == 60
        if s == 60:
            s = 0
            m = m + 1
        
        ## if h == 24
        if h == 24:
            h = 0
            d = d + 1
        
        #print(s)
        return time(int(h),int(m),int(s), int(ms))
        
    ########################################################################
    ## function to check file extension
    ########################################################################
    @staticmethod
    def checkExt(filename, exts):
        file_ext = str.split(filename,".")[1]
        if file_ext in exts:
            return True
        else:
            return False
    ########################################################################
    ## Function to merge more than one Trace files
    ########################################################################
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
    
    ########################################################################
    ## Get folder size in MB
    ########################################################################
    @staticmethod
    def get_folder_size(path):
        """Calculate total size of a directory in bytes."""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
                except OSError:
                    pass  # Skip unreadable files
        return total

    @staticmethod
    def build_tree(path):
        """Recursively build folder tree with size info."""
        if not os.path.exists(path):
            return None

        result = {
        "name": os.path.basename(path),
        "path": path,
        "size_kb": round(Utils.get_folder_size(path) / 1024, 2),
        "children": []
        }

        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    child = Utils.build_tree(entry.path)
                    if child:
                        result["children"].append(child)
        except PermissionError:
            pass  # Skip folders without access

        return result
        
        
    ########################################################################
    ## function to parse trace files
    ## Takes list [groupName, projectName, pipelineVer]
    ########################################################################
    @staticmethod
    def parseTraceFiles(metadataList, traceFilePath, actionSource, random_group_proj):
        
        ## function input
        groupName   = metadataList[0]
        projectName = metadataList[1]
        pipeline    = metadataList[2]
        pipelineVer = metadataList[3]

        ## Create a group record if does not exist
        g = Group.query.filter_by(name=groupName).first()
        if not g:
            g = Group(name=groupName)
            db.session.add(g)
            db.session.flush() # Flush to get g.id for project
        
        ## Create a project record if does not exist
        p = Project.query.filter_by(name=projectName, group_id=g.id).first()
        if not p: 
            p = Project(name=projectName, group=g)
            db.session.add(p)
            db.session.flush() # Flush to get p.id for run
        
        if os.path.isfile(traceFilePath):
            allFiles = [traceFilePath]
        elif os.path.isdir(traceFilePath):
             allFiles = glob.glob(os.path.join(traceFilePath, "TRACE__*"))
        else:
            allFiles = []

        print(f"[apps.home.Utils ] WORKFLOW: {pipeline}\tVERSION:  {pipelineVer}\tGROUP  :  {groupName}\tPROJECT:  {projectName}")
        print(f"[apps.home.Utils ] FILES   :  \n" + "\n".join(allFiles))
        
        total_new_processes = 0
        total_existing_processes = 0
        run_exists_flag = 0

        for traceFile in allFiles:
            submitted_time = Utils.checkRunFromTraceFile(traceFile, "submitted")
            if not submitted_time:
                print(f"Skipping file with no completed processes: {traceFile}")
                continue

            runExists = Run.query.filter_by(pipeline=pipeline, 
                                            version=pipelineVer,
                                            submitted=submitted_time,
                                            status="COMPLETED",
                                            project=p).first()
            
            if runExists:
                run_exists_flag = 1
                total_existing_processes = -1 # Special flag to indicate run exists
                continue

            r = Run(pipeline=pipeline, 
                    version=pipelineVer, 
                    submitted=submitted_time, 
                    trace_file=os.path.basename(traceFile),
                    run_count=1,
                    project=p,
                    entry_via=actionSource)
            db.session.add(r)
            db.session.flush() # Flush to get r.id for processes

            try:
                # Read trace file into a pandas DataFrame for faster processing
                df = pd.read_csv(traceFile, sep='\t', on_bad_lines='skip')
                df = df.dropna(subset=['submit'])
                df = df[df.submit != '-']
            except Exception as e:
                print(f"Error reading or processing trace file {traceFile} with pandas: {e}")
                continue

            if df.empty:
                continue

            # Get all unique hashes from the dataframe
            all_hashes = df['hash'].unique().tolist()
            # Query the database once for all existing hashes to reduce DB calls
            existing_hashes = {res[0] for res in Process.query.filter(Process.hash.in_(all_hashes)).with_entities(Process.hash)}
            
            new_processes_list = []
            # Filter dataframe to only include new processes not already in the database
            df_filtered = df[~df['hash'].isin(existing_hashes)]
            
            run_status = "COMPLETED"
            submitted_list = []
            completed_list = []
            rss = 0
            disk_read = 0
            disk_write = 0

            # Iterate over the full dataframe to calculate run statistics
            for index, row in df.iterrows():
                if row['status'] == 'COMPLETED':
                    submit_dt = datetime.strptime(row['submit'], "%Y-%m-%d %H:%M:%S.%f")
                    realtime_str = row.get('realtime', '0s')
                    realtime_td = Utils.getTimeObj(realtime_str if pd.notna(realtime_str) else '0s')
                    completed_dt = submit_dt + timedelta(hours=realtime_td.hour, minutes=realtime_td.minute, seconds=realtime_td.second, microseconds=realtime_td.microsecond)
                    
                    submitted_list.append(submit_dt)
                    completed_list.append(completed_dt)
                    
                    rss += Utils.toMB(row.get('peak_rss', '0'))
                    disk_read += Utils.toMB(row.get('rchar', '0'))
                    disk_write += Utils.toMB(row.get('wchar', '0').rstrip("\n"))

                elif row['status'] in ["FAILED", "ABORTED"]:
                    run_status = row['status']
            
            # Iterate over the filtered dataframe to create new Process objects
            for index, row in df_filtered.iterrows():
                proc = Process(
                    task_id=row['task_id'], hash=row['hash'], native_id=row['native_id'],
                    name=row['name'], status=row['status'], exit=row['exit'],
                    submit=datetime.strptime(row['submit'], "%Y-%m-%d %H:%M:%S.%f"),
                    duration_min=Utils.duration_to_min(row['duration']), 
                    realtime_min=Utils.duration_to_min(row['realtime']),
                    cpu=row['%cpu'], peak_rss=row.get('peak_rss'), peak_vmem=row.get('peak_vmem'),
                    rchar=row.get('rchar'), wchar=row.get('wchar'), runs=r
                )
                new_processes_list.append(proc)

            # Bulk save new processes to the database for improved performance
            if new_processes_list:
                db.session.bulk_save_objects(new_processes_list)
            
            num_new = len(new_processes_list)
            num_existing = len(df) - num_new
            total_new_processes += num_new
            total_existing_processes += num_existing

            if submitted_list and completed_list:
                r.submitted = min(submitted_list)
                r.completed = max(completed_list)
                rt = r.completed - r.submitted
                r.run_time_hr = f"{rt.total_seconds() / 3600:.2f}"
            
            r.status = run_status
            if run_status != "ABORTED":
                r.read_TB = f"{disk_read / (1000*1000):.4f}"
                r.write_TB = f"{disk_write / (1000*1000):.4f}"
                r.memory_GB = f"{rss / 1000:.4f}"
            else:
                r.read_TB, r.write_TB, r.memory_GB = '0', '0', '0'

        if total_new_processes == 0 and random_group_proj:
            # Rollback changes if no new processes were added for a randomly generated group/project
            db.session.rollback()
            # Manually delete if they were committed in a previous iteration
            if g.id and not g.projects:
                db.session.delete(g)
            return {"message": "No new records inserted.", "response": "warning"}

        db.session.commit()

        if run_exists_flag and total_existing_processes == -1:
            return {"message": "No records inserted; a matching run already exists.", "response": "warning"}
        
        if total_existing_processes > 0 and total_new_processes > 0:
            return {"message": f"Partially inserted: {total_new_processes} new, {total_existing_processes} existing.", "response": "warning"}
        elif total_existing_processes > 0 and total_new_processes == 0:
            return {"message": f"No new records inserted, {total_existing_processes} processes already exist.", "response": "warning"}
        
        return {"message": f"Successfully inserted {total_new_processes} new processes.", "response": "success"}


    ########################################################################
    ## Function to check status, submitted time and completed time of a run.
    ## Data is collected from trace file
    ########################################################################
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
                    
                    ## skip empty lines
                    if line.strip() == "" or "null" in line:
                        continue
                    
                    ## get columns
                    if lineCounter == -1:
                        header_line = line.strip()
                        columns = header_line.split("\t")
                        
                        
                        status_pos      = columns.index('status')
                        submit_pos      = columns.index('submit')
                        realtime_pos    = columns.index('realtime')
                        
                    #print("===========================================================")
                    #print("Line: " + line)	
                    ## skip header line
                    if lineCounter >= 0:
                        
                        ## print line
                        # print(line.strip())
                        ## split by tab
                        split = line.split("\t")
                        
                        ## skip if this job was not submitted
                        if(split[status_pos] == "-"):
                            continue
                            
                        ## get jon status from 5th column
                        status    = split[status_pos]
                        
                        ## split submitted time and get a time object
                        submit    = datetime.strptime(split[submit_pos], "%Y-%m-%d %H:%M:%S.%f")
                        realtime_min  = Utils.duration_to_min(split[realtime_pos])
                        
                        
                        ## if a job is COMPLETED or CACHED 
                        ## append submit time to submitted list
                        ## append completed time to completed list
                        if status=="COMPLETED" or status=="CACHED":
                            submitted_list.append(submit)
                            completed_list.append(submit + timedelta(minutes=realtime_min) )
                        
                        ## if a job has FAILED add 'failed' to status list
                        if status=="FAILED":
                            submitted_list.append(submit)
                            completed_list.append(submit + timedelta(minutes=realtime_min) )
                            status_list.append("FAILED")
                        ## for aborted put submitted time = completed time
                        if status=="ABORTED":
                            submitted_list.append(submit)
                            completed_list.append(submit)
                            status_list.append("ABORTED")
                        
                    lineCounter += 1
        ## send status (sends failed if FAILED value is found in submitted list)
        #print(submitted_list)
        
        # Return None if no completed jobs are found in the trace file
        if not submitted_list:
            return None

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

