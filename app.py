from flask import Flask, render_template, request, redirect, session, flash, jsonify
import json
import datetime
from passlib.hash import pbkdf2_sha256

now = datetime.datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_here"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
file = open('todos.json')
todos = json.load(file)
file.close()
file2 = open('users.json')
users = json.load(file2)
file2.close()

@app.route('/')
@app.route('/index')
def index():
	global todos
	if not session.get('logged_in'):
		return redirect('/login')
	return render_template('index.html', todo = todos[session['username']])

@app.route('/update', methods=['POST'])
def update():
	global todos
	if not session.get('logged_in'):
		return redirect('/login')
	id = request.form['id']
	todos[session['username']][id][0] = "Done"
	todos[session['username']][id][4] = datetime.datetime.today().strftime('%d-%m-%Y')
	file = open('todos.json', 'w')
	json.dump(todos, file, indent=4)
	file.close()
	return redirect('/')

@app.route('/add')
def add():
	if not session.get('logged_in'):
		return redirect('/login')
	return render_template('add.html')

@app.route('/addtodo', methods=['POST'])
def addtodo():
	global todos
	if not session.get('logged_in'):
		return redirect('/login')
	title = request.form['title']
	if title in todos[session['username']]:
		flash('A Todo with an Identical Title already exists. Try the title "'+title+' 2'+'"')
		return redirect('/add')
	desc = request.form['desc']
	comdate = request.form['comdate']
	date = datetime.datetime.today().strftime('%d-%m-%Y')
	if title=='' or desc=='' or comdate=='':
		flash("You can't leave any of the fields blank")
		return redirect('/add')
	todos[session['username']].update({title: ["Not Done", desc, date, comdate, ""]})
	file = open('todos.json', 'w')
	json.dump(todos, file, indent=4)
	file.close()	
	return redirect('/')

@app.route('/login')
def login():
	if session.get('logged_in'):
		return redirect('/')
	return render_template('login.html')

@app.route('/loginattempt', methods=['POST'])
def loginattempt():
	attempted_id = request.form['loginid']
	attempted_pass = request.form['loginpass']
	if attempted_id=='' or attempted_pass=='':
		flash("You can't leave any of the fields blank")
		return redirect('/login')
	if attempted_id in users:
		if pbkdf2_sha256.verify(attempted_pass, users[attempted_id]):
			session['logged_in'] = True
			session['username'] = attempted_id
			return redirect('/')
		else:
			flash('Wrong Password')
			return redirect('/login')
	else:
		flash('No such username exists')
		return redirect('/login')

@app.route('/logout')
def logout():
	if not session.get('logged_in'):
		return redirect('/login')
	session.pop('logged_in', None)
	session.pop('username', None)
	return redirect('/login')

@app.route('/register')
def register():
	if session.get('logged_in'):
		return redirect('/')
	return render_template('register.html')

@app.route('/registerattempt', methods=['POST'])
def registerattempt():
	register_id = request.form['registerid']
	register_pass = request.form['registerpass']
	if register_id=='' or register_pass=='':
		flash("You can't leave any of the fields blank")
		return redirect('/register')
	register_pass_hashed = pbkdf2_sha256.hash(register_pass)
	if register_id in users:
		flash('Username already taken')
		return redirect('/register')
	else:
		users.update({register_id: register_pass_hashed})
		todos.update({register_id: {}})
		session['logged_in'] = True
		session['username'] = register_id
		file2 = open('users.json', 'w')
		json.dump(users, file2, indent=4)
		file2.close()
		file = open('todos.json', 'w')
		json.dump(todos, file, indent=4)
		file.close()
		return redirect('/')

@app.route('/api', methods=['GET'])
def api():
	try:
		api_user = request.args.get('user')
		api_pass = request.args.get('pass')
		if api_user in users:
			if pbkdf2_sha256.verify(api_pass, users[api_user]):
				return jsonify(todos[api_user])
			else:
				return "Wrong Password"
		else:
			return "User Not Found"
	except:
		return "Wrong Syntax"

@app.route('/apidoc')
def apidoc():
	return render_template('apidoc.html')

if __name__ == "__main__":
    app.run()
