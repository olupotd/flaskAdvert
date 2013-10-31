from flask import Flask, render_template, redirect, url_for, request, flash, session, send_from_directory
app = Flask(__name__)
from models import *
import os
from flask_oauth import OAuth

FACEBOOK_APP_ID = '189263487927760'
FACEBOOK_APP_SECRET = '8f7c6a5ffb774e6d74d669dad92045fc'
#@app.route('/favicon.ico')
#def favicon():
#	return send_from_dorectory(os.path.join(app.rout_path, 'static'), 'ico/favicon.ico')




@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index')
def home():
	return render_template('index.html')

@app.route('/about_us')
def about():
	return render_template('about_us.html')
	
@app.route('/profile')
def profile():
	#get userdata from facebook profile
	data = facebook.get('/me').data
	if 'id' in data and 'name' in data:
    		user_id = data['id']
    		user_name = data['name']
	return render_template('profile.html')
	
@app.route('/contact')
def contact():
	return render_template('contact_us.html')
	
@app.route('/rankings')
def rankings():
	return render_template('rankings.html')
	
#@app.route('/logout')
#def logout():
#	session.pop('logged_in', None)
#	flash('Logged out')
#	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.method == 'POST':
		if request.form['usern'] == '':
			error = "You must have username"		
		elif request.form['email'] == '':
			error = "Your email is invalid"
		elif request.form['passwd'] == '' or len(request.form['passwd']) < 8:
			error = "Password must atleast 8 digits"
		elif request.form['passAgain'] != request.form['passwd']:
			error = "Passwords Don't match"
		else:
			result = registerUser(request.form['usern'], request.form['passwd'], request.form['email'])
			flash(result)	
			return redirect(url_for('index'))
		
	return render_template('login.html', error=error)


#@app.route('/login', methods=['GET', 'POST'])
#def login():
#	error = None
#	if request.method == 'POST':
#		#checking for login
#		if request.form['user_check'] == 'login':
#			if request.form['user'] == '':
#				error = "Username Missing"
#			elif request.form['pass'] == '':
#				error = "password Missing"
#			else:
#				ans = loginUser(request.form['user'],request.form['passwd'])
#				#if ans[0] == 
#				session['logged_in'] = True
#				session['username'] = 'olupot'
#				flash('Login Successful')
#				return redirect(url_for('index'))
#		
#	return render_template('login.html', error=error)
	
#Facebook login
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))


