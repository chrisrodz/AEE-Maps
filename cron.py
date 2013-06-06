import json
from datetime import datetime

from aeemaps import db, Area, Incident
import prepa

city_data = json.loads(prepa.getAll())

for town in city_data:
    for incident in town['incidents']:
        if not Area.query.filter_by(name=incident['area']).first():
            new = Area(pueblo=town['name'],name=incident['area'])
            db.session.add(new)
            db.session.commit()
        area_instance = Area.query.filter_by(name=incident['area']).first()
        time = incident['last_update'].split(' ')
        last_update = datetime.strptime(time[0]+' '+time[1], "%m/%d/%Y %H:%M")
        i = Incident(area_id=area_instance.id,status=incident['status'],last_update=last_update,parent_id=None)
        db.session.add(i)
        db.session.commit()

