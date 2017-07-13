from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)

app.secretkey = "holyhandgrenade"

mysql = MySQLConnector(app, "semi_restful_users_demo")

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def index():
    users = mysql.query_db('SELECT * FROM users')
    return render_template('index.html', users=users)

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/create', methods=["POST"])
def create():
    # PLEASE VALIDATE THESE FORM FIELDS BEFORE YOU PUT STUFF IN DATABASE
    query = 'INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())'
    data = {
        "first_name": request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    user_id = mysql.query_db(query, data)
    #we assume all of this worked
    return redirect('/users/{}'.format(user_id))

@app.route('/users/<id>')
def show(id):
    user = mysql.query_db('SELECT * FROM users WHERE id = :id', {"id":id})
    return render_template('show.html', user=user[0])

@app.route('/users/<id>/edit')
def edit(id):
    user = mysql.query_db('SELECT * FROM users WHERE id = :id', {"id":id})
    return render_template('edit.html', user=user[0])

@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    query = 'UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW()'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/users/{}'.format(id))

@app.route('/users/<id>/delete')
def delete(id):
    mysql.query_db('DELETE FROM users WHERE id = :id', {"id":id})
    return redirect('/users')


app.run(debug=True)
