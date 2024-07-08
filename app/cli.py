from app import db, app
from app.base.models import User
from app.home.models import Group, Project, Run, Process
from app.base.models import Settings

import sqlite3
from sqlite_dump import iterdump

import click 
import jwt
import datetime


@app.cli.command('seed')
def seed_app():
	""" Seed a Nextpie database. """
	
	username = "admin"
	password = "admin"
	
	## generate api key
	key = jwt.encode({"key": username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, password, algorithm="HS256") 
	key = key[-30:]
        
	user = User(username=username, 
	            email="admin@example.com",
	            password="admin",
	            key=key,
	            active=1,
	            super_user=1,
	            enable_api=1)
	
	db.session.add(user)
	
	
	## add SMTP paramerters in Sewttings
	
	setting_rows = [
	{"SMTP_SERVER": "smtp.gmail.com"},
	{"SMTP_PORT": "587"},
	{"SMTP_USE_TLS": "1"},
	{"SMTP_USERNAME": ""},
	{"SMTP_PASSWORD": ""},
	{"REPLY_EMAIL": ""}]
	
	# Insert rows from the list into the database
	for row in setting_rows:
		for key, value in row.items():
			setting = Settings(name=key, value=value)
			db.session.add(setting)
	
	db.session.commit()
	
	try:
		db.session.commit()
		print('Database seeded!')
	except:
		db.session.rollback()
		print('Database not seeded!')

@app.cli.command('clear')
@click.option("--gid", "-g", help="Group IDs (separated by commas) to remove.", required=True)

def clear_db(gid):
	"Remove test data from the database."
	db.init_app(app)
	gids_lst   = gid.split(",")
	
	for gid in gids_lst:
		group      = Group.query.get(int(gid))
		if group:
			db.session.delete(group)
			db.session.commit()
			print("Database records deleted for group " + str(group) + " (group ID: " + gid + ")")
		else:
			print("Record deletion unsucessful. Group ID=" + str(gid) + " not found in the database.")
		


@app.cli.command('dump')
@click.option("--database", "-d", help="SQLite database path.", required=True, type=click.Path())
@click.option("--out", "-o", help="Output file path.", required=True, type=click.Path())	
def dump_db(database, out):
	"Dump Nextpie database (SQLite) to a file."
	
	myfile = open(out, 'w')
	
	conn = sqlite3.connect(database)
	for line in iterdump(conn):
		#print(line)
		myfile.write(line)
	
	## close file
	myfile.close()





