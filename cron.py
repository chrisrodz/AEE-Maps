# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sendgrid
import os

from aeemaps import db, Area, Incident, Subscriber
import prepa


def sendmail(email, msg):
    # make a secure connection to SendGrid
    s = sendgrid.Sendgrid(os.environ.get('SENDGRID_USERNAME'), os.environ.get('SENDGRID_PASSWORD'), secure=True)

    # make a message object
    message = sendgrid.Message("christian.etpr10@gmail.com", "Nuevo Reporte de Avería", msg, msg)
    # add a recipient
    message.add_to(email, email)

    # use the Web API to send your message
    s.web.send(message)

city_data = json.loads(prepa.getAll())
# json_data = ""

# For each area in db
# Get last incident
# If area is not in city_data
# Update last incident status to 'Completed'

# Find Incidents for this area_instance
# Look for the last incident found and check if it's the one that closes the incident.
# If its the one that closes the insident we create a new incident with parent_id=None
# Else create an incident for that parent_id

for town in city_data:

    areas = Area.query.filter_by(pueblo=town['name']).all()
    for area in areas:
        last_incident = Incident.query.filter_by(area=area).order_by('-id').first()
        if last_incident:
            close = True
            for incident in town['incidents']:
                if last_incident and incident['area'] == last_incident.area.name:
                    close = False
            if close:
                last_incident.status = 'Closed'
                db.session.commit()

    for incident in town['incidents']:
        # If Area does not exist create it
        if not Area.query.filter_by(pueblo=town['name'], name=incident['area']).first():
            new = Area(pueblo=town['name'], name=incident['area'])
            db.session.add(new)
            db.session.commit()

        # Get instance of Area
        area_instance = Area.query.filter_by(pueblo=town['name'], name=incident['area']).first()

        # Setup datetime object of incident
        time = incident['last_update'].split(' ')
        last_update = datetime.strptime(time[0]+' '+time[1], "%m/%d/%Y %H:%M")

        # Get last incident of this area
        last_incident = Incident.query.filter_by(area=area_instance).order_by('-id').first()

        # If last incident is closed save as new collection, else it's parent is the
        # same as last incident
        if last_incident and last_incident.status == 'Closed':
            i = Incident(area_id=area_instance.id, status=incident['status'],
                         last_update=last_update, parent_id=None)
            db.session.add(i)
            db.session.commit()
            subscribers = Subscriber.query.filter_by(area=area_instance).all()
            for subscriber in subscribers:
                message = u"Ha ocurrido una averia en %s, %s! \n Status: %s" % (area_instance.name, area_instance.pueblo, i.status)
                sendmail(subscriber.email, message)
        elif last_incident:
            i = Incident(area_id=area_instance.id, status=incident['status'],
                last_update=last_update, parent_id=last_incident.parent_id)
            if last_incident.status != i.status:
                db.session.add(i)
                db.session.commit()
                subscribers = Subscriber.query.filter_by(area=area_instance).all()
                for subscriber in subscribers:
                    message = u"Ha ocurrido una averia en %s, %s! \n Status: %s" % (area_instance.name, area_instance.pueblo, i.status)
                    sendmail(subscriber.email, message)
        else:
            i = Incident(area_id=area_instance.id, status=incident['status'],
                last_update=last_update, parent_id=None)
            db.session.add(i)
            db.session.commit()
            subscribers = Subscriber.query.filter_by(area=area_instance).all()
            for subscriber in subscribers:
                message = u"Ha ocurrido una averia en %s, %s! \n Status: %s" % (area_instance.name, area_instance.pueblo, i.status)
                sendmail(subscriber.email, message)
