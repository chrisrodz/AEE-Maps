from flask import Flask, render_template
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

    def to_dict(self):
        return {
            "id": self.id,
            "pueblo": self.pueblo,
            "name": self.name
        }

    def __repr__(self):
        return u'{}: {}'.format(self.pueblo, self.name)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.relationship('Area', backref=db.backref('incident_area', lazy='dynamic'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    status = db.Column(db.String(140))
    last_update = db.Column(db.DateTime)
    parent = db.relationship('Incident', backref='children', lazy='select', remote_side=[id])
    parent_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "area": self.area.to_dict(),
            "status": self.status,
            "last_update": self.last_update.isoformat(),
            "parent": self.parent.to_dict() if self.parent else None
        }

    def __repr__(self):
        return u'{}: {}'.format(self.status, self.last_update.isoformat())


# Admin Model views
admin.add_view(ModelView(Area, db.session))
admin.add_view(ModelView(Incident, db.session))


@app.route('/', methods=['Get'])
def getAllData():
    json_response = prepa.getAll()
    return json_response


@app.route('/municipios/<municipio>', methods=['Get'])
def getData(municipio):
    if municipio is None:
        return {'error': "municipio can't be empty"}
    else:
        json_response = prepa.getByCity(municipio)
        return json_response


@app.route('/historic', methods=['Get'])
def getAllHistoricData():
    # Retrive all historic data from database
    incidents = []

    for incident in Incident.query.all():
        incidents.append(incident.to_dict())

    return json.dumps(incidents)


@app.route('/historic/municipios/<municipio>', methods=['Get'])
def getHistoricData(municipio):
    # Retrive historic data for a specified municipality from database
    incidents = []

    for area in Area.query.filter_by(pueblo=municipio.upper()).all():
        for incident in Incident.query.filter_by(area=area).all():
            incidents.append(incident.to_dict())

    return json.dumps(incidents)


@app.route('/map')
def map():
    return render_template('index.html')


@app.route('/geotiles/pueblos.json')
def geotile():
    return render_template('pueblos.json')


if __name__ == "__main__":
    app.debug = True
    app.run()
