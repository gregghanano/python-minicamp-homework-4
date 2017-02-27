from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/movie', methods = ['POST'])
def add_movie():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    name = request.form['name']
    genre = request.form['genre']
    year = request.form['year']
    try:
        cursor.execute('INSERT INTO movies (name, genre, year) VALUES (?,?,?)',(name, genre, year))
        connection.commit()
        message = "successfully inserted into db"
    except:
        connection.rollback()
        message='ERROR: failed to insert into db'
    finally:
        connection.close()
        return message

@app.route('/movies')
def get_movies():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies')
    movieList = cursor.fetchall()
    connection.close()
    return jsonify(movieList)

@app.route('/search',methods = ['GET'])
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = request.args.get('name')
        name = "%" + name + "%"
        cursor.execute("SELECT * FROM movies WHERE name LIKE '%s'" % name)
    except:
        connection.rollback()
        message = 'error in searching movies'
    finally:
        results = cursor.fetchall()
        connection.close()
        return jsonify(results)

app.run(debug=True)
