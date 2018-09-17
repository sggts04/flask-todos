from flask import Flask, render_template, request, redirect
import json
import datetime

now = datetime.datetime.now()

app = Flask(__name__)
file = open('todos.json')
todos = json.load(file)
file.close()

@app.route('/')
@app.route('/index')
def index():
	global todos
	return render_template('index.html', todo = todos)

@app.route('/update', methods=['POST'])
def update():
	global todos
	id = request.form['id']
	todos[id][0] = "Done"
	todos[id][4] = datetime.datetime.today().strftime('%d-%m-%Y')
	file = open('todos.json', 'w')
	json.dump(todos, file, indent=4)
	file.close()
	return redirect('/')

@app.route('/add')
def add():
	return render_template('add.html')

@app.route('/addtodo', methods=['POST'])
def addtodo():
	global todos
	title = request.form['title']
	desc = request.form['desc']
	comdate = request.form['comdate']
	date = datetime.datetime.today().strftime('%d-%m-%Y')
	todos.update({title: ["Not Done", desc, date, comdate, ""]})
	file = open('todos.json', 'w')
	json.dump(todos, file, indent=4)
	file.close()	
	return redirect('/')

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)