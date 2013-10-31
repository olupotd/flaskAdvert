import MySQLdb
import MySQLdb.cursors
import base64, os
from views import app

DEBUG = True
SECRET_KEY = os.urandom(24)
DHOST = "localhost"
DUSER = "root"
DNAME = "books"
DPASSWD = "justinah"
DPORT = 3306

SERVER_HOST = "http://10.0.0.6/"
app.config.from_object(__name__)

def get_connection():
	return MySQLdb.connect(host=DHOST, user=DUSER, passwd=DPASSWD, db=DNAME, cursorclass=MySQLdb.cursors.DictCursor)

def loginUser(user, passwd):
	details = dict()
	if user != '' and passwd != '':
		db = get_connection()
		cur = db.cursor()
		cur.execute("select * from users where user='%s' and passwd='%s'" %(user, passwd))
		details = [dict(uid=row['usr_id'], uname=row['uname'], email=row['passwd']) for row in cur.fetchall() ]
		#for detail in details[0]:
		#	print detail 	
	else:
		details = () #return an empty dictionary
	return details

def registerUser(usr, pas, email):
	status = None
	paswd = base64.encodestring(pas)
	if usr != '' and pas != '' and email != '':
		db = get_connection()
		cur = db.cursor()
		done = cur.execute('insert into users (user, passwd, email) values( ?, ? ,?)', [usr, paswd, email])
		if done > 0:
			status = 'Registration Successful'
	else:
		status = "Unable to register user \'%s\'" %usr
	return status

