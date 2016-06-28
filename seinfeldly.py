import os
import sqlite3
from flask import Flask, request, redirect, g, render_template, url_for
import url_encoder

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'seinfeldly.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('URLPY_SETTINGS', silent=True)

def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if one is not present."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized database'

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    long = request.form['long']
    cur = db.execute('insert into urls (long) values(?)', [long])
    id = cur.lastrowid
    short = url_encoder.encode(id)
    db.execute('update urls set short=? where id=?', [short, id])
    db.commit()
    return '{} is now short for {}.'.format('localhost:5000/' + short, long)

@app.route('/<short>', methods=['GET'])
def redirect_from_short(short):
    db = get_db()
    id = url_encoder.decode(short)
    cur = db.execute('select long from urls where id=?', [id])
    url =  cur.fetchone()
    if url:
        return redirect(url[0])
    else:
        return 'No url found'
