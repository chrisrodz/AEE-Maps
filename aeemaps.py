from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.sqlalchemy import SQLAlchemy

import prepa
import os
import json

app = Flask(__name__)
admin = Admin(app)
app.config['SECRET_KEY'] = "@S\x8f\x0e\x1e\x04\xd0\xfa\x9a\xdf,oJ'\x1e\xe6\xc0\xaeZ'\x8am\xee."
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
    area = db.relationship('Area', backref=db.backref('children', lazy='dynamic'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    status = db.Column(db.String(140))
    last_update = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

    def __repr__(self):
        return "%s: %s" % (self.area, self.status)

# Admin Model views
admin.add_view(ModelView(Area, db.session))
admin.add_view(ModelView(Incident, db.session))


@app.route('/getdata', methods=['Get'])
def getAllData():
    json_response = prepa.getAll()
    return json_response


@app.route('/getdata/municipios/<municipio>', methods=['Get'])
def getData(municipio):
    if municipio is None:
        return {error: "municipio can't be empty"}
    else:
        json_response = prepa.getByCity(municipio)
        return json_response

@app.route('/getdata/historic', methods=['Get'])
def getAllHistoricData():
    # Retrive all historic data from database
    incidents = Incident.query.all()
    return json.dumps(incidents)

@app.route('/getdata/historic/municipios/<municipio>', methods=['Get'])
def getHistoricData(municipio):
    # Retrive historic data for a specified municipality from database
    incidentes = []

    for area in Area.query.filter_by(pueblo=municipio).all():
        for incident in Incident.query.filter_by(area=area).all():
            incidentes.append(incident)

    return json.dumps(incidentes)

if __name__ == "__main__":
    app.debug = True
    app.run()
