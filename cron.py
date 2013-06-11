# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from app import db, Area, Incident
import prepa

logging.basicConfig(level=logging.ERROR)


def get_datetime(update):
    time = update.split(' ')
    return datetime.strptime(time[0]+' '+time[1], "%m/%d/%Y %H:%M")


city_data = json.loads(prepa.getAll())
# data = json.dumps([{
#             "incidents": [
#                     {
#                         "status": "Averia Reportada",
#                         "area": "Bo Guayo",
#                         "last_update": "06/07/2013 08:36 pm"
#                     }
#             ],
#             "name": "AGUADA"
#         },
#         {
#             "incidents": [
#                     {
#                         "status": "Personal Asignado",
#                         "area": "Bo Guayo",
#                         "last_update": "06/07/2013 09:36 pm"
#                     }
#             ],
#             "name": "AGUADA"
#         }])
# city_data = json.loads(data)

# For each area in db
# Get last incident
# If area is not in city_data
# Update last incident status to 'Completed'

areas = Area.query.all()
for area in areas:
    last_incident = Incident.query.filter_by(area=area).order_by('-id').first()
    if last_incident:
        close = True
        for town in city_data:
            if last_incident.area.pueblo == town['name']:
                for incident in town['incidents']:
                    if incident['area'] == last_incident.area.name:
                        close = False
    if last_incident and close:
        last_incident.status = 'Closed'
        print 'Closing: ', last_incident.status, last_incident.area.name
        db.session.commit()


for town in city_data:

    # Find Incidents for this area_instance
    # Look for the last incident found and check if it's the one that closes the incident.
    # If its the one that closes the insident we create a new incident with parent_id=None
    # Else create an incident for that parent_id

    for incident in town['incidents']:
        # If Area does not exist create it
        if not Area.query.filter_by(pueblo=town['name'], name=incident['area']).first():
            new = Area(pueblo=town['name'], name=incident['area'])
            db.session.add(new)
            db.session.commit()

        # Get instance of Area
        area_instance = Area.query.filter_by(pueblo=town['name'], name=incident['area']).first()

        last_update = get_datetime(incident['last_update'])

        # Get last incident of this area
        last_incident = Incident.query.filter_by(area=area_instance).order_by('-id').first()

        ocurred = False

        # If last incident is closed save as new collection, else it's parent is the
        # same as last incident

        flag = Incident.query.filter_by(area_id=area_instance.id, status=incident['status'], last_update=last_update).all()

        if not flag:
            if last_incident and last_incident.status == 'Closed':
                i = Incident(area_id=area_instance.id, status=incident['status'],
                             last_update=last_update, parent_id=None)
                db.session.add(i)
                db.session.commit()
                ocurred = True

            elif last_incident and last_incident.parent_id is not None:
                i = Incident(area_id=area_instance.id, status=incident['status'],
                             last_update=last_update, parent_id=last_incident.parent_id)
                if last_incident.status != i.status:
                    db.session.add(i)
                    db.session.commit()
                    ocurred = True
            elif last_incident and last_incident.parent_id is None:
                i = Incident(area_id=area_instance.id, status=incident['status'],
                             last_update=last_update, parent_id=last_incident.id)
                if last_incident.status != i.status:
                    db.session.add(i)
                    db.session.commit()
                    ocurred = True
            else:
                i = Incident(area_id=area_instance.id, status=incident['status'],
                             last_update=last_update, parent_id=None)
                db.session.add(i)
                db.session.commit()
                ocurred = True

            if not ocurred:
                i = Incident(area_id=area_instance.id, status=incident['status'],
                             last_update=last_update, parent_id=None)
                db.session.add(i)
                db.session.commit()
                ocurred = True
