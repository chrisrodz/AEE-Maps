from suds.client import Client
import json

aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

def getAll():
    count = []
    summary = aee_client.service.getBreakdownsSummary()
    for city in summary:
        data = {}
        name = city.r1TownOrCity
        data['name'] = name
        data['incidents'] = json.loads(getByCity(name))
        count.append(data)
    return json.dumps(count)

def getByCity(city):
    city = city.upper()
    results = aee_client.service.getBreakdownsByTownOrCity(city)
    total_averias = []
    for result in results:
        averia = {}
        averia['area'] = result.r2Area
        averia['status'] = result.r3Status
        averia['last_update'] = result.r4LastUpdate
        total_averias.append(averia)
    return json.dumps(total_averias)