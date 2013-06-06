from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

import prepa
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/test.db')
db = SQLAlchemy(app)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pueblo = db.Column(db.String(80))
    name = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return u"%s: %s" % (self.pueblo,self.name)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer)
    status = db.Column(db.String(140))
    last_update = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return "%s: %s" % (self.pueblo,self.name)

@app.route('/getdata', methods=['Get'])
def getAllData():
    json_response = prepa.getAll()
    return json_response

@app.route('/getdata/municipios/<municipio>', methods=['Get'])
def getData(municipio):
    if municipio is None:
        return "error: municipio can't be empty"
    else:
        json_response = prepa.getByCity(municipio)
        return json_response

if __name__ == "__main__":
    app.debug=True
    app.run()
