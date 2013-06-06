import json
from datetime import datetime

from aeemaps import db, Area, Incident
import prepa

city_data = json.loads(prepa.getAll())

for key,incidents in city_data.iteritems():
    for incident in incidents:
        if not Area.query.filter_by(name=incident['Area']).first():
            new = Area(pueblo=key,name=incident['Area'])
            db.session.add(new)
            db.session.commit()
        area_instance = Area.query.filter_by(name=incident['Area']).first()
        time = incident['LastUpdate'].split(' ')
        last_update = datetime.strptime(time[0]+' '+time[1], "%m/%d/%Y %H:%M")
        i = Incident(area_id=area_instance.id,status=incident['Status'],last_update=last_update,parent_id=None)
        db.session.add(i)
        db.session.commit()

