from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from urlparse import urlparse
import os
import url_encoder

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String, unique=True)
    short = db.Column(db.String)

    def __init__(self, long):
        self.long = long
        self.short = None

    def create_short(self):
        db.session.add(self)
        db.session.commit()
        self.short = url_encoder.encode(self.id)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    long = request.form['long']
    url = Url.query.filter_by(long=long).first()

    if url == None:
        url = Url(long)
        url.create_short()

    return render_template('index.html', short=url.short, long=url.long)

@app.route('/<short>', methods=['GET'])
def redirect_from_short(short):
    id = url_encoder.decode(short)
    url = Url.query.get(id)
    if url is not None:
        link = url.long
        if link.find("http://") != 0 and link.find("https://") != 0:
            link = "http://" + link
        return redirect(link)
    return 'No url found'
